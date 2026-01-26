# calculadoras/cacao_convencional/calculadora_cacao_convencional.py
"""
Calculadora de Ficha Técnica - Cacao Convencional
Basado en valores promedio del Excel oficial
Soporta cálculos sensibilizados y no sensibilizados
"""

from typing import Dict, Any
from . import parametros as p

class CalculadoraCacaoConvencional:
    def __init__(self, hectareas: float = 1.0, sensibilizado: bool = True):
        """
        Inicializa la calculadora de cacao convencional
        
        Args:
            hectareas: Número de hectáreas (mayor a 0)
            sensibilizado: Si True, usa costos sensibilizados. Si False, usa costos normales
        """
        if hectareas <= 0:
            raise ValueError("Las hectáreas deben ser mayores a 0")
        self.hectareas = hectareas
        self.sensibilizado = sensibilizado

    def generar_ficha_tecnica(self) -> Dict[str, Any]:
        """
        Genera la ficha técnica completa con ambos tipos de cálculos
        
        Returns:
            Dict con resultados sensibilizados, no sensibilizados y toggle activo
        """
        # Generar ambos tipos de cálculos
        resultado_sensibilizado = self._calcular_ficha(sensibilizado=True)
        resultado_no_sensibilizado = self._calcular_ficha(sensibilizado=False)
        
        # Retornar el resultado activo según el modo seleccionado
        resultado_activo = resultado_sensibilizado if self.sensibilizado else resultado_no_sensibilizado
        
        return {
            **resultado_activo,
            'modo_sensibilizado': self.sensibilizado,
            'calculos_alternativos': {
                'sensibilizado': resultado_sensibilizado,
                'no_sensibilizado': resultado_no_sensibilizado
            }
        }

    def _calcular_ficha(self, sensibilizado: bool) -> Dict[str, Any]:
        """
        Realiza el cálculo de la ficha técnica
        
        Args:
            sensibilizado: Si True, usa costos sensibilizados (+23% en instalación)
        
        Returns:
            Dict con todos los datos de la ficha técnica
        """
        # ===== PARÁMETROS DE PRODUCCIÓN (constantes) =====
        PRODUCCION_PROMEDIO_QQ = 26.17  # qq/ha/año
        NUMERO_TOTAL_PLANTONES = self.hectareas * 10000/9
        PRODUCCION_ARBOL_ANIO = p.PRODUCCION_QQ_POR_ARBOL_AÑO  # 0.03 qq/árbol/año
        MERMA_PRODUCTIVA = p.MERMA_PRODUCTIVA  # 0.02 (2%)
        
        # ===== COSTOS DE INSTALACIÓN =====
        # Costo base de instalación (año 0): 9,567 S/
        COSTO_INSTALACION_BASE = 9997.85
        # Sensibilización: +4.5% = 431 S/
        SENSIBILIZACION_INSTALACION = 1840.00
        
        if sensibilizado:
            costo_instalacion_ha = COSTO_INSTALACION_BASE - SENSIBILIZACION_INSTALACION  # 9,998
        else:
            costo_instalacion_ha = COSTO_INSTALACION_BASE  # 9,567
        
        # ===== PRODUCTIVIDAD Y RENDIMIENTO =====
        # Años 4-6: 24 qq, rendimiento 80%
        # Años 7-9: 27 qq, rendimiento 90%
        # Años 10-11: 30 qq, rendimiento 100%
        # Años 12-13: 28.5 qq, rendimiento 95%
        # Años 14-15: 24 qq, rendimiento 80%
        # Promedio ponderado: ~26.2 qq/ha/año
        
        # Cálculo optimizado de producción
        produccion_qq = NUMERO_TOTAL_PLANTONES * PRODUCCION_ARBOL_ANIO * 0.89 * (1 - MERMA_PRODUCTIVA)
        
        # ===== INGRESOS Y COSTOS ANUALES PROMEDIO =====
        # Precio promedio de venta: 440 S/. por qq
        PRECIO_VENTA_PROMEDIO = p.PRECIO_VENTA_PROMEDIO  # 440.00
        
        # Ingreso anual promedio
        ingreso_anual_ha = produccion_qq * PRECIO_VENTA_PROMEDIO  # 11,528
        
        # ===== COSTOS DE PRODUCCIÓN ANUAL =====
        # Costo base de producción: 4,871 S/. por ha (años 4-9)
        # Costo sensibilizado años 10-15: 8,158 S/. por ha
        COSTO_PRODUCCION_BASE = 5550.50
        COSTO_PRODUCCION_SENSIBILIZADO = 680.00
        
        if sensibilizado:
            # Promedio ponderado con sensibilización en años 10-15
            # 6 años base (4-9) + 6 años sensibilizados (10-15) = 12 años productivos
            costo_anual_ha = COSTO_PRODUCCION_BASE - COSTO_PRODUCCION_SENSIBILIZADO  # 6,514.50
        else:
            # Sin sensibilización: costo base constante
            costo_anual_ha = COSTO_PRODUCCION_BASE  # 4,870.50
        
        # ===== ESCALADO POR HECTÁREAS =====
        inversion_inicial = costo_instalacion_ha * self.hectareas
        ingreso_anual = ingreso_anual_ha
        costo_anual = costo_anual_ha * self.hectareas
        utilidad_anual = ingreso_anual - costo_anual
        
        # ===== ANÁLISIS FINANCIERO =====
        # ROI Anual: (Utilidad anual / Inversión inicial) * 100
        roi_anual = (utilidad_anual / inversion_inicial * 100) if inversion_inicial > 0 else 0
        
        # ===== PROYECCIÓN 15 AÑOS =====
        # 3 años de desarrollo (sin producción) + 12 años productivos
        AÑOS_PRODUCTIVOS = 12
        
        ingresos_12años = ingreso_anual * AÑOS_PRODUCTIVOS
        costos_12años = costo_anual * AÑOS_PRODUCTIVOS
        utilidad_neta_15años = ingresos_12años - costos_12años - inversion_inicial
        
        # ROI 15 años: (Utilidad neta total / Inversión inicial) * 100
        roi_15años = (utilidad_neta_15años / inversion_inicial * 100) if inversion_inicial > 0 else 0
        
        # ===== VAN y TIR =====
        # Valores calculados del Excel con tasa de descuento del 10%
        # VAN sensibilizado: ~26,445 S/. por ha
        # VAN no sensibilizado: ~28,500 S/. por ha (estimado)
        # TIR: ~29.33% (relativamente estable entre ambos escenarios)
        
        if sensibilizado:
            van_10pct_ha = 26445.20
            tir_pct = 29.33
        else:
            van_10pct_ha = 28500.00  # Estimación (mayor al reducir costos)
            tir_pct = 32.50  # Estimación (mayor al tener mejores flujos)
        
        van_10pct = van_10pct_ha * self.hectareas
        
        return {
            'datos_proyecto': {
                'hectareas': self.hectareas,
                'variedad': p.VARIEDAD,
                'region': p.REGION,
                'ciclo_productivo_años': p.PERIODO_VEGETATIVO_TOTAL,
                'años_desarrollo': p.PERIODO_DESARROLLO,
                'años_productivos': AÑOS_PRODUCTIVOS
            },
            'instalacion': {
                'costo_total': round(inversion_inicial, 2),
                'costo_por_hectarea': round(costo_instalacion_ha, 2),
                'sensibilizado': sensibilizado,
                'desglose': {
                    'costo_base': round(COSTO_INSTALACION_BASE * self.hectareas, 2),
                    'sensibilizacion': round(SENSIBILIZACION_INSTALACION * self.hectareas, 2) if sensibilizado else 0
                }
            },
            'produccion_promedio': {
                'produccion_qq': round(produccion_qq, 2),
                'produccion_qq_por_ha': round(PRODUCCION_PROMEDIO_QQ, 2),
                'precio_venta_qq': PRECIO_VENTA_PROMEDIO,
                'ingresos': round(ingreso_anual, 2),
                'costos': round(costo_anual, 2),
                'utilidad': round(utilidad_anual, 2),
                'margen_utilidad_pct': round((costo_anual / ingreso_anual * 100) if ingreso_anual > 0 else 0, 2)
            },
            'analisis_financiero': {
                'van_tasa_10_pct': round(van_10pct, 2),
                'tir_porcentaje': round(tir_pct, 2),
                'roi_anual_porcentaje': round(roi_anual, 2),
                'roi_15años_porcentaje': round(roi_15años, 2),
                'inversion_inicial': round(inversion_inicial, 2),
                'utilidad_anual_promedio': round(utilidad_anual, 2),
                'utilidad_neta_15años': round(utilidad_neta_15años, 2),
                'punto_equilibrio_años': round(inversion_inicial / utilidad_anual, 2) if utilidad_anual > 0 else 0
            },
            'proyeccion_15_años': {
                'instalacion': {
                    'año_0': {
                        'año': 0,
                        'costo': round(inversion_inicial, 2),
                        'ingreso': 0,
                        'utilidad': round(-inversion_inicial, 2),
                        'descripcion': 'Año de inversión inicial'
                    }
                },
                'desarrollo': {
                    'años_1_3': {
                        'años': '1-3',
                        'costo_anual': 0,
                        'ingreso_anual': 0,
                        'descripcion': 'Período de desarrollo sin producción'
                    }
                },
                'produccion': {
                    'años_4_15': {
                        'años': '4-15',
                        'años_productivos': AÑOS_PRODUCTIVOS,
                        'ingreso_anual_promedio': round(ingreso_anual, 2),
                        'costo_anual_promedio': round(costo_anual, 2),
                        'utilidad_anual_promedio': round(utilidad_anual, 2),
                        'ingreso_total': round(ingresos_12años, 2),
                        'costo_total': round(costos_12años, 2)
                    }
                },
                'resumen': {
                    'hectareas': self.hectareas,
                    'inversion_inicial': round(inversion_inicial, 2),
                    'ingreso_total_15años': round(ingresos_12años, 2),
                    'costo_total_15años': round(costos_12años + inversion_inicial, 2),
                    'utilidad_neta_15años': round(utilidad_neta_15años, 2),
                    'roi_total_porcentaje': round(roi_15años, 2)
                }
            }
        }