# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code and model
COPY app.py .
COPY templates ./templates
COPY land_value_model.pkl .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
