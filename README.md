# Career Ego Chatbot

A **Gradio-based AI chatbot** that acts as a **virtual persona** for a personal website.  
This project is designed to **answer questions** about an individual's **career and background** by leveraging their **LinkedIn profile** and a **personal summary**.  
A key feature is its **self-evaluation mechanism**, ensuring that all responses are **high-quality** and **accurately reflect** the individual's persona.

---

## 🚀 Features

### **AI Persona**
- Engages users in a **professional, conversational manner**, acting as a **digital representative** of an individual.

### **Context-Aware Responses**
- Uses data from:
  - **LinkedIn Profile** (`Profile.pdf`)
  - **Personal Summary** (`summary.txt`)
- Provides **informed** and **relevant** answers.

### **Self-Correction Loop**
- Uses an **AI-powered evaluator** to review and refine answers.
- If a response is **subpar**, it is **regenerated** based on **constructive feedback** before being sent to the user.

### **Tool Integration**
- The chatbot can:
  - Record **contact information** for interested users.
  - Log **unanswered questions**.
- Triggers **push notifications** via **Pushover** for **real-time alerts**.

---

## 🏗️ Architecture Overview

The application is built around **three core Python modules**:

| Module      | Description                                                                 |
|------------|-----------------------------------------------------------------------------|
| **main.py**    | Entry point for the app, managing the **Gradio chat interface** and the main **interaction loop**. |
| **prompts.py** | Builds detailed **system prompts** from the `.pdf` and `.txt` sources, shaping the AI's **persona** and **knowledge base**. |
| **tools.py**   | Defines external **functions** the AI can execute, such as recording data and sending notifications. |

---

## ⚡ Workflow

1. The chatbot **receives a user's message**.
2. A **context-rich prompt** is generated using the LinkedIn profile and personal summary.
3. The prompt is sent to the **Gemini API** for response generation.
4. The response is passed to a **separate evaluator agent**:
   - If **approved** → The response is sent to the user.
   - If **rejected** → A **new response** is generated using evaluator feedback.
5. During the process, the AI can **trigger tools** to:
   - Record data
   - Log unanswered questions
   - Send push notifications via **Pushover**

---

## 🛠️ Tech Stack

- **Python**
- **Gradio** – Interactive chat interface  
- **Gemini API** – Response generation  
- **Pushover API** – Real-time notifications  

---

## 📂 Project Structure

```bash
career-ego/
├── main.py         # Entry point for the chatbot app
├── prompts.py      # Builds prompts from LinkedIn + summary
├── tools.py        # External integrations (logging, notifications, etc.)
├── Profile.pdf     # LinkedIn profile data
├── summary.txt     # Personal career summary
└── README.md       # Project documentation
