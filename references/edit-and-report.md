# Three measured passes, with meaning intact

## Before changing anything

Preserve an original snapshot and the author's terms, examples, judgments and argument. Identify protected quotations, numbers, citations, technical names, negation, uncertainty and causal language. If an edit would require deciding an unresolved scientific question, flag it and work elsewhere; this skill does not perform a full source audit.

First read the references qualitatively. Does the author explain with examples, explicitly attribute findings, express judgments directly, or use long design clauses? Sentence length alone will not capture those choices. Match the current purpose rather than an immutable personal fingerprint.

## Cleanup, separate from personal calibration

Remove formulaic framing only where it adds nothing: chatbot residue, vague fanfare, empty claims of importance, repeated summaries, rhetorical verdicts, unnecessarily ornate verbs, and chained unrelated findings. Prefer direct language over replacing every suspect word with a synonym.

Do not blacklist natural author habits, impose a maximum dash count, or force sentences longer than a generic minimum. Technical uses of words such as robust or significant remain. Keep useful qualifications; cut redundant ones that do not alter interpretation. Never turn “may” into “does” to improve a statistic. Avoid excessive short sentences as a cure for long ones.

If using an available de-slop skill, read its guidance and protected-term reference before applying it. Its measured rates from another genre are prompts for inspection, not targets for this author. Keep any calibration local; do not overwrite the shared skill's quotas.

## Passes

**Pass 1:** choose a few large, stable discrepancies with clear prose examples. Start where a local edit is obviously better. Split a chain of unrelated findings, remove a duplicate closing sentence, or replace repeated announcements with the finding itself. Explain what will change before a broad batch.

**Pass 2:** inspect the new rates and remaining discrepancies. Work on frequent function words in context: for example, an unnecessary “and” may disappear when independent findings are separated. It is not a license to delete coordination that expresses a real relationship. Restore author-typical attribution or transitions only where they make sense. Do not add twenty instances of “However” to match the old paper.

**Pass 3:** address only useful residual opportunities, then read continuously. Check antecedents, comma splices, paragraph flow, duplicated summaries and connectors whose logic broke during sentence splitting. If a feature still differs because this document has a different purpose, keep it and explain briefly. Zero edits is a valid outcome.

After every pass: inspect the actual diff, confirm preserved numbers/citations/negation/modal force/technical names, assess paragraph reasoning, and rerun measurements with unchanged baseline and extraction. Build/render when editing a structured manuscript. Save before/after passages and any reverted edit. Never claim a semantic check from a matching count alone.

## Progress and final report

Give a short update after each pass, not a long report only at the end. Use plain colleague-like wording. Example structure, with actual values only:

> Pass 1 is done. I split the multi-result chains and removed repeated summaries. Semicolon frequency moved from [original] to [current] per 1,000 words; your references are at [reference]. I left [specific constructions] because changing them would weaken the claim. Next I will inspect [remaining feature] in context.

At the end explain the experiment plainly:

> I compared [documents/sections and word counts], excluding [material]. The model uses function-word frequencies, punctuation and sentence lengths. It is a regularized logistic regression with [grouping]; it distinguishes these text sets, not human versus AI writing.

Then give a compact table of only the useful features: reference / original / cleanup / final, with units. Link per-pass details rather than dumping hundreds of features. Show two or three actual before/after edits; explain any tradeoff or failure. Report grouped model performance only if it was meaningfully computed, and label later frozen-model margins descriptive. Do not compress everything into a “voice similarity” score.

Close with pass count, remaining differences and whether further work is worth it. Avoid “transformed,” “authentic voice unlocked,” “80% fixed,” praise of the workflow, or unsupported guarantees. Honest examples: “The rhythm is closer. Articles still differ; I left them where a change would sound forced.” Or: “The reference corpus was too small for a defensible classifier. I used descriptive rates and reading instead.”
