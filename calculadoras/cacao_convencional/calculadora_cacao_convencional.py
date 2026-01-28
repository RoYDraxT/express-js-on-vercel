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
            'costos_produccion_detallado': {
                'costos_directos': [
                    {
                        'categoria': '1. LABORES DE CULTIVO',
                        'subtotal': round(960.00 * self.hectareas, 2),
                        'items': [
                            {'nombre': 'Preparación de plantones de sombra', 'costo_total': round(80 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 2, 'ud': 'Jornal', 'meses': {'ago': 80, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Desyerbe mecánico (desbrozadora)', 'costo_total': round(160 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 2, 'ud': 'Jornal', 'meses': {'ago': 53.33, 'sep': 0, 'oct': 0, 'nov': 53.33, 'dic': 0, 'ene': 0, 'feb': 53.33, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Poda de mantenimiento de café (flosadora)', 'costo_total': round(160 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 4, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 160, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Abonamiento y/o fertilización', 'costo_total': round(160 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 4, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 0, 'oct': 80, 'nov': 80, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Poda de sombra especies arbóreas', 'costo_total': round(280 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 7, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 40, 'oct': 40, 'nov': 40, 'dic': 40, 'ene': 40, 'feb': 0, 'mar': 40, 'abr': 40, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Poda de sombra especies arbóreas', 'costo_total': round(120 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 3, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 0, 'oct': 120, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}}
                        ]
                    },
                    {
                        'categoria': '2. FERTILIZACIÓN',
                        'subtotal': round(1553.80 * self.hectareas, 2),
                        'items': [
                            {'nombre': 'Urea', 'costo_total': round(909 * self.hectareas, 2), 'precio_unitario': 195, 'cantidad': 4.66, 'ud': 'Saco (50 Kg)', 'meses': {'ago': 0, 'sep': 0, 'oct': 454.35, 'nov': 454.35, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Roca Fosfórica', 'costo_total': round(62 * self.hectareas, 2), 'precio_unitario': 50, 'cantidad': 1.24, 'ud': 'Saco (50 Kg)', 'meses': {'ago': 0, 'sep': 0, 'oct': 31, 'nov': 31, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Sulfato de potasio', 'costo_total': round(475 * self.hectareas, 2), 'precio_unitario': 210, 'cantidad': 2.26, 'ud': 'Saco (50 Kg)', 'meses': {'ago': 0, 'sep': 0, 'oct': 237.30, 'nov': 237.30, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Guano de isla', 'costo_total': round(39 * self.hectareas, 2), 'precio_unitario': 55, 'cantidad': 0.7, 'ud': 'Saco (50 Kg)', 'meses': {'ago': 0, 'sep': 0, 'oct': 19.25, 'nov': 19.25, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Abono foliar', 'costo_total': round(70 * self.hectareas, 2), 'precio_unitario': 35, 'cantidad': 2, 'ud': 'Litro', 'meses': {'ago': 0, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 70, 'may': 0, 'jun': 0, 'jul': 0}}
                        ]
                    },
                    {
                        'categoria': '3. CONTROL FITOSANITARIO',
                        'subtotal': round(989 * self.hectareas, 2),
                        'items': [
                            {'nombre': 'Insecticida y Nematicida (Carfouran - Killifuran)', 'costo_total': round(690 * self.hectareas, 2), 'precio_unitario': 115, 'cantidad': 6, 'ud': 'Litro', 'meses': {'ago': 0, 'sep': 345, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 345, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Fungicida cúprico', 'costo_total': round(90 * self.hectareas, 2), 'precio_unitario': 90, 'cantidad': 1, 'ud': 'Kg', 'meses': {'ago': 0, 'sep': 0, 'oct': 45, 'nov': 45, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Adherente', 'costo_total': round(74 * self.hectareas, 2), 'precio_unitario': 37, 'cantidad': 2, 'ud': 'Litro', 'meses': {'ago': 0, 'sep': 10.57, 'oct': 10.57, 'nov': 10.57, 'dic': 10.57, 'ene': 10.57, 'feb': 0, 'mar': 10.57, 'abr': 10.57, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Herbicida (Basoxla - Glyphosate)', 'costo_total': round(135 * self.hectareas, 2), 'precio_unitario': 45, 'cantidad': 3, 'ud': 'Litro', 'meses': {'ago': 0, 'sep': 45, 'oct': 0, 'nov': 0, 'dic': 45, 'ene': 0, 'feb': 0, 'mar': 45, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}}
                        ]
                    },
                    {
                        'categoria': '4. COSECHA',
                        'subtotal': round(880 * self.hectareas, 2),
                        'items': [
                            {'nombre': 'Cosecha de mazorcas', 'costo_total': round(400 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 10, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 400, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Quiebre de mazorcas', 'costo_total': round(80 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 2, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 80, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Fermentación', 'costo_total': round(160 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 4, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 160, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Secado', 'costo_total': round(80 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 2, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 80, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Limpieza y Selección de granos', 'costo_total': round(80 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 2, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 80, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Envasado', 'costo_total': round(80 * self.hectareas, 2), 'precio_unitario': 40, 'cantidad': 2, 'ud': 'Jornal', 'meses': {'ago': 0, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 80, 'jun': 0, 'jul': 0}}
                        ]
                    },
                    {
                        'categoria': '5. GASTOS ESPECIALES',
                        'subtotal': round(853.52  * self.hectareas, 2),
                        'items': [
                            {'nombre': 'Plantones de reposición de sombra', 'costo_total': round(21 * self.hectareas, 2), 'precio_unitario': 0.70, 'cantidad': 30, 'ud': 'Unid', 'meses': {'ago': 21, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Transporte de insumos', 'costo_total': round(36 * self.hectareas, 2), 'precio_unitario': 3.00, 'cantidad': 12, 'ud': 'Sacos', 'meses': {'ago': 36, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Transporte de cosecha', 'costo_total': round(78 * self.hectareas, 2), 'precio_unitario': 3.00, 'cantidad': 26, 'ud': 'Sacos', 'meses': {'ago': 0, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 78, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Sacos (1 QQ)', 'costo_total': round(52 * self.hectareas, 2), 'precio_unitario': 2.00, 'cantidad': 26, 'ud': 'Unid', 'meses': {'ago': 0, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 52, 'jun': 0, 'jul': 0}},
                            {'nombre': 'Costo de la instalación inicial (Para 15 Años)', 'costo_total': round(666.52 * self.hectareas, 2), 'precio_unitario': 667, 'cantidad': 1, 'ud': 'Global', 'meses': {'ago': 66.65, 'sep': 66.65, 'oct': 66.65, 'nov': 66.65, 'dic': 66.65, 'ene': 66.65, 'feb': 66.65, 'mar': 66.65, 'abr': 66.65, 'may': 66.65, 'jun': 0, 'jul': 0}}
                        ]
                    }
                ],
                'costos_indirectos': [
                    {'nombre': 'Imprevistos (1.5%)', 'porcentaje': 1.5, 'costo': round(78.54 * self.hectareas, 2), 'meses': {'ago': 0, 'sep': 26.18, 'oct': 0, 'nov': 0, 'dic': 26.18, 'ene': 0, 'feb': 0, 'mar': 26.18, 'abr': 0, 'may': 0, 'jun': 0, 'jul': 0}},
                    {'nombre': 'Gastos operativos (Pago de agua, compra y reparación de herramientas)', 'porcentaje': 2.5, 'costo': round(130.91 * self.hectareas, 2), 'meses': {'ago': 44, 'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0, 'ene': 43.64, 'feb': 0, 'mar': 0, 'abr': 0, 'may': 43.64, 'jun': 0, 'jul': 0}},
                    {'nombre': 'Asistencia técnica', 'porcentaje': 2.0, 'costo': round(104.73 * self.hectareas, 2), 'meses': {'ago': 0, 'sep': 0, 'oct': 52.36, 'nov': 0, 'dic': 0, 'ene': 0, 'feb': 0, 'mar': 0, 'abr': 52.36, 'may': 0, 'jun': 0, 'jul': 0}}
                ],
                'costo_tecnico': round(5550.50 * self.hectareas, 2),
                'gastos_asumidos_productor': round(680.00 * self.hectareas, 2),
                'costo_sensibilizado': round(costo_anual - round(680.00 * self.hectareas, 2), 2)
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