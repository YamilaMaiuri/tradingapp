"""
Agente de Trading Inteligente Multi-Agente
Sistema automatizado con reglas de negocio para operaciones de trading
"""
from typing import TypedDict, Annotated, Sequence, Optional, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
import operator
import json
from datetime import datetime
from pathlib import Path
import re

# Importar reglas de negocio
from reglas_negocio import MotorReglasNegocio, NivelRiesgo, TipoOperacion


# Estado del agente con contexto
class AgentState(TypedDict):
    """Estado del agente de trading con contexto"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    context: Dict[str, Any]  # Contexto de la conversación


# Instancia global del motor de reglas
motor_reglas = MotorReglasNegocio()


# Función para cargar la cartera
def cargar_cartera():
    """Carga la cartera desde el archivo JSON"""
    try:
        cartera_path = Path(__file__).parent / "cartera_default.json"
        with open(cartera_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        # Cartera por defecto si no se puede cargar
        return {
            "cliente": {"perfil_riesgo": "MODERADO", "capital_total": 50000.0},
            "posiciones": [],
            "transacciones_historicas": [],
            "configuracion": {"stop_loss_global": 5.0}
        }


# Función para guardar transacción
def guardar_transaccion(transaccion: dict):
    """Guarda una nueva transacción en el historial"""
    try:
        cartera_path = Path(__file__).parent / "cartera_default.json"
        cartera = cargar_cartera()
        cartera["transacciones_historicas"].append(transaccion)
        
        with open(cartera_path, 'w', encoding='utf-8') as f:
            json.dump(cartera, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False


# ==================== HERRAMIENTAS DEL AGENTE ====================

@tool
def analizar_accion_con_reglas(
    simbolo: str,
    perfil_riesgo: str = "MODERADO"
) -> dict:
    """
    Analiza una acción y determina la operación a realizar según las reglas de negocio.
    
    Args:
        simbolo: Símbolo de la acción (ej: AAPL, GOOGL, MSFT)
        perfil_riesgo: Perfil del cliente (CONSERVADOR, MODERADO, AGRESIVO)
    
    Returns:
        Análisis completo con decisión operativa basada en reglas
    """
    
    cartera = cargar_cartera()
    capital_disponible = cartera["cliente"]["capital_total"]
    
    # Simular datos de mercado
    datos_mercado = {
        "simbolo": simbolo.upper(),
        "precio_actual": 150.50,
        "precio_apertura": 148.20,
        "variacion_porcentual": 1.55,
        "volumen": 2500000,
        "volumen_promedio": 2000000,
        "rsi": 45,
        "macd": "POSITIVO",
        "media_movil_50": "CRUCE_ALCISTA",
        "media_movil_200": "PRECIO_SUPERIOR",
        "soporte": 145.00,
        "resistencia": 155.00,
        "tendencia": "ALCISTA"
    }
    
    perfil_cliente = {
        "nivel_riesgo": perfil_riesgo,
        "capital_total": capital_disponible,
        "capital_disponible": capital_disponible * 0.8,
        "posiciones_actuales": len(cartera["posiciones"]),
        "perdida_diaria": 0.5
    }
    
    # Evaluar con motor de reglas
    decision = motor_reglas.evaluar_operacion(datos_mercado, perfil_cliente)
    
    # Calcular tamaño de posición
    if decision["operacion"] == TipoOperacion.COMPRA.value:
        if perfil_riesgo == "CONSERVADOR":
            tamano_posicion = capital_disponible * 0.05
        elif perfil_riesgo == "MODERADO":
            tamano_posicion = capital_disponible * 0.10
        else:
            tamano_posicion = capital_disponible * 0.15
        
        acciones_a_comprar = int(tamano_posicion / datos_mercado["precio_actual"])
        costo_total = acciones_a_comprar * datos_mercado["precio_actual"]
    else:
        acciones_a_comprar = 0
        costo_total = 0
    
    operacion_propuesta = {
        "tipo": decision["operacion"],
        "monto": costo_total,
        "concentracion": (costo_total / capital_disponible) * 100
    }
    
    validacion = motor_reglas.validar_operacion(operacion_propuesta, perfil_cliente)
    
    return {
        "simbolo": simbolo.upper(),
        "precio_actual": f"${datos_mercado['precio_actual']:.2f}",
        "variacion_dia": f"+{datos_mercado['variacion_porcentual']:.2f}%",
        "tendencia": datos_mercado["tendencia"],
        "operacion_recomendada": decision["operacion"],
        "regla_aplicada": decision["regla_aplicada"],
        "justificacion": decision["justificacion"],
        "confianza": f"{decision['confianza']*100:.1f}%",
        "acciones_a_operar": acciones_a_comprar,
        "monto_operacion": f"${costo_total:.2f}",
        "stop_loss": f"${datos_mercado['soporte']:.2f}",
        "take_profit": f"${datos_mercado['resistencia']:.2f}",
        "operacion_aprobada": validacion["aprobada"],
        "alertas": validacion["alertas"],
        "restricciones": validacion["restricciones"],
        "indicadores": {
            "RSI": datos_mercado["rsi"],
            "MACD": datos_mercado["macd"],
            "Volumen": f"{(datos_mercado['volumen']/datos_mercado['volumen_promedio']*100):.0f}% del promedio",
            "Soporte": f"${datos_mercado['soporte']:.2f}",
            "Resistencia": f"${datos_mercado['resistencia']:.2f}"
        }
    }


@tool
def consultar_cartera() -> dict:
    """
    Consulta la cartera actual del cliente con todas sus posiciones y métricas.
    
    Returns:
        Información completa de la cartera incluyendo posiciones, rendimiento y alertas
    """
    
    cartera = cargar_cartera()
    
    # Calcular valores actuales
    posiciones_detalle = []
    valor_total_posiciones = 0
    alertas = []
    recomendaciones = []
    
    for pos in cartera["posiciones"]:
        valor_actual = pos["cantidad"] * pos["precio_actual"]
        valor_compra = pos["cantidad"] * pos["precio_compra"]
        ganancia_perdida = valor_actual - valor_compra
        ganancia_pct = (ganancia_perdida / valor_compra) * 100
        concentracion = (valor_actual / cartera["cliente"]["capital_total"]) * 100
        
        valor_total_posiciones += valor_actual
        
        posiciones_detalle.append({
            "simbolo": pos["simbolo"],
            "nombre": pos["nombre"],
            "cantidad": pos["cantidad"],
            "precio_compra": f"${pos['precio_compra']:.2f}",
            "precio_actual": f"${pos['precio_actual']:.2f}",
            "valor_actual": f"${valor_actual:.2f}",
            "ganancia_perdida": f"${ganancia_perdida:+.2f}",
            "ganancia_pct": f"{ganancia_pct:+.2f}%",
            "concentracion": f"{concentracion:.1f}%",
            "sector": pos["sector"],
            "dias_en_cartera": (datetime.now() - datetime.strptime(pos["fecha_compra"], "%Y-%m-%d")).days
        })
        
        # Evaluar alertas
        if concentracion > 20:
            alertas.append(f"⚠️ {pos['simbolo']}: Concentración del {concentracion:.1f}% excede el límite del 20%")
            acciones_a_vender = int((concentracion - 20) / 100 * pos['cantidad'])
            recomendaciones.append(f"Reducir posición en {pos['simbolo']} vendiendo {acciones_a_vender} acciones")
        
        perfil = cartera["cliente"]["perfil_riesgo"]
        if perfil == "MODERADO" and ganancia_pct >= 15:
            alertas.append(f"✅ {pos['simbolo']}: Ganancia del {ganancia_pct:.1f}% alcanzó objetivo de take profit")
            recomendaciones.append(f"Considerar tomar ganancias parciales en {pos['simbolo']}")
        elif perfil == "CONSERVADOR" and ganancia_pct >= 8:
            alertas.append(f"✅ {pos['simbolo']}: Ganancia del {ganancia_pct:.1f}% alcanzó objetivo de take profit")
            recomendaciones.append(f"Considerar tomar ganancias en {pos['simbolo']}")
        
        if ganancia_pct <= -5:
            alertas.append(f"🔴 {pos['simbolo']}: Pérdida del {ganancia_pct:.1f}% activó stop loss")
            recomendaciones.append(f"URGENTE: Vender {pos['simbolo']} para limitar pérdidas")
    
    efectivo = cartera["cliente"]["capital_total"] - valor_total_posiciones
    exposicion_pct = (valor_total_posiciones / cartera["cliente"]["capital_total"]) * 100
    
    # Análisis por sector
    sectores = {}
    for pos in cartera["posiciones"]:
        sector = pos["sector"]
        valor = pos["cantidad"] * pos["precio_actual"]
        if sector in sectores:
            sectores[sector] += valor
        else:
            sectores[sector] = valor
    
    distribucion_sectores = {
        sector: f"{(valor/valor_total_posiciones)*100:.1f}%"
        for sector, valor in sectores.items()
    }
    
    return {
        "resumen": {
            "capital_total": f"${cartera['cliente']['capital_total']:.2f}",
            "valor_posiciones": f"${valor_total_posiciones:.2f}",
            "efectivo_disponible": f"${efectivo:.2f}",
            "numero_posiciones": len(cartera["posiciones"]),
            "exposicion": f"{exposicion_pct:.1f}%",
            "perfil_riesgo": cartera["cliente"]["perfil_riesgo"],
            "rendimiento_total": f"+{cartera['metricas']['rendimiento_total']:.2f}%"
        },
        "posiciones": posiciones_detalle,
        "distribucion_sectores": distribucion_sectores,
        "alertas": alertas if alertas else ["✅ Cartera dentro de los parámetros de riesgo"],
        "recomendaciones": recomendaciones if recomendaciones else ["✅ Cartera balanceada correctamente"],
        "cumplimiento_reglas": {
            "diversificacion": "OK" if all(float(p["concentracion"].rstrip('%')) <= 20 for p in posiciones_detalle) else "⚠️ ALERTA",
            "exposicion_total": "OK" if exposicion_pct <= 90 else "⚠️ ALTA",
            "liquidez": "OK" if efectivo >= cartera["cliente"]["capital_total"] * 0.1 else "⚠️ BAJA"
        },
        "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@tool
def ejecutar_compra(
    simbolo: str,
    cantidad: int,
    precio_limite: Optional[float] = None
) -> dict:
    """
    Ejecuta una orden de compra de acciones.
    
    Args:
        simbolo: Símbolo de la acción a comprar
        cantidad: Cantidad de acciones a comprar
        precio_limite: Precio límite para la compra (opcional)
    
    Returns:
        Confirmación de la orden ejecutada
    """
    
    cartera = cargar_cartera()
    precio_ejecucion = precio_limite if precio_limite else 150.50
    comision = cantidad * precio_ejecucion * cartera["configuracion"]["comision_compra"]
    monto_total = (cantidad * precio_ejecucion) + comision
    
    # Validar fondos disponibles
    posiciones_valor = sum(p["cantidad"] * p["precio_actual"] for p in cartera["posiciones"])
    efectivo_disponible = cartera["cliente"]["capital_total"] - posiciones_valor
    
    if monto_total > efectivo_disponible:
        return {
            "estado": "RECHAZADA",
            "motivo": "Fondos insuficientes",
            "efectivo_disponible": f"${efectivo_disponible:.2f}",
            "monto_requerido": f"${monto_total:.2f}",
            "faltante": f"${monto_total - efectivo_disponible:.2f}"
        }
    
    # Generar orden
    orden_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    transaccion = {
        "id": orden_id,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": "COMPRA",
        "simbolo": simbolo.upper(),
        "cantidad": cantidad,
        "precio": precio_ejecucion,
        "monto_total": monto_total
    }
    
    # Guardar transacción
    guardar_transaccion(transaccion)
    
    return {
        "estado": "✅ EJECUTADA",
        "orden_id": orden_id,
        "simbolo": simbolo.upper(),
        "tipo_operacion": "COMPRA",
        "cantidad_acciones": cantidad,
        "precio_ejecucion": f"${precio_ejecucion:.2f}",
        "subtotal": f"${cantidad * precio_ejecucion:.2f}",
        "comision": f"${comision:.2f}",
        "monto_total": f"${monto_total:.2f}",
        "efectivo_restante": f"${efectivo_disponible - monto_total:.2f}",
        "timestamp": transaccion["fecha"],
        "mensaje": f"✅ Compra de {cantidad} acciones de {simbolo.upper()} ejecutada exitosamente"
    }


@tool
def ejecutar_venta(
    simbolo: str,
    cantidad: int,
    precio_limite: Optional[float] = None
) -> dict:
    """
    Ejecuta una orden de venta de acciones.
    
    Args:
        simbolo: Símbolo de la acción a vender
        cantidad: Cantidad de acciones a vender
        precio_limite: Precio límite para la venta (opcional)
    
    Returns:
        Confirmación de la orden ejecutada
    """
    
    cartera = cargar_cartera()
    
    # Buscar posición
    posicion = next((p for p in cartera["posiciones"] if p["simbolo"] == simbolo.upper()), None)
    
    if not posicion:
        return {
            "estado": "RECHAZADA",
            "motivo": f"No tienes posición en {simbolo.upper()}",
            "posiciones_disponibles": [p["simbolo"] for p in cartera["posiciones"]]
        }
    
    if cantidad > posicion["cantidad"]:
        return {
            "estado": "RECHAZADA",
            "motivo": "Cantidad insuficiente",
            "cantidad_disponible": posicion["cantidad"],
            "cantidad_solicitada": cantidad
        }
    
    precio_ejecucion = precio_limite if precio_limite else posicion["precio_actual"]
    comision = cantidad * precio_ejecucion * cartera["configuracion"]["comision_venta"]
    monto_bruto = cantidad * precio_ejecucion
    monto_neto = monto_bruto - comision
    
    # Calcular ganancia/pérdida
    costo_original = cantidad * posicion["precio_compra"]
    ganancia_perdida = monto_neto - costo_original
    ganancia_pct = (ganancia_perdida / costo_original) * 100
    
    orden_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    transaccion = {
        "id": orden_id,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": "VENTA",
        "simbolo": simbolo.upper(),
        "cantidad": cantidad,
        "precio": precio_ejecucion,
        "monto_total": monto_neto,
        "ganancia_perdida": ganancia_perdida
    }
    
    guardar_transaccion(transaccion)
    
    return {
        "estado": "✅ EJECUTADA",
        "orden_id": orden_id,
        "simbolo": simbolo.upper(),
        "tipo_operacion": "VENTA",
        "cantidad_acciones": cantidad,
        "precio_ejecucion": f"${precio_ejecucion:.2f}",
        "monto_bruto": f"${monto_bruto:.2f}",
        "comision": f"${comision:.2f}",
        "monto_neto": f"${monto_neto:.2f}",
        "ganancia_perdida": f"${ganancia_perdida:+.2f}",
        "rendimiento": f"{ganancia_pct:+.2f}%",
        "timestamp": transaccion["fecha"],
        "mensaje": f"✅ Venta de {cantidad} acciones de {simbolo.upper()} ejecutada con {('ganancia' if ganancia_perdida > 0 else 'pérdida')} de ${abs(ganancia_perdida):.2f}"
    }


@tool
def consultar_historial_transacciones(limite: int = 10) -> dict:
    """
    Consulta el historial de transacciones realizadas.
    
    Args:
        limite: Número máximo de transacciones a mostrar
    
    Returns:
        Lista de transacciones recientes
    """
    
    cartera = cargar_cartera()
    transacciones = cartera["transacciones_historicas"][-limite:]
    transacciones.reverse()  # Más recientes primero
    
    total_compras = sum(1 for t in cartera["transacciones_historicas"] if t["tipo"] == "COMPRA")
    total_ventas = sum(1 for t in cartera["transacciones_historicas"] if t["tipo"] == "VENTA")
    
    return {
        "total_transacciones": len(cartera["transacciones_historicas"]),
        "total_compras": total_compras,
        "total_ventas": total_ventas,
        "transacciones_recientes": transacciones,
        "periodo": f"Últimas {len(transacciones)} transacciones"
    }


@tool
def consultar_reglas_negocio() -> dict:
    """
    Consulta las reglas de negocio activas del sistema de trading.
    
    Returns:
        Lista de reglas activas y su descripción
    """
    reglas = motor_reglas.obtener_reglas_activas()
    
    return {
        "total_reglas": len(reglas),
        "reglas_activas": reglas,
        "descripcion": "Reglas de negocio que el sistema evalúa automáticamente para cada operación",
        "categorias": {
            "Protección de Capital": [
                "STOP_LOSS_AUTOMATICO - Venta automática si pérdida > 5%",
                "LIMITE_PERDIDA_DIARIA - Detiene operaciones si pérdida diaria > 3%",
                "LIMITE_CONCENTRACION - Máximo 20% del portfolio en una acción"
            ],
            "Toma de Ganancias": [
                "TAKE_PROFIT_CONSERVADOR - Venta automática con ganancia del 8%",
                "TAKE_PROFIT_MODERADO - Venta automática con ganancia del 15%"
            ],
            "Señales Técnicas": [
                "COMPRA_SOPORTE_FUERTE - Compra cuando precio toca soporte con volumen",
                "VENTA_RESISTENCIA - Venta cuando precio toca resistencia",
                "COMPRA_TENDENCIA_ALCISTA - Compra en confirmación de tendencia alcista",
                "VENTA_CAMBIO_TENDENCIA - Venta cuando se detecta cambio de tendencia"
            ]
        }
    }


# Lista de herramientas
tools = [
    analizar_accion_con_reglas,
    consultar_cartera,
    ejecutar_compra,
    ejecutar_venta,
    consultar_historial_transacciones,
    consultar_reglas_negocio
]


# ==================== LÓGICA DEL AGENTE ====================

def extraer_simbolo(texto: str) -> str:
    """Extrae el símbolo de una acción del texto"""
    palabras = texto.upper().split()
    for palabra in palabras:
        # Buscar palabras de 1-5 letras mayúsculas (símbolos típicos)
        if 1 <= len(palabra) <= 5 and palabra.isalpha():
            return palabra
    return "AAPL"  # Default

def extraer_cantidad(texto: str) -> int:
    """Extrae la cantidad de acciones del texto"""
    numeros = re.findall(r'\d+', texto)
    return int(numeros[0]) if numeros else 10  # Default 10

def obtener_contexto_previo(messages: Sequence[BaseMessage]) -> Dict[str, Any]:
    """Obtiene el contexto de mensajes anteriores"""
    contexto = {
        "ultimo_simbolo": None,
        "ultima_cartera": None,
        "alertas_pendientes": []
    }
    
    # Buscar en mensajes de herramientas
    for msg in reversed(list(messages)):
        if isinstance(msg, ToolMessage):
            try:
                data = json.loads(msg.content)
                
                # Guardar último símbolo analizado
                if "simbolo" in data and not contexto["ultimo_simbolo"]:
                    contexto["ultimo_simbolo"] = data["simbolo"]
                
                # Guardar última cartera consultada
                if "posiciones" in data and not contexto["ultima_cartera"]:
                    contexto["ultima_cartera"] = data
                    
                    # Extraer alertas
                    if "alertas" in data:
                        contexto["alertas_pendientes"] = data["alertas"]
            except:
                pass
    
    return contexto


def should_continue(state: AgentState) -> str:
    """Determina si el agente debe continuar o terminar"""
    messages = state["messages"]
    last_message = messages[-1]
    
    if isinstance(last_message, AIMessage) and not last_message.tool_calls:
        return "end"
    return "continue"


def call_model(state: AgentState) -> dict:
    """
    Procesa el mensaje del usuario y decide qué herramienta usar.
    Mantiene contexto de la conversación.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if isinstance(last_message, HumanMessage):
        user_input = str(last_message.content).lower()
        contexto = obtener_contexto_previo(messages)
        
        # Analizar intención con contexto
        if any(word in user_input for word in ["cartera", "portfolio", "posiciones", "mis acciones", "tengo"]):
            response = AIMessage(
                content="Consultando tu cartera actual...",
                tool_calls=[{
                    "name": "consultar_cartera",
                    "args": {},
                    "id": "call_cartera"
                }]
            )
        
        elif any(word in user_input for word in ["analiza", "analizar", "análisis", "que opinas", "recomiendas"]):
            # Buscar símbolo en el mensaje o usar el del contexto
            simbolo = extraer_simbolo(user_input)
            if simbolo == "AAPL" and contexto["ultimo_simbolo"]:
                simbolo = contexto["ultimo_simbolo"]
            
            response = AIMessage(
                content=f"Analizando {simbolo} con las reglas de negocio...",
                tool_calls=[{
                    "name": "analizar_accion_con_reglas",
                    "args": {"simbolo": simbolo, "perfil_riesgo": "MODERADO"},
                    "id": "call_analizar"
                }]
            )
        
        elif any(word in user_input for word in ["compra", "comprar", "adquirir", "cómprala", "comprala"]):
            # Intentar extraer símbolo del mensaje
            simbolo = extraer_simbolo(user_input)
            
            # Si no hay símbolo claro, usar el del contexto
            if simbolo == "AAPL" and contexto["ultimo_simbolo"] and any(word in user_input for word in ["la", "esa", "esta"]):
                simbolo = contexto["ultimo_simbolo"]
            
            cantidad = extraer_cantidad(user_input)
            
            response = AIMessage(
                content=f"Ejecutando compra de {cantidad} acciones de {simbolo}...",
                tool_calls=[{
                    "name": "ejecutar_compra",
                    "args": {"simbolo": simbolo, "cantidad": cantidad},
                    "id": "call_compra"
                }]
            )
        
        elif any(word in user_input for word in ["vende", "vender", "liquidar", "reducir", "vendela"]):
            # Buscar símbolo en el mensaje
            simbolo = extraer_simbolo(user_input)
            
            # Si dice "reducir" sin símbolo, buscar en alertas
            if "reducir" in user_input and simbolo == "AAPL":
                if contexto["alertas_pendientes"]:
                    # Extraer símbolo de la primera alerta
                    for alerta in contexto["alertas_pendientes"]:
                        match = re.search(r'([A-Z]{1,5}):', alerta)
                        if match:
                            simbolo = match.group(1)
                            break
            
            # Si no hay símbolo claro, usar el del contexto
            if simbolo == "AAPL" and contexto["ultimo_simbolo"] and any(word in user_input for word in ["la", "esa", "esta"]):
                simbolo = contexto["ultimo_simbolo"]
            
            cantidad = extraer_cantidad(user_input)
            
            response = AIMessage(
                content=f"Ejecutando venta de {cantidad} acciones de {simbolo}...",
                tool_calls=[{
                    "name": "ejecutar_venta",
                    "args": {"simbolo": simbolo, "cantidad": cantidad},
                    "id": "call_venta"
                }]
            )
        
        elif any(word in user_input for word in ["historial", "transacciones", "operaciones", "movimientos"]):
            response = AIMessage(
                content="Consultando historial de transacciones...",
                tool_calls=[{
                    "name": "consultar_historial_transacciones",
                    "args": {"limite": 10},
                    "id": "call_historial"
                }]
            )
        
        elif any(word in user_input for word in ["reglas", "normativa", "políticas", "criterios"]):
            response = AIMessage(
                content="Consultando reglas de negocio activas...",
                tool_calls=[{
                    "name": "consultar_reglas_negocio",
                    "args": {},
                    "id": "call_reglas"
                }]
            )
        
        else:
            response = AIMessage(
                content="""¡Hola! Soy tu Agente de Trading Inteligente.

Opero con un sistema de **reglas de negocio automatizadas** que incluyen:

🛡️ **Protección de Capital:**
• Stop Loss automático al 5% de pérdida
• Límite de pérdida diaria del 3%
• Máximo 20% de concentración por acción

📈 **Toma de Ganancias:**
• Take Profit automático según perfil de riesgo
• Conservador: 8% | Moderado: 15% | Agresivo: 25%

🎯 **Señales Técnicas:**
• Compra en soportes fuertes con volumen
• Venta en resistencias con sobrecompra
• Seguimiento de tendencias y cruces de medias móviles

**¿Qué puedo hacer por ti?**

1️⃣ **Analizar acciones** con reglas de negocio
   📊 "Analiza AAPL" o "Qué opinas de GOOGL"

2️⃣ **Consultar tu cartera** actual
   💼 "Muestra mi cartera" o "Cómo están mis posiciones"

3️⃣ **Ejecutar operaciones**
   💰 "Compra 10 acciones de MSFT"
   💸 "Vende 5 acciones de AAPL"

4️⃣ **Ver historial** de transacciones
   📋 "Muestra mis transacciones" o "Historial de operaciones"

5️⃣ **Consultar reglas** del sistema
   📖 "Muéstrame las reglas" o "Qué criterios usas"

Todas las operaciones se validan automáticamente contra las reglas de negocio antes de ejecutarse."""
            )
    
    else:
        # Procesar resultados de herramientas
        tool_messages = [msg for msg in state["messages"] if isinstance(msg, ToolMessage)]
        
        if tool_messages:
            last_tool = tool_messages[-1]
            tool_name = last_tool.name if hasattr(last_tool, 'name') else "unknown"
            tool_content = last_tool.content
            
            # Parsear el contenido JSON si es posible
            try:
                result_data = json.loads(tool_content)
            except:
                result_data = None
            
            # Generar respuesta según la herramienta ejecutada
            if tool_name == "consultar_cartera" and result_data:
                resumen = result_data.get("resumen", {})
                posiciones = result_data.get("posiciones", [])
                alertas = result_data.get("alertas", [])
                recomendaciones = result_data.get("recomendaciones", [])
                
                response_text = f"""📊 **RESUMEN DE TU CARTERA**

💰 **Capital Total:** {resumen.get('capital_total', 'N/A')}
📈 **Valor Posiciones:** {resumen.get('valor_posiciones', 'N/A')}
💵 **Efectivo Disponible:** {resumen.get('efectivo_disponible', 'N/A')}
🎯 **Rendimiento Total:** {resumen.get('rendimiento_total', 'N/A')}
📊 **Exposición:** {resumen.get('exposicion', 'N/A')}

🏢 **TUS POSICIONES ({len(posiciones)}):**
"""
                for pos in posiciones:
                    response_text += f"\n• **{pos['simbolo']}** ({pos['nombre']})\n"
                    response_text += f"  └─ {pos['cantidad']} acciones @ ${pos['precio_actual']}\n"
                    response_text += f"  └─ Valor: {pos['valor_actual']} | P&L: {pos['ganancia_perdida']} ({pos['ganancia_pct']})\n"
                
                if alertas:
                    response_text += "\n\n⚠️ **ALERTAS:**\n"
                    for alerta in alertas:
                        response_text += f"• {alerta}\n"
                
                if recomendaciones:
                    response_text += "\n💡 **RECOMENDACIONES:**\n"
                    for rec in recomendaciones:
                        response_text += f"• {rec}\n"
                
                response = AIMessage(content=response_text)
            
            elif tool_name == "analizar_accion_con_reglas" and result_data:
                response_text = f"""📊 **ANÁLISIS DE {result_data.get('simbolo', 'N/A')}**

💰 **Precio Actual:** ${result_data.get('precio_actual', 'N/A')}
📈 **Cambio:** {result_data.get('cambio_pct', 'N/A')}

🎯 **RECOMENDACIÓN:** {result_data.get('recomendacion', 'N/A')}

📋 **Reglas Aplicadas:**
"""
                for regla in result_data.get('reglas_aplicadas', []):
                    response_text += f"• {regla}\n"
                
                response_text += f"\n💡 **Justificación:**\n{result_data.get('justificacion', 'N/A')}"
                
                response = AIMessage(content=response_text)
            
            elif tool_name == "ejecutar_compra" and result_data:
                response_text = f"""✅ **COMPRA EJECUTADA**

📊 **Acción:** {result_data.get('simbolo', 'N/A')}
📈 **Cantidad:** {result_data.get('cantidad', 'N/A')} acciones
💰 **Precio:** ${result_data.get('precio', 'N/A')}
💵 **Total:** ${result_data.get('total', 'N/A')}
🔖 **Orden ID:** {result_data.get('orden_id', 'N/A')}

✅ {result_data.get('mensaje', 'Operación completada')}
"""
                response = AIMessage(content=response_text)
            
            elif tool_name == "ejecutar_venta" and result_data:
                response_text = f"""✅ **VENTA EJECUTADA**

📊 **Acción:** {result_data.get('simbolo', 'N/A')}
📉 **Cantidad:** {result_data.get('cantidad', 'N/A')} acciones
💰 **Precio:** ${result_data.get('precio', 'N/A')}
💵 **Total:** ${result_data.get('total', 'N/A')}
📊 **P&L:** {result_data.get('ganancia_perdida', 'N/A')} ({result_data.get('rendimiento_pct', 'N/A')})
🔖 **Orden ID:** {result_data.get('orden_id', 'N/A')}

✅ {result_data.get('mensaje', 'Operación completada')}
"""
                response = AIMessage(content=response_text)
            
            elif tool_name == "consultar_historial_transacciones" and result_data:
                transacciones = result_data.get('transacciones', [])
                estadisticas = result_data.get('estadisticas', {})
                
                response_text = f"""📋 **HISTORIAL DE TRANSACCIONES**

📊 **Estadísticas:**
• Total operaciones: {estadisticas.get('total_operaciones', 0)}
• Compras: {estadisticas.get('total_compras', 0)}
• Ventas: {estadisticas.get('total_ventas', 0)}

🕐 **Últimas {len(transacciones)} operaciones:**
"""
                for tx in transacciones:
                    tipo_emoji = "🟢" if tx['tipo'] == 'COMPRA' else "🔴"
                    response_text += f"\n{tipo_emoji} **{tx['tipo']}** - {tx['simbolo']}\n"
                    response_text += f"  └─ {tx['cantidad']} acciones @ ${tx['precio']}\n"
                    response_text += f"  └─ {tx['fecha']} | ID: {tx['orden_id']}\n"
                
                response = AIMessage(content=response_text)
            
            elif tool_name == "consultar_reglas_negocio" and result_data:
                response_text = "📖 **REGLAS DE NEGOCIO ACTIVAS**\n\n"
                
                for categoria, reglas in result_data.items():
                    if categoria != "total_reglas":
                        response_text += f"\n**{categoria.upper()}:**\n"
                        for regla in reglas:
                            response_text += f"• {regla}\n"
                
                response = AIMessage(content=response_text)
            
            else:
                # Respuesta genérica si no se reconoce la herramienta
                response = AIMessage(
                    content=f"✅ Operación completada.\n\n{tool_content[:500]}"
                )
        else:
            response = AIMessage(
                content="He completado la operación. ¿Necesitas algo más?"
            )
    
    return {"messages": [response]}


# ==================== CONSTRUCCIÓN DEL GRAFO ====================

def create_agent(config: Optional[RunnableConfig] = None):
    """
    Crea el agente de trading con reglas de negocio.
    Esta función es llamada por watsonx.orchestrate.
    """
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    
    workflow.add_edge("tools", "agent")
    
    return workflow


# Instancia para testing local
graph = create_agent().compile()


if __name__ == "__main__":
    print("🤖 Agente de Trading - Test Local")
    print("=" * 60)
    
    test_queries = [
        "Hola, ¿qué puedes hacer?",
        "Muestra mi cartera",
        "Analiza AAPL",
        "Compra 10 acciones de GOOGL"
    ]
    
    for query in test_queries:
        print(f"\n👤 Usuario: {query}")
        result = graph.invoke({"messages": [HumanMessage(content=query)]})
        print(f"🤖 Agente: {result['messages'][-1].content[:200]}...")
        print("-" * 60)

# Made with Bob
