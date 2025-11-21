# 🚀 KenPire Mesh OS - Production Deployment Guide

## Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/kenpire/kenpire-mesh-os-production.git
cd kenpire-mesh-os-production

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_production.py

# Start the server
python main.py server --host 0.0.0.0 --port 8080
```

### Docker Development
```bash
# Build and run with Docker
docker-compose up -d

# View logs
docker-compose logs -f kenpire-mesh-os

# Stop services
docker-compose down
```

### GitHub Codespaces (Recommended)
1. Click "Code" → "Create codespace on main"
2. Wait for environment to initialize
3. Run: `python main.py server`
4. Access via forwarded port

## Production Deployment

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n kenpire-mesh-os

# View logs
kubectl logs -f deployment/kenpire-mesh-os -n kenpire-mesh-os
```

### Environment Variables
Create `.env` file with required variables:
```env
# AI API Keys (Required)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key  
GOOGLE_API_KEY=your_google_key

# Database & Cache
DATABASE_URL=postgresql://user:password@host:port/db
REDIS_URL=redis://host:port

# Security
SECRET_KEY=your_secret_key_here

# Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### SSL/TLS Configuration
```bash
# Install certificates
kubectl create secret tls kenpire-tls \
  --cert=path/to/cert.pem \
  --key=path/to/key.pem \
  -n kenpire-mesh-os
```

## API Usage Examples

### Authentication
```bash
# Get API key (replace with actual endpoint)
curl -X POST https://api.kenpire.tech/auth/api-key \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Smart Card Processing
```bash
# Process a smart narrative card
curl -X POST https://api.kenpire.tech/api/v1/cards/process \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": "unique-card-id",
    "content": "Your narrative content here",
    "metadata": {
      "priority": "high",
      "category": "analysis"
    }
  }'
```

### AI Orchestration
```bash
# Orchestrate AI models
curl -X POST https://api.kenpire.tech/api/v1/ai/orchestrate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "analysis",
    "input": "Analyze this complex data...",
    "coordination": "trifecta_handshake",
    "models": ["gpt-4", "claude-3", "gemini-pro"]
  }'
```

### Mesh Consensus
```bash
# Achieve distributed consensus
curl -X POST https://api.kenpire.tech/api/v1/mesh/consensus \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "proposal": {
      "action": "update_config",
      "parameters": {"timeout": 30},
      "priority": "medium"
    },
    "consensus_type": "raft"
  }'
```

### System Status
```bash
# Check system status
curl -X GET https://api.kenpire.tech/api/v1/status \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Python SDK Usage

### Installation
```bash
pip install kenpire-mesh-os
```

### Basic Usage
```python
from kenpire import (
    SmartNarrativeCard,
    TrifectaCoordinator, 
    SecurityHardening,
    MeshOrchestrator
)

# Initialize components
security = SecurityHardening()
coordinator = TrifectaCoordinator()
mesh = MeshOrchestrator()

# Process smart card
card = SmartNarrativeCard("card-id", "content")
result = await card.process()

# AI orchestration
response = await coordinator.coordinate_models(
    task="analysis",
    input_data="Your data here"
)

# Mesh consensus
consensus = await mesh.achieve_consensus({
    "proposal": "system_update",
    "parameters": {"version": "2.1.0"}
})
```

### Advanced Configuration
```python
from kenpire.utils import config_utils, setup_logging

# Setup logging
setup_logging(level="INFO")

# Load configuration
config = config_utils.get_default_config()
env_config = config_utils.load_env_config()
config.update(env_config)

# Initialize with custom config
coordinator = TrifectaCoordinator(config=config)
```

## Monitoring & Observability

### Metrics Endpoints
- Health: `GET /health`
- Readiness: `GET /ready` 
- Metrics: `GET /metrics` (Prometheus format)
- Status: `GET /api/v1/status`

### Logging
```bash
# View application logs
kubectl logs -f deployment/kenpire-mesh-os -n kenpire-mesh-os

# View specific pod logs  
kubectl logs -f pod/kenpire-mesh-os-xyz -n kenpire-mesh-os

# Follow logs from multiple pods
kubectl logs -f -l app=kenpire-mesh-os -n kenpire-mesh-os
```

### Grafana Dashboards
Access monitoring dashboards at:
- Production: `https://monitoring.kenpire.tech/grafana`
- Staging: `https://staging-monitoring.kenpire.tech/grafana`

Default credentials: `admin/admin` (change on first login)

