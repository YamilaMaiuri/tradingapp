#!/bin/bash

# Script para desplegar Trading Agent API en IBM Code Engine
# Solo CREA una nueva aplicación, no modifica nada existente

echo "🚀 Desplegando Trading Agent API en IBM Code Engine..."

# Variables
APP_NAME="trading-agent-api"
PROJECT_NAME="wx-orchestrate-tools"
REGION="us-east"

# 1. Seleccionar el proyecto existente
echo "📦 Seleccionando proyecto: $PROJECT_NAME"
ibmcloud target -r $REGION
ibmcloud ce project select --name $PROJECT_NAME

# 2. Crear NUEVA aplicación (no toca nada existente)
echo "🔨 Creando NUEVA aplicación: $APP_NAME"
ibmcloud ce application create \
  --name $APP_NAME \
  --build-source . \
  --strategy dockerfile \
  --port 8080 \
  --min-scale 1 \
  --max-scale 3 \
  --cpu 0.25 \
  --memory 0.5G \
  --wait

# 3. Obtener URL de la aplicación
echo "✅ Obteniendo URL de la aplicación..."
APP_URL=$(ibmcloud ce application get --name $APP_NAME --output json | grep -o '"url":"[^"]*' | cut -d'"' -f4)

echo ""
echo "✅ ¡Deployment completado!"
echo "📡 URL de tu API: $APP_URL"
echo ""
echo "🧪 Prueba tu API:"
echo "curl $APP_URL/health"
echo ""
echo "📝 Actualiza openapi.yaml línea 11 con:"
echo "  - url: $APP_URL"
echo ""

# Made with Bob
