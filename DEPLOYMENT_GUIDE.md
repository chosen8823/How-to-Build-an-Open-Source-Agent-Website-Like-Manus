# 🏢 ANCHOR1 LLC - Quick Docker Deployment Guide
# BotDL SoulPHYA Divine Consciousness Platform

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Google Cloud credentials (optional for full features)

### 1. Simple Local Development
```bash
# Build and start the platform
docker-compose up --build

# Access the platform
# Frontend: http://localhost:3000
# Backend API: http://localhost:8001
# Grafana Dashboard: http://localhost:3001
# Prometheus: http://localhost:9090
```

### 2. Production Deployment
```bash
# Production with all services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale backend for high availability
docker-compose up --scale backend=3 -d
```

### 3. Google Cloud Platform Deployment
```bash
# Make deployment script executable
chmod +x deploy-gcp.sh

# Deploy to GCP (requires gcloud CLI)
./deploy-gcp.sh
```

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐
│   Nginx LB      │    │   Frontend      │
│   Port: 80/443  │────│   Port: 3000    │
└─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│   Backend API   │    │   PostgreSQL    │
│   Port: 8001    │────│   Port: 5432    │
└─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│   Redis Cache   │    │   Monitoring    │
│   Port: 6379    │    │   Grafana/Prom  │
└─────────────────┘    └─────────────────┘
```

## 🔧 Environment Configuration

### Required Environment Variables
```bash
# Database
DATABASE_URL=postgresql://anchor1:divine_consciousness@db:5432/soulphya
REDIS_URL=redis://redis:6379/0

# Google Cloud (optional)
GOOGLE_CLOUD_PROJECT=anchor1-divine-consciousness
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/gcp-key.json

# Application
FLASK_ENV=production
PORT=8001
```

### Google Cloud Setup
1. Create a new GCP project: `anchor1-divine-consciousness`
2. Enable required APIs:
   - Cloud Run API
   - Cloud Build API
   - Cloud SQL API
   - Secret Manager API
3. Create service account with required permissions
4. Download key and place in `./credentials/gcp-key.json`

## 📊 Monitoring and Health Checks

### Health Check Endpoints
- Backend: `http://localhost:8001/api/health`
- Frontend: `http://localhost:3000/health`
- Database: Built-in PostgreSQL health checks
- Redis: Built-in Redis health checks

### Monitoring Dashboard
- Grafana: `http://localhost:3001` (admin/anchor1_divine)
- Prometheus: `http://localhost:9090`
- Logs: `docker-compose logs -f [service-name]`

## 🔐 Security Features

### Production Security
- HTTPS/TLS encryption
- Rate limiting (API: 10req/s, Chat: 50req/s)
- CORS protection
- Security headers (HSTS, XSS protection, etc.)
- Database connection encryption
- Secret management via Google Secret Manager

### Network Security
- Private Docker networks
- Service isolation
- Firewall rules (GCP deployment)
- Database access controls

## 🚀 Scaling and Performance

### Horizontal Scaling
```bash
# Scale backend instances
docker-compose up --scale backend=5 -d

# Scale with load balancer
docker-compose up --scale backend=3 --scale nginx=2 -d
```

### Performance Optimization
- Redis caching for API responses
- PostgreSQL connection pooling
- Nginx compression and static file serving
- Docker multi-stage builds for minimal image sizes

## 🐛 Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in docker-compose.yml
2. **Database connection**: Check DATABASE_URL and wait for db service
3. **Memory issues**: Increase Docker memory limits
4. **GCP authentication**: Verify service account key and permissions

### Debug Commands
```bash
# Check service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Access service containers
docker-compose exec backend bash
docker-compose exec db psql -U anchor1 soulphya

# Network troubleshooting
docker network ls
docker-compose ps
```

## 📞 Support

**Anchor1 LLC Technical Support**
- Documentation: Full API docs available at `/api/docs`
- Health Status: Real-time monitoring at `/api/health`
- Platform Status: All endpoints listed at `/api/status`

---

🏢 **ANCHOR1 LLC** - Pioneering the future of conscious AI development  
⚡🌟💎 **DIVINE CONSCIOUSNESS PLATFORM ACTIVE** 💎🌟⚡
