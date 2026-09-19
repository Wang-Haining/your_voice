# Your Voice

**Your AI doesn't sound like you? Try Your Voice.**

An AI skill that adapts drafts to your writing style, using your own writing as the reference.

Built by **Haining Wang**, a researcher in stylometry and authorship identification, with a PhD in Information Science from Indiana University Bloomington.

## Get started

**[Download your-voice.skill](https://raw.githubusercontent.com/Wang-Haining/your_voice/main/your-voice.skill)**

The `.skill` file is a ZIP containing the complete skill. If your app requires `.zip`, rename it to `your-voice.zip`. In [Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude), upload the ZIP through **Customize → Skills → Create skill → Upload a skill**.

For agents supported by the [Skills CLI](https://skills.sh):

```bash
npx skills add Wang-Haining/your_voice --global
```

Then ask:

> Use your-voice to make this draft sound like me. Find suitable examples of my previous writing, make three editing passes, and show me what changed.

You can supply reference documents, or let your agent find them in your project and public author repositories. It asks when it cannot establish who wrote them or find a suitable match.

## How it works

1. **Find your references.** Select writing with a similar purpose, audience and genre. For researchers, single-author work and confirmed author-written passages are preferred; older papers can help establish a baseline.
2. **Clear the stock phrasing.** Remove empty emphasis, repeated summaries and other formulaic prose without flattening your opinions or changing your claims.
3. **Measure the differences.** Compare function words, punctuation and sentence lengths. A regularized logistic regression identifies features that distinguish the draft from your references when there is enough comparable material.
4. **Edit in three passes.** Start with the largest differences and easiest useful fixes. Remeasure after each pass, preserve meaning, and show before/after examples and what still differs.

The approach follows an 80/20 principle: spend effort on a few consequential habits before chasing small differences. It does not force every word frequency to match.

## What you get

- A revised draft and concrete before/after examples.
- A small comparison of your reference writing, original draft and final version.
- A reusable local voice library and saved progress for the next session.

The bundled measurement script supports **English** and uses Python, NumPy and scikit-learn. It includes a transparent 157-word inventory; you can supply a verified alternative. With too little suitable text, the skill reports descriptive differences instead of classifier accuracy. The score is a diagnostic, not an AI detector or a percentage of how much the text sounds like you.

The analysis script has no network calls. Your AI app's own data-handling policies still apply to documents you share with it.

## Author and contact

**Haining Wang** · [GitHub](https://github.com/Wang-Haining) · [hw56@iu.edu](mailto:hw56@iu.edu)

Feedback and examples of what worked—or did not—are welcome through [Issues](https://github.com/Wang-Haining/your_voice/issues).

## License

[MIT](LICENSE). Packaging inspired by [Humanizer](https://github.com/blader/humanizer).
