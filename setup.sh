#!/bin/bash
set -e

# Smart Setup Script for personal-llm-box
# Detects native Ollama and system resources, configures accordingly

echo "🔍 Personal AI Box - Smart Setup"
echo "================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if native Ollama is installed
echo -n "Checking for native Ollama installation... "
NATIVE_OLLAMA=false
OLLAMA_RUNNING=false
OLLAMA_VERSION=""

if command -v ollama &> /dev/null; then
    OLLAMA_VERSION=$(ollama --version 2>/dev/null | grep -o '[0-9.]*' | head -1)
    echo -e "${GREEN}✓ Found${NC} (version $OLLAMA_VERSION)"
    NATIVE_OLLAMA=true

    # Check if Ollama service is running
    if systemctl is-active --quiet ollama 2>/dev/null || curl -s http://localhost:11434/api/version &>/dev/null; then
        echo -e "   ${GREEN}✓ Ollama service is running${NC}"
        OLLAMA_RUNNING=true
    else
        echo -e "   ${YELLOW}⚠ Ollama is installed but not running${NC}"
        echo -e "   ${YELLOW}  Start it with: sudo systemctl start ollama${NC}"
    fi
else
    echo -e "${YELLOW}✗ Not found${NC}"
    echo -e "   ${BLUE}ℹ Will use Docker Ollama container${NC}"
fi

echo ""

# Check system resources
echo "Checking system resources..."
echo "----------------------------"

# Check RAM
TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
AVAILABLE_RAM=$(free -g | awk '/^Mem:/{print $7}')
echo -e "RAM: ${GREEN}${TOTAL_RAM}GB${NC} total, ${GREEN}${AVAILABLE_RAM}GB${NC} available"

# Check GPU
GPU_NAME=""
GPU_VRAM=0
if command -v nvidia-smi &> /dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)
    GPU_VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
    GPU_VRAM_GB=$((GPU_VRAM / 1024))
    echo -e "GPU: ${GREEN}${GPU_NAME}${NC} (${GREEN}${GPU_VRAM_GB}GB${NC} VRAM)"
else
    echo -e "GPU: ${YELLOW}No NVIDIA GPU detected${NC} (CPU-only mode)"
fi

echo ""

# Recommend model based on resources
echo "Recommending model..."
echo "---------------------"

RECOMMENDED_MODEL=""
MODEL_SIZE=""

if [ "$GPU_VRAM_GB" -ge 16 ]; then
    RECOMMENDED_MODEL="qwen2.5:14b"
    MODEL_SIZE="~9GB"
elif [ "$GPU_VRAM_GB" -ge 8 ]; then
    RECOMMENDED_MODEL="qwen2.5:7b"
    MODEL_SIZE="~4.7GB"
elif [ "$GPU_VRAM_GB" -ge 4 ]; then
    RECOMMENDED_MODEL="qwen2.5:3b"
    MODEL_SIZE="~2GB"
elif [ "$TOTAL_RAM" -ge 16 ]; then
    RECOMMENDED_MODEL="qwen2.5:3b"
    MODEL_SIZE="~2GB (CPU)"
else
    RECOMMENDED_MODEL="tinyllama:latest"
    MODEL_SIZE="~637MB (CPU)"
fi

echo -e "Recommended model: ${GREEN}${RECOMMENDED_MODEL}${NC} (${MODEL_SIZE})"
echo ""

# Check if recommended model is already available
if [ "$NATIVE_OLLAMA" = true ] && [ "$OLLAMA_RUNNING" = true ]; then
    echo "Checking available models..."
    if ollama list 2>/dev/null | grep -q "$(echo $RECOMMENDED_MODEL | cut -d: -f1)"; then
        echo -e "${GREEN}✓ Recommended model family already available${NC}"
    else
        echo -e "${YELLOW}⚠ Recommended model not found${NC}"
        echo -e "   To install: ${BLUE}ollama pull $RECOMMENDED_MODEL${NC}"
    fi
    echo ""
