FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run the standard FastAPI uvicorn server
CMD ["uvicorn", "main_app:app", "--host", "0.0.0.0", "--port", "8000"]
