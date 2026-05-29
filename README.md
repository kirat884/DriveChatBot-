# DriveChatBot 🤖📁
An intelligent, stateful Conversational AI Assistant built with Python and the modern Google GenAI SDK that seamlessly searches and filters files within a designated Google Drive folder using natural language.

🔗 **Live Production Demo:** [https://drivechatbot.onrender.com/](https://drivechatbot.onrender.com/)

---

## 🚀 My Refactoring & Engineering Journey

I originally built a raw prototype of this concept in my legacy [drive-agent](https://github.com/kirat884/drive-agent) repository, which was functional but had unoptimized dependencies, stateless logic, and hardcoded local configurations.

For this repository (**DriveChatBot**), I refactored the entire system from the ground up to professional, production-grade engineering standards:

* **Modern SDK Migration:** Upgraded from the deprecated `google-generativeai` package to the state-of-the-art `google-genai` SDK.
* **Production Security:** Implemented multi-environment fallback authentication (using `GOOGLE_CREDENTIALS_JSON` environment variables for secure Render hosting, and a robust `.gitignore` shield to keep local keys safe).
* **Dependency Optimization:** Resolved Linux-build `ResolutionImpossible` conflicts by cleaning up cluttered Windows `pip freeze` specifications into a high-level, platform-agnostic `requirements.txt`.
* **Stateful Chat Memory:** Upgraded from stateless one-off LLM requests to a persistent, stateful `chats.create` session object stored inside Streamlit's `st.session_state` vault.

---

## 🛠️ Technology Stack
* **Language:** Python 3.11
* **AI Model:** Google Gemini 2.5 Flash
* **SDK:** `google-genai` (Modern official SDK)
* **Frontend:** Streamlit (Chat UI elements & Session Memory)
* **Cloud API:** Google Drive API v3 (OAuth 2.0 Service Account)
* **Deployment:** Render Cloud Platform
