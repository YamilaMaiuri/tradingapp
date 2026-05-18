# Deploy Trading Agent API en IBM Code Engine

> Guía paso a paso para desplegar la API de trading en Code Engine
> Basada en el tutorial de AGIP - Adaptada para Trading Agent

---

## 📋 Prerequisitos

- Docker Desktop instalado y corriendo
- Cuenta activa en IBM Cloud
- `jq` instalado: `brew install jq`
- Repositorio: https://github.com/YamilaMaiuri/tradingapp

---

## Paso 1 — Instalar IBM Cloud CLI y plugins

```bash
# Instalar IBM Cloud CLI
brew install ibm-cloud-cli

# Instalar plugins necesarios
ibmcloud plugin install code-engine
ibmcloud plugin install container-registry
```

Verificar instalación:
```bash
ibmcloud version
ibmcloud ce version
```

---

## Paso 2 — Login a IBM Cloud

```bash
ibmcloud login --sso
```

- Se abre el browser
- Copiás el one-time passcode
- Lo pegás en la terminal
- Seleccionás la **cuenta** y la **región** (us-south recomendado)

---

## Paso 3 — Apuntar al Resource Group

```bash
# Ver los resource groups disponibles
ibmcloud resource groups

# Apuntar al grupo correcto (ajustar según tu cuenta)
ibmcloud target -g Default
```

> **Importante:** Sin este paso, los comandos de `ibmcloud cr` fallan.

---

## Paso 4 — Login al Container Registry

```bash
ibmcloud cr login
```

Esto hace el `docker login` automáticamente a `us.icr.io`.

---

## Paso 5 — Crear un namespace en el Container Registry

```bash
ibmcloud cr namespace-add trading-agent
```

El namespace es el "folder" donde van a vivir tus imágenes Docker.
La imagen quedará en: `us.icr.io/trading-agent/api:latest`

---

## Paso 6 — Clonar el repositorio (si no lo tienes)

```bash
cd ~/Desktop
git clone https://github.com/YamilaMaiuri/tradingapp.git
cd tradingapp
```

---

## Paso 7 — Verificar el Dockerfile

El Dockerfile ya está configurado correctamente con:
- ✅ `--platform=linux/amd64` (crítico para Code Engine)
- ✅ Copia `api_server.py` y `requirements_api.txt`
- ✅ Puerto 8080
- ✅ Gunicorn con 2 workers

```dockerfile
FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

COPY api_server.py .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "api_server:app"]
```

---

## Paso 8 — Build de la imagen Docker

```bash
docker build --platform linux/amd64 \
  -t us.icr.io/trading-agent/api:latest .
```

> **Crítico:** Siempre usar `--platform linux/amd64` si buildeas desde Mac con
> Apple Silicon (M1/M2/M3). Sin esto, el contenedor no arranca en Code Engine.

Verificar que la imagen se creó:
```bash
docker images | grep trading-agent
```

---

## Paso 9 — Push de la imagen al registry

```bash
docker push us.icr.io/trading-agent/api:latest
```

Si da error de autorización, corré `ibmcloud cr login` (Paso 4) y reintentá.

Verificar que la imagen está en el registry:
```bash
ibmcloud cr images | grep trading-agent
```

---

## Paso 10 — Crear el proyecto en Code Engine

```bash
ibmcloud ce project create --name trading-agent-project
```

Tarda ~30 segundos en activarse. Luego:

```bash
ibmcloud ce project select --name trading-agent-project
```

> Un proyecto es el contenedor lógico de todas tus apps en Code Engine.

---

## Paso 11 — Crear el registry secret

Code Engine necesita credenciales para pullear la imagen desde el ICR:

```bash
ibmcloud ce registry create \
  --name icr-secret \
  --server us.icr.io \
  --username iamapikey \
  --password $(ibmcloud iam api-key-create trading-ce-key --output json | jq -r .apikey)
```

Esto crea una API key de IBM Cloud y la guarda como secret dentro del proyecto.

---

## Paso 12 — Deploy de la aplicación

```bash
ibmcloud ce application create \
  --name trading-agent-api \
  --image us.icr.io/trading-agent/api:latest \
  --registry-secret icr-secret \
  --port 8080 \
  --min-scale 1 \
  --max-scale 3 \
  --cpu 0.25 \
  --memory 0.5G
```

