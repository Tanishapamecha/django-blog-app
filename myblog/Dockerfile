# Step 1: Use official Python image as the base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt into the container
COPY requirements.txt /app/

# Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the Django project files into the container
COPY . /app/

# Step 6: Collect static files (for production)
RUN python manage.py collectstatic --noinput

# Step 7: Expose the port the app will run on
EXPOSE 8000

# Step 8: Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
