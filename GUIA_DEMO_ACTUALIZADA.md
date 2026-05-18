# 🎯 Guía de Demo - Agente de Trading con Reglas de Negocio ICBC

## 📋 Resumen Ejecutivo

**Agente:** Sistema de Trading Inteligente con Reglas de Negocio Automatizadas
**Propósito:** Demostrar operaciones automáticas basadas en reglas predefinidas del ICBC
**Tecnología:** IBM watsonx.orchestrate + LangGraph + Motor de Reglas
**Idioma:** 100% Español

---

## 🤖 ¿Qué es este Sistema?

Un **sistema multi-agente de trading** que:
- ✅ **Opera automáticamente** según reglas de negocio predefinidas
- ✅ **Responde en español** de forma natural
- ✅ **Valida todas las operaciones** contra políticas del banco
- ✅ **Protege el capital** con stop loss y límites automáticos
- ✅ **Toma decisiones** sin intervención humana cuando se cumplen las condiciones

---

## 🛠️ Reglas de Negocio Implementadas

### 🛡️ Protección de Capital (Prioridad 1)

1. **Stop Loss Automático**
   - Venta automática si pérdida > 5%
   - Aplica a perfiles Conservador y Moderado

2. **Límite de Pérdida Diaria**
   - Detiene operaciones si pérdida diaria > 3%
   - Protección del capital total

3. **Límite de Concentración**
   - Máximo 20% del portfolio en una acción
   - Previene riesgo de concentración

4. **Horario de Operación**
   - Solo opera en horario de mercado
   - 9:30 AM - 4:00 PM EST

### 📈 Toma de Ganancias (Prioridad 2)

5. **Take Profit Conservador**
   - Venta automática con ganancia del 8%
   - Para clientes conservadores

6. **Take Profit Moderado**
   - Venta automática con ganancia del 15%
   - Para clientes moderados

### 🎯 Señales Técnicas (Prioridad 3-4)

7. **Compra en Soporte Fuerte**
   - Precio cerca del soporte
   - Volumen > 150% del promedio
   - RSI < 35 (sobreventa)
   - Tendencia alcista

8. **Venta en Resistencia**
   - Precio cerca de resistencia
   - RSI > 70 (sobrecompra)
   - Volumen alto

9. **Compra en Tendencia Alcista**
   - Cruce alcista de media móvil 50
   - Precio sobre media móvil 200
   - MACD positivo
   - Volumen confirmatorio

10. **Venta por Cambio de Tendencia**
    - Cruce bajista de media móvil 50
    - RSI < 50
    - Volumen confirmatorio

---

## 💬 Consultas para la Demo

### 1. Presentación del Sistema

**Consulta:** "Hola, ¿qué puedes hacer?"

**Respuesta Esperada:**
- Presentación en español
- Lista de 10 reglas de negocio
- Explicación de protección de capital
- Menú de opciones disponibles

**Explicar:**
> "El sistema opera con 10 reglas de negocio automatizadas que protegen el capital, toman ganancias automáticamente y ejecutan operaciones basadas en señales técnicas. Todo en español y sin intervención manual."

---

### 2. Análisis con Reglas de Negocio

**Consulta:** "Analiza AAPL"

**Respuesta Esperada:**
```
✅ Operación Recomendada: COMPRA
📋 Regla Aplicada: COMPRA_TENDENCIA_ALCISTA
💡 Justificación: Compra cuando hay confirmación de tendencia alcista
🎯 Confianza: 85%

📊 Detalles de la Operación:
• Acciones a comprar: 66
• Monto: $9,933.00
• Stop Loss: $145.00
• Take Profit: $155.00

✅ Operación APROBADA
⚠️ Alertas: Ninguna
🚫 Restricciones: Ninguna

📈 Indicadores Técnicos:
• RSI: 45
• MACD: POSITIVO
• Volumen: 125% del promedio
• Tendencia: ALCISTA

🔍 Reglas Evaluadas: 10
✅ Reglas Aplicables: 3
```

**Explicar:**
> "El sistema evaluó las 10 reglas de negocio automáticamente. Identificó que se cumplen las condiciones para COMPRA según la regla de tendencia alcista. Calculó el tamaño de posición (10% del capital para perfil moderado), validó que no excede límites de concentración, y determinó los niveles de stop loss y take profit automáticos."

---

### 3. Consultar Reglas del Sistema

**Consulta:** "Muéstrame las reglas de negocio"

