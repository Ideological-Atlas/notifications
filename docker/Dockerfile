FROM python:3.14-slim

# Prepare work directory
RUN mkdir -p /src
WORKDIR /src

# Install uv system-wide
RUN pip install --no-cache-dir uv
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Copy only dependency files first to leverage Docker cache
COPY src/pyproject.toml src/uv.lock /src/

# Install dependencies
RUN uv sync --frozen --no-install-project

# Create logs dir
RUN mkdir -p /src/logs

# Copy source code
COPY src/ /src/

# Install the project itself
RUN uv sync --frozen

# Add terminal colors
COPY docker/.bashrc /root/.bashrc

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
