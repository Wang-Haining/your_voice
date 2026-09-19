"""English reference/draft diagnostics, not an authorship or AI detector.

Input: manifest of extracted JSON sentence arrays. See corpus-and-model.md.
Dependencies: numpy, scikit-learn. Never writes to source documents.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.preprocessing import StandardScaler

ROLES = ['reference', 'baseline', 'cleanup', 'pass1', 'pass2', 'pass3']
PUNCT = {',': 'comma', ';': 'semicolon', ':': 'colon', '.': 'period', '?': 'question',
         '!': 'exclamation', '(': 'opening_parenthesis', '-': 'hyphen', '—': 'em_dash'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text):
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower().replace('’', "'"))


def feature_vector(sentences, inventory):
    text = ' '.join(sentences)
    tokens = words(text)
    require(bool(tokens), 'text contains no English lexical tokens')
    counts = Counter(tokens)
    lengths = [len(words(s)) for s in sentences]
    require(min(lengths) > 0, 'sentence has no English lexical tokens')
    stripped = re.sub(r'(?<=\d)[.,:–−-](?=\d)', '', text)
    return np.array([1000 * counts[w] / len(tokens) for w in inventory]
                    + [np.mean(lengths), np.std(lengths), np.percentile(lengths, 90)]
                    + [1000 * stripped.count(p) / len(tokens) for p in PUNCT])


def chunk(sentences):
    batches, current, size = [], [], 0
    for sentence in sentences:
        current.append(sentence)
        size += len(words(sentence))
        if size >= 350:
            batches.append(current)
            current, size = [], 0
    if current:
        if batches:
            batches[-1].extend(current)
        else:
            batches.append(current)
    return batches


def fit(x, y, groups):
    # Equal total training weight per group/role cell.
    cells = Counter(zip(groups.tolist(), y.tolist()))
    weight = np.array([1 / cells[g, label] for g, label in zip(groups, y)])
    weight *= len(weight) / weight.sum()
    scaler = StandardScaler().fit(x, sample_weight=weight)
    model = LogisticRegression(C=0.1, max_iter=3000, random_state=18)
    model.fit(scaler.transform(x), y, sample_weight=weight)
    require(int(model.n_iter_.max()) < 3000, 'logistic regression did not converge')
    return scaler, model


def run(manifest_path, out):
    require(not out.exists(), f'output already exists: {out}; use a new pass directory')
    manifest = json.loads(manifest_path.read_text())
    require(manifest.get('language') == 'en', 'English-only script: expected language=en')
    require(bool(manifest.get('grouping_note')), 'missing grouping_note')
    base = manifest_path.parent
    spec = manifest.get('inventory')
    if spec is None:
        inv_path = Path(__file__).resolve().parents[1] / 'assets/function_words_en.txt'
        inv_name, inv_source = 'your-voice curated English alternative', 'Bundled explicit list; not Koppel-512'
    else:
        inv_path = (base / spec['path']).resolve()
        inv_name, inv_source = spec['name'], spec['provenance']
        require(bool(inv_name and inv_source), 'inventory needs name and provenance')
    inventory = inv_path.read_text().splitlines()
    require(bool(inventory) and len(inventory) == len(set(inventory)), 'empty or duplicate inventory')
    require(all(re.fullmatch(r"[a-z]+(?:'[a-z]+)?", w) for w in inventory), 'inventory must contain lowercase single tokens')
    names = ['fw_' + w for w in inventory] + ['sentence_mean', 'sentence_sd', 'sentence_p90'] + list(PUNCT.values())
    documents = manifest.get('documents', [])
    require(bool(documents), 'documents is empty')
    ids, units, rows, corpora, sources, exact = set(), set(), [], {}, [], {}
    for doc in documents:
        doc_id, role, group = doc['id'], doc['role'], doc['group']
        unit = doc['unit']
        require(doc_id not in ids, f'duplicate document id: {doc_id}')
        require(role in ROLES and isinstance(group, str) and bool(group), f'invalid role/group: {doc}')
        require(bool(doc.get('source')), f'missing source provenance: {doc_id}')
        require(isinstance(unit, str) and bool(unit), f'missing scope unit: {doc_id}')
        require((role, unit) not in units, f'duplicate scope unit for role: {(role, unit)}')
        units.add((role, unit))
        ids.add(doc_id)
        path = (base / doc['path']).resolve()
        sentences = json.loads(path.read_text())
        require(isinstance(sentences, list) and bool(sentences), f'expected nonempty sentence list: {path}')
        require(all(isinstance(s, str) and s.strip() for s in sentences), f'invalid sentence: {path}')
        feature_vector(sentences, inventory)
        corpora.setdefault(role, []).extend(sentences)
        sources.append(dict(doc, path=str(path), sha256=digest(path), words=sum(len(words(s)) for s in sentences)))
        for batch in chunk(sentences):
            normalized = ' '.join(words(' '.join(batch)))
            if role in ['reference', 'baseline']:
                require(normalized not in exact, f'duplicate training chunk: {doc_id}, previously {exact.get(normalized)}; resolve overlap')
                exact[normalized] = doc_id
            rows.append(dict(role=role, group=group, unit=unit, words=len(words(' '.join(batch))), x=feature_vector(batch, inventory)))
    require('reference' in corpora and 'baseline' in corpora, 'need reference and baseline roles')
    baseline_scope = {(r['group'], r['unit']) for r in rows if r['role'] == 'baseline'}
    for role in corpora:
        if role not in ['reference', 'baseline']:
            actual = {(r['group'], r['unit']) for r in rows if r['role'] == role}
            require(actual == baseline_scope, f'{role} scope units {actual} differ from baseline {baseline_scope}; compare the same scope')
    training = [r for r in rows if r['role'] in ['reference', 'baseline']]
    x = np.vstack([r['x'] for r in training])
    y = np.array([int(r['role'] == 'baseline') for r in training])
    groups = np.array([r['group'] for r in training])
    require(np.isfinite(x).all(), 'non-finite feature matrix')
    unique_groups = sorted(set(groups))
    eligible = len(unique_groups) >= 3 and all(len(set(y[groups == g])) == 2 for g in unique_groups)
    coefficients, stability, folds, margins = None, None, [], {}
    if eligible:
        fold_coefs = []
        for g in unique_groups:
            test = groups == g
            scaler, model = fit(x[~test], y[~test], groups[~test])
            pred = model.predict(scaler.transform(x[test]))
            fold_words = {role: sum(r['words'] for r in training if r['group'] == g and r['role'] == role) for role in ['reference', 'baseline']}
            folds.append({'group': g, 'n': int(test.sum()), 'words': fold_words, 'balanced_accuracy': float(balanced_accuracy_score(y[test], pred))})
            fold_coefs.append(model.coef_[0])
        scaler, model = fit(x, y, groups)
        coefficients = model.coef_[0]
        stability = np.mean(np.sign(np.vstack(fold_coefs)) == np.sign(coefficients), axis=0)
        for role in corpora:
            role_rows = [r for r in rows if r['role'] == role]
            by_group = []
            for g in sorted({r['group'] for r in role_rows}):
                xx = np.vstack([r['x'] for r in role_rows if r['group'] == g])
                by_group.append(float(model.decision_function(scaler.transform(xx)).mean()))
            margins[role] = float(np.mean(by_group))
    rates = {role: feature_vector(sentences, inventory) for role, sentences in corpora.items()}
    feature_rows = []
    for i, name in enumerate(names):
        row = {'feature': name, 'unit': 'words/sentence' if name.startswith('sentence_') else 'per_1000_tokens'}
        row.update({role: float(rates[role][i]) for role in ROLES if role in rates})
        row.update(coefficient=None if coefficients is None else float(coefficients[i]),
                   sign_agreement=None if stability is None or abs(coefficients[i]) < 1e-10 else float(stability[i]))
        feature_rows.append(row)
    if eligible:
        feature_rows.sort(key=lambda r: abs(r['coefficient']), reverse=True)
    summary = dict(language='en', inventory=dict(name=inv_name, provenance=inv_source, sha256=digest(inv_path), count=len(inventory)),
                   manifest_sha256=digest(manifest_path), sources=sources, grouping_note=manifest['grouping_note'],
                   settings=dict(chunk_words=350, C=0.1, seed=18, sklearn=sklearn.__version__, numpy=np.__version__, script_sha256=digest(Path(__file__))),
                   mode='grouped_exploratory' if eligible else 'descriptive_only',
                   words={role: len(words(' '.join(s))) for role, s in corpora.items()},
                   training_chunks=len(training), folds=folds,
                   macro_group_balanced_accuracy=float(np.mean([f['balanced_accuracy'] for f in folds])) if folds else None,
                   frozen_model_mean_margin=margins,
                   small_group_warning=any(min(f['words'].values()) < 350 for f in folds),
                   limitations='Not AI detection or authorship certification. Positive margin means baseline-like; negative means reference-like, not better without limit. Later margins are descriptive, not held-out accuracy. Rates are token-pooled; model training and margins balance groups. Exact duplicate training chunks are rejected; near-duplicate/lineage and sentence-boundary checks remain the operator responsibility. Fewer than three paired groups gives descriptive-only output. Group count does not guarantee adequate data; inspect fold word counts.')
    out.mkdir(parents=True)
    with (out / 'features.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(feature_rows[0]))
        writer.writeheader()
        writer.writerows(feature_rows)
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: summary[k] for k in ['mode', 'words', 'training_chunks', 'macro_group_balanced_accuracy', 'frozen_model_mean_margin', 'small_group_warning']}, indent=2))
    print(f'Wrote {len(feature_rows)} feature rows and provenance to {out}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run(args.manifest.resolve(), args.out.resolve())
