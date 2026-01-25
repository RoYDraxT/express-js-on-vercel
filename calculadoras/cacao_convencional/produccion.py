# calculadoras/cacao_convencional/produccion.py
"""
Calculadora de Ficha Técnica de PRODUCCIÓN de Cacao
Año 4 en adelante: Producción y cosecha
Base: 1 hectárea
"""

from ..base_calculadora import CalculadoraFichaTecnica
from . import parametros as p
from typing import Dict, Any

class CacaoProduccion(CalculadoraFichaTecnica):
    """
    Calcula todos los costos de producción y mantenimiento del cultivo de cacao
    Para años productivos (4to año en adelante)
    """
    
    def __init__(self, hectareas: float = 1.0, año_produccion: int = 4):
        """
        Inicializa calculadora de producción
        
        Args:
            hectareas: Número de hectáreas
            año_produccion: Año del ciclo productivo (4-15)
        """
        super().__init__(hectareas)
        
        if año_produccion < 4 or año_produccion > 15:
            raise ValueError("Año de producción debe estar entre 4 y 15")
        
        self.año_produccion = año_produccion
        self.productividad = self._obtener_productividad()
        self.costos_directos = {}
        self.ingresos = {}
    
    def _obtener_productividad(self) -> Dict[str, float]:
        """
        Obtiene los parámetros de productividad según el año
        
        Returns:
            Dict con qq, rendimiento, primera, segunda
        """
        if 4 <= self.año_produccion <= 6:
            return p.PRODUCTIVIDAD['año_4_6']
        elif 7 <= self.año_produccion <= 9:
            return p.PRODUCTIVIDAD['año_7_9']
        elif 10 <= self.año_produccion <= 11:
            return p.PRODUCTIVIDAD['año_10_11']
        elif 12 <= self.año_produccion <= 13:
            return p.PRODUCTIVIDAD['año_12_13']
        else:  # 14-15
            return p.PRODUCTIVIDAD['año_14_15']
    
    # ===== 1. LABORES DE CULTIVO =====
    def calcular_labores_cultivo(self) -> float:
        """
        Cálculo de labores de cultivo durante el año de producción
        """
        # Plantado reposición de sombra (Agosto)
        reposicion_sombra = {
            'descripcion': 'Plantado para reposicion de plantones de sombra',
            'jornales': 2,
            'subtotal': 2 * p.PRECIOS['jornal'],  # 80
            'mes': 'ago'
        }
        
        # Deshierbo mecánico (3 veces: ago, oct, ene)
        deshierbo_mecanico = {
            'descripcion': 'Deshierbo mecánico (desbrozadora)',
            'dias': 2,
            'precio_dia': p.PRECIOS['dia_mecanizado'],  # 80
            'subtotal': 2 * p.PRECIOS['dia_mecanizado'],  # 160
            'distribucion': {
                'ago': 53, 'oct': 53, 'ene': 53
            }
        }
        
        # Poda de mantenimiento (Septiembre)
        poda_mantenimiento = {
            'descripcion': 'Poda de mantenimiento de café (fitosanitaria)',
            'jornales': 4,
            'subtotal': 4 * p.PRECIOS['jornal'],  # 160
            'mes': 'sep'
        }
        
        # Abonamiento (Oct-Nov)
        abonamiento = {
            'descripcion': 'Abonamiento y/o fertilizacion',
            'jornales': 4,
            'subtotal': 4 * p.PRECIOS['jornal'],  # 160
            'distribucion': {
                'oct': 80, 'nov': 80
            }
        }
        
        # Fumigados (Sep-Abr, 7 meses)
        fumigados = {
            'descripcion': 'Fumigados',
            'jornales': 7,
            'subtotal': 7 * p.PRECIOS['jornal'],  # 280
            'distribucion': {
                'sep': 40, 'oct': 40, 'nov': 40, 'dic': 40,
                'ene': 40, 'mar': 40, 'abr': 40
            }
        }
        
        # Poda de sombra (Octubre)
        poda_sombra = {
            'descripcion': 'Poda de sombra especies arbóreas',
            'jornales': 3,
            'subtotal': 3 * p.PRECIOS['jornal'],  # 120
            'mes': 'oct'
        }
        
        total = (reposicion_sombra['subtotal'] + deshierbo_mecanico['subtotal'] +
                 poda_mantenimiento['subtotal'] + abonamiento['subtotal'] +
                 fumigados['subtotal'] + poda_sombra['subtotal'])  # 960
        
        # Agregar al cronograma
        self.cronograma['ago'] += reposicion_sombra['subtotal']
        for mes, valor in deshierbo_mecanico['distribucion'].items():
            self.cronograma[mes] += valor
        self.cronograma['sep'] += poda_mantenimiento['subtotal']
        for mes, valor in abonamiento['distribucion'].items():
            self.cronograma[mes] += valor
        for mes, valor in fumigados['distribucion'].items():
            self.cronograma[mes] += valor
        self.cronograma['oct'] += poda_sombra['subtotal']
        
        self.costos_directos['labores_cultivo'] = {
            'reposicion_sombra': reposicion_sombra,
            'deshierbo_mecanico': deshierbo_mecanico,
            'poda_mantenimiento': poda_mantenimiento,
            'abonamiento': abonamiento,
            'fumigados': fumigados,
            'poda_sombra': poda_sombra,
            'total': total
        }
        
        return total
    
    # ===== 2. FERTILIZACIÓN =====
    def calcular_fertilizacion(self) -> float:
        """
        Fertilización durante año de producción
        """
        urea = {
            'descripcion': 'Urea',
            'cantidad': 4.66,  # sacos
            'precio': p.PRECIOS['urea'],
            'subtotal': 4.66 * p.PRECIOS['urea'],  # 909
            'distribucion': {'oct': 454, 'nov': 454}
        }
        
        roca_fosforica = {
            'descripcion': 'Roca Fosforica',
            'cantidad': 1.24,
            'precio': p.PRECIOS['roca_fosforica'],
            'subtotal': 1.24 * p.PRECIOS['roca_fosforica'],  # 62
            'distribucion': {'oct': 31, 'nov': 31}
        }
        
        sulfato_potasio = {
            'descripcion': 'Sulfato de potasio',
            'cantidad': 2.26,
            'precio': p.PRECIOS['sulfato_potasio'],
            'subtotal': 2.26 * p.PRECIOS['sulfato_potasio'],  # 475
            'distribucion': {'oct': 237, 'nov': 237}
        }
        
        guano_isla = {
            'descripcion': 'Guano de Isla',
            'cantidad': 0.7,
            'precio': p.PRECIOS['guano_isla'],
            'subtotal': 0.7 * p.PRECIOS['guano_isla'],  # 39
            'distribucion': {'oct': 19, 'nov': 19}
        }
        
        abono_foliar = {
            'descripcion': 'Abono foliar',
            'cantidad': 2,  # litros
            'precio': p.PRECIOS['abono_foliar'],
            'subtotal': 2 * p.PRECIOS['abono_foliar'],  # 70
            'mes': 'abr'
        }
        
        total = (urea['subtotal'] + roca_fosforica['subtotal'] + 
                 sulfato_potasio['subtotal'] + guano_isla['subtotal'] + 
                 abono_foliar['subtotal'])  # 1,554
        
        # Agregar al cronograma
        for fertilizante in [urea, roca_fosforica, sulfato_potasio, guano_isla]:
            for mes, valor in fertilizante['distribucion'].items():
                self.cronograma[mes] += valor
        self.cronograma['abr'] += abono_foliar['subtotal']
        
        self.costos_directos['fertilizacion'] = {
            'urea': urea,
            'roca_fosforica': roca_fosforica,
            'sulfato_potasio': sulfato_potasio,
            'guano_isla': guano_isla,
            'abono_foliar': abono_foliar,
            'total': total
        }
        
        return total
    
    # ===== 3. CONTROL FITOSANITARIO =====
    def calcular_control_fitosanitario(self) -> float:
        """
        Control de plagas y enfermedades
        """
        insecticida = {
            'descripcion': 'Insecticida y Nematicida (Carfoburan - Killfuran)',
            'cantidad': 6,  # litros
            'precio': p.PRECIOS['insecticida_nematicida'],
            'subtotal': 6 * p.PRECIOS['insecticida_nematicida'],  # 690
            'distribucion': {'sep': 345, 'ene': 345}
        }
        
        fungicida = {
            'descripcion': 'Fungicida cuprico',
            'cantidad': 1,  # kg
            'precio': p.PRECIOS['fungicida_cuprico'],
            'subtotal': 1 * p.PRECIOS['fungicida_cuprico'],  # 90
            'distribucion': {'oct': 45, 'nov': 45}
        }
        
        adherente = {
            'descripcion': 'Adherente',
            'cantidad': 2,  # litros
            'precio': p.PRECIOS['adherente'],
            'subtotal': 2 * p.PRECIOS['adherente'],  # 74
            'distribucion': {
                'sep': 11, 'oct': 11, 'nov': 11, 'dic': 11,
                'ene': 11, 'mar': 11, 'abr': 11
            }
        }
        
        herbicida = {
            'descripcion': 'Herbicida (Bazooka - Glyphosate)',
            'cantidad': 3,  # litros
            'precio': p.PRECIOS['herbicida'],
            'subtotal': 3 * p.PRECIOS['herbicida'],  # 135
            'distribucion': {'sep': 45, 'nov': 45, 'feb': 45}
        }
        
        total = (insecticida['subtotal'] + fungicida['subtotal'] + 
                 adherente['subtotal'] + herbicida['subtotal'])  # 989
        
        # Agregar al cronograma
        for mes, valor in insecticida['distribucion'].items():
            self.cronograma[mes] += valor
        for mes, valor in fungicida['distribucion'].items():
            self.cronograma[mes] += valor
        for mes, valor in adherente['distribucion'].items():
            self.cronograma[mes] += valor
        for mes, valor in herbicida['distribucion'].items():
            self.cronograma[mes] += valor
        
        self.costos_directos['control_fitosanitario'] = {
            'insecticida': insecticida,
            'fungicida': fungicida,
            'adherente': adherente,
            'herbicida': herbicida,
            'total': total
        }
        
        return total
    
    # ===== 4. COSECHA =====
    def calcular_cosecha(self) -> float:
        """
        Costos de cosecha y post-cosecha
        """
        cosecha_mazorca = {
            'descripcion': 'Cosecha de mazorca',
            'jornales': 10,
            'subtotal': 10 * p.PRECIOS['jornal'],  # 400
            'mes': 'may'
        }
        
        quiebre = {
            'descripcion': 'Quiebre de mazorcas',
            'jornales': 2,
            'subtotal': 2 * p.PRECIOS['jornal'],  # 80
            'mes': 'may'
        }
        
        fermentacion = {
            'descripcion': 'Fermentacion',
            'jornales': 4,
            'subtotal': 4 * p.PRECIOS['jornal'],  # 160
            'mes': 'may'
        }
        
        secado = {
            'descripcion': 'Secado',
            'jornales': 2,
            'subtotal': 2 * p.PRECIOS['jornal'],  # 80
            'mes': 'may'
        }
        
        limpieza = {
            'descripcion': 'Limpieza y Selección de granos',
            'jornales': 2,
            'subtotal': 2 * p.PRECIOS['jornal'],  # 80
            'mes': 'may'
        }
        
        ensacado = {
            'descripcion': 'Ensacado',
            'jornales': 2,
            'subtotal': 2 * p.PRECIOS['jornal'],  # 80
            'mes': 'may'
        }
        
        total = (cosecha_mazorca['subtotal'] + quiebre['subtotal'] + 
                 fermentacion['subtotal'] + secado['subtotal'] + 
                 limpieza['subtotal'] + ensacado['subtotal'])  # 880
        
        self.cronograma['may'] += total
        
        self.costos_directos['cosecha'] = {
            'cosecha_mazorca': cosecha_mazorca,
            'quiebre': quiebre,
            'fermentacion': fermentacion,
            'secado': secado,
            'limpieza': limpieza,
            'ensacado': ensacado,
            'total': total
        }
        
        return total
    
    # ===== 5. GASTOS ESPECIALES =====
    def calcular_gastos_especiales(self) -> float:
        """
        Transporte y otros gastos
        """
        # Calcular QQ producidos
        qq_producidos = self.calcular_produccion_qq()
        
        reposicion_sombra = {
            'descripcion': 'Plantones de reposicion de sombra',
            'cantidad': 30,
            'precio': p.PRECIOS['planton_sombra_platano'],
            'subtotal': 30 * p.PRECIOS['planton_sombra_platano'],  # 21
            'mes': 'ago'
        }
        
        transporte_insumos = {
            'descripcion': 'Transporte de insumos',
            'sacos': 12,
            'precio': p.PRECIOS['transporte_insumo'],
            'subtotal': 12 * p.PRECIOS['transporte_insumo'],  # 36
            'mes': 'ago'
        }
        
        transporte_cosecha = {
            'descripcion': 'Transporte de cosecha',
            'qq': qq_producidos,
            'precio': p.PRECIOS['transporte_cosecha'],
            'subtotal': qq_producidos * p.PRECIOS['transporte_cosecha'],  # ~78
            'mes': 'may'
        }
        
        sacos = {
            'descripcion': 'Sacos (1 QQ)',
            'cantidad': qq_producidos,
            'precio': p.PRECIOS['saco_yute'],
            'subtotal': qq_producidos * p.PRECIOS['saco_yute'],  # ~52
            'mes': 'may'
        }
        
        # Costo de instalación amortizado (667/15 años = ~44.47 por año)
        # Distribuido mensualmente
        costo_instalacion_mensual = 667 / 15 / 12  # ~3.7 por mes
        costo_instalacion_anual = 667 / 15  # ~44.47
        
        instalacion = {
            'descripcion': 'Costo de la Instalacion Inicial (Para 15 Años)',
            'costo_total_instalacion': 667,
            'años_amortizacion': 15,
            'subtotal': costo_instalacion_anual,
            'distribucion_mensual': {mes: costo_instalacion_mensual for mes in p.MESES if mes != 'jun' and mes != 'jul'}
        }
        
        # Total sin instalación
        total_sin_instalacion = (reposicion_sombra['subtotal'] + 
                                transporte_insumos['subtotal'] + 
                                transporte_cosecha['subtotal'] + 
                                sacos['subtotal'])
        
        total = total_sin_instalacion + instalacion['subtotal']  # ~854
        
        # Agregar al cronograma
        self.cronograma['ago'] += reposicion_sombra['subtotal'] + transporte_insumos['subtotal']
        self.cronograma['may'] += transporte_cosecha['subtotal'] + sacos['subtotal']
        
        # Distribuir costo de instalación
        for mes in instalacion['distribucion_mensual']:
            self.cronograma[mes] += costo_instalacion_mensual
        
        self.costos_directos['gastos_especiales'] = {
            'reposicion_sombra': reposicion_sombra,
            'transporte_insumos': transporte_insumos,
            'transporte_cosecha': transporte_cosecha,
            'sacos': sacos,
            'instalacion_amortizada': instalacion,
            'total': total
        }
        
        return total
    
    # ===== CÁLCULO DE PRODUCCIÓN =====
    def calcular_produccion_qq(self) -> float:
        """
        Calcula los QQ producidos según el año
        
        Returns:
            Quintales producidos (con merma)
        """
        qq_bruto = self.productividad['qq']
        merma = qq_bruto * p.MERMA_PRODUCTIVA
        qq_neto = qq_bruto - merma
        
        return self.redondear(qq_neto, 1)
    
    def calcular_ingresos(self) -> Dict[str, Any]:
        """
        Calcula los ingresos por venta de cacao
        """
        qq_total = self.calcular_produccion_qq()
        
        # Distribución entre primera y segunda
        qq_primera = qq_total * self.productividad['primera']
        qq_segunda = qq_total * self.productividad['segunda']
        
        ingreso_primera = qq_primera * p.PRECIO_VENTA_PRIMERA
        ingreso_segunda = qq_segunda * p.PRECIO_VENTA_SEGUNDA
        ingreso_total = ingreso_primera + ingreso_segunda
        
        self.ingresos = {
            'qq_total': qq_total,
            'qq_primera': self.redondear(qq_primera, 1),
            'qq_segunda': self.redondear(qq_segunda, 1),
            'precio_primera': p.PRECIO_VENTA_PRIMERA,
            'precio_segunda': p.PRECIO_VENTA_SEGUNDA,
            'ingreso_primera': self.redondear(ingreso_primera),
            'ingreso_segunda': self.redondear(ingreso_segunda),
            'ingreso_total': self.redondear(ingreso_total)
        }
        
        return self.ingresos
    
    # ===== COSTOS DIRECTOS E INDIRECTOS =====
    def calcular_costos_directos(self) -> float:
        """
        Calcula todos los costos directos de producción
        """
        labores = self.calcular_labores_cultivo()
        fertilizacion = self.calcular_fertilizacion()
        fitosanitario = self.calcular_control_fitosanitario()
        cosecha = self.calcular_cosecha()
        gastos_esp = self.calcular_gastos_especiales()

        total = labores + fertilizacion + fitosanitario + cosecha + gastos_esp
        return total
    
    def calcular_costos_indirectos(self, total_directos: float) -> float:
        """
        Calcula costos indirectos para producción
        """
        indirectos = self.calcular_costos_indirectos_estandar(
            total_directos,
            porcentaje_imprevistos=p.PORCENTAJE_IMPREVISTOS_PROD,
            porcentaje_gastos_operativos=p.PORCENTAJE_GASTOS_OPERATIVOS_PROD,
            porcentaje_asistencia_tecnica=p.PORCENTAJE_ASISTENCIA_TECNICA_PROD
        )
        
        self.costos_indirectos = indirectos
        return indirectos['total']

    # ===== CÁLCULO COMPLETO =====
    def calcular(self) -> Dict[str, Any]:
        """
        Ejecuta todos los cálculos y retorna resultado completo
        """
        # Calcular costos
        total_directos = self.calcular_costos_directos()
        total_indirectos = self.calcular_costos_indirectos(total_directos)
        costo_total = total_directos + total_indirectos
        
        # Calcular ingresos
        ingresos = self.calcular_ingresos()
        
        # Calcular utilidad
        utilidad = ingresos['ingreso_total'] - costo_total
        margen = (utilidad / ingresos['ingreso_total'] * 100) if ingresos['ingreso_total'] > 0 else 0
        
        # Escalar por hectáreas
        resultado = {
            'hectareas': self.hectareas,
            'año_produccion': self.año_produccion,
            'productividad': self.productividad,
            
            'produccion': {
                'qq_producidos': ingresos['qq_total'] * self.hectareas,
                'qq_primera': ingresos['qq_primera'] * self.hectareas,
                'qq_segunda': ingresos['qq_segunda'] * self.hectareas,
            },
            
            'ingresos': {
                'ingreso_primera': ingresos['ingreso_primera'] * self.hectareas,
                'ingreso_segunda': ingresos['ingreso_segunda'] * self.hectareas,
                'ingreso_total': ingresos['ingreso_total'] * self.hectareas,
            },
            
            'costos_directos': {
                'labores_cultivo': self.costos_directos['labores_cultivo']['total'] * self.hectareas,
                'fertilizacion': self.costos_directos['fertilizacion']['total'] * self.hectareas,
                'control_fitosanitario': self.costos_directos['control_fitosanitario']['total'] * self.hectareas,
                'cosecha': self.costos_directos['cosecha']['total'] * self.hectareas,
                'gastos_especiales': self.costos_directos['gastos_especiales']['total'] * self.hectareas,
                'total': total_directos * self.hectareas
            },
            
            'costos_indirectos': {
                'imprevistos': self.costos_indirectos['imprevistos']['monto'] * self.hectareas,
                'gastos_operativos': self.costos_indirectos['gastos_operativos']['monto'] * self.hectareas,
                'asistencia_tecnica': self.costos_indirectos['asistencia_tecnica']['monto'] * self.hectareas,
                'total': total_indirectos * self.hectareas
            },
            
            'costos_totales': {
                'directos': total_directos * self.hectareas,
                'indirectos': total_indirectos * self.hectareas,
                'total': costo_total * self.hectareas,
                'costo_por_qq': (costo_total / ingresos['qq_total']) * self.hectareas if ingresos['qq_total'] > 0 else 0
            },
            
            'rentabilidad': {
                'utilidad_bruta': utilidad * self.hectareas,
                'margen_utilidad_porcentaje': self.redondear(margen, 2),
                'roi': self.redondear((utilidad / costo_total * 100), 2) if costo_total > 0 else 0
            },
            
            'cronograma_mensual': {mes: valor * self.hectareas for mes, valor in self.cronograma.items()},
            
            'metadata': {
                **self.metadata,
                'tipo_ficha': 'produccion',
                'cultivo': 'cacao_convencional',
                'region': p.REGION
            }
        }
    
        return resultado


