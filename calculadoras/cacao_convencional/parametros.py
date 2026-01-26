# calculadoras/cacao/parametros.py
"""
Parámetros y constantes para Cacao Convencional - Región Cusco
Basado en la ficha técnica Excel
"""

# ===== INFORMACIÓN GENERAL =====
REGION = "Cusco"
PROVINCIAS = ["La Convencion", "Calca"]
VARIEDAD = "CCN 51 (Hibrido)"
TIPO_PRODUCCION = "Campo abierto"
FUENTE_RIEGO = "Canales de riego y de lluvias"

# ===== CICLO PRODUCTIVO =====
PERIODO_VEGETATIVO_TOTAL = 15  # años (incluye 3 de desarrollo)
PERIODO_DESARROLLO = 3  # años sin producción
PERIODO_POST_COSECHA = 1  # mes

DISTANCIAMIENTO = {
    'entre_surcos': 3.0,  # metros
    'entre_plantas': 3.0   # metros
}

# ===== PRODUCTIVIDAD POR AÑOS =====
PRODUCTIVIDAD = {
    'año_1_3': {'qq': 0, 'rendimiento': 0, 'primera': 0, 'segunda': 0},
    'año_4_6': {'qq': 24.0, 'rendimiento': 0.80, 'primera': 0.90, 'segunda': 0.10},
    'año_7_9': {'qq': 27.0, 'rendimiento': 0.90, 'primera': 0.90, 'segunda': 0.10},
    'año_10_11': {'qq': 30.0, 'rendimiento': 1.00, 'primera': 0.95, 'segunda': 0.05},
    'año_12_13': {'qq': 28.5, 'rendimiento': 0.95, 'primera': 0.80, 'segunda': 0.20},
    'año_14_15': {'qq': 24.0, 'rendimiento': 0.80, 'primera': 0.75, 'segunda': 0.25}
}

# ===== COSTOS SENSIBILIZADOS DE PRODUCCIÓN POR AÑO (del Excel) =====
COSTOS_SENSIBILIZADOS_PROD = {
    'año_4_6': 4871,
    'año_7_9': 4871,
    'año_10_11': 8158,   # ← ¡Este es el valor correcto para año 10!
    'año_12_13': 8158,
    'año_14_15': 8158,
}

# ===== COSTO DE INSTALACIÓN SENSIBILIZADO (del Excel) =====
COSTO_INSTALACION_SENSIBILIZADO = 9998  # 9,567 + 431

# ===== PARÁMETROS PRODUCTIVOS =====
NUMERO_PLANTONES_POR_HA = 1111
PRODUCCION_QQ_POR_ARBOL_AÑO = 30/1111
MERMA_PRODUCTIVA = 0.02  # 2%

# ===== PRECIOS (S/.) =====
PRECIOS = {
    # Mano de obra
    'jornal': 40.00,
    'dia_mecanizado': 80.00,
    
    # Plantones
    'planton_cacao': 1.00,
    'planton_sombra_platano': 0.70,
    
    # Fertilizantes
    'fosfato_diamonico': 255.00,      # saco 50kg
    'cloruro_potasio': 240.00,         # saco 50kg
    'guano_isla': 55.00,               # saco 50kg
    'compost': 20.00,                  # saco 50kg
    'abono_foliar': 35.00,             # litro
    'urea': 195.00,                    # saco 50kg
    'roca_fosforica': 50.00,           # saco 50kg
    'sulfato_potasio': 210.00,         # saco 50kg
    
    # Fitosanitarios
    'insecticida_nematicida': 115.00,  # litro (Carfoburan)
    'fungicida_cuprico': 90.00,        # kg
    'adherente': 37.00,                # litro
    'desinfectante': 0.24,             # gramo (Captan)
    'herbicida': 45.00,                # litro (Glyphosate)
    
    # Otros
    'saco_yute': 2.00,                 # unidad
    'transporte_insumo': 3.00,         # por saco
    'transporte_cosecha': 3.00,        # por QQ
}

# ===== PRECIOS DE VENTA =====
PRECIO_VENTA_PRIMERA = 480.00  # S/. por QQ
PRECIO_VENTA_SEGUNDA = 400.00  # S/. por QQ
PRECIO_VENTA_PROMEDIO = 440.00  # S/. por QQ (en chacra)

# ===== COSTOS INDIRECTOS (%) =====
PORCENTAJE_IMPREVISTOS = 0.01       # 1.0%
PORCENTAJE_GASTOS_OPERATIVOS = 0.015  # 1.5%
PORCENTAJE_ASISTENCIA_TECNICA = 0.02  # 2.0%

# Para producción
PORCENTAJE_IMPREVISTOS_PROD = 0.015      # 1.5%
PORCENTAJE_GASTOS_OPERATIVOS_PROD = 0.025 # 2.5%
PORCENTAJE_ASISTENCIA_TECNICA_PROD = 0.02  # 2.0%

# ===== MESES =====
MESES = ['ago', 'sep', 'oct', 'nov', 'dic', 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul']

MESES_MANTENIMIENTO = ['dic', 'ene', 'abr', 'may', 'jun', 'jul']
MESES_POST_COSECHA = ['abr', 'may', 'jun', 'jul']
MESES_COMERCIALIZACION = ['abr', 'may', 'jun', 'jul']