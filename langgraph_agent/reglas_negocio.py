"""
Reglas de Negocio para Trading Automatizado
Estas reglas determinan las operaciones automáticas del agente
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class TipoOperacion(Enum):
    """Tipos de operaciones permitidas"""
    COMPRA = "COMPRA"
    VENTA = "VENTA"
    MANTENER = "MANTENER"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"


class NivelRiesgo(Enum):
    """Niveles de riesgo del cliente"""
    CONSERVADOR = "CONSERVADOR"
    MODERADO = "MODERADO"
    AGRESIVO = "AGRESIVO"


@dataclass
class ReglaNegocio:
    """Definición de una regla de negocio"""
    nombre: str
    descripcion: str
    condiciones: Dict
    accion: TipoOperacion
    prioridad: int


class MotorReglasNegocio:
    """
    Motor de reglas de negocio para operaciones de trading automatizado
    """
    
    def __init__(self):
        self.reglas = self._cargar_reglas()
    
    def _cargar_reglas(self) -> List[ReglaNegocio]:
        """Carga las reglas de negocio predefinidas"""
        return [
            # REGLA 1: Stop Loss Automático
            ReglaNegocio(
                nombre="STOP_LOSS_AUTOMATICO",
                descripcion="Venta automática si la pérdida supera el 5%",
                condiciones={
                    "perdida_porcentual": {"min": 5.0},
                    "tipo_cliente": [NivelRiesgo.CONSERVADOR, NivelRiesgo.MODERADO]
                },
                accion=TipoOperacion.STOP_LOSS,
                prioridad=1  # Máxima prioridad
            ),
            
            # REGLA 2: Take Profit Conservador
            ReglaNegocio(
                nombre="TAKE_PROFIT_CONSERVADOR",
                descripcion="Venta automática con ganancia del 8% para clientes conservadores",
                condiciones={
                    "ganancia_porcentual": {"min": 8.0},
                    "tipo_cliente": [NivelRiesgo.CONSERVADOR]
                },
                accion=TipoOperacion.TAKE_PROFIT,
                prioridad=2
            ),
            
            # REGLA 3: Take Profit Moderado
            ReglaNegocio(
                nombre="TAKE_PROFIT_MODERADO",
                descripcion="Venta automática con ganancia del 15% para clientes moderados",
                condiciones={
                    "ganancia_porcentual": {"min": 15.0},
                    "tipo_cliente": [NivelRiesgo.MODERADO]
                },
                accion=TipoOperacion.TAKE_PROFIT,
                prioridad=2
            ),
            
            # REGLA 4: Compra en Soporte Fuerte
            ReglaNegocio(
                nombre="COMPRA_SOPORTE_FUERTE",
                descripcion="Compra automática cuando el precio toca soporte con volumen alto",
                condiciones={
                    "precio_cerca_soporte": True,
                    "volumen": {"min": 1.5},  # 150% del promedio
                    "tendencia": "ALCISTA",
                    "rsi": {"max": 35}  # Sobreventa
                },
                accion=TipoOperacion.COMPRA,
                prioridad=3
            ),
            
            # REGLA 5: Venta en Resistencia
            ReglaNegocio(
                nombre="VENTA_RESISTENCIA",
                descripcion="Venta automática cuando el precio toca resistencia",
                condiciones={
                    "precio_cerca_resistencia": True,
                    "rsi": {"min": 70},  # Sobrecompra
                    "volumen": {"min": 1.2}
                },
                accion=TipoOperacion.VENTA,
                prioridad=3
            ),
            
            # REGLA 6: Diversificación Máxima
            ReglaNegocio(
                nombre="LIMITE_CONCENTRACION",
                descripcion="No permitir más del 20% del portfolio en una sola acción",
                condiciones={
                    "concentracion_porcentual": {"max": 20.0}
                },
                accion=TipoOperacion.MANTENER,
                prioridad=1
            ),
            
            # REGLA 7: Horario de Operación
            ReglaNegocio(
                nombre="HORARIO_OPERACION",
                descripcion="Solo operar en horario de mercado (9:30 AM - 4:00 PM EST)",
                condiciones={
                    "hora_mercado": True
                },
                accion=TipoOperacion.MANTENER,
                prioridad=1
            ),
            
            # REGLA 8: Límite de Pérdida Diaria
            ReglaNegocio(
                nombre="LIMITE_PERDIDA_DIARIA",
                descripcion="Detener operaciones si pérdida diaria supera 3%",
                condiciones={
                    "perdida_diaria_porcentual": {"max": 3.0}
                },
                accion=TipoOperacion.MANTENER,
                prioridad=1
            ),
            
            # REGLA 9: Compra en Tendencia Alcista Confirmada
            ReglaNegocio(
                nombre="COMPRA_TENDENCIA_ALCISTA",
                descripcion="Compra cuando hay confirmación de tendencia alcista",
                condiciones={
                    "media_movil_50": "CRUCE_ALCISTA",
                    "media_movil_200": "PRECIO_SUPERIOR",
                    "volumen": {"min": 1.3},
                    "macd": "POSITIVO"
                },
                accion=TipoOperacion.COMPRA,
                prioridad=4
            ),
            
            # REGLA 10: Venta por Cambio de Tendencia
            ReglaNegocio(
                nombre="VENTA_CAMBIO_TENDENCIA",
                descripcion="Venta cuando se detecta cambio de tendencia",
                condiciones={
                    "media_movil_50": "CRUCE_BAJISTA",
                    "volumen": {"min": 1.2},
                    "rsi": {"max": 50}
                },
                accion=TipoOperacion.VENTA,
                prioridad=3
            )
        ]
    
    def evaluar_operacion(self, datos_mercado: Dict, perfil_cliente: Dict) -> Dict:
        """
        Evalúa las reglas de negocio y determina la operación a realizar
        
        Args:
            datos_mercado: Datos actuales del mercado
            perfil_cliente: Perfil de riesgo y configuración del cliente
            
        Returns:
            Diccionario con la decisión y justificación
        """
        reglas_aplicables = []
        
        # Ordenar reglas por prioridad
        reglas_ordenadas = sorted(self.reglas, key=lambda r: r.prioridad)
        
        for regla in reglas_ordenadas:
            if self._evaluar_condiciones(regla.condiciones, datos_mercado, perfil_cliente):
                reglas_aplicables.append(regla)
        
        if not reglas_aplicables:
            return {
                "operacion": TipoOperacion.MANTENER.value,
                "regla_aplicada": "NINGUNA",
                "justificacion": "No se cumplen las condiciones para ninguna regla de negocio",
                "confianza": 0.5
            }
        
        # Tomar la regla de mayor prioridad
        regla_seleccionada = reglas_aplicables[0]
        
        return {
            "operacion": regla_seleccionada.accion.value,
            "regla_aplicada": regla_seleccionada.nombre,
            "justificacion": regla_seleccionada.descripcion,
            "confianza": self._calcular_confianza(regla_seleccionada, datos_mercado),
            "reglas_evaluadas": len(self.reglas),
            "reglas_aplicables": [r.nombre for r in reglas_aplicables]
        }
    
    def _evaluar_condiciones(self, condiciones: Dict, datos_mercado: Dict, perfil_cliente: Dict) -> bool:
        """Evalúa si se cumplen las condiciones de una regla"""
        # Implementación simplificada para la demo
        # En producción, esto sería más complejo
        return True  # Para demo, siempre retorna True
    
    def _calcular_confianza(self, regla: ReglaNegocio, datos_mercado: Dict) -> float:
        """Calcula el nivel de confianza de la operación"""
        # Basado en la prioridad y condiciones del mercado
        confianza_base = 1.0 - (regla.prioridad * 0.1)
        return max(0.6, min(0.95, confianza_base))
    
    def obtener_reglas_activas(self) -> List[str]:
        """Retorna la lista de reglas activas"""
        return [f"{r.nombre}: {r.descripcion}" for r in self.reglas]
    
    def validar_operacion(self, operacion: Dict, perfil_cliente: Dict) -> Dict:
        """
        Valida una operación propuesta contra las reglas de negocio
        
        Returns:
            Diccionario con resultado de validación
        """
        validaciones = {
            "aprobada": True,
            "alertas": [],
            "restricciones": []
        }
        
        # Validar límites de riesgo
        if perfil_cliente.get("nivel_riesgo") == NivelRiesgo.CONSERVADOR.value:
            if operacion.get("monto", 0) > perfil_cliente.get("capital_total", 0) * 0.1:
                validaciones["aprobada"] = False
                validaciones["restricciones"].append(
                    "Operación excede el 10% del capital para perfil conservador"
                )
        
        # Validar diversificación
        if operacion.get("concentracion", 0) > 20:
            validaciones["alertas"].append(
                "Advertencia: La operación aumenta la concentración por encima del 20%"
            )
        
        return validaciones

# Made with Bob
