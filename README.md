# CivicLens AI

Understand important documents in seconds.

## Problem Statement
Lengthy official documents, government notices, and legal requirements are often dense and difficult to quickly understand. Important deadlines, requirements, and actions are buried in paragraphs of jargon.

## Solution
**CivicLens AI** is an open-source tool built to help users quickly understand lengthy and complicated official documents. By simply pasting text or uploading a document, users can get a concise AI-generated summary, a word-count analysis, and an extraction of important dates, requirements, and actions.

## Features
- **Document Input:** Paste text directly or upload a `.txt` file.
- **AI Summarization:** Uses a state-of-the-art Hugging Face model (`Falconsai/text_summarization`) to generate concise summaries.
- **Document Analysis:** View original vs. summary word counts, reduction percentage, and sentence count.
- **Important Information Extraction:** Automatically highlights dates, requirements, and required actions.
- **Sample Documents:** One-click loading of sample documents to test the application.
- **Clean UI:** Professional, responsive Streamlit interface.

## Architecture & Technology Stack
- **Frontend / Backend:** Python & [Streamlit](https://streamlit.io/)
- **AI Model Integration:** [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- **Machine Learning Backend:** PyTorch

## AI Model Used
This application uses **[Falconsai/text_summarization](https://huggingface.co/Falconsai/text_summarization)** from Hugging Face.

**Why this model?**
It is a fast, efficient, open-source summarization model fine-tuned on T5. It provides excellent results for general document summarization without relying on proprietary or paid APIs like OpenAI or Gemini, ensuring the project remains fully open-source and free to run.

## Installation Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/civiclens-ai.git
   cd civiclens-ai
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Local Run Instructions
To run the application locally:
```bash
streamlit run app.py
```
The application will open in your default web browser (usually at `http://localhost:8501`). The first time you run it, the Hugging Face model will be downloaded automatically.

## Streamlit Deployment Instructions
This project is ready to be deployed on [Streamlit Community Cloud](https://streamlit.io/cloud):
1. Push your code to a public GitHub repository.
2. Log in to Streamlit Community Cloud and click **New app**.
3. Select your repository, branch, and set the main file path as `app.py`.
4. Click **Deploy!**
*Note: No API keys or secrets are required since the model is loaded directly from Hugging Face.*

## Open-Source Contribution Instructions
We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on how you can help improve CivicLens AI.

## Responsible AI Disclaimer
AI-generated summaries may contain errors. Always verify important information against the original document. This tool does not provide official legal or government advice.