### Alerting
Alerts are configured for:
- High error rates (>10%)
- High latency (>1s p95)
- Pod failures
- Resource usage (CPU >80%, Memory >80%)

## Troubleshooting

### Common Issues

#### Pod Startup Failures
```bash
# Check pod events
kubectl describe pod <pod-name> -n kenpire-mesh-os

# Check container logs
kubectl logs <pod-name> -c kenpire-api -n kenpire-mesh-os
```

#### Database Connection Issues
```bash
# Test database connectivity
kubectl run test-db --rm -it --image=postgres:15 -- \
  psql $DATABASE_URL -c "SELECT 1"
```

#### Redis Connection Issues  
```bash
# Test Redis connectivity
kubectl run test-redis --rm -it --image=redis:alpine -- \
  redis-cli -u $REDIS_URL ping
```

#### SSL Certificate Issues
```bash
# Check certificate status
kubectl describe secret kenpire-tls -n kenpire-mesh-os

# Check ingress status
kubectl describe ingress kenpire-mesh-os-ingress -n kenpire-mesh-os
```

### Performance Tuning

#### Resource Optimization
```yaml
# Adjust resource requests/limits in k8s/deployment.yaml
resources:
  requests:
    memory: "512Mi"  # Increase for high load
    cpu: "500m"      # Increase for high load
  limits:
    memory: "1Gi"    # Set appropriate limits
    cpu: "1000m"     # Set appropriate limits
```

#### Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX CONCURRENTLY idx_cards_timestamp ON smart_cards(created_at);
CREATE INDEX CONCURRENTLY idx_sessions_user ON user_sessions(user_id);
```

#### Redis Configuration
```yaml
# Add Redis configuration in docker-compose.yml
redis:
  image: redis:alpine
  command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```

## Security Considerations

### API Security
- All endpoints require valid API keys
- Rate limiting configured (100 req/min)
- HTTPS enforced in production
- CORS properly configured

### Container Security
- Non-root user execution
- Read-only root filesystem
- Minimal base images
- Regular security scanning

### Network Security
- Network policies implemented
- Service mesh (optional)
- TLS encryption for all communication
- Secrets management with Kubernetes secrets

### Compliance
- GDPR compliance features
- Audit logging enabled  
- Data encryption at rest
- Regular security assessments

## Scaling Guidelines

### Horizontal Scaling
```bash
# Scale deployment manually
kubectl scale deployment kenpire-mesh-os --replicas=5 -n kenpire-mesh-os

# Auto-scaling is configured via HPA:
# - Min replicas: 3
# - Max replicas: 10
# - CPU target: 70%
# - Memory target: 80%
```

### Database Scaling
- Use read replicas for read-heavy workloads
- Implement connection pooling
- Consider database sharding for very large datasets

### Cache Scaling
- Redis cluster for high availability
- Implement cache warming strategies
- Monitor cache hit ratios

## Backup & Recovery

### Database Backups
```bash
# Create database backup
kubectl create job backup-db --from=cronjob/postgres-backup -n kenpire-mesh-os

# Restore from backup
kubectl apply -f backup/restore-job.yaml
```

### Configuration Backups
```bash
# Backup Kubernetes configurations
kubectl get all -n kenpire-mesh-os -o yaml > backup/k8s-config.yaml

# Backup secrets
kubectl get secrets -n kenpire-mesh-os -o yaml > backup/secrets.yaml
```

## Support & Maintenance

### Update Procedures
1. Test changes in staging environment
2. Run full test suite
3. Deploy during maintenance window
4. Monitor system health post-deployment
5. Have rollback plan ready

### Health Checks
- Automated health monitoring every 30 seconds
- Readiness probes every 10 seconds
- Liveness probes every 10 seconds

### Maintenance Windows
- Scheduled monthly maintenance: 1st Sunday 02:00-04:00 UTC
- Emergency maintenance as needed
- 48-hour advance notice for planned maintenance

---

## 🎯 Production Checklist

Before going live, ensure:

- [ ] All environment variables configured
- [ ] SSL certificates installed
- [ ] Database migrations completed
- [ ] Monitoring dashboards configured
- [ ] Alerting rules tested
- [ ] Backup procedures verified
- [ ] Load testing completed
- [ ] Security scan passed
- [ ] Documentation updated
- [ ] Team trained on operations

---

**Support Contact**: support@kenpire.tech  
**Documentation**: https://docs.kenpire.tech  
**Status Page**: https://status.kenpire.tech