**Respuesta Esperada:**
```
📋 Total de Reglas Activas: 10

🛡️ Protección de Capital:
• STOP_LOSS_AUTOMATICO
• LIMITE_PERDIDA_DIARIA
• LIMITE_CONCENTRACION

📈 Toma de Ganancias:
• TAKE_PROFIT_CONSERVADOR
• TAKE_PROFIT_MODERADO

🎯 Señales Técnicas:
• COMPRA_SOPORTE_FUERTE
• VENTA_RESISTENCIA
• COMPRA_TENDENCIA_ALCISTA
• VENTA_CAMBIO_TENDENCIA

⚙️ Operativas:
• HORARIO_OPERACION
```

**Explicar:**
> "Estas son las reglas que el sistema evalúa en cada operación. Están priorizadas: primero protección de capital (prioridad 1), luego toma de ganancias (prioridad 2), y finalmente señales técnicas (prioridad 3-4). Si múltiples reglas aplican, se ejecuta la de mayor prioridad."

---

### 4. Análisis de Portfolio

**Consulta:** "Analiza mi portfolio"

**Respuesta Esperada:**
```
📊 Resumen del Portfolio:
• Capital Total: $50,000.00
• Valor Posiciones: $21,927.00
• Efectivo Disponible: $28,073.00
• Número de Posiciones: 3
• Exposición: 43.9%

📈 Posiciones Actuales:
• AAPL: 15.1% | Ganancia: +3.79%
• GOOGL: 5.7% | Ganancia: +1.64%
• MSFT: 23.1% | Ganancia: +1.37%

⚠️ Alertas:
• MSFT: Concentración del 23.1% excede el límite del 20%

💡 Recomendaciones:
• Reducir posición en MSFT vendiendo 5 acciones

✅ Cumplimiento de Reglas:
• Diversificación: ALERTA
• Exposición Total: OK
• Liquidez: OK
```

**Explicar:**
> "El sistema analiza el portfolio completo y valida el cumplimiento de todas las reglas. Detectó que MSFT excede el límite de concentración del 20% y recomienda automáticamente reducir la posición. También verifica que haya suficiente liquidez (mínimo 10%) y que la exposición total no exceda el 90%."

---

### 5. Ejecución Automática

**Consulta:** "Ejecuta la compra de 10 acciones de AAPL"

**Respuesta Esperada:**
```
✅ OPERACIÓN EJECUTADA

📋 Detalles:
• Orden ID: ORD-20260517183045
• Símbolo: AAPL
• Tipo: COMPRA
• Cantidad: 10 acciones
• Precio: $150.50
• Monto Total: $1,506.51
• Comisión: $1.51
• Timestamp: 2026-05-17 18:30:45

✅ Operación COMPRA ejecutada exitosamente
```

**Explicar:**
> "El sistema ejecutó la operación automáticamente después de validarla contra todas las reglas de negocio. Generó un ID de orden único, calculó comisiones, y registró la transacción con timestamp. En producción, esto se conectaría directamente al broker para ejecución real."

---

## 🎬 Script de Demostración (7 minutos)

### Introducción (1 minuto)
> "Les presento nuestro Sistema de Trading Inteligente con Reglas de Negocio Automatizadas. A diferencia de un simple asistente que da recomendaciones, este sistema **opera automáticamente** cuando se cumplen condiciones predefinidas, siempre protegiendo el capital del cliente."

### Demo 1: Presentación (1 minuto)
**Escribir:** "Hola, ¿qué puedes hacer?"

**Destacar:**
- Responde en español
- 10 reglas de negocio activas
- 3 categorías: Protección, Ganancias, Señales
- Operación automática

### Demo 2: Análisis con Reglas (2 minutos)
**Escribir:** "Analiza AAPL"

**Destacar:**
- Evaluó 10 reglas automáticamente
- Identificó 3 reglas aplicables
- Seleccionó la de mayor prioridad
- Calculó tamaño de posición según perfil
- Validó contra límites de concentración
- Determinó stop loss y take profit automáticos
- Operación aprobada sin intervención humana

### Demo 3: Reglas del Sistema (1 minuto)
**Escribir:** "Muéstrame las reglas"

**Destacar:**
- 10 reglas organizadas por categoría
- Priorización automática
- Protección de capital es prioridad #1
- Reglas configurables según política del banco

### Demo 4: Portfolio Compliance (1 minuto)
**Escribir:** "Analiza mi portfolio"

