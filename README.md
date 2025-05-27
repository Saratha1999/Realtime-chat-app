# Realtime Chat Application

A modern real-time chat application built with Django, Django Channels, WebSockets, and Bootstrap. Deployed on AWS EC2 using Docker containers with automated CI/CD pipeline via GitHub Actions and AWS ECR.

## Features

- **Public and Private Chat Rooms**: Open rooms and invitation-only private rooms
- **Direct Messaging**: One-on-one private conversations between users
- **Real-time Communication**: Instant messaging using WebSockets
- **Typing Indicators**: Live typing status updates
- **Message Management**: Users can delete their own messages
- **Theme Toggle**: Light/dark mode with localStorage persistence
- **Room Access Control**: Fine-grained permissions for private rooms
- **User Authentication**: Secure registration, login, and session management

## Technology Stack

**Backend:**
- Django 4.2+ - Web framework
- Django Channels - WebSocket support
- Redis - Message broker and session storage

**Frontend:**
- HTML5, Bootstrap 5, JavaScript
- WebSocket API for real-time communication

**Infrastructure:**
- Docker - Application containerization
- AWS EC2 - Cloud hosting
- AWS ECR - Docker container registry
- GitHub Actions - CI/CD pipeline

## Local Development Setup

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Redis

### Quick Start

1. **Clone Repository**
   ```bash
   git clone https://github.com/Saratha1999/Realtime-chat-app.git
   cd Realtime-chat-app
   ```

2. **Environment Setup**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Start Services**
   ```bash
   # Start Redis
   redis-server
   
   # Start Django with WebSocket support
   daphne -p 8000 chatapp.asgi:application
   ```

5. **Access Application**
   - Web Interface: `http://localhost:8000`

### Docker Development

```bash
# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Deployment Architecture

### AWS Infrastructure

**EC2 Instance:**
- Ubuntu 22.04 LTS
- Docker installed
- AWS CLI configured
- Security groups configured for HTTP/HTTPS/SSH
- Region: us-east-2

**ECR Repository:**
- Repository name: `realtime-chat-app`
- Region: us-east-2
- Stores Docker images with `latest` tag
- Integrated with GitHub Actions for automated pushes

## CI/CD Pipeline

### GitHub Actions Workflow

The pipeline is split into two separate workflows:

1. **Django CI** - Continuous Integration (testing)
2. **Django CD** - Continuous Deployment (build and deploy)

The CD workflow triggers automatically after CI completes successfully.

## Environment Variables

Required GitHub Secrets:

```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# EC2 Configuration
EC2_HOST=your-ec2-ip-address
EC2_SSH_KEY=your-private-key-content

# ECR Configuration
ECR_REGISTRY=your-account-id.dkr.ecr.us-east-2.amazonaws.com
```

Application Environment Variables:
```bash
# Django
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com,localhost

# Redis
REDIS_URL=redis://localhost:6379
```

## Deployment Process

### Initial Setup

1. **AWS ECR Repository**
   ```bash
   aws ecr create-repository --repository-name realtime-chat-app --region us-east-2
   ```

2. **EC2 Instance Setup**
   ```bash
   # Install Docker
   sudo apt update
   sudo apt install docker.io
   
   # Install AWS CLI
   sudo apt install awscli
   
   # Configure AWS credentials
   aws configure
   ```

3. **GitHub Secrets Configuration**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `EC2_HOST`
   - `EC2_SSH_KEY`
   - `ECR_REGISTRY`

### Automated Deployment

The deployment process:
1. **CI Workflow**: Runs tests on every push/PR
2. **CD Workflow**: Triggers after CI completes successfully
3. **Build**: Creates Docker image and pushes to ECR
4. **Deploy**: SSH to EC2, pulls latest image, stops old container, starts new container

### Container Deployment

The application runs as a single Docker container:
- Container name: `realtime-chat`
- Port mapping: `8000:8000`
- Automatic restart on deployment
- Old containers are stopped and removed before new deployment

## Project Structure

```
realtime-chat-app/
├── .github/workflows/     # GitHub Actions CI/CD
├── chatapp/               # Django project
├── chat/                  # Chat application
├── templates/             # HTML templates
├── static/                # Static files
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container definition
├── docker-compose.yml     # Docker services
└── README.md              # This file
```

## Troubleshooting

### Common Issues

**Docker Build Fails:**
```bash
# Check Dockerfile syntax
docker build -t test-image .

# View build logs
docker build --no-cache -t test-image .
```

**ECR Push Issues:**
```bash
# Login to ECR (us-east-2 region)
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-2.amazonaws.com

# Check repository exists
aws ecr describe-repositories --repository-names realtime-chat-app --region us-east-2
```

**EC2 Deployment Issues:**
```bash
# SSH to EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Check container status
docker ps

# View container logs
docker logs realtime-chat

# Check if container is running
docker inspect realtime-chat

# Manually pull and run container
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin your-ecr-registry
docker pull your-ecr-registry/realtime-chat-app:latest
docker run -d --name realtime-chat -p 8000:8000 your-ecr-registry/realtime-chat-app:latest
```

**GitHub Actions Failures:**
- Check repository secrets are configured
- Verify AWS permissions
- Review action logs in GitHub

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Push to your fork
5. Create a Pull Request

The CI/CD pipeline will automatically test and deploy approved changes.

**Deployment Status**: Production Ready with Automated CI/CD
