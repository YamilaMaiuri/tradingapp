# 🚀 Guía de Deployment - Trading Agent API

Esta guía te ayudará a desplegar la API REST y conectarla con watsonx.orchestrate.

---

## 📦 Archivos del Proyecto

```
trading-demo/
├── api_server.py              # Servidor Flask con 4 endpoints
├── openapi.yaml               # Especificación OpenAPI para watsonx.orchestrate
├── requirements_api.txt       # Dependencias Python
├── Procfile                   # Configuración para Render
├── runtime.txt                # Versión de Python
└── DEPLOYMENT_GUIDE.md        # Esta guía
```

---

## 🎯 Paso 1: Desplegar la API en Render

### 1.1 Crear Repositorio en GitHub

```bash
cd /Users/yamilamaiuri/Desktop/trading-demo

# Inicializar git (si no lo has hecho)
git init

# Agregar archivos
git add api_server.py requirements_api.txt Procfile runtime.txt openapi.yaml

# Commit
git commit -m "Initial commit - Trading Agent API"

# Crear repo en GitHub y push
git remote add origin https://github.com/TU_USUARIO/trading-agent-api.git
git branch -M main
git push -u origin main
```

### 1.2 Desplegar en Render

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura el servicio:

```
Name: trading-agent-api
Environment: Python 3
Branch: main
Build Command: pip install -r requirements_api.txt
Start Command: gunicorn api_server:app
Instance Type: Free (para pruebas)
```

5. Click en **"Create Web Service"**
6. Espera a que se despliegue (2-3 minutos)

### 1.3 Obtener tu URL

Una vez desplegado, Render te dará una URL como:
```
https://trading-agent-api-XXXXX.onrender.com
```

**¡Guarda esta URL!** La necesitarás para el siguiente paso.

### 1.4 Verificar que funciona

```bash
# Reemplaza con tu URL de Render
curl https://trading-agent-api-XXXXX.onrender.com/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "Trading Agent API - ICBC",
  "version": "1.0.0",
  "timestamp": "2024-05-18T02:00:00"
}
```

---

## 🔗 Paso 2: Actualizar openapi.yaml con tu URL

1. Abre `openapi.yaml`
2. En la línea 11, reemplaza la URL:

```yaml
servers:
  - url: https://trading-agent-api-XXXXX.onrender.com  # ← TU URL AQUÍ
    description: Servidor de producción en Render
```

3. Guarda el archivo

---

## 🎨 Paso 3: Conectar con watsonx.orchestrate

### 3.1 Subir OpenAPI Specification

1. Accede a tu instancia de watsonx.orchestrate
2. Ve a **"Skills"** o **"Tools"** (depende de la versión)
3. Click en **"Add Skill"** o **"Import API"**
4. Selecciona **"OpenAPI Specification"**
5. Sube el archivo `openapi.yaml`
6. Click en **"Import"**

### 3.2 Verificar las Herramientas Importadas

Deberías ver 4 nuevas herramientas:

1. ✅ **Execute Order** - Ejecutar órdenes de compra/venta
2. ✅ **Get Portfolio State** - Consultar estado del portfolio
3. ✅ **Get Business Rules** - Obtener reglas de negocio
4. ✅ **Get Market Prices** - Consultar precios de mercado

### 3.3 Probar las Herramientas

En watsonx.orchestrate, prueba con estos comandos:

```
"Muéstrame el estado de mi portfolio"
→ Debería llamar a get_portfolio_state

"Cuáles son las reglas de negocio activas"
→ Debería llamar a get_business_rules

"Dame los precios de YPF, AL30 y GGAL"
→ Debería llamar a get_market_prices

"Ejecuta una compra de 1000 acciones de YPF en BYMA por la regla R1"
→ Debería llamar a execute_order
```

---

## 📡 Endpoints Disponibles

### 1. Health Check
```bash
GET /health
```

### 2. Ejecutar Orden
```bash
POST /api/execute_order
Content-Type: application/json

{
  "activo": "YPF",
  "tipo": "COMPRA",
  "cantidad": 1000,
  "mercado": "BYMA",
  "regla_origen": "R1"
}
```

