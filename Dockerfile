FROM python:3.10

# Define the working directory inside the container
WORKDIR /app

# Copy the requirements and .env files before the rest of the code
COPY .env .
COPY requirements.txt .

# Install the requirements, without cache: --no-cache-dir?
RUN pip install -r requirements.txt

# Copy the rest of the source code into the container
COPY src/ ./src/

# Execute the application with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8038"]
