# Agente de Trading Inteligente - LangGraph

Sistema multi-agente conversacional con reglas de negocio automatizadas para operaciones de trading.

## 🚀 Características Principales

### 🤖 Agente Conversacional Inteligente
- **Inteligencia Contextual**: Mantiene el contexto de toda la conversación
- **Proactivo**: Sugiere y ejecuta acciones basándose en alertas y recomendaciones
- **Transaccional**: Ejecuta operaciones reales de compra/venta
- **Validación Automática**: Todas las operaciones se validan contra reglas de negocio

### 📊 Capacidades del Sistema

1. **Análisis de Acciones**
   - Análisis técnico con 10 reglas de negocio
   - Recomendaciones automáticas (COMPRAR/VENDER/MANTENER)
   - Validación contra perfil de riesgo

2. **Gestión de Cartera**
   - Consulta de posiciones en tiempo real
   - Cálculo de P&L por posición
   - Alertas de cumplimiento de reglas
   - Recomendaciones automáticas

3. **Ejecución de Operaciones**
   - Compra de acciones con validación de fondos
   - Venta de acciones con cálculo de ganancias
   - Generación de IDs de orden
   - Registro en historial

4. **Historial de Transacciones**
   - Registro completo de operaciones
   - Estadísticas de compras/ventas
   - Consulta por fecha

5. **Motor de Reglas de Negocio**
   - 10 reglas automatizadas priorizadas
   - Protección de capital (Stop Loss, límites)
   - Toma de ganancias (Take Profit)
   - Señales técnicas (soportes, resistencias)

## 🛠️ Herramientas Disponibles

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `analizar_accion_con_reglas` | Analiza una acción con reglas de negocio | `simbolo`, `perfil_riesgo` |
| `consultar_cartera` | Muestra cartera completa con alertas | - |
| `ejecutar_compra` | Compra acciones validando fondos | `simbolo`, `cantidad` |
| `ejecutar_venta` | Vende acciones calculando P&L | `simbolo`, `cantidad` |
| `consultar_historial_transacciones` | Muestra historial de operaciones | `limite` |
| `consultar_reglas_negocio` | Explica las reglas activas | - |

## 📦 Archivos del Proyecto

```
langgraph_agent/
├── agent.py                    # Agente principal con LLM
├── reglas_negocio.py          # Motor de 10 reglas automatizadas
├── cartera_default.json       # Datos de cartera por defecto
├── agent.yaml                 # Configuración para watsonx.orchestrate
├── requirements.txt           # Dependencias Python
├── .env                       # Variables de entorno
└── README.md                  # Este archivo
```

## 🎯 Ejemplos de Uso

### Conversación Contextual

```
Usuario: "Muestra mi cartera"
Agente: [Consulta cartera]
        📊 Tu cartera tiene 5 posiciones...
        ⚠️ MSFT excede el límite de concentración del 20%

Usuario: "Quiero reducir entonces MSFT"
Agente: [Analiza contexto, calcula cantidad, ejecuta venta]
        ✅ Vendiendo 5 acciones de MSFT para reducir concentración...
        Orden ID: ORD-20260517-001

Usuario: "Perfecto, ahora analiza AAPL"
Agente: [Analiza AAPL con reglas]
        📊 AAPL está en $150.50, tendencia alcista
        🎯 Recomendación: COMPRAR

Usuario: "Cómprala"
Agente: [Recuerda que hablamos de AAPL, ejecuta compra]
        ✅ Comprando 10 acciones de AAPL a $150.50...
```

### Consultas Simples

- "¿Cuáles son mis posiciones?"
- "Analiza GOOGL"
- "Compra 15 acciones de MSFT"
- "Vende 5 acciones de JPM"
- "Muestra mis transacciones"
- "¿Qué reglas usas?"

## 🔧 Deployment a watsonx.orchestrate

### Paso 1: Crear ZIP

```bash
zip -r trading_agent.zip langgraph_agent/ -x "*.pyc" -x "__pycache__/*"
```

### Paso 2: Subir a watsonx.orchestrate

1. Accede a tu instancia de watsonx.orchestrate
2. Ve a la sección de agentes
3. Sube el archivo ZIP
4. El sistema detectará automáticamente `agent.yaml`
5. Sigue el wizard de deployment

### Paso 3: Configurar

El agente usa las credenciales configuradas en `.env`:
- `WATSONX_PROJECT_ID`: ID del proyecto de watsonx.ai
- `WATSONX_DEPLOYMENT_ID`: ID del deployment del modelo
- `WATSONX_URL`: URL base de watsonx.ai

## 🧠 Arquitectura del Agente

### LLM + Herramientas
```
Usuario → LLM → Decide herramienta → Ejecuta → Formatea respuesta
          ↑                            ↓
          └──── Mantiene contexto ─────┘
```

### Motor de Reglas (10 Reglas Priorizadas)

**Prioridad 1 - Protección de Capital:**
1. Stop Loss automático al 5%
2. Límite de pérdida diaria del 3%
3. Concentración máxima del 20% por acción

**Prioridad 2 - Toma de Ganancias:**
4. Take Profit según perfil de riesgo
5. Trailing Stop para proteger ganancias

**Prioridad 3-4 - Señales Técnicas:**
6. Compra en soportes fuertes
7. Venta en resistencias
8. Seguimiento de tendencias
9. Análisis de volumen
10. Cruces de medias móviles

## 🔐 Seguridad

- Validación de fondos antes de compras
- Verificación de posiciones antes de ventas
- Límites de concentración por acción
- Stop Loss automático
- Límite de pérdida diaria

## 📝 Notas Importantes

1. **Datos de Demo**: La cartera usa datos simulados en `cartera_default.json`
2. **Precios Simulados**: Los precios son ejemplos, no datos reales de mercado
3. **Producción**: Para producción, integrar con APIs reales de mercado
4. **Contexto**: El agente mantiene el contexto completo de la conversación
5. **LLM**: El agente usa el modelo configurado en watsonx.ai

## 🆘 Troubleshooting

**Error: "No se puede resolver la importación"**
- Normal en desarrollo local sin las librerías instaladas
- Funcionará correctamente en watsonx.orchestrate

**El agente no mantiene contexto**
- Verifica que el LLM esté correctamente configurado
- Revisa que `WATSONX_PROJECT_ID` esté configurado

**Operaciones no se ejecutan**
- Verifica los fondos disponibles en `cartera_default.json`
- Revisa que las posiciones existan para ventas

## 📚 Recursos

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [IBM watsonx.orchestrate](https://www.ibm.com/products/watsonx-orchestrate)
- [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai)

---

**Versión**: 2.0 - Agente Conversacional con LLM
**Última actualización**: Mayo 2026