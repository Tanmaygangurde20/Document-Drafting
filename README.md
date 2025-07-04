# 📝 Legal Document Drafting Assistant

A modern, production-ready Streamlit app for conversational legal document drafting using LLMs (OpenRouter). Draft NDAs, contracts, and leases through a guided chat interface. Only LLM-generated documents are shown for maximum reliability.

---

## Features
- **Conversational UI:** Answer questions, get a complete legal document.
- **LLM-powered:** Uses OpenRouter LLMs for high-quality, custom output.
- **No template fallback:** Only shows LLM-generated documents.
- **Session management:** Start new sessions, download results.
- **Modern, user-friendly design.**

---

## Quickstart

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get an OpenRouter API key:**
   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Copy your API key (starts with `sk-or-...`)

4. **Run the app:**
   ```bash
   streamlit run ui.py
   ```

5. **Enter your API key in the UI** when prompted.

---

## Usage
- **Describe your document** (e.g., "Draft an NDA between Alice and Bob").
- **Answer the AI's questions** to provide all required details.
- **Download your document** once generated (only LLM output is shown).

---

## Troubleshooting
- **401 Authentication Error:**
  - Double-check your API key (no spaces, correct key).
  - Make sure your OpenRouter account is active and has model access.
- **LLM Fallback Warning:**
  - If you see a warning about the LLM not generating the document, your API key is invalid or the LLM is unavailable.
  - Try a new session and re-enter your key.
- **No document shown:**
  - Only LLM-generated documents are displayed. If the LLM fails, you will see a warning instead.

---

## License
MIT License. See [LICENSE](LICENSE) for details.

---

## Credits
- Built with [Streamlit](https://streamlit.io/), [LangChain](https://python.langchain.com/), and [OpenRouter](https://openrouter.ai/). 