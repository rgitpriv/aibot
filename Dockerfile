FROM python:3.9-alpine

# Install dependencies
RUN apk add --no-cache gcc musl-dev openssl-dev libffi-dev python3 py3-pip

# Set working directory
WORKDIR /app

# Copy program files to container
COPY src/bot.py /app

# Install Python dependencies
RUN pip install irc openai

# Set the entrypoint to run the bot.py script with the specified command line arguments
ENTRYPOINT ["python3", "/app/bot.py"]

# Set default values for command line arguments
CMD ["--server", "irc.example.com", "--nickname", "my-bot", "--channel", "#my-channel", "--port", "6667"]