| Flag | Qué hace |
|---|---|
| `--name` | Nombre de la app: `trading-agent-api` |
| `--image` | Imagen Docker a usar |
| `--registry-secret` | Secret con credenciales del ICR |
| `--port` | Puerto 8080 (el que expone la app) |
| `--min-scale 1` | Siempre 1 instancia corriendo |
| `--max-scale 3` | Máximo 3 instancias en paralelo |
| `--cpu 0.25` | 0.25 vCPU por instancia |
| `--memory 0.5G` | 512 MB de RAM por instancia |

---

## Paso 13 — Verificar el deploy

```bash
ibmcloud ce application get -n trading-agent-api
```

Buscás estas líneas:

```
Status Summary:  Application deployed successfully
URL:             https://trading-agent-api.xxxxxx.us-south.codeengine.appdomain.cloud
```

**¡Guarda esa URL!** La necesitarás para actualizar `openapi.yaml`.

Si dice `Application failed to deploy`, revisá los logs:

```bash
ibmcloud ce application logs -f -n trading-agent-api
```

---

## Paso 14 — Probar la API

```bash
# Reemplaza con tu URL real
export API_URL="https://trading-agent-api.xxxxxx.us-south.codeengine.appdomain.cloud"

# Health check
curl $API_URL/health

# Portfolio state
curl $API_URL/api/get_portfolio_state

# Market prices
curl -X POST $API_URL/api/get_market_prices \
  -H "Content-Type: application/json" \
  -d '{"activos": ["YPF", "AL30"]}'
```

---

## Paso 15 — Actualizar openapi.yaml

Editá el archivo `openapi.yaml` línea 11 con la URL de Code Engine:

```yaml
servers:
  - url: https://trading-agent-api.xxxxxx.us-south.codeengine.appdomain.cloud
    description: IBM Code Engine deployment
```

Luego subí el cambio a GitHub:

```bash
git add openapi.yaml
git commit -m "Update API URL for Code Engine"
git push
```

---

## Actualizar la app (re-deploy)

Cada vez que cambiás el código:

```bash
# 1. Rebuild con plataforma correcta
docker build --platform linux/amd64 -t us.icr.io/trading-agent/api:latest .

# 2. Push
docker push us.icr.io/trading-agent/api:latest

# 3. Update (Code Engine pullea la nueva imagen)
ibmcloud ce application update \
  --name trading-agent-api \
  --image us.icr.io/trading-agent/api:latest
```

---

## Comandos útiles de operación

```bash
# Ver estado de la app
ibmcloud ce application get -n trading-agent-api

# Ver logs en tiempo real
ibmcloud ce application logs -f -n trading-agent-api

# Ver eventos del sistema
ibmcloud ce application events -n trading-agent-api

# Listar todas las apps del proyecto
ibmcloud ce application list

# Listar proyectos
ibmcloud ce project list

# Eliminar la app
ibmcloud ce application delete --name trading-agent-api

# Eliminar el proyecto completo
ibmcloud ce project delete --name trading-agent-project
```

---

## Errores comunes y soluciones

| Error | Causa | Solución |
|---|---|---|
| `Authorization required` al hacer push | `ibmcloud cr login` no se hizo | Correr `ibmcloud cr login` y volver a pushear |
| `no resource group is targeted` | Falta apuntar al resource group | `ibmcloud target -g Default` |
| `Initial scale was never achieved` | Imagen buildeada para ARM | Rebuild con `--platform linux/amd64` |
| `Failed to pull image` | Registry secret incorrecto | Recrear el secret (Paso 11) |
| `Application is not ready` | App tarda en iniciar | Esperar 2-3 minutos, ver logs |

---

## Próximos pasos

1. ✅ API desplegada en Code Engine
2. ✅ URL pública obtenida
3. ⏳ Actualizar `openapi.yaml` con la URL
4. ⏳ Importar en watsonx.orchestrate:
   - Skills → Add skills → Custom API
   - Subir `openapi.yaml`
5. ⏳ Probar las 4 tools desde watsonx.orchestrate

---

## URLs de referencia

- **IBM Cloud Console:** https://cloud.ibm.com/codeengine/projects
- **Container Registry:** https://cloud.ibm.com/registry/images
- **Repositorio GitHub:** https://github.com/YamilaMaiuri/tradingapp

---

## Resumen de recursos creados

```
Namespace ICR:     us.icr.io/trading-agent
Imagen Docker:     us.icr.io/trading-agent/api:latest
Proyecto CE:       trading-agent-project
Aplicación CE:     trading-agent-api
Registry Secret:   icr-secret
API Key:           trading-ce-key
```

---

**¡Listo para conectar con watsonx.orchestrate!** 🚀