FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

COPY backend ./backend
COPY ai-agent ./ai-agent
COPY monitor ./monitor
COPY tournament ./tournament
COPY postmortems ./postmortems

WORKDIR /app/backend

EXPOSE 5000

CMD ["python", "app.py"]
