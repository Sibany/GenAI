<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Logo" width="120" height="120">
</p>
<h1 align="center">GenAI Recruiter Chatbot</h1>

<p align="center">An AI-powered recruiter chatbot 🤖 that evaluates job candidates, schedules interviews, <br>
and simulates human-like conversations using OpenAI, LangChain, and Streamlit.<br>
  <a href="https://github.com/yourname/GAI-Project/issues">Report Bug</a>
  ·
  <a href="https://github.com/yourname/GAI-Project/issues">Request Feature</a>
</p></p>

---

## 💡 Overview

This project provides a modular chatbot system with specialized agents to:

- Ask screening questions
- Evaluate qualifications using a job description
- Schedule interviews from available time slots
- Politely exit conversations when needed



**Technologies used:**

- Python
- Streamlit
- LangChain
- OpenAI API
- Microsoft SQL Server

---

## 🚀 Features

- Modular design using LangChain agents
- Custom job description embedding for matching qualifications
- Automatic time slot generation from SQL Server
- Chat history export to JSON and text
- Streamlit-based UI

---

## 🚧 Installation

### Prerequisites

- Python 3.10+
- SQL Server with ODBC driver
- OpenAI API key

### Setup Steps

```bash
# Clone the repo
git clone https://github.com/yourname/recruiter-chatbot.git
cd recruiter-chatbot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📂 Database Setup

1. Open SQL Server Management Studio (SSMS)
2. Run `Tech.sql` to create the `Tech` database and fill the `dbo.Schedule` table

Create a `.env` file in the root directory with:

```
OPENAI_API_KEY=your_key
SQL_SERVER=your_server
DB_TECH=Tech
SQL_TRUSTED=yes
```

---

## 📃 Run the App

Follow the instructions below to launch your chatbot locally:

```bash
# Activate environment
source .venv/bin/activate

# Run the Streamlit chatbot app
streamlit run streamlit_main_new.py
```

---

## 🖼️ Screenshots

<p float="left">
  <img src="https://github.com/Sibany/GAI-Project/blob/main/Screenshot_22.jpg"  width="400"/>
  <img src="https://github.com/Sibany/GAI-Project/blob/main/WhatsApp%20Video%202025-08-06%20at%2022.26.36.gif"  width="400"/>
</p>



---

## 📒 Project Structure

```
recruiter-chatbot/
├── app_main_new.py             # LangChain agent orchestrator
├── module_2.py                 # Info advisor logic
├── module_exit.py             # Exit advisor logic
├── module_schedule.py         # Scheduling advisor logic
├── streamlit_main_new.py      # Streamlit interface
├── Tech.sql                   # SQL database creation script
├── README.md
```

---

## 🔹 Future Improvements

- [   ] Print all available slots of the selected date by user
- [   ] Reminder / Confirmation day before the meeting

---

## ✉️ Contact

**Shahaf Tobaly**\
Email: [tobaly.shahaf@gmail.com](mailto\:tobaly.shahaf@gmail.com)

**Nimrod Schweitzer**

Email: [snimsss@gmail.com](mailto\:snimsss@gmail.com)

**Maroon Sibany**

Email: [Sibany85@gmail.com](mailto\:Sibany85@gmail.com)

# GenAI
