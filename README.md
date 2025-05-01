# Django Blog App 📝

A fully functional blog platform built with Django. Users can register, log in, create, edit, and delete blog posts, upload profile pictures, and comment.

## 🚀 Features
- User authentication (Login, Register, Logout)
- Create/edit/delete blog posts
- Like posts ❤️
- Upload profile pictures 🖼️
- Comment on posts
- Responsive UI using Bootstrap
- REST API using Django REST Framework

## 📂 Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (development)
- Bootstrap (frontend)

## 🧪 API Endpoints
Use tools like Postman or DRF’s browsable API to test:
- `/api/posts/` – List/Create
- `/api/posts/<id>/` – Retrieve/Update/Delete
- `/api/comments/` – Add/View comments

## 🌐 Live Demo
🔗 [Link to live app](#) (Coming Soon)

## ⚙️ How to Run Locally
```bash
git clone https://github.com/Tanishapamecha/django-blog-app.git
cd django-blog-app
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py runserver
