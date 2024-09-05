# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SentencePiece and Supervisor
RUN apt-get update && apt-get install -y cmake libprotobuf-dev protobuf-compiler supervisor
RUN pip install sentencepiece

# Install cloudflared
RUN apt-get install -y wget
RUN wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
RUN dpkg -i cloudflared-linux-amd64.deb

# Copy the rest of the application code
COPY . .

# Download models and save them in the image
RUN python download_models.py

# Create logs directory
RUN mkdir -p /app/logs

# Copy Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY config.yml /etc/cloudflared/config.yml

# Expose the port the app runs on
EXPOSE 8000

# Command to run Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
