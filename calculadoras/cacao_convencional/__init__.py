# calculadoras/cacao_convencional/__init__.py
"""
Calculadoras para Cacao Convencional - Región Cusco
Incluye calculadoras de instalación y producción
"""

from .instalacion import CacaoInstalacion
from .produccion import CacaoProduccion
from .calculadora_cacao_convencional import CalculadoraCacaoConvencional
from . import parametros

__all__ = [
    'CacaoInstalacion',
    'CacaoProduccion',
    'CalculadoraCacaoConvencional',
    'parametros'
]