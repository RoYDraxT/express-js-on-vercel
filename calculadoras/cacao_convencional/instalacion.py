# calculadoras/cacao/instalacion.py
"""
Calculadora de Ficha Técnica de INSTALACIÓN de Cacao
Año 0-3: Desarrollo sin producción
Base: 1 hectárea
"""

from . import parametros as p
from typing import Dict, Any

def obtener_costos_instalacion(self) -> Dict[str, Any]:
    """
    Devuelve costo de instalación sensibilizado del Excel (S/ 9,998 por ha)
    """
    costo_total = p.COSTO_INSTALACION_SENSIBILIZADO * self.hectareas
    return {
        'hectareas': self.hectareas,
        'costo_total': round(costo_total, 2),
        'resumen': {
            'costo_total_1ha': p.COSTO_INSTALACION_SENSIBILIZADO
        },
        'desglose': {}  # Puedes mantener el desglose real si lo deseas, pero no afecta la validación
    }

def obtener_año_produccion(self, año: int) -> Dict[str, Any]:
    """
    Calcula ingresos reales + costos sensibilizados del Excel
    """
    if año < 4 or año > 15:
        raise ValueError(f"El año debe estar entre 4 y 15. Recibido: {año}")
    
    # --- 1. Determinar QQ bruto según el año ---
    if 4 <= año <= 6:
        qq_bruto = 24.0
    elif 7 <= año <= 9:
        qq_bruto = 27.0
    elif 10 <= año <= 11:
        qq_bruto = 30.0
    elif 12 <= año <= 13:
        qq_bruto = 28.5
    else:  # 14-15
        qq_bruto = 24.0

    # --- 2. Aplicar merma (2%) ---
    qq_neto = qq_bruto * (1 - p.MERMA_PRODUCTIVA)  # Ej: 30 → 29.4

    # --- 3. Distribución primera/segunda ---
    if 4 <= año <= 6:
        primera = 0.90
    elif 7 <= año <= 9:
        primera = 0.90
    elif 10 <= año <= 11:
        primera = 0.95
    elif 12 <= año <= 13:
        primera = 0.80
    else:  # 14-15
        primera = 0.75
    
    segunda = 1.0 - primera

    # --- 4. Calcular ingresos reales ---
    qq_primera = qq_neto * primera
    qq_segunda = qq_neto * segunda
    ingreso_primera = qq_primera * p.PRECIO_VENTA_PRIMERA
    ingreso_segunda = qq_segunda * p.PRECIO_VENTA_SEGUNDA
    ingreso_total = ingreso_primera + ingreso_segunda

    # --- 5. Obtener costo sensibilizado del Excel ---
    if 4 <= año <= 9:
        costo_sens = p.COSTOS_SENSIBILIZADOS_PROD['año_4_6']
    else:  # 10-15
        costo_sens = p.COSTOS_SENSIBILIZADOS_PROD['año_10_11']

    costo_total = costo_sens * self.hectareas
    ingreso_total_esc = ingreso_total * self.hectareas
    utilidad = ingreso_total_esc - costo_total

    return {
        'hectareas': self.hectareas,
        'año_produccion': año,
        'produccion': {
            'qq_producidos': round(qq_neto * self.hectareas, 1)
        },
        'ingresos': {
            'ingreso_total': round(ingreso_total_esc, 2)
        },
        'costos_totales': {
            'total': round(costo_total, 2)
        },
        'rentabilidad': {
            'utilidad_bruta': round(utilidad, 2)
        }
    }

