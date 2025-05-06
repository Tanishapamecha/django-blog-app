# Django Blog App 

A fully functional blog platform built with Django. Users can register, log in, create, edit, and delete blog posts, upload profile pictures, and comment.

##  Features
- **User Authentication**: Register, login, logout
- **Blog Posts**: Create, edit, delete posts
- **Like Posts**: Users can like posts 
- **Profile Picture Upload**: Users can upload profile pictures 🖼️
- **Comment on Posts**: Add comments to blog posts 
- **Responsive UI**: Built using Bootstrap
- **REST API**: Exposes blog data via Django REST Framework

##  Tech Stack
- **Python**: Backend language
- **Django**: Web framework
- **Django REST Framework (DRF)**: For building REST APIs
- **SQLite**: Database (development)
- **Bootstrap**: Frontend for styling
- **GitHub Actions** (Optional for CI/CD): Set up for continuous integration

##  API Endpoints
Use tools like Postman or DRF’s browsable API to test the following endpoints:
- `GET /api/posts/` – List all posts
- `POST /api/posts/` – Create a new post
- `GET /api/posts/<id>/` – Retrieve post by ID
- `PUT /api/posts/<id>/` – Update post by ID
- `DELETE /api/posts/<id>/` – Delete post by ID
- `POST /api/comments/` – Add a comment
- `GET /api/comments/` – View comments

##  Live Demo
🔗 [Link to live app](#) (Coming Soon – Deployment in progress)

## ⚙ How to Run Locally
Follow these steps to run the app locally on your machine:

1. Clone the repository:
    ```bash
    git clone https://github.com/Tanishapamecha/django-blog-app.git
    ```
2. Navigate into the project directory:
    ```bash
    cd django-blog-app
    ```
3. Set up a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On Mac/Linux:
      ```bash
      source venv/bin/activate
      ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Apply migrations to set up the database:
    ```bash
    python manage.py migrate
    ```
7. Collect static files:
    ```bash
    python manage.py collectstatic
    ```
8. Run the Django development server:
    ```bash
    python manage.py runserver
    ```

The app will be running at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

##  Development Notes
- **Static and Media Files**: Ensure you properly configure static and media file handling during deployment. You can set `STATIC_ROOT` and `MEDIA_ROOT` in your `settings.py`.
- **API Testing**: Use Postman or the Django REST Framework’s UI to interact with API endpoints.
- **Running Tests**: You can add unit tests for API endpoints and models.

## 📝 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

