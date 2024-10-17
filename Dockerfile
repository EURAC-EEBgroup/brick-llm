# Use the official Ollama Docker image
FROM ollama/ollama:latest

# Set a working directory for the model files
WORKDIR /root/.llm

# Download the .gguf file and place it in the .llm directory
# You can download the file manually if wget/curl does not support the direct link
# Using curl for this purpose
RUN apt-get update && apt-get install -y curl && \
    curl -L -o unsloth.Q4_K_M.gguf https://huggingface.co/Giudice7/llama31-8B-brick-v8/resolve/main/unsloth.Q4_K_M.gguf

# Create the Modelfile in the .llm directory
RUN echo "FROM ./unsloth.Q4_K_M.gguf" > Modelfile

# Expose port 11434
EXPOSE 11434

# Command to create the model in Ollama using the Modelfile
RUN ollama create llama3.1:8b-brick-v8 -f Modelfile

# Command to run Ollama and serve
ENTRYPOINT ["/bin/ollama"]
CMD ["serve"]
