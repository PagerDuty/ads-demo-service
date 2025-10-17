# Copilot Instructions for ads-demo-service

## Repository Overview

This is a demo service used to test the Anomaly Detection Service (ADS). It consists of a simple C-based worker application that runs in a Kubernetes environment.

## Project Structure

- `worker.c` - Main C application that processes work with intentional memory behavior for testing
- `Dockerfile` - Container image definition using Alpine Linux with GCC
- `Makefile` - Build and deployment automation
- `infra/kubernetes/` - Kubernetes deployment configuration

## Technology Stack

- **Language**: C
- **Compiler**: GCC on Alpine Linux
- **Container**: Docker
- **Orchestration**: Kubernetes (via minikube for local development)
- **Build Tool**: Make

## Build Instructions

Build the Docker image and load it into minikube:
```bash
make build
```

This command:
1. Builds the Docker image with tag `worker:latest`
2. Removes any existing image from minikube
3. Loads the new image into minikube

## Deployment Instructions

Deploy to Kubernetes cluster:
```bash
make deploy
```

Delete from Kubernetes cluster:
```bash
make delete
```

Redeploy (delete and apply):
```bash
make redeploy
```

## Code Characteristics

The `worker.c` application:
- Processes work in a continuous loop
- Allocates memory buffers of configurable size (default: 10MB)
- Has intentional memory management behavior for testing purposes
- Runs indefinitely until stopped

## Resource Constraints

The Kubernetes deployment specifies:
- Memory limit: 64Mi
- CPU limit: 250m
- Image pull policy: IfNotPresent

## Development Guidelines

1. **C Code Changes**: When modifying `worker.c`, ensure proper compilation with GCC
2. **Memory Management**: Be aware that this is a demo service with intentional resource usage patterns
3. **Docker Changes**: If modifying the Dockerfile, test the build locally before deployment
4. **Kubernetes Config**: Changes to deployment.yaml should consider the resource constraints
5. **Testing**: This is a demo service - test changes in a minikube or development cluster before production

## Common Tasks

- **Modify memory allocation size**: Update the `PAYLOAD_MB` define in `worker.c`
- **Change resource limits**: Edit `infra/kubernetes/deployment.yaml`
- **Update base image**: Modify the `FROM` directive in `Dockerfile`
- **Adjust replica count**: Update `replicas` in the deployment configuration

## Important Notes

- This service is designed for testing and demonstration purposes
- The worker intentionally demonstrates specific resource usage patterns
- Always test in a development environment (minikube) before deploying elsewhere
- Monitor resource usage to ensure the service behaves as expected for testing scenarios
