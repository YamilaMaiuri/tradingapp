# Deployment Manual en IBM Code Engine

Como no tienes el CLI instalado, sigue estos pasos desde la consola web:

## 📋 Paso 1: Preparar el Código

Ya tienes todos los archivos listos en `/Users/yamilamaiuri/Desktop/trading-demo/`

## 🌐 Paso 2: Desplegar desde la Consola Web

### Opción A: Desde la UI de Code Engine

1. Ve a https://cloud.ibm.com/codeengine/projects
2. Click en tu proyecto **"wx-orchestrate-tools"**
3. Click en **"Applications"** en el menú izquierdo
4. Click en **"Create"**
5. Configura:
   - **Name:** `trading-agent-api`
   - **Code:** Selecciona "Source code"
   - **Code repo URL:** (necesitas subir a GitHub primero - ver abajo)
   - **Branch:** main
   - **Dockerfile:** Dockerfile
   - **Listening port:** 8080
   - **Resources:**
     - CPU: 0.25
     - Memory: 0.5 GB
   - **Scaling:**
     - Min instances: 1
     - Max instances: 3

6. Click **"Create"**

### Opción B: Subir a GitHub y Conectar

#### 1. Crear repo en GitHub

```bash
cd /Users/yamilamaiuri/Desktop/trading-demo

# Inicializar git
git init

# Agregar archivos
git add Dockerfile api_server.py requirements_api.txt openapi.yaml

# Commit
git commit -m "Trading Agent API"

# Crear repo en GitHub y conectar
# Ve a github.com y crea un nuevo repositorio
# Luego ejecuta:
git remote add origin https://github.com/TU_USUARIO/trading-agent-api.git
git branch -M main
git push -u origin main
```

#### 2. Conectar desde Code Engine

1. Ve a https://cloud.ibm.com/codeengine/projects
2. Selecciona **"wx-orchestrate-tools"**
3. Click en **"Applications"** → **"Create"**
4. En "Code":
   - Selecciona "Source code"
   - Pega la URL de tu repo de GitHub
   - Branch: main
   - Dockerfile path: Dockerfile
5. Port: 8080
6. Click **"Create"**

## 🎯 Paso 3: Obtener la URL

Una vez desplegado:

1. Ve a tu aplicación en Code Engine
2. Copia la URL (será algo como: `https://trading-agent-api.xxxxx.us-east.codeengine.appdomain.cloud`)
3. Prueba: `curl TU_URL/health`

## 📝 Paso 4: Actualizar openapi.yaml

1. Abre `openapi.yaml`
2. Línea 11, reemplaza con tu URL:
```yaml
servers:
  - url: https://trading-agent-api.xxxxx.us-east.codeengine.appdomain.cloud
```

## 🔗 Paso 5: Conectar con watsonx.orchestrate

1. Ve a watsonx.orchestrate
2. **Skills** → **Import API**
3. Sube `openapi.yaml`
4. Las 4 herramientas se importarán automáticamente

## ✅ Listo!

Prueba en watsonx.orchestrate:
- "Muéstrame el estado de mi portfolio"
- "Cuáles son las reglas de negocio"
- "Dame los precios de YPF y AL30"