fi

# Generate docker-compose.yml
echo "Generating docker-compose.yml..."
echo "---------------------------------"

COMPOSE_FILE="docker-compose.yml"
BACKUP_FILE="docker-compose.yml.backup"

# Backup existing file if it exists
if [ -f "$COMPOSE_FILE" ]; then
    cp "$COMPOSE_FILE" "$BACKUP_FILE"
    echo -e "${BLUE}ℹ Backed up existing config to $BACKUP_FILE${NC}"
fi

if [ "$NATIVE_OLLAMA" = true ] && [ "$OLLAMA_RUNNING" = true ]; then
    # Use native Ollama
    echo -e "${GREEN}✓ Configuring for native Ollama${NC}"

    cat > "$COMPOSE_FILE" << 'EOF'
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
    volumes:
      - open_webui_data:/app/backend/data
    ports:
      - "3000:8080"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: unless-stopped

  backend:
    build: .
    container_name: personal-ai-box-backend
    environment:
      - OLLAMA_URL=http://host.docker.internal:11434
      - OLLAMA_MODEL=MODEL_PLACEHOLDER
      - KNOWLEDGE_DIR=/knowledge
    volumes:
      - ./knowledge:/knowledge
    ports:
      - "8000:8000"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: unless-stopped

volumes:
  open_webui_data:
EOF

else
    # Use Docker Ollama
    echo -e "${BLUE}ℹ Configuring for Docker Ollama${NC}"

    cat > "$COMPOSE_FILE" << 'EOF'
services:
  ollama:
    image: ollama/ollama:latest
    container_name: personal-llm-box-ollama
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - open_webui_data:/app/backend/data
    ports:
      - "3000:8080"
    restart: unless-stopped

  backend:
    build: .
    container_name: personal-ai-box-backend
    depends_on:
      - ollama
    environment:
      - OLLAMA_URL=http://ollama:11434
      - OLLAMA_MODEL=MODEL_PLACEHOLDER
      - KNOWLEDGE_DIR=/knowledge
    volumes:
      - ./knowledge:/knowledge
    ports:
      - "8000:8000"
    restart: unless-stopped

volumes:
  ollama_data:
  open_webui_data:
EOF

fi

# Replace model placeholder
sed -i "s/MODEL_PLACEHOLDER/$RECOMMENDED_MODEL/" "$COMPOSE_FILE"

echo -e "${GREEN}✓ Generated $COMPOSE_FILE with model: $RECOMMENDED_MODEL${NC}"
echo ""

# Summary and next steps
echo "Setup complete!"
echo "==============="
echo ""

if [ "$NATIVE_OLLAMA" = false ] || [ "$OLLAMA_RUNNING" = false ]; then
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Start services: docker-compose up -d"
    if [ "$NATIVE_OLLAMA" = false ]; then
        echo "2. Pull the model: docker exec personal-llm-box-ollama ollama pull $RECOMMENDED_MODEL"
    fi
    echo "3. Access Open WebUI: http://localhost:3000"
    echo "4. Access Backend API: http://localhost:8000/health"
else
    echo -e "${YELLOW}Next steps:${NC}"
    if ! ollama list 2>/dev/null | grep -q "$(echo $RECOMMENDED_MODEL | cut -d: -f1)"; then
        echo "1. Pull the model: ollama pull $RECOMMENDED_MODEL"
        echo "2. Start services: docker-compose up -d"
    else
        echo "1. Start services: docker-compose up -d"
    fi
    echo "2. Access Open WebUI: http://localhost:3000"
    echo "3. Access Backend API: http://localhost:8000/health"
fi

echo ""
echo -e "${GREEN}Configuration saved to $COMPOSE_FILE${NC}"
echo -e "${BLUE}Run this script again if your Ollama setup changes${NC}"
