# calculadoras/base_calculadora.py
"""
Clase base abstracta para todas las calculadoras de fichas técnicas
Contiene métodos comunes y estructura base
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime

class CalculadoraFichaTecnica(ABC):
    """
    Clase base para todas las calculadoras de fichas técnicas agrícolas
    
    Atributos:
        hectareas (float): Número de hectáreas a calcular
        cronograma (Dict[str, float]): Costos mensuales
        costos_directos (Dict): Desglose de costos directos
        costos_indirectos (Dict): Desglose de costos indirectos
    """
    
    # Meses del año agrícola (Agosto - Julio)
    MESES = ['ago', 'sep', 'oct', 'nov', 'dic', 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul']
    
    def __init__(self, hectareas: float = 1.0):
        """
        Inicializa la calculadora
        
        Args:
            hectareas: Número de hectáreas (default: 1.0)
        
        Raises:
            ValueError: Si hectareas es menor o igual a 0
        """
        if hectareas <= 0:
            raise ValueError("El número de hectáreas debe ser mayor a 0")
        
        self.hectareas = hectareas
        self.cronograma = self._inicializar_cronograma()
        self.costos_directos = {}
        self.costos_indirectos = {}
        self.metadata = {
            'fecha_calculo': datetime.now().isoformat(),
            'version': '1.0'
        }
    
    def _inicializar_cronograma(self) -> Dict[str, float]:
        """
        Inicializa el cronograma mensual en ceros
        
        Returns:
            Dict con meses como keys y 0.0 como valores
        """
        return {mes: 0.0 for mes in self.MESES}
    
    def escalar(self, valor: float) -> float:
        """
        Escala un valor base (1 ha) al número de hectáreas solicitadas
        
        Args:
            valor: Valor base para 1 hectárea
        
        Returns:
            Valor escalado a las hectáreas especificadas
        """
        return valor * self.hectareas
    
    def redondear(self, valor: float, decimales: int = 2) -> float:
        """
        Redondea un valor a n decimales
        
        Args:
            valor: Valor a redondear
            decimales: Número de decimales (default: 2)
        
        Returns:
            Valor redondeado
        """
        return round(valor, decimales)
    
    def calcular_porcentaje(self, base: float, porcentaje: float) -> float:
        """
        Calcula un porcentaje de un valor base
        
        Args:
            base: Valor base
            porcentaje: Porcentaje a calcular (ejemplo: 0.15 para 15%)
        
        Returns:
            Resultado del cálculo
        """
        return self.redondear(base * porcentaje)
    
    def distribuir_en_meses(self, total: float, meses: List[str]) -> Dict[str, float]:
        """
        Distribuye un costo total equitativamente entre varios meses
        
        Args:
            total: Costo total a distribuir
            meses: Lista de meses donde distribuir
        
        Returns:
            Dict con la distribución mensual
        """
        if not meses:
            return {}
        
        costo_por_mes = total / len(meses)
        return {mes: self.redondear(costo_por_mes) for mes in meses}
    
    def agregar_al_cronograma(self, mes: str, valor: float):
        """
        Agrega un valor al cronograma de un mes específico
        
        Args:
            mes: Mes a agregar (debe estar en MESES)
            valor: Valor a agregar
        
        Raises:
            ValueError: Si el mes no es válido
        """
        if mes not in self.MESES:
            raise ValueError(f"Mes inválido: {mes}. Debe ser uno de {self.MESES}")
        
        self.cronograma[mes] += valor
    
    def obtener_total_cronograma(self) -> float:
        """
        Calcula el total del cronograma mensual
        
        Returns:
            Suma de todos los valores mensuales
        """
        return self.redondear(sum(self.cronograma.values()))
    
    def calcular_costos_indirectos_estandar(
        self, 
        costos_directos: float,
        porcentaje_imprevistos: float = 0.01,
        porcentaje_gastos_operativos: float = 0.015,
        porcentaje_asistencia_tecnica: float = 0.02
    ) -> Dict[str, float]:
        """
        Calcula costos indirectos estándar basados en porcentajes
        
        Args:
            costos_directos: Total de costos directos
            porcentaje_imprevistos: % para imprevistos (default: 1%)
            porcentaje_gastos_operativos: % para gastos operativos (default: 1.5%)
            porcentaje_asistencia_tecnica: % para asistencia técnica (default: 2%)
        
        Returns:
            Dict con desglose de costos indirectos
        """
        imprevistos = self.calcular_porcentaje(costos_directos, porcentaje_imprevistos)
        gastos_operativos = self.calcular_porcentaje(costos_directos, porcentaje_gastos_operativos)
        asistencia_tecnica = self.calcular_porcentaje(costos_directos, porcentaje_asistencia_tecnica)
        
        return {
            'imprevistos': {
                'porcentaje': porcentaje_imprevistos,
                'monto': imprevistos
            },
            'gastos_operativos': {
                'porcentaje': porcentaje_gastos_operativos,
                'monto': gastos_operativos
            },
            'asistencia_tecnica': {
                'porcentaje': porcentaje_asistencia_tecnica,
                'monto': asistencia_tecnica
            },
            'total': imprevistos + gastos_operativos + asistencia_tecnica
        }
    
    # ===== MÉTODOS ABSTRACTOS (deben implementarse en subclases) =====
    
    @abstractmethod
    def calcular_costos_directos(self) -> float:
        """
        Calcula todos los costos directos de producción
        Debe ser implementado por cada calculadora específica
        
        Returns:
            Total de costos directos
        """
        pass
    
    @abstractmethod
    def calcular_costos_indirectos(self, total_directos: float) -> float:
        """
        Calcula todos los costos indirectos
        Debe ser implementado por cada calculadora específica
        
        Args:
            total_directos: Total de costos directos calculados
        
        Returns:
            Total de costos indirectos
        """
        pass
    
    @abstractmethod
    def calcular(self) -> Dict[str, Any]:
        """
        Ejecuta todos los cálculos y retorna el resultado completo
        Debe ser implementado por cada calculadora específica
        
        Returns:
            Dict con todos los resultados de la ficha técnica
        """
        pass
    
    # ===== MÉTODOS DE UTILIDAD =====
    
    def validar_resultado(self, resultado: Dict[str, Any]) -> bool:
        """
        Valida que el resultado tenga la estructura mínima esperada
        
        Args:
            resultado: Dict resultado de calcular()
        
        Returns:
            True si es válido, False si no
        """
        campos_requeridos = ['hectareas', 'costos_directos', 'costos_indirectos', 
                            'costo_total', 'cronograma_mensual']
        
        return all(campo in resultado for campo in campos_requeridos)
    
    def exportar_resumen(self) -> Dict[str, Any]:
        """
        Genera un resumen ejecutivo de los cálculos
        
        Returns:
            Dict con resumen de costos y cronograma
        """
        return {
            'hectareas': self.hectareas,
            'costo_total_cronograma': self.obtener_total_cronograma(),
            'meses_con_actividad': [mes for mes, valor in self.cronograma.items() if valor > 0],
            'metadata': self.metadata
        }
    
    def __repr__(self) -> str:
        """Representación string de la calculadora"""
        return f"{self.__class__.__name__}(hectareas={self.hectareas})"