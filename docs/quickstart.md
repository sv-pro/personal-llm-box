# Quick Start Guide

## Automated Setup (Recommended)

The project includes a smart setup script that automatically detects your system configuration and sets up the optimal environment.

```bash
# Run the setup script
./setup.sh

# Follow the on-screen instructions
# The script will:
# - Detect if you have native Ollama installed
# - Check your system resources (RAM, GPU VRAM)
# - Recommend the best model for your hardware
# - Generate an optimized docker-compose.yml

# Start the services
docker-compose up -d

# Access the applications
# - Open WebUI: http://localhost:3000
# - Backend API: http://localhost:8000
# - Health check: http://localhost:8000/health
```

## What the Setup Script Does

### Native Ollama Detection
- **If native Ollama is found and running:**
  - Configures Docker containers to use your native Ollama service
  - Saves resources by not running Ollama in Docker
  - Uses `host.docker.internal` networking

- **If no native Ollama:**
  - Includes Ollama container in docker-compose.yml
  - Automatically pulls the recommended model after startup

### Model Recommendation

Based on your GPU VRAM:

| VRAM | Recommended Model | Size |
|------|------------------|------|
| 16GB+ | qwen2.5:14b | ~9GB |
| 8-16GB | qwen2.5:7b | ~4.7GB |
| 4-8GB | qwen2.5:3b | ~2GB |
| <4GB (CPU) | tinyllama | ~637MB |

### Resource Detection

The script checks:
- Total and available RAM
- GPU presence and VRAM capacity
- Ollama installation status and version
- Available Ollama models

## Manual Setup (Alternative)

If you prefer manual configuration:

1. **Edit `docker-compose.yml`** manually:
   - Set `OLLAMA_MODEL` to your preferred model
   - Configure Ollama service (Docker or native)

2. **Start services:**
   ```bash
   docker-compose up -d
   ```

3. **If using Docker Ollama, pull the model:**
   ```bash
   docker exec personal-llm-box-ollama ollama pull qwen2.5:3b
   ```

## Verification

After setup, verify all services are working:

```bash
# Check service status
docker-compose ps

# Test health endpoint
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# Test artifact save
curl -X POST http://localhost:8000/artifact/save \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"Hello world","tags":["test"]}'

# Test LLM digest
curl -X POST http://localhost:8000/digest \
  -H "Content-Type: application/json" \
  -d '{"text":"I need to finish the project by Friday. The team is waiting for my code review."}'
```

## Troubleshooting

### Port Conflicts

If ports 3000, 8000, or 11434 are in use:

```bash
# Find what's using a port
lsof -i :8000

# Stop conflicting services or modify ports in docker-compose.yml
```

### Git Permission Issues

If you see git errors when saving artifacts:

```bash
# Add the knowledge directory to git safe directories
docker exec personal-ai-box-backend git config --global --add safe.directory /knowledge
docker exec personal-ai-box-backend git config --global user.email "box@local"
docker exec personal-ai-box-backend git config --global user.name "Personal AI Box"
```

This is automatically configured in the Dockerfile, but may be needed if using an older image.

### Ollama Connection Issues

**If using native Ollama:**
```bash
# Check if Ollama is running
systemctl status ollama
# or
curl http://localhost:11434/api/version

# Start Ollama if needed
sudo systemctl start ollama
```

**If using Docker Ollama:**
```bash
# Check container logs
docker-compose logs ollama

# Restart the service
docker-compose restart ollama
```

### Out of Memory

If the LLM runs out of memory:

```bash
# Run setup script again to get a lighter model recommendation
./setup.sh

# Or manually switch to a smaller model in docker-compose.yml
# Edit OLLAMA_MODEL to: tinyllama:latest (smallest)
```

## Re-running Setup

You can run `./setup.sh` anytime to reconfigure:
- After installing/removing native Ollama
- After upgrading your GPU
- To switch to a different model size
- To reset to optimal configuration

The script backs up your existing `docker-compose.yml` to `docker-compose.yml.backup`.

## Next Steps

Once everything is running:

1. **Access Open WebUI** at http://localhost:3000
   - Create an account
   - Start chatting with your local LLM

2. **Use the API endpoints:**
   - `/artifact/save` - Save structured documents
   - `/ingest` - Import and chunk text
   - `/search?q=query` - Search your knowledge base
   - `/digest` - Get LLM analysis (summary + signals + actions)

3. **Browse your knowledge:**
   - All data is stored in `./knowledge/` directory
   - Each file is markdown with YAML frontmatter
   - Everything is git-tracked automatically

4. **Read the full documentation:**
   - `README.md` - Complete API reference
   - `CLAUDE.md` - Developer guide
   - `docs/verification-plan.md` - Testing procedures
