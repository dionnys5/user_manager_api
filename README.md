# 🧩 Django API Project

This is a Django-based project with integrated authentication using **JWT tokens** via `djangorestframework-simplejwt`. It also includes Django Admin, REST framework login UI, and application-specific routes.

---

## 🚀 Features

- 🔐 JWT Authentication (Login + Token Refresh)
- 🧭 REST Framework Browsable API
- ⚙️ Django Admin Interface
- 🧩 Modular URL structure

---

## 🛠️ Tech Stack

- Python 3.11+
- Django 4.x
- Django REST Framework
- SimpleJWT

---

## 🗂️ Project Routes

| Endpoint                    | Description                              |
|----------------------------|------------------------------------------|
| `/admin/`                  | Django Admin Panel                       |
| `/api-auth/`               | Login/logout UI from Django REST Framework |
| `/api/token/`              | Obtain JWT access and refresh token      |
| `/api/token/refresh/`      | Refresh JWT access token                 |
| `/`                        | Includes application-specific routes     |

> ✅ Your custom app routes should be defined in the `urls.py` included in the root with `include(urls)`.

---

## 🔐 Authentication

This project uses **JWT (JSON Web Token)** authentication via the `SimpleJWT` library.

### 🔑 Token Endpoints:
- **Login:**  
  `POST /api/token/`  
  **Payload:**  
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