**Destacar:**
- Validación automática de cumplimiento
- Detectó violación de concentración
- Recomendación específica de rebalanceo
- Monitoreo continuo de límites

### Demo 5: Ejecución Automática (1 minuto)
**Escribir:** "Ejecuta la compra de 10 acciones de AAPL"

**Destacar:**
- Ejecución inmediata
- Validación previa contra reglas
- Generación de orden con ID único
- Cálculo automático de comisiones
- Registro completo de la transacción

---

## 🎯 Puntos Clave para Destacar

### Diferenciadores Técnicos:
✅ **Motor de Reglas de Negocio** - No solo recomendaciones, sino decisiones automáticas
✅ **Priorización Inteligente** - Protección de capital siempre primero
✅ **Validación Automática** - Todas las operaciones se validan contra políticas
✅ **100% Español** - Interfaz y respuestas en español
✅ **Trazabilidad Completa** - Cada decisión documenta qué regla la generó

### Ventajas de Negocio:
💰 **Reduce riesgo operacional** - Reglas consistentes, sin error humano
📊 **Cumplimiento automático** - Garantiza adherencia a políticas del banco
🔄 **Operación 24/7** - Monitoreo y ejecución continua
📈 **Escalabilidad** - Mismo sistema para miles de clientes
🎯 **Personalización** - Reglas adaptadas al perfil de cada cliente

---

## 🚀 Arquitectura del Sistema

```
┌─────────────────────────────────────────┐
│   Usuario (Analista/Cliente)           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Agente Conversacional (Español)      │
│   • Interpreta consultas               │
│   • Genera respuestas naturales        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Motor de Reglas de Negocio           │
│   • 10 reglas predefinidas             │
│   • Priorización automática            │
│   • Validación de operaciones          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Herramientas de Trading               │
│   • Análisis de acciones               │
│   • Ejecución de operaciones           │
│   • Análisis de portfolio              │
│   • Consulta de reglas                 │
└─────────────────────────────────────────┘
```

---

## 📊 Casos de Uso Reales

### Caso 1: Protección Automática
**Escenario:** Cliente tiene AAPL con pérdida del 6%
**Acción Automática:** Sistema ejecuta STOP_LOSS automáticamente
**Resultado:** Capital protegido, pérdida limitada al 5%

### Caso 2: Toma de Ganancias
**Escenario:** Cliente conservador con ganancia del 9% en GOOGL
**Acción Automática:** Sistema ejecuta TAKE_PROFIT
**Resultado:** Ganancias aseguradas según perfil

### Caso 3: Rebalanceo de Portfolio
**Escenario:** Concentración en MSFT supera 20%
**Acción Automática:** Sistema alerta y recomienda venta parcial
**Resultado:** Portfolio balanceado, riesgo controlado

---

## 📝 Preguntas Frecuentes

**P: ¿El sistema opera sin supervisión humana?**
R: El sistema puede operar automáticamente cuando se cumplen las reglas, pero siempre con límites predefinidos y posibilidad de supervisión.

**P: ¿Qué pasa si dos reglas entran en conflicto?**
R: El sistema usa priorización. Protección de capital siempre tiene prioridad 1 y prevalece sobre otras reglas.

**P: ¿Se pueden modificar las reglas?**
R: Sí, las reglas son configurables y se pueden ajustar según las políticas del banco y perfil del cliente.

**P: ¿Cómo se garantiza el cumplimiento regulatorio?**
R: Todas las operaciones se validan contra las reglas antes de ejecutarse. Hay trazabilidad completa de qué regla generó cada decisión.

**P: ¿Funciona con datos reales?**
R: Esta demo usa datos simulados. En producción se conecta a APIs de mercado en tiempo real y brokers para ejecución.

---

## 🎯 Próximos Pasos

### Fase Actual - MVP:
✅ 10 reglas de negocio implementadas
✅ Motor de priorización
✅ Validación automática
✅ Interfaz en español
✅ 4 herramientas operativas

### Fase 2 - Integración (2-4 semanas):
🔄 Conexión con APIs de mercado real
🔄 Integración con broker del banco
🔄 Base de datos de operaciones
🔄 Dashboard de monitoreo

### Fase 3 - Avanzado (1-2 meses):
📋 Machine Learning para optimizar reglas
📋 Backtesting automático
📋 Alertas proactivas
📋 Reportes regulatorios automáticos

---

**¡Éxito en la demo!** 🎉

El sistema está listo para demostrar operaciones automáticas basadas en reglas de negocio del ICBC.