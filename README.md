#  SkillBridge Backend API

A role-based attendance management backend built using FastAPI, PostgreSQL (Neon), and JWT authentication.

This project simulates a state-level skilling programme system with multiple roles and strict backend-enforced access control.

---

# 📌 Live API

*(Add after deployment)*
Base URL: `https://your-api-url.com`

---

# 🧠 Overview

SkillBridge supports five roles:

* **Student** → Marks attendance
* **Trainer** → Creates sessions, manages batches
* **Institution** → Views batch-level analytics
* **Programme Manager** → Views programme-level analytics
* **Monitoring Officer** → Read-only global access via scoped token

---

# ⚙️ Tech Stack

* **Backend**: FastAPI
* **Database**: PostgreSQL (Neon)
* **ORM**: SQLAlchemy
* **Authentication**: JWT (python-jose)
* **Testing**: pytest
* **Deployment**: Render / Railway

---

# 🚀 Local Setup

```bash
git clone <your-repo-link>
cd skillbridge-backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env`:

```env
DATABASE_URL=your_neon_db_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
MONITORING_API_KEY=supersecretmonitorkey
```

Run server:

```bash
uvicorn app.main:app --reload
```

---

# 🧪 Test Accounts

Seeded accounts:

```
Student:
student0@mail.com / 123

Trainer:
trainer0@mail.com / 123

Institution:
inst1@mail.com / 123
```

Manual signup required:

```
Programme Manager
Monitoring Officer
```

---

# 🔐 Authentication

## Standard JWT

Payload:

```json
{
  "user_id": int,
  "role": "student | trainer | institution | programme_manager | monitoring_officer",
  "exp": timestamp
}
```

---

## Monitoring Token (Scoped)

Flow:

1. Login → get JWT
2. Call `/auth/monitoring-token` with API key
3. Receive **1-hour scoped token**

Payload includes:

```json
{
  "user_id": int,
  "role": "monitoring_officer",
  "scope": "monitoring",
  "exp": timestamp
}
```

Used ONLY for:

```
GET /monitoring/attendance
```

---

# 📡 API Usage (cURL Examples)

## 🔹 Signup

```bash
curl -X POST http://127.0.0.1:8000/auth/signup \
-H "Content-Type: application/json" \
-d '{"name":"User","email":"user@mail.com","password":"123","role":"student"}'
```

---

## 🔹 Login

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"student0@mail.com","password":"123"}'
```

---

## 🔹 Create Batch (Trainer)

```bash
curl -X POST http://127.0.0.1:8000/batches \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"name":"Batch A","institution_id":1}'
```

---

## 🔹 Join Batch (Student)

```bash
curl -X POST http://127.0.0.1:8000/batches/join \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"token":"invite-token"}'
```

---

## 🔹 Mark Attendance

```bash
curl -X POST http://127.0.0.1:8000/attendance/mark \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"session_id":1,"status":"present"}'
```

---

## 🔹 Monitoring Token

```bash
curl -X POST http://127.0.0.1:8000/auth/monitoring-token \
-H "Authorization: Bearer <LOGIN_TOKEN>" \
-H "Content-Type: application/json" \
-d '{"key":"supersecretmonitorkey"}'
```

---

## 🔹 Monitoring Attendance

```bash
curl -X GET http://127.0.0.1:8000/monitoring/attendance \
-H "Authorization: Bearer <MONITOR_TOKEN>"
```

---

# 🧱 Schema Design Decisions

### 🔹 Many-to-Many Relationships

Used:

* `batch_students`
* `batch_trainers`

This ensures scalability and avoids duplication.

---

### 🔹 Invite System

* Token-based batch joining
* Supports expiry and single-use
* Decouples enrollment logic from direct DB writes

---

### 🔹 Dual Token Architecture

Monitoring officer uses:

* Login JWT (authentication)
* Scoped token (authorization)

This isolates read-only access securely.

---

# 🧪 Tests

Run:

```bash
pytest
```

Covers:

* Signup + login
* Session creation
* Attendance marking
* Monitoring 405 check
* Unauthorized access

---

# ⚠️ Error Handling

* `401` → Missing/invalid token
* `403` → Role not permitted
* `404` → Invalid resource
* `422` → Validation failure

---

# ✅ What’s Complete

* Full core API
* JWT + RBAC
* Monitoring dual-token system
* Seed data
* Basic test coverage

---

# ⚠️ What’s Partially Done / Missing

* `GET /institutions/{id}/summary` (not implemented)
* Some tests are minimal and can be expanded
* No pagination for large datasets

---

# 🔧 One Improvement (If More Time)

I would implement **token revocation / blacklist system** to invalidate tokens before expiry, improving security in real-world deployments.

---

# Contact

Name: Varshitha L U
Email: [luvarshitha3139@gmail.com](mailto:luvarshitha3139@gmail.com)
GitHub: https://github.com/varshithalu
LinkedIn: https://www.linkedin.com/in/varshithalu01
