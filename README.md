# 🚀 SkillBridge Backend API

A production-style backend system for managing attendance in a state-level skilling programme.
Built using FastAPI with JWT authentication, role-based access control, and PostgreSQL.

---

# 📌 Live API

*(Add after deployment)*
Base URL: `https://your-api-url.com`

---

# 🧠 Overview

SkillBridge is a backend system supporting multiple roles:

* **Student** → Marks attendance
* **Trainer** → Creates sessions, manages batches
* **Institution** → Oversees batches
* **Programme Manager** → Views analytics
* **Monitoring Officer** → Read-only global access (special token)

---

# ⚙️ Tech Stack

* **Backend**: FastAPI
* **Database**: PostgreSQL (Neon)
* **ORM**: SQLAlchemy
* **Authentication**: JWT (python-jose)
* **Testing**: pytest
* **Deployment**: (Render / Railway)

---

# 🏗️ Project Structure

```
app/
 ├── api/
 ├── core/
 ├── db/
 ├── models/
 ├── schemas/
 ├── services/
 └── utils/

tests/
.env
requirements.txt
README.md
```

---

# 🔐 Authentication

### 🔑 JWT Token (Login)

Payload includes:

* `user_id`
* `role`
* `exp`

### 🔥 Monitoring Token (Special)

* Requires API key + JWT
* 1-hour expiry
* Scoped for monitoring endpoints only

---

# 🧪 Test Accounts

```
Student:
email: student0@mail.com
password: 123

Trainer:
email: trainer0@mail.com
password: 123

Institution:
email: inst1@mail.com
password: 123

Programme Manager:
(Create manually via signup)

Monitoring Officer:
(Create manually via signup)
```

---

# 🚀 Setup Instructions

## 1️⃣ Clone repo

```
git clone <your-repo-link>
cd skillbridge-backend
```

## 2️⃣ Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

## 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

## 4️⃣ Configure environment variables

Create `.env`:

```
DATABASE_URL=your_neon_db_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
MONITORING_API_KEY=supersecretmonitorkey
```

## 5️⃣ Run server

```
uvicorn app.main:app --reload
```

---

# 📊 Seed Data

The system automatically seeds:

* 2 Institutions
* 4 Trainers
* 15 Students
* 3 Batches
* 8 Sessions
* Attendance records

---

# 📡 API Endpoints

## 🔐 Auth

* `POST /auth/signup`
* `POST /auth/login`
* `POST /auth/monitoring-token`

---

## 📦 Batches

* `POST /batches`
* `POST /batches/{id}/invite`
* `POST /batches/join`

---

## 📅 Sessions

* `POST /sessions`
* `GET /sessions/{id}/attendance`

---

## 📊 Attendance

* `POST /attendance/mark`

---

## 📈 Reports

* `GET /batches/{id}/summary`
* `GET /programme/summary`

---

## 👁️ Monitoring

* `GET /monitoring/attendance`

---

# 🧪 Running Tests

```
pytest
```

---

# ⚠️ Error Handling

* `401` → Unauthorized
* `403` → Forbidden
* `404` → Not Found
* `422` → Validation error

---

# 🧠 Design Decisions

### 🔹 Many-to-Many Relationships

Used separate tables:

* `batch_students`
* `batch_trainers`

👉 Enables scalable querying and flexibility

---

### 🔹 Invite-Based Enrollment

* Token-based joining system
* Supports expiry + single-use

---

### 🔹 Dual Token System

Monitoring Officer uses:

* Login JWT
* Scoped monitoring token

👉 Adds extra security layer

---

# features

* Core API endpoints
* JWT + RBAC
* Monitoring system
* Seed data
* Tests




# Contact

Name: Varshitha L U
Email: luvarshitha3139@gmail.com
GitHub: https://github.com/varshithalu
LinkedIn: https://www.linkedin.com/in/varshithalu01
