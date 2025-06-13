# CodeLighthouse-Back

**Backend service for CodeLighthouse** – a full-stack coding assessment and learning platform designed to offer real-time feedback, user authentication, and collaborative features. The backend handles core business logic, data persistence, and API delivery for the CodeLighthouse system.

---

## 🔍 Overview

The `CodeLighthouse-Back` service is the server-side component powering:
- User registration, authentication, and session management  
- RESTful API endpoints for problem sets, coding submissions, and results  
- Database integration for users, submissions, analytics, and achievements

This service is designed to work in tandem with the `CodeLighthouse-Front` UI.

---

## ⚠️ Security Notice

Some API keys or tokens may appear to be exposed in commit history or `.env` examples. **These keys were used strictly for testing and demonstration purposes and were immediately deactivated.**  
No active credentials are exposed in the current version.

---

## 🛠 Technologies Used

- **Language & Framework:** Python 3 + Django / Django REST Framework  
- **Real-time Communication:** Django Channels (WebSocket support)  
- **Database:** PostgreSQL  
- **Containerization:** Docker & Docker Compose  
- **Deployment:** NGINX + Gunicorn  
- **CI/CD Integration:** Jenkins pipeline for builds and automated testing

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose  
- Node.js & npm (optional, for integration testing)

## 🧩 API Endpoints (Examples)

| Endpoint                      | Description                                  |
|------------------------------|----------------------------------------------|
| `POST /api/auth/register/`   | User registration                            |
| `POST /api/auth/login/`      | User login and JWT/session issuance          |
| `GET /api/problems/`         | Retrieve coding problems list                |
| `POST /api/submit/`          | Submit code for evaluation                   |
| `GET /api/feedback/{id}/`    | Get real-time/cached code evaluation results |

---

## 📄 License

MIT License.

---

## 📬 Contact

Maintainer: [Ștefan Secrieru](https://stefansecrieru.com)  
GitHub: [@Stefan3002](https://github.com/Stefan3002)
