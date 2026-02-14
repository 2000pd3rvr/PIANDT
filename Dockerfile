# Serve PIANDT static site on port 7860 (HF Spaces default for Docker)
FROM python:3.11-slim

WORKDIR /app
COPY . /app

EXPOSE 7860
CMD ["python", "server.py"]
