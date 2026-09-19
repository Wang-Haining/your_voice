# Your Voice <img src="assets/logo.png" alt="Your Voice pixel-art speech bubble and text cursor" align="right" width="80">

**Make AI sound like you.**

Learns from your writing. Refines drafts in three passes.

## Get started

**[Download your-voice.skill](https://raw.githubusercontent.com/Wang-Haining/your_voice/main/your-voice.skill)**

The `.skill` file is a ZIP. Rename it to `.zip` if your app requires it, then upload through its Skills settings.

For agents supported by the [Skills CLI](https://skills.sh):

```bash
npx skills add Wang-Haining/your_voice --global
```

Then ask:

> Use your-voice to make this draft sound like me. Find my previous writing and show me what changed.

## How it works

1. Find your writing with a similar purpose and audience.
2. Remove stock AI phrasing; compare function words, punctuation and sentence lengths with logistic regression.
3. Fix the largest useful differences first, over three passes. Show the changes and preserve your meaning.

Includes a reusable voice library and before/after measurements. English analysis uses Python, NumPy and scikit-learn. Small samples get descriptive comparisons, not classifier claims. This is not an AI detector. Your AI app's data policies apply.

## Author and contact

Built by **Haining Wang**, a stylometry and authorship-identification researcher. PhD in Information Science, Indiana University Bloomington.

[hw56@iu.edu](mailto:hw56@iu.edu) · [Feedback](https://github.com/Wang-Haining/your_voice/issues)

## License

[MIT](LICENSE). Packaging inspired by [Humanizer](https://github.com/blader/humanizer).
