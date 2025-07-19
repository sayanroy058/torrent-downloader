FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-libtorrent && pip install -r requirements.txt

# Copy app files
COPY . .

EXPOSE 10000

# Start the app
CMD ["bash", "start.sh"]
