# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask (optional, but good practice)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose the port Flask runs on (if you prefer 8000, that's fine, but default is 5000)
EXPOSE 8000

# Run Flask app using 'flask run' command, with 0.0.0.0 to make it accessible externally
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
