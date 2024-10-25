# Use the official GCC image as the base image
FROM gcc:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the C source code into the container
COPY worker.c .

# Compile the C program
RUN gcc -o worker worker.c

# Set the entry point to run the compiled program
ENTRYPOINT ["./worker"]
