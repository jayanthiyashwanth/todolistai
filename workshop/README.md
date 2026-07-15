# SmartTodoAI - Intelligent & Modern Task Management System

SmartTodoAI is a production-ready, beautiful, and secure Streamlit Todo List application designed with a dark glassmorphic UI, responsive grids, and real-time statistics. It operates entirely on a local JSON database and is fully prepared for instant deployment on hosting platforms like Render.

## Features

- 🔐 **Secure Authentication**: Hashed password registration and login using `bcrypt` to protect user credentials.
- 🎨 **Premium UI/UX Design**: Full dark mode, glassmorphic cards, gradient headers, custom buttons with micro-animations, and styled scrolls.
- 📊 **Real-time Analytics**: Tracks Total Tasks, Pending Tasks, Completed Tasks, and displays a graphical completion percentage.
- 📝 **Full CRUD Functionality**: Support for adding tasks, updating tasks dynamically through state-driven inline forms, and toggling task completion.
- 🗑 **Trash Recycle Bin (Soft Delete)**: Tasks deleted from the dashboard are moved to a professional History page where they can be restored or permanently destroyed.
- 👤 **Interactive Profile Management**: Tracks member details, metrics (Total, Completed, Pending), updates full name and email, and allows updating password credentials.
- 🚀 **Zero-Config Deployment**: Bundled with a custom `.streamlit/config.toml` layout and a `render.yaml` blueprint for one-click Render deployment.

---

## Project Structure

```text
SmartTodoAI/
├── .streamlit/
│   └── config.toml        # Theme and layout configuration
├── assets/
│   ├── logo.png           # AI generated application logo
│   └── background.jpg     # AI generated premium background pattern
├── database/
│   ├── users.json         # Users JSON database
│   └── todos.json         # Todos JSON database
├── pages/
│   ├── login.py           # User login portal
│   ├── register.py        # Account registration
│   ├── dashboard.py       # Main task control panel
│   ├── history.py         # Soft-deleted task manager
│   └── profile.py         # Profile & credential management
├── utils/
│   ├── auth.py            # Hashing and authentication helpers
│   ├── database.py        # JSON filesystem CRUD engine
│   ├── session.py         # Auth gates and session routing
│   ├── styles.py          # CSS injectors and custom sidebar navigation
│   └── validation.py      # Input constraint checkers
├── .env                   # Configuration parameters
├── app.py                 # Application router and entrypoint
├── README.md              # Project documentation
├── render.yaml            # Render deployment blueprint
└── requirements.txt       # Project python dependencies
```

---

## Local Setup Instructions

### 1. Prerequisites
Make sure you have **Python 3.12** or higher installed.

### 2. Clone and Navigate
Clone this repository and open the workspace folder.

### 3. Install Dependencies
Install all required libraries using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Streamlit development server locally:
```bash
streamlit run app.py
```
This will open the application in your default web browser (usually at `http://localhost:8501`).

---

## Render Deployment Blueprint

This project is pre-configured for **Render**.

1. Commit and push the project files to a GitHub repository.
2. Go to [Render](https://render.com) and sign in.
3. Click **New** > **Blueprint**.
4. Connect your GitHub repository.
5. Render will automatically parse the `render.yaml` file, provision a web service, install the dependencies, and deploy the application.
