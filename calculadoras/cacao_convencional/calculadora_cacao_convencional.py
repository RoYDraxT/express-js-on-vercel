# calculadoras/cacao_convencional/calculadora_cacao_convencional.py
"""
Calculadora de Ficha Técnica - Cacao Convencional
Basado en valores promedio del Excel oficial
"""

from typing import Dict, Any
from . import parametros as p

class CalculadoraCacaoConvencional:
    def __init__(self, hectareas: float = 1.0):
        if hectareas <= 0:
            raise ValueError("Las hectáreas deben ser mayores a 0")
        self.hectareas = hectareas

    def generar_ficha_tecnica(self) -> Dict[str, Any]:
        # ===== VALORES DEL EXCEL OFICIAL (promedios anuales) =====
        COSTO_INSTALACION = 9998.00          # S/ por ha (único, en año 0)
        PRODUCCION_PROMEDIO_QQ = 26.2        # qq/ha/año
        INGRESO_ANUAL_PROMEDIO = 11514.19    # S/ por ha/año
        COSTO_ANUAL_PROMEDIO = 4870.50       # S/ por ha/año
        UTILIDAD_ANUAL_PROMEDIO = INGRESO_ANUAL_PROMEDIO - COSTO_ANUAL_PROMEDIO  # ~6,643.69

        # Escalar por hectáreas
        inversion_inicial = COSTO_INSTALACION * self.hectareas
        produccion_qq = PRODUCCION_PROMEDIO_QQ * self.hectareas
        ingreso_anual = INGRESO_ANUAL_PROMEDIO * self.hectareas
        costo_anual = COSTO_ANUAL_PROMEDIO * self.hectareas
        utilidad_anual = UTILIDAD_ANUAL_PROMEDIO * self.hectareas

        # ROI: Utilidad anual vs inversión (no acumulada)
        roi_anual = (utilidad_anual / inversion_inicial * 100) if inversion_inicial > 0 else 0

        # === Cálculo de 15 años (12 años productivos) ===
        ingresos_12años = ingreso_anual * 12
        costos_12años = costo_anual * 12
        utilidad_neta_15años = ingresos_12años - costos_12años - inversion_inicial

        roi_15años = (utilidad_neta_15años / inversion_inicial * 100) if inversion_inicial > 0 else 0

        # VAN y TIR: Deben venir del Excel o de un cálculo real con flujos año por año.
        # Si no haces proyección detallada, NO calcules VAN/TIR aquí.
        # Usa los valores del Excel como constantes:
        van_10pct = 26445.20 * self.hectareas  # Ajustado por escala (si aplica)
        tir_pct = 29.33  # Valor fijo del Excel

        return {
            'datos_proyecto': {
                'hectareas': self.hectareas,
                'variedad': p.VARIEDAD,
                'region': p.REGION,
                'ciclo_productivo_años': p.PERIODO_VEGETATIVO_TOTAL
            },
            'instalacion': {
                'costo_total': round(inversion_inicial, 2),
                'costo_por_hectarea': round(COSTO_INSTALACION, 2),
                'desglose': {}
            },
            'produccion_promedio': {
                'produccion_qq': round(produccion_qq, 1),
                'ingresos': round(ingreso_anual, 2),
                'costos': round(costo_anual, 2),
                'utilidad': round(utilidad_anual, 2)
            },
            'analisis_financiero': {
                'van_tasa_10_pct': round(van_10pct, 2),
                'tir_porcentaje': tir_pct,
                'roi_anual_porcentaje': round(roi_anual, 2),
                'inversion_inicial': round(inversion_inicial, 2),
                'utilidad_anual_promedio': round(utilidad_anual, 2),
                'utilidad_neta_15años': round(utilidad_neta_15años, 2)
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
                'produccion': {},  # Vacío si no hay proyección detallada
                'resumen': {
                    'hectareas': self.hectareas,
                    'inversion_inicial': round(inversion_inicial, 2),
                    'ingreso_anual_promedio': round(ingreso_anual, 2),
                    'costo_anual_promedio': round(costo_anual, 2),
                    'utilidad_anual_promedio': round(utilidad_anual, 2),
                    'roi_anual_porcentaje': round(roi_anual, 2)
                }
            }
        }