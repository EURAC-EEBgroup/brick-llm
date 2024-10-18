# Use the official Ollama Docker image
FROM ollama/ollama:latest

# Install curl to download the model file
RUN apt-get update && apt-get install -y curl

# Set a working directory for the model files
WORKDIR /root/.llm

# Download the .gguf file and place it in the .llm directory
RUN curl -L -o unsloth.Q4_K_M.gguf https://huggingface.co/Giudice7/llama31-8B-brick-v8/resolve/main/unsloth.Q4_K_M.gguf

# Create the Modelfile in the .llm directory
RUN echo "FROM ./unsloth.Q4_K_M.gguf" > Modelfile

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 11434
EXPOSE 11434

# Use the custom entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
