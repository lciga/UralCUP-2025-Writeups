FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir cryptography

# Copy server script from deploy directory
COPY server.py ./server.py

# Expose the DH server port
EXPOSE 5099

# Launch the server
CMD ["python", "server.py"]
