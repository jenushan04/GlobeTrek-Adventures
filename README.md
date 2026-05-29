# 🌍 GlobeTrek Adventures

### ✈️ Full-Stack Travel & Tourism Management System

Built with **Django 4.2**, Bootstrap 5, Chart.js & SQLite

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite" />
  <img src="https://img.shields.io/badge/Responsive-Design-success?style=for-the-badge" />
</p>

---

## 📌 Overview

**GlobeTrek Adventures** is a modern full-stack travel & tourism management platform developed using **Django 4.2**.

The system allows customers to browse curated travel packages, make bookings, complete mock payments, submit inquiries, and manage trips — while staff and administrators manage operations through dedicated dashboards.

Designed with a clean **indigo-themed UI**, responsive layouts, and role-based access control.

---

# ✨ Key Features

## 👤 Customer Features

* 🔍 Browse tour packages with advanced filtering
* 🌍 Destination-based travel exploration
* 📅 Online booking system
* 💳 Mock payment integration
* 🧾 Booking history & cancellation
* ⭐ Leave reviews after completed trips
* 📩 Submit inquiries to support
* 👤 Profile management with image upload

---

## 🧑‍💼 Staff Features

* 📦 Tour package CRUD operations
* ✅ Confirm / cancel bookings
* 💬 Reply to customer inquiries
* 🏁 Mark trips as completed

---

## 👑 Admin Features

* 📊 Sales & revenue analytics dashboard
* 📈 Booking trends using Chart.js
* 👥 Staff account management
* 🔐 Full Django admin access
* 🧠 System-wide management controls

---

# 🛠 Tech Stack

| Layer    | Technology                     |
| -------- | ------------------------------ |
| Backend  | Django 4.2                     |
| Language | Python 3.10+                   |
| Database | SQLite                         |
| Frontend | Django Templates + Bootstrap 5 |
| Charts   | Chart.js                       |
| Styling  | Custom Indigo Theme            |
| Icons    | Bootstrap Icons                |
| Fonts    | Poppins + Inter                |

---

# 🎨 UI Theme

The project uses a custom **Indigo-inspired modern UI**.

| Theme Element | Color     |
| ------------- | --------- |
| Primary       | `#4F46E5` |
| Primary Dark  | `#3730A3` |
| Accent        | `#818CF8` |
| Success       | `#10B981` |
| Danger        | `#EF4444` |
| Warning       | `#F59E0B` |

---

# 🔐 Authentication & Security

* ✅ Session-based authentication
* ✅ Role-based access control
* ✅ CSRF protection
* ✅ Password reset functionality
* ✅ Server-side validation
* ✅ Client-side form validation
* ✅ Protected dashboards

---

# 📊 Admin Dashboard Reports

The admin dashboard includes:

* 📈 Revenue trends
* 📦 Booking statistics
* 🌟 Top-performing tour packages
* 👥 Customer activity insights

Powered by **Chart.js**.

---

# 📂 Project Structure

```bash
globetrek/
│
├── apps/
│   ├── accounts/
│   ├── tours/
│   ├── bookings/
│   ├── inquiries/
│   ├── dashboard/
│   └── core/
│
├── templates/
├── static/
├── media/
├── globetrek/
├── manage.py
└── requirements.txt
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/jenushan04/GlobeTrek-Adventures.git
cd globetrek-adventures
```

---

## 2️⃣ Create Virtual Environment

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5️⃣ Load Sample Data

```bash
python manage.py seed
```

This seeds:

* 👤 Admin users
* 👨‍💼 Staff accounts
* 🌍 Destinations
* 🎒 Tour packages
* 📅 Bookings
* 💬 Inquiries
* ⭐ Reviews

---

## 6️⃣ Run Server

```bash
python manage.py runserver
```

Open:

```bash
http://127.0.0.1:8000/
```

---

# 🧪 Demo Accounts

| Role        | Username    | Password     |
| ----------- | ----------- | ------------ |
| 👑 Admin    | `admin`     | `admin@1234` |
| 🧑‍💼 Staff | `staff1`    | `staff@1234` |
| 👤 Customer | `customer1` | `cust@1234`  |

---

# 🌐 Important Routes

| Route               | Description     |
| ------------------- | --------------- |
| `/`                 | Home Page       |
| `/tours/`           | Tour Packages   |
| `/dashboard/`       | Role Dashboard  |
| `/dashboard/admin/` | Admin Analytics |
| `/accounts/login/`  | Login           |
| `/admin/`           | Django Admin    |

---

# 📱 Responsive Design

The application is fully responsive and optimized for:

* 📱 Mobile
* 💻 Laptop
* 🖥 Desktop
* 📲 Tablet

---

# 🚀 Future Improvements

* 🌎 Real payment gateway integration
* 🧭 Google Maps integration
* 🤖 AI-based tour recommendations
* 📧 Email notifications
* 📱 REST API + Mobile App
* ☁️ Docker deployment


---

# 🧠 What I Learned

This project helped strengthen my understanding of:

* Django architecture
* Authentication systems
* Role-based authorization
* Full-stack CRUD workflows
* Dashboard analytics
* Responsive UI design
* Form validation & security

---

# 👨‍💻 Author

## Jenushan

Full Stack Developer from Sri Lanka 🇱🇰

* Django Development
* PostgreSQL
* SaaS Systems
* ERP / HRMS Platforms
* UI/UX Focused Web Applications

---

# ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 🧠 Share feedback
* 🚀 Connect with me

---

<p align="center">
  Made with ❤️ using Django
</p>
