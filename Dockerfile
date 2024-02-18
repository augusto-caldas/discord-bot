# Get python image
FROM python:latest

# Set docker directory
WORKDIR /app

# Install python libraries
RUN pip install discord
RUN pip install openai

# Copy files into container
COPY main.py .
COPY tokens.txt .

# Run script to start docker
CMD ["python", "./main.py"]
