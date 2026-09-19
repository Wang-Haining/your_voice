---
name: your-voice
license: MIT
description: Restore the user's own writing voice in an AI-assisted draft using comparable author-written reference documents, interpretable stylometry, and three measured editing passes. Find suitable references with minimal user input, remove formulaic prose, then prioritize function words, punctuation and sentence rhythm using regularized logistic regression when data permit. Use for personal voice calibration, humanizing a draft without generic house style, or checking before/after stylistic drift; not an AI detector or a fact-checking workflow.
---

# Your Voice

Make this sound like the user, writing for this purpose. Preserve their meaning, judgments, technical vocabulary, citations and evidence. Do not replace a generic AI voice with a generic editor's voice.

## Start with context, not a questionnaire

Announce this skill. Inspect the draft and available project context to infer the author, language, intended audience, document type, purpose, domain, and writing conditions. Domain includes subject, genre and register; conditions can also include collaboration, editing, translation, time and section function. Record what is known versus inferred.

Read [references/corpus-and-model.md](references/corpus-and-model.md) before collecting references or measuring style. First look in the user-provided materials and relevant project folders, not their entire drive. If the author's identity is established, look for legitimate public author copies of comparable work. Prefer strong authorship provenance and comparable purpose: single-author work, confirmed author-written passages, then first-author work with a coauthor-editing caveat. Pre-ChatGPT work is useful when otherwise comparable, not proof of unaided authorship. Never guess an identity or attribute a coauthored paper's entire voice to its first author.

Aim for a few good references, not a large mismatched corpus. Usually three to five comparable documents are a useful starting point, not a validity threshold. A same-purpose recent document can be better than an old unrelated paper. Do the discovery work yourself; ask one concise question only if identity, access, authorship or purpose cannot be resolved. Do not manufacture a personal baseline when no suitable references exist.

## Establish a local voice library

Reuse the project's existing analysis/review area or create `your_voice/` beside the draft. Keep original references unchanged. Save source URLs/paths, authorship confidence, date, domain/conditions, extraction exclusions and checksums; then store clean prose and a short qualitative voice profile. Do not upload private documents or redistribute downloaded papers in the skill. A reusable personal library remains local and is partitioned by language/genre, not pooled into one universal fingerprint.

Use `state.md` to record original draft snapshot, selected references, frozen extraction/model setup, current stage, each pass's outputs/checks, remaining issues and exact next action. Read it when resuming; preserve the original baseline rather than overwriting it with revised text. Later AI-assisted revisions are comparison outputs, not new independent reference material.

## Procedure

Read [references/edit-and-report.md](references/edit-and-report.md) before editing. Preserve an original draft and verify that this is a language-editing task; flag unresolved science instead of polishing it into apparent certainty.

1. **Baseline.** Read representative reference passages, describe their actual habits, and measure comparable reference/draft prose. Use function words, punctuation and sentence lengths. Tables and other non-author material are excluded from analysis, not deleted from the manuscript.
2. **Light de-slop.** Remove obvious chatbot residue, empty emphasis, repetitive summaries and mannered framing where they add nothing. If a de-slop/plain-academic skill is available, read and use it; otherwise use the self-contained guidance in the editing reference. Do not impose its generic quotas or sentence-length floors against this author's evidence. Save this as `cleanup`, distinct from the original and the three personal-voice passes.
3. **Pass 1 — easy, large differences.** Inspect three to five stable high-impact features. Edit only natural opportunities: chained findings, repetitive openings, or unnecessary connective scaffolding. Preserve good original sentences.
4. **Pass 2 — contextual function-word and rhythm work.** Remeasure; address the largest remaining differences where actual sentences justify it. Check modals, conjunctions, pronouns and articles for meaning, not just frequency. Do not insert filler to make rates agree.
5. **Pass 3 — residuals and full reading.** Remeasure, make remaining clearly useful changes, and read for flow, grammar, reasoning and recognizable voice. A pass can honestly make zero edits. Do not force three rounds of arbitrary changes.

After **each** pass, save a diff, measure with the frozen setup, check claims/numbers/citations/terminology, and briefly show the user what changed. Continue the three passes without unnecessary questions unless scope, permissions, or scientific meaning needs a decision. Respect local batch-size limits.

The 80/20 rule prioritizes effort; it does not mean five matched frequencies solve 80% of style. Stop after three passes with an honest account of what remains. Further refitting or editing needs a reason, not a desire to reach chance accuracy.

## Measurement

The bundled [scripts/compare_voice.py](scripts/compare_voice.py) measures English sentence-segmented prose and fits standardized, regularized logistic regression when a matched grouped design is available. Its dependencies are NumPy and scikit-learn for transparent feature analysis and grouped classification. It never edits the draft. Read the corpus/model reference for input format, extraction, grouping, limitations and invocation.

Use a verified Koppel-512 inventory if available and its use is permitted. The supplied [assets/function_words_en.txt](assets/function_words_en.txt) is an explicitly labeled small English alternative, **not Koppel-512**. Do not claim a list's provenance based on its length. Other languages require appropriate tokenization and inventories; do not feed Chinese or translated text through the English script and report valid personal-voice measurements.

This classifier separates reference and draft samples under a specific design. It does not identify AI writing, certify authorship, estimate “how human,” or measure a percentage of the user's voice. Correlated coefficients are diagnostic clues, not causal word importance. A decline in distinguishability is not sufficient evidence of better writing.

## Report like a colleague

Be brief, direct and specific. Explain the model in one or two sentences, show a small reference/original/final comparison for the most relevant features, and two or three representative before/after edits. State unchanged scientific content only after checking it. Mention weak reference provenance, insufficient data, extraction limits and changes that did not help. No theatrical enthusiasm, aphorisms, grand claims, or ceremonial “not X but Y” framing.

Deliver the edited draft, local measurement/provenance paths, completed pass count and unresolved items. Do not publish, send or commit private references. Follow existing permission for manuscript commits; final submission and AI-use disclosure remain the author's responsibility.
