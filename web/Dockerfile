FROM python:3.12-slim
WORKDIR /web
COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY web/ .
CMD ["python", "app.py"]