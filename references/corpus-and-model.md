# Comparable references and an interpretable diagnostic

## Selection and discovery

Infer context from the actual document and conversation. Search supplied files and the project before asking the user. For public scholarly discovery, establish identity from consistent affiliation, ORCID, personal site or known publications; a name match is insufficient. Use legal author/publisher repositories. Do not purchase, bypass access controls, contact people or upload private drafts without authorization.

Rank references primarily by purpose, audience, genre, language, section function and authorship confidence. Then consider topic and time. Older single-author work is especially useful for an academic baseline, but neither first authorship nor a pre-2022 date establishes exclusive authorship. Record these as selection reasons, not certificates. Avoid mixing grant aims, experimental Results and informal emails just because the author is the same. Recent confirmed unaided writing may be the best match.

Read candidate prose rather than choosing by metadata alone. Keep a manifest of accepted and rejected candidates with short reasons. If a useful source cannot be retrieved after reasonable attempts, ask for that specific document. If no trustworthy personal references exist, offer plain editing with no personal-voice claim; do not silently substitute famous writers or a generic published corpus.

## Extraction

Produce sentence lists from prose only. Use a language-appropriate tokenizer; inspect abbreviation, citation and decimal handling. For LaTeX, parse structure, for example with Pandoc, rather than count raw commands. For PDF, inspect extraction for hyphenation, column order, headers and OCR errors. Preserve case/punctuation in sentence strings. Exclude tables, bibliography, citation tokens, formulas, quotations, code, headings and other people's words consistently. Document treatment of lists, notes and captions. Never edit the original merely to exclude material from analysis.

Store a UTF-8 JSON array of nonempty sentence strings for each document/section. Keep source checksum, location, extraction method, excluded material and reader checks in the manifest's source records. Inputs to the script must already be reviewed prose; the script does not infer full-text structure or verify sentence boundaries.

Inspect overlap between references, revisions, and repeated sections. Put related document families in the same validation group; exclude duplicated passages when appropriate and record it. Do not split the same document family into random train/test chunks. When only one earlier paper and its revision exist, section-paired folds may be useful **within that lineage**, but they do not estimate performance on independent documents or an enduring author style.

## Input and execution

The supplied script accepts a JSON manifest with this structure (adapt paths; do not use these as actual observations):

```json
{
  "language": "en",
  "grouping_note": "Matched section families; shared lineage, not independent publications.",
  "inventory": {"path": "function_words.txt", "name": "project English inventory", "provenance": "Exact source or explicitly curated alternative"},
  "documents": [
    {"id": "old_intro", "unit": "old_intro", "role": "reference", "group": "introduction", "path": "old_intro.sentences.json", "source": "Reference document/version, authorship and extraction provenance"},
    {"id": "new_intro", "unit": "draft_intro", "role": "baseline", "group": "introduction", "path": "new_intro.sentences.json", "source": "Unedited draft snapshot"},
    {"id": "edited_intro", "unit": "draft_intro", "role": "pass1", "group": "introduction", "path": "edited_intro.sentences.json", "source": "Pass 1 snapshot with same extraction scope"}
  ]
}
```

Roles are `reference`, `baseline`, `cleanup`, `pass1`, `pass2`, `pass3`. `unit` identifies the same document/section across editing passes; `group` defines the validation grouping and can contain several units. Each later role must cover exactly the baseline's group/unit pairs. This catches missing sections even when the group remains represented; inspect extraction coverage inside each unit separately. Add later roles as they become available; never relabel them as references. Omit `inventory` to use the bundled curated English alternative. The model's training corpus is always the fixed reference plus original baseline. Keep the manifest and outputs in the private project library, not inside a shared installed skill.

```bash
python /path/to/your-voice/scripts/compare_voice.py manifest.json --out results_pass1
```

Dependencies: `numpy`, `scikit-learn`; prefer an existing environment. The script uses sentence-boundary chunks of about 350 lexical tokens; normalized rates are per 1,000 tokens. It reports raw role-level feature rates, regularized standardized coefficients and sign consistency across held-out groups. Sentence mean/SD/90th percentile use words per sentence, not per-1,000 rates. The word tokenizer supports English letters with internal apostrophes; contractions stay whole, so interpret the inventory accordingly. Numeric punctuation is excluded from punctuation counts, not from sentence segmentation already performed upstream.

Koppel et al.'s paper describes a 512-function-word feature set ([author copy](https://u.cs.biu.ac.il/~koppel/papers/authorship-JASIST-final.pdf)); that description does not supply or license an exact reconstructed inventory. The bundled alternative is curated for this tool. If supplying Koppel-512, verify the actual artifact and provenance first; don't rename an ordinary stop-word list. Multiword inventories need explicit feature extraction changes, not silent token omission.

## Design and interpretation

Use a grouped comparison with both reference and baseline represented in each held-out group. The script requires at least three such groups for its exploratory grouped diagnostic; this is an operational safeguard, not a statistical adequacy guarantee. For fewer or unmatched groups it reports descriptive rates only, not classifier accuracy. Do not invent matching groups to enable the model. Very short inputs can yield unreliable rates even if accepted by the script.

Fit the scaler inside each training fold. Use fixed regularization/settings, balanced classes and group/role-balanced training weights so a long section does not dominate. Report macro-group balanced accuracy and fold sizes, not just an impressive pooled score. Do not optimize hyperparameters on the same tiny corpus being edited.

Feature importance is the combination of rate differences, coefficient magnitude, consistency across folds, and inspection of actual sentences. Correlated words can exchange weights. Small differences, unstable coefficients or zero-variance reference features should not dictate edits. Preserve function words that express causal, epistemic or argumentative relationships.

The script refits the same deterministic model on the unchanged reference/baseline for each report. Later passes are scored only as a **frozen-model descriptive margin**, not as new held-out accuracy or calibrated probabilities. Positive is baseline-like and negative is reference-like; increasingly negative is not automatically better. Check reference/baseline source hashes, inventory, script and settings across runs, not the entire manifest hash (which changes when adding passes). Comparing edited versions to a repeatedly consulted model is not independent validation. A separate documented refit after the three passes may find residual differences, but do not present a lower refitted score as directly comparable to the original frozen score.

Report fold word counts and any small-group warning alongside accuracy; even perfect separation on tiny samples is not compelling validation. The 350-token warning is a practical flag, not a power calculation. Zero coefficients receive no stability score and must not be called influential.

No threshold certifies voice restoration. Read the edited text alongside references. If rates get closer but the writing gets worse, revert those edits and say so.
