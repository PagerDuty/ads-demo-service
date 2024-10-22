# Use the official GCC image as the base image
FROM gcc:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the C source code into the container
COPY memory_usage_program.c .

# Compile the C program
RUN gcc -o memory_usage_program memory_usage_program.c

# Set the entry point to run the compiled program
ENTRYPOINT ["./memory_usage_program"]
