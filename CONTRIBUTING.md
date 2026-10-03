# Contributing to CivicLens AI

First off, thank you for considering contributing to CivicLens AI! It's people like you that make CivicLens AI such a great tool.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check if there's already an issue open for it. If not, open a new issue!

## Fork & create a branch

If this is something you think you can fix, then fork CivicLens AI and create a branch with a descriptive name.

## Get the test suite running

Make sure you're using Python 3.8+ and install the dependencies in `requirements.txt`.
Make sure the application runs correctly using `streamlit run app.py`.

## Implement your fix or feature

At this point, you're ready to make your changes. Feel free to ask for help!

## Make a Pull Request

At this point, you should switch back to your master branch and make sure it's up to date with CivicLens AI's master branch:

```bash
git remote add upstream https://github.com/yourusername/civiclens-ai.git
git fetch upstream
git merge upstream/master
```

Then update your feature branch from your local copy of master, and push it!

Finally, go to GitHub and make a Pull Request.

## Keeping it Open-Source
Remember that this project is strictly open-source and relies on openly available models like those on Hugging Face. Please do not add proprietary API dependencies (e.g. OpenAI, Anthropic, Google Gemini).
