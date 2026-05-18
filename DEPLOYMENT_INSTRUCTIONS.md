# 📦 Instrucciones de Despliegue - Trading Agent

## ✅ Archivo Listo para Desplegar

**Archivo:** `trading_agent_langgraph.zip`
**Ubicación:** `/Users/yamilamaiuri/Desktop/trading-demo/trading_agent_langgraph.zip`

## 🚀 Pasos para Desplegar en watsonx.orchestrate

### 1. Accede a tu Instancia de watsonx.orchestrate

Abre tu navegador y ve a:
```
https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/b897ec27-a5e0-4c43-8af7-f54b8112411a
```

### 2. Navega a la Sección de Agentes

- Busca la opción de **"Agents"** o **"Custom Agents"** en el menú
- Haz clic en **"Create Agent"** o **"Import Agent"**

### 3. Sube el Archivo ZIP

- Selecciona la opción para subir un archivo LangGraph
- Haz clic en **"Upload"** o **"Choose File"**
- Selecciona el archivo: `trading_agent_langgraph.zip`

### 4. Configura el Agente

Durante el proceso de deployment, es posible que te pida:

**Nombre del Agente:**
```
TradingAnalystAgent
```

**Descripción:**
```
AI agent specialized in analyzing market trends and providing trading insights for ICBC demo
```

**Graph Name:** (si te lo pide)
```
trading_agent
```

### 5. Completa el Deployment

- Revisa la configuración
- Haz clic en **"Deploy"** o **"Create"**
- Espera a que el agente se despliegue (puede tomar 1-2 minutos)

### 6. Prueba el Agente

Una vez desplegado, prueba el agente con estas consultas:

1. **"Hello, what can you do?"**
   - Debería presentarse y listar sus capacidades

2. **"Analyze AAPL stock"**
   - Debería analizar Apple y dar recomendaciones

3. **"What's the market sentiment?"**
   - Debería dar el sentimiento general del mercado

4. **"Calculate risk for a $1000 position"**
   - Debería calcular métricas de riesgo

## 📋 Contenido del ZIP

El archivo ZIP contiene:

```
langgraph_agent/
├── agent.py              # Implementación del agente
├── requirements.txt      # Dependencias Python
├── langgraph.json       # Configuración LangGraph
├── .env                 # Variables de entorno
└── README.md            # Documentación
```

## 🛠️ Herramientas del Agente

El agente incluye 3 herramientas:

1. **analyze_market_symbol(symbol)**
   - Analiza un símbolo de stock específico
   - Retorna: recomendación, confianza, razonamiento, nivel de riesgo

2. **get_market_sentiment(sector)**
   - Obtiene el sentimiento del mercado para un sector
   - Retorna: sentimiento general, factores clave, outlook

3. **calculate_risk_metrics(symbol, position_size)**
   - Calcula métricas de riesgo para una posición
   - Retorna: pérdida máxima, ratio riesgo/recompensa, stop loss recomendado

## 🔍 Verificación

Después del deployment, verifica que:

- [ ] El agente aparece en tu lista de agentes
- [ ] El estado es "Active" o "Running"
- [ ] Puedes enviar mensajes al agente
- [ ] El agente responde correctamente

## 📞 Soporte

Si encuentras problemas durante el deployment:

1. Verifica que tu API key tenga permisos para crear agentes
2. Revisa los logs de deployment en la UI
3. Asegúrate de que el archivo ZIP no esté corrupto
4. Contacta al soporte de IBM watsonx.orchestrate si es necesario

## 📚 Documentación de Referencia

- [watsonx.orchestrate CI/CD](https://developer.watson-orchestrate.ibm.com/tutorials/ci_cd/deployment-cicd-approach-1)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

**¡Listo para desplegar!** 🎉

El archivo `trading_agent_langgraph.zip` está en tu Desktop y listo para ser subido a watsonx.orchestrate.