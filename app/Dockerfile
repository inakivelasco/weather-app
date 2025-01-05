FROM python:3.12-slim
WORKDIR /app

# Copy only the requirements.txt first
COPY app/requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY app/ .

CMD ["python", "app.py"]
# TODO mejorar