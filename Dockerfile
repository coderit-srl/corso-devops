# Base image: official Python 3.12, "slim" variant.
# slim = Debian without compilers/docs — much smaller image (~50 MB vs ~1 GB).
FROM python:3.12-slim

# Set the working directory inside the container.
# All subsequent COPY and RUN commands will be relative to /app.
WORKDIR /app

# Copy the dependencies file BEFORE copying the source code.
# Docker builds in layers: if requirements.txt hasn't changed, this layer is
# cached and pip install is skipped on the next build — much faster.
COPY requirements.txt .

# Install Python dependencies.
# --no-cache-dir avoids writing the pip download cache to disk, keeping the
# image smaller (we don't need the cache after the build).
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code.
# This layer changes on every code edit, but the pip layer above is still cached.
COPY app/ ./app/

# Document that the container listens on port 8000.
# This is informational — it does NOT actually publish the port.
# The actual port mapping is done with `docker run -p 8000:8000` or in Koyeb settings.
EXPOSE 8000

# Default command: start the Uvicorn ASGI server.
# --host 0.0.0.0  → listen on all interfaces (required inside a container)
# --port 8000     → must match the EXPOSE value above
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
