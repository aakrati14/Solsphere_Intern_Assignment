# 🖥️ Complete System Health Monitoring Solution – Utility + Backend API + Frontend (Admin Dashboard)

A complete cross-platform solution to monitor system security and configuration compliance across devices. This project includes:

- ✅ A Python-based **System Utility** (client)
- 🖥️ A **Flask-based Backend API server**
- 🌐 A **Web-based Admin Dashboard (Frontend)**

---

## 🛠️ Technologies Used

### ✅ System Utility (Client Script)
- **Language:** Python 3
- **Modules:** `subprocess`, `platform`, `schedule`, `requests`, `json`, `os`
- **Features:**
  - Cross-platform (tested on Windows)
  - Background task using `schedule`
  - System checks: disk encryption, OS updates, antivirus, and inactivity sleep
  - Sends data only when changes occur

### 🖥️ Backend API Server
- **Framework:** Flask
- **Database:** SQLite
- **Libraries:** `flask`, `flask-cors`, `sqlite3`, `datetime`, `csv`
- **Endpoints:**
  - `/report` - POST system health report
  - `/latest/<device_id>` - GET latest report for device
  - `/reports` - GET all latest reports with optional filters
  - `/export` - Download all reports in CSV

### 🌐 Frontend Admin Dashboard
- **Languages:** HTML, CSS, JavaScript (Vanilla JS)
- **Features:**
  - Input any device ID to view the latest report
  - View all device statuses with filter options
  - Flag issues visually with icons and color-coding
  - Export all reports to CSV

---

## 📦 Project Structure

```plaintext
submission_package/
│
├── backend/
│   ├── app.py              # Flask backend server
│   └── reports.db          # SQLite DB (auto-generated)
│
├── frontend/
│   ├── index.html          # Web dashboard
│   ├── style.css           # Styling for dashboard
│   └── script.js           # JavaScript for frontend logic
│
├── utility/
│   └── system_checker.py   # Python system utility script
│
├── screenshots/
│   └── dashboard_view.png  # Included screenshots here
│
└── README.md               # You're here!

```

🚀 Setup Instructions
🖥️ 1. Run Backend Server (Flask)
bash
cd backend
pip install flask flask-cors
python app.py

- Server will start at http://127.0.0.1:5000/reports

✅ 2. Run System Utility
bash
cd utility
pip install schedule requests
python system_checker.py

- Will run every 10 minutes (adjustable in script)
- Sends report only if a change is detected

🌐 3. View Frontend Dashboard
- Open frontend/index.html in your browser

- Enter a device ID to fetch its latest report

- Scroll to view all devices and use filters or export to CSV

📸 Screenshots
🌐 Web Dashboard

![Screenshot (267)](https://github.com/user-attachments/assets/1c9aa7f3-84d9-475b-b72c-ea15de138394)

🌐 Utility Output 

![Utility_output](https://github.com/user-attachments/assets/b4924847-0a06-4bac-a2d1-27edff896b11)




🛡️ Features Summary
System Utility
Checks:
✅ Disk encryption
🕒 OS update status
🛡️ Antivirus presence
😴 Sleep settings (≤10 min)

- Sends only if changes
- Lightweight daemon via schedule

Backend:
- SQLite DB to store reports
- RESTful API for interaction
- JSON-based secure reporting

Frontend:
- Fetch device-wise reports
- Flagging of misconfigurations
- CSV export
- Filters by OS status, antivirus, sleep issues, etc.

## 🌍 Live Deployment Links

### ✅ Backend API (Flask)
🔗 [https://your-backend-url.up.railway.app](https://your-backend-url.up.railway.app)

### 🌐 Admin Dashboard (Frontend)
🔗 [ https://system-health-frontend-dashboard01.netlify.app/ ]

> ℹ️ Note: The system utility (`system_checker.py`) is meant to run locally and is not deployed online.