### 3. Estado del Portfolio
```bash
GET /api/get_portfolio_state
```

### 4. Reglas de Negocio
```bash
GET /api/get_business_rules
```

### 5. Precios de Mercado
```bash
POST /api/get_market_prices
Content-Type: application/json

{
  "activos": ["YPF", "AL30", "GGAL", "USD"]
}
```

---

## 🧪 Pruebas con cURL

### Probar Health Check
```bash
curl https://TU-URL.onrender.com/health
```

### Probar Portfolio
```bash
curl https://TU-URL.onrender.com/api/get_portfolio_state
```

### Probar Reglas
```bash
curl https://TU-URL.onrender.com/api/get_business_rules
```

### Probar Precios
```bash
curl -X POST https://TU-URL.onrender.com/api/get_market_prices \
  -H "Content-Type: application/json" \
  -d '{"activos":["YPF","AL30","GGAL"]}'
```

### Probar Orden
```bash
curl -X POST https://TU-URL.onrender.com/api/execute_order \
  -H "Content-Type: application/json" \
  -d '{
    "activo": "YPF",
    "tipo": "COMPRA",
    "cantidad": 1000,
    "mercado": "BYMA",
    "regla_origen": "R1"
  }'
```

---

## 🔧 Troubleshooting

### Error: "Application failed to start"
- Verifica que `requirements_api.txt` esté en el repositorio
- Revisa los logs en Render Dashboard
- Asegúrate de que el `Procfile` esté correcto

### Error: "404 Not Found"
- Verifica que la URL sea correcta
- Asegúrate de incluir `/api/` en el path
- Revisa que el servicio esté corriendo en Render

### Error en watsonx.orchestrate: "Failed to connect"
- Verifica que la URL en `openapi.yaml` sea correcta
- Asegúrate de que el servicio esté desplegado y corriendo
- Prueba el endpoint `/health` primero

### Render Free Tier se duerme
- El tier gratuito de Render se duerme después de 15 minutos de inactividad
- La primera llamada después de dormir puede tardar 30-60 segundos
- Para producción, considera el plan pago

---

## 📊 Datos de Ejemplo

### Portfolio de Ejemplo
```json
{
  "posiciones": [
    {"activo": "YPF",  "cantidad": 10000, "valor_actual": 12845000},
    {"activo": "AL30", "cantidad": 50000, "valor_actual": 3107500},
    {"activo": "GGAL", "cantidad": 5000,  "valor_actual": 4675000}
  ],
  "cash_disponible": 5000000,
  "valor_total_portfolio": 25627500
}
```

### Reglas de Ejemplo
```json
{
  "reglas": [
    {
      "id": "R1",
      "condicion": "YPF sube más del 2%",
      "accion": "Evaluar compra de GGAL"
    },
    {
      "id": "R2",
      "condicion": "AL30 baja más del 1%",
      "accion": "Vender 30% de la posición en AL30"
    }
  ]
}
```

---

## 🎯 Próximos Pasos

1. ✅ Desplegar API en Render
2. ✅ Actualizar `openapi.yaml` con tu URL
3. ✅ Subir OpenAPI a watsonx.orchestrate
4. ✅ Probar las 4 herramientas
5. 🔄 Integrar con tu agente LangGraph (opcional)

---

## 📚 Recursos

- [Render Documentation](https://render.com/docs)
- [OpenAPI Specification](https://swagger.io/specification/)
- [watsonx.orchestrate Skills](https://www.ibm.com/docs/en/watsonx/watson-orchestrate)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 💡 Tips

1. **Logs en Render:** Ve a tu servicio → "Logs" para ver errores
2. **Reiniciar servicio:** En Render, click en "Manual Deploy" → "Deploy latest commit"
3. **Variables de entorno:** Si necesitas configurar algo, usa "Environment" en Render
4. **CORS:** Ya está habilitado para watsonx.orchestrate
5. **Timeout:** Render Free tier tiene timeout de 30 segundos

---

**¡Tu API REST está lista para conectar con watsonx.orchestrate!** 🎉

Si tienes problemas, revisa los logs en Render o prueba los endpoints con cURL primero.