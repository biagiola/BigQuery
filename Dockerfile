FROM python:3.12-slim

# 1. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Set the working directory
WORKDIR /app

# 3. Copy only dependency files
COPY pyproject.toml uv.lock ./

# 4. Install dependencies into the container
RUN uv sync --frozen --no-cache

# 5. Add the virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# 6. Copy the rest of your code (including config.py, database.py, etc.)
COPY . .

# 7. Start the app using uvicorn directly
# We use 0.0.0.0 so it's accessible externally
# We use the PORT environment variable provided by Cloud Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]