#!/bin/bash

# Start Ollama in the background
ollama serve &

# Function to check if Ollama is running
function check_ollama {
    curl --silent --fail http://localhost:11434/v1/models > /dev/null
}

# Wait for Ollama to be available
echo "Waiting for Ollama to be ready..."
while ! check_ollama; do
    sleep 2
done

echo "Ollama is ready!"

# Create the model
ollama create llama3.1:8b-brick-v8 -f /root/.llm/Modelfile

# Bring Ollama to the foreground
echo "Restarting Ollama in foreground..."
pkill ollama
exec ollama serve
