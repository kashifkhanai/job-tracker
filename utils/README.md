# 💼 Job Tracker – Role-Based Job Portal API

**Job Tracker** is a modern and secure job portal backend built with **FastAPI**, **MongoDB**, and **JWT Authentication**. It supports three distinct user roles — `Job Seeker`, `Employer`, and `Admin` — allowing them to register, login, post or view jobs, and manage users through well-organized and secure APIs.

---

## 🚀 Features

- ✅ User Registration & Secure Login (Email/Username based)
- 🔐 JWT Token Authentication
- 🧠 Role-Based Access: Job Seekers, Employers, Admins
- 💼 Employers can Post Jobs
- 🔍 Job Seekers can View & Filter Jobs
- 🧹 Admin Panel: View, Add, and Delete Users
- 🌐 Responsive Frontend with Dark/Light Mode
- 🧪 Clean API Structure with Pydantic Schemas & Validators
- 📦 MongoDB Integration using Motor (Async I/O)
- 🐳 Dockerized Setup with `.env` Configuration

---

## 🛠️ Tech Stack

| Layer        | Technology                      |
|--------------|----------------------------------|
| Framework    | FastAPI                          |
| Database     | MongoDB (Async Motor)            |
| Auth         | OAuth2 + JWT (PyJWT)             |
| Validation   | Pydantic v2                      |
| Passwords    | PassLib (`bcrypt`)               |
| Frontend     | HTML + CSS (Dark/Light Mode)     |
| DevOps       | Docker, Docker Compose           |

---

## 🔐 Role Permissions

| Role        | Permissions                              |
|-------------|-------------------------------------------|
| Job Seeker  | View jobs, filter by title                |
| Employer    | Post jobs                                 |
| Admin       | Manage all users (add/delete/view)        |

---

## 🔁 API Endpoints Overview

### Authentication Routes

| Method | Endpoint         | Description                        |
|--------|------------------|------------------------------------|
| POST   | `/auth/register` | Register as job seeker/employer    |
| POST   | `/auth/login`    | Login via email/username           |

### Job Routes (Job Seekers & Employers)

| Method | Endpoint                           | Role        | Description               |
|--------|------------------------------------|-------------|---------------------------|
| POST   | `/jobs/post`                       | Employer    | Post a new job            |
| GET    | `/jobs/all`                        | Job Seeker  | View all jobs             |
| GET    | `/jobs/titles`                     | Job Seeker  | Get distinct job titles   |
| GET    | `/jobs/filter-by-title?title=XYZ`  | Job Seeker  | Filter jobs by title      |

### Admin Routes

| Method | Endpoint              | Description               |
|--------|-----------------------|---------------------------|
| GET    | `/admin/users`        | View all users (no passwords) |
| POST   | `/admin/add-admin`    | Add a new admin           |
| DELETE | `/admin/user/{id}`    | Delete user by ID         |

---

## ⚙️ Local Development Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/kashifkhanai/job-tracker.git
cd job-tracker
```

### Step 2: Create Virtual Environment

```bash

python -m venv env
source env/bin/activate  

# Step 3: Install Requirements

pip install -r requirements_fronted.txt
    #  **OR**
### If want run just Backend
pip install -r requirements.txt

```

---

### Step 4: Create .env File

Create a **.env** file in root with this content:

```bash

MONGO_URL=mongodb://localhost:27017
MONGO_INITDB_DATABASE=jobtracker

SECRET_KEY=your-strong-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

APP_NAME=Job Tracker
APP_VERSION=1.0.0
PORT=8000

```

---

### Step 5: Run the Server

```bash
uvicorn run:app --reload
```

Visit: <http://127.0.0.1:8000>

---

***🐳 Docker Setup (Optional)***
Make sure Docker & Docker Compose are installed.

### Step 1: Build and Run

```bash
docker-compose up --build
```

#### This will

- Build the Docker image
- Run the container
- Map port 8000 from the container to your local machine
- Map the MongoDB container to your local machine

---

## 🤝 Author

Made with  by **Muhammad Kashif**  

📧 Contact: <mkashifkhanai@gmail.com>

🔗 [LinkedIn](https://www.linkedin.com/in/muhammadxkashif) • [GitHub](https://github.com/kashifkhanai)

## 📄 License

This project is licensed under the [MIT License](./).

---
