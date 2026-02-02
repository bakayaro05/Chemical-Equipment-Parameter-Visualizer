# Chemical Equipment Parameter Visualizer  
**Hybrid Web + Desktop Application**

A hybrid **Web + Desktop data visualization application** for analyzing chemical equipment parameters from CSV files.  
Built using a **single Django REST backend**, consumed by both **React (Web)** and **PyQt5 (Desktop)** frontends.

---



https://github.com/user-attachments/assets/57c26379-ff31-4c86-9520-3bec8fc4cffa



## 🚀 Project Overview

This application allows users to:

- Upload a CSV file containing chemical equipment data
- View computed summary statistics
- Visualize equipment distribution using charts
- View upload history (last 5 datasets)
- Click history items to reload full summaries & charts
- Download a generated PDF report
- Use the same backend for both Web & Desktop apps

---

##🛠 Tech Stack
<pre>
| Layer             | Technology                      |
| ----------------- | ------------------------------- |
| Backend           | Django + Django REST Framework  |
| Data Processing   | Pandas                          |
| Database          | SQLite                          |
| Web Frontend      | React.js + Chart.js             |
| Desktop Frontend  | PyQt5 + Matplotlib              |
| PDF Generation    | ReportLab                       |
| API Communication | Axios (Web), Requests (Desktop) |
</pre>

---

## 📁 Project Structure

<pre>
  chemical-visualizer/
│
├── server/                 # Django backend
│   ├── api/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── migrations/
│   ├── db.sqlite3
│   └── manage.py
│
├── web/                    # React web frontend
│   ├── public/
│   ├── src/
│   │   ├── api.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── App.css
│   ├── package.json
│   └── README.md
│
├── desktop/                # PyQt5 desktop frontend
│   ├── main.py
│   ├── api.py
│   ├── charts.py
│   └── __pycache__/
│
└── README.md               # Project documentation

</pre>
---
## ⚙️ Backend Setup (Django)

## 1️⃣ Install dependencies

pip install django djangorestframework pandas reportlab django-cors-headers

## 2️⃣Run migrations

cd server
python manage.py migrate

## 3️⃣ Start the backend server
python manage.py runserver
backend runs at : 
http://127.0.0.1:8000

---

## 🌐 Web Frontend Setup (React)

## 1️⃣ Install dependencies

cd web
npm install

## 2️⃣ Start React app

npm start
Web app runs at:
http://localhost:3000

## Web Features

- CSV upload
- Summary statistics
- Chart.js bar chart visualization
- Upload history (clickable)
- PDF report download

---

## 🖥 Desktop Frontend Setup (PyQt5)

## 1️⃣ Install dependencies

pip install pyqt5 matplotlib requests

## 2️⃣ Run the desktop app

cd desktop
python main.py

## Desktop Features

- CSV upload
- Summary display
- Matplotlib bar chart
- Upload history (clickable)
- PDF report download (opens browser)

---

## 🔌 API Endpoints
<pre>
| Method | Endpoint             | Description                |
| ------ | -------------------- | -------------------------- |
| POST   | `/api/upload/`       | Upload CSV and get summary |
| GET    | `/api/history/`      | Fetch last 5 uploads       |
| GET    | `/api/dataset/<id>/` | Fetch dataset summary      |
| GET    | `/api/pdf/`          | Download PDF report        |
  
</pre>