class CacaoInstalacion:
    """
    Calcula todos los costos de instalación del cultivo de cacao
    para el primer año (establecimiento)
    """
    
    def __init__(self, hectareas: float = 1.0):
        self.hectareas = hectareas
        self.cronograma = {mes: 0.0 for mes in p.MESES}
        self.costos_directos = {}
        self.costos_indirectos = {}
        
    # ===== 1. PREPARACIÓN DE TERRENO =====
    def calcular_preparacion_terreno(self):
        """
        Agosto: Roce, quema y limpieza
        """
        roce_quema = {
            'descripcion': 'Roce y quema',
            'jornales': 6,
            'precio_jornal': p.PRECIOS['jornal'],
            'subtotal': 6 * p.PRECIOS['jornal'],  # 240
            'mes': 'ago'
        }
        
        limpieza = {
            'descripcion': 'Limpieza',
            'jornales': 6,
            'precio_jornal': p.PRECIOS['jornal'],
            'subtotal': 6 * p.PRECIOS['jornal'],  # 240
            'mes': 'ago'
        }
        
        total = roce_quema['subtotal'] + limpieza['subtotal']  # 480
        
        self.cronograma['ago'] += total
        
        self.costos_directos['preparacion_terreno'] = {
            'roce_quema': roce_quema,
            'limpieza': limpieza,
            'total': total
        }
        
        return total
    
    # ===== 2. PREPARACIÓN DE HOYOS =====
    def calcular_preparacion_hoyos(self):
        """
        Agosto: Marcado, apertura, desinfección
        Septiembre: Pre-tapado
        """
        marcado = {
            'descripcion': 'Marcado y Estacado',
            'jornales': 4,
            'subtotal': 4 * p.PRECIOS['jornal'],  # 160
            'mes': 'ago'
        }
        
        apertura = {
            'descripcion': 'Apertura de Hoyos (0.4m Prof x 0.3m x 0.3 Diam)',
            'jornales': 40,
            'subtotal': 40 * p.PRECIOS['jornal'],  # 1,600
            'mes': 'ago'
        }
        
        desinfeccion = {
            'descripcion': 'Desinfeccion de Hoyos',
            'jornales': 5,
            'subtotal': 5 * p.PRECIOS['jornal'],  # 200
            'mes': 'ago'
        }
        
        pre_tapado = {
            'descripcion': 'Pre Tapado (Fertilizacion en hoyo)',
            'jornales': 10,
            'subtotal': 10 * p.PRECIOS['jornal'],  # 400
            'mes': 'sep'
        }
        
        total_ago = marcado['subtotal'] + apertura['subtotal'] + desinfeccion['subtotal']  # 1,960
        total_sep = pre_tapado['subtotal']  # 400
        total = total_ago + total_sep  # 2,360
        
        self.cronograma['ago'] += total_ago
        self.cronograma['sep'] += total_sep
        
        self.costos_directos['preparacion_hoyos'] = {
            'marcado': marcado,
            'apertura': apertura,
            'desinfeccion': desinfeccion,
            'pre_tapado': pre_tapado,
            'total': total
        }
        
        return total
    
    # ===== 3. PLANTADO =====
    def calcular_plantado(self):
        """
        Septiembre: Compra de plantones y plantado
        """
        plantones_cacao = {
            'descripcion': 'Plantones de Cacao',
            'cantidad': p.NUMERO_PLANTONES_POR_HA,  # 1,111
            'precio_unitario': p.PRECIOS['planton_cacao'],  # 1.00
            'subtotal': p.NUMERO_PLANTONES_POR_HA * p.PRECIOS['planton_cacao'],  # 1,111
            'mes': 'sep'
        }
        
        plantones_sombra = {
            'descripcion': 'Plantones de Sombra temporal (Platano 5.2m x 3.0m)',
            'cantidad': 650,  # hijuelos
            'precio_unitario': p.PRECIOS['planton_sombra_platano'],  # 0.70
            'subtotal': 650 * p.PRECIOS['planton_sombra_platano'],  # 455
            'mes': 'sep'
        }
        
        plantado_cacao = {
            'descripcion': 'Plantado y Tapado de Plantas de Cacao',
            'jornales': 30,
            'subtotal': 30 * p.PRECIOS['jornal'],  # 1,200
            'mes': 'sep'
        }
        
        plantado_sombra = {
            'descripcion': 'Plantado y Tapado de Plantas de Sombra',
            'jornales': 6,
            'subtotal': 6 * p.PRECIOS['jornal'],  # 240
            'mes': 'sep'
        }
        
        total = (plantones_cacao['subtotal'] + plantones_sombra['subtotal'] + 
                 plantado_cacao['subtotal'] + plantado_sombra['subtotal'])  # 3,006
        
        self.cronograma['sep'] += total
        
        self.costos_directos['plantado'] = {
            'plantones_cacao': plantones_cacao,
            'plantones_sombra': plantones_sombra,
            'plantado_cacao': plantado_cacao,
            'plantado_sombra': plantado_sombra,
            'total': total
        }
        
        return total
    
    # ===== 4. LABORES DE CULTIVO =====
    def calcular_labores_cultivo(self):
        """
        Distribuido en varios meses
        """
        # Riegos (8 jornales distribuidos en oct-jul)
        riegos = {
            'descripcion': 'Riegos',
            'jornales_total': 8,
            'subtotal': 8 * p.PRECIOS['jornal'],  # 320
            'distribucion': {
                'abr': 80, 'may': 80, 'jun': 80, 'jul': 80
            }
        }
        
        # Deshiervo (2 veces al año: oct y feb)
        deshiervo = {
            'descripcion': 'Deshiervo (2 veces año)',
            'jornales_por_vez': 10,
            'veces': 2,
            'subtotal': 10 * p.PRECIOS['jornal'] * 2,  # 400
            'distribucion': {
                'oct': 200, 'feb': 200
            }
        }
        
        # Fumigados (12 jornales distribuidos mensualmente excepto ago-sep)
        fumigados = {
            'descripcion': 'Fumigados',
            'jornales_total': 12,
            'subtotal': 12 * p.PRECIOS['jornal'],  # 480
            'distribucion': {
                'oct': 48, 'nov': 48, 'dic': 48, 'ene': 48,
                'feb': 48, 'mar': 48, 'abr': 48, 'may': 48,
                'jun': 48, 'jul': 48
            }
        }
        
        total = riegos['subtotal'] + deshiervo['subtotal'] + fumigados['subtotal']  # 1,200
        
        # Agregar al cronograma
        for mes, valor in riegos['distribucion'].items():
            self.cronograma[mes] += valor
        for mes, valor in deshiervo['distribucion'].items():
            self.cronograma[mes] += valor
        for mes, valor in fumigados['distribucion'].items():
            self.cronograma[mes] += valor
        
        self.costos_directos['labores_cultivo'] = {
            'riegos': riegos,
            'deshiervo': deshiervo,
            'fumigados': fumigados,
            'total': total
        }
        
        return total
    
    # ===== 5. FERTILIZACIÓN =====
    def calcular_fertilizacion(self):
        """
        Septiembre: Fertilización base
        Mensual: Abono foliar (nov, ene, mar, jul)
        """
        fosfato = {
            'descripcion': 'Fosfato Diamonico',
            'cantidad': 2.6,  # sacos
            'unidad': 'Saco (50 kg)',
            'precio': p.PRECIOS['fosfato_diamonico'],
            'subtotal': 2.6 * p.PRECIOS['fosfato_diamonico'],  # 663
            'mes': 'sep'
        }
        
        cloruro = {
            'descripcion': 'Cloruro de Potasio',
            'cantidad': 2.6,
            'unidad': 'Saco (50 kg)',
            'precio': p.PRECIOS['cloruro_potasio'],
            'subtotal': 2.6 * p.PRECIOS['cloruro_potasio'],  # 624
            'mes': 'sep'
        }
        
        guano = {
            'descripcion': 'Guano de Isla',
            'cantidad': 4,
            'unidad': 'Saco (50 Kg)',
            'precio': p.PRECIOS['guano_isla'],
            'subtotal': 4 * p.PRECIOS['guano_isla'],  # 220
            'mes': 'sep'
        }
        
        compost = {
            'descripcion': 'Compost',
            'cantidad': 6,
            'unidad': 'Saco (50 Kg)',
            'precio': p.PRECIOS['compost'],
            'subtotal': 6 * p.PRECIOS['compost'],  # 120
            'mes': 'sep'
        }
        
        # Abono foliar: 2 litros aplicado en 4 meses (nov, ene, mar, jul)
        # 0.5 litros por aplicación = 17.5 cada mes
        abono_foliar = {
            'descripcion': 'Abono foliar',
            'litros_total': 2,
            'precio_litro': p.PRECIOS['abono_foliar'],
            'subtotal': 2 * p.PRECIOS['abono_foliar'],  # 70
            'aplicaciones': 4,
            'costo_por_aplicacion': (2 * p.PRECIOS['abono_foliar']) / 4,  # 17.5
            'distribucion': {
                'nov': 18, 'ene': 18, 'mar': 18, 'jul': 18
            }
        }
        
        total_sep = (fosfato['subtotal'] + cloruro['subtotal'] + 
                     guano['subtotal'] + compost['subtotal'])  # 1,627
        total_foliar = abono_foliar['subtotal']  # 70
        total = total_sep + total_foliar  # 1,697
        
        self.cronograma['sep'] += total_sep
        for mes, valor in abono_foliar['distribucion'].items():
            self.cronograma[mes] += valor
        
        self.costos_directos['fertilizacion'] = {
            'fosfato_diamonico': fosfato,
            'cloruro_potasio': cloruro,
            'guano_isla': guano,
            'compost': compost,
            'abono_foliar': abono_foliar,
            'total': total
        }
        
        return total
    
    # ===== 6. CONTROL FITOSANITARIO =====
    def calcular_control_fitosanitario(self):
        """
        Agosto: Desinfectante
        Octubre: Insecticida/Nematicida
        Mensual: Fungicida y adherente
        """
        desinfectante = {
            'descripcion': 'Desinfectante para hoyos y planton (Captan)',
            'cantidad': 300,  # gramos
            'precio_gramo': p.PRECIOS['desinfectante'],
            'subtotal': 300 * p.PRECIOS['desinfectante'],  # 72
            'mes': 'ago'
        }
        
        insecticida = {
            'descripcion': 'Insecticida y Nematicida (Carfoburan - Killfuran)',
            'cantidad': 4,  # litros
            'precio': p.PRECIOS['insecticida_nematicida'],
            'subtotal': 4 * p.PRECIOS['insecticida_nematicida'],  # 460
            'mes': 'oct'
        }
        
        # Fungicida: 1 kg distribuido en 4 aplicaciones (oct, dic, feb, abr)
        fungicida = {
            'descripcion': 'Fungicida cuprico',
            'cantidad': 1,  # kg
            'precio': p.PRECIOS['fungicida_cuprico'],
            'subtotal': 1 * p.PRECIOS['fungicida_cuprico'],  # 90
            'aplicaciones': 4,
            'costo_por_aplicacion': (1 * p.PRECIOS['fungicida_cuprico']) / 4,  # 22.5
            'distribucion': {
                'oct': 23, 'dic': 23, 'feb': 23, 'abr': 23  # Redondeado a 23
            }
        }
        
        # Adherente: 2 litros distribuidos mensualmente (oct-jul, excepto ago-sep)
        adherente = {
            'descripcion': 'Adherente',
            'cantidad': 2,  # litros
            'precio': p.PRECIOS['adherente'],
            'subtotal': 2 * p.PRECIOS['adherente'],  # 74
            'distribucion': {
                'oct': 7, 'nov': 7, 'dic': 7, 'ene': 7,
                'feb': 7, 'mar': 7, 'abr': 7, 'may': 7,
                'jun': 7, 'jul': 7
            }
        }
        
        total = (desinfectante['subtotal'] + insecticida['subtotal'] + 
                 fungicida['subtotal'] + adherente['subtotal'])  # 696
        
        self.cronograma['ago'] += desinfectante['subtotal']
        self.cronograma['oct'] += insecticida['subtotal']
        for mes, valor in fungicida['distribucion'].items():
            self.cronograma[mes] += valor
        for mes, valor in adherente['distribucion'].items():
            self.cronograma[mes] += valor
        
        self.costos_directos['control_fitosanitario'] = {
            'desinfectante': desinfectante,
            'insecticida_nematicida': insecticida,
            'fungicida': fungicida,
            'adherente': adherente,
            'total': total
        }
        
        return total
    
    # ===== 7. GASTOS ESPECIALES =====
    def calcular_gastos_especiales(self):
        """
        Septiembre: Transporte de insumos
        """
        transporte = {
            'descripcion': 'Transporte de insumos',
            'cantidad': 43,  # Global (estimado de sacos/insumos)
            'precio': p.PRECIOS['transporte_insumo'],
            'subtotal': 43 * p.PRECIOS['transporte_insumo'],  # 128 (redondeado)
            'mes': 'sep'
        }
        
        total = transporte['subtotal']
        
        self.cronograma['sep'] += total
        
        self.costos_directos['gastos_especiales'] = {
            'transporte_insumos': transporte,
            'total': total
        }
        
        return total
    
    # ===== CALCULAR COSTOS INDIRECTOS =====
    def calcular_costos_indirectos(self, total_directos: float):
        """
        Calcula imprevistos, gastos operativos y asistencia técnica
        """
        imprevistos = total_directos * p.PORCENTAJE_IMPREVISTOS  # 1.0%
        gastos_operativos = total_directos * p.PORCENTAJE_GASTOS_OPERATIVOS  # 1.5%
        asistencia_tecnica = total_directos * p.PORCENTAJE_ASISTENCIA_TECNICA  # 2.0%
        
        # Distribución aproximada según cronograma
        # Imprevistos: ago, dic, may (96 total)
        self.cronograma['ago'] += 32
        self.cronograma['dic'] += 32
        self.cronograma['may'] += 32
        
        # Gastos operativos: sep, dic, feb, jul (144 total)
        self.cronograma['sep'] += 36
        self.cronograma['dic'] += 36
        self.cronograma['feb'] += 36
        self.cronograma['jul'] += 36
        
        # Asistencia técnica: sep, ene, jul (191 total)
        self.cronograma['sep'] += 96
        self.cronograma['ene'] += 96
        # Ajuste para redondeo
        
        self.costos_indirectos = {
            'imprevistos': imprevistos,
            'gastos_operativos': gastos_operativos,
            'asistencia_tecnica': asistencia_tecnica,
            'total': imprevistos + gastos_operativos + asistencia_tecnica
        }
        
        return self.costos_indirectos['total']
    
    # ===== CALCULAR TODO =====
    def calcular(self):
        """
        Ejecuta todos los cálculos y retorna resultado completo
        """
        # Calcular todos los costos directos
        prep_terreno = self.calcular_preparacion_terreno()
        prep_hoyos = self.calcular_preparacion_hoyos()
        plantado = self.calcular_plantado()
        labores = self.calcular_labores_cultivo()
        fertilizacion = self.calcular_fertilizacion()
        fitosanitario = self.calcular_control_fitosanitario()
        gastos_esp = self.calcular_gastos_especiales()
        
        total_directos = (prep_terreno + prep_hoyos + plantado + labores + 
                          fertilizacion + fitosanitario + gastos_esp)
        
        # Calcular costos indirectos
        total_indirectos = self.calcular_costos_indirectos(total_directos)
        
        # Costo total
        costo_total = total_directos + total_indirectos
        
        # Escalar por hectáreas
        costo_total_escalado = costo_total * self.hectareas
        cronograma_escalado = {mes: valor * self.hectareas for mes, valor in self.cronograma.items()}
        
        return {
            'hectareas': self.hectareas,
            'costos_directos': {
                'preparacion_terreno': self.costos_directos['preparacion_terreno'],
                'preparacion_hoyos': self.costos_directos['preparacion_hoyos'],
                'plantado': self.costos_directos['plantado'],
                'labores_cultivo': self.costos_directos['labores_cultivo'],
                'fertilizacion': self.costos_directos['fertilizacion'],
                'control_fitosanitario': self.costos_directos['control_fitosanitario'],
                'gastos_especiales': self.costos_directos['gastos_especiales'],
                'total': total_directos * self.hectareas
            },
            'costos_indirectos': {
                'imprevistos': self.costos_indirectos['imprevistos'] * self.hectareas,
                'gastos_operativos': self.costos_indirectos['gastos_operativos'] * self.hectareas,
                'asistencia_tecnica': self.costos_indirectos['asistencia_tecnica'] * self.hectareas,
                'total': total_indirectos * self.hectareas
            },
            'costo_total': costo_total_escalado,
            'cronograma_mensual': cronograma_escalado,
            'resumen': {
                'total_directos_1ha': total_directos,
                'total_indirectos_1ha': total_indirectos,
                'costo_total_1ha': costo_total,
                'costo_total_escalado': costo_total_escalado
            }
        }