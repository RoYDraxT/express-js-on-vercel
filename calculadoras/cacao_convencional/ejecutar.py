#!/usr/bin/env python3
"""Script auxiliar para ejecutar calculadora desde Node.js"""
import sys
import json

def main():
    try:
        # Obtener hectáreas del argumento
        hectareas = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
        
        # Importar calculadora (ahora con imports relativos que funcionan)
        from .calculadora_cacao_convencional import CalculadoraCacaoConvencional
        
        # Crear instancia y generar ficha
        calc = CalculadoraCacaoConvencional(hectareas=hectareas)
        ficha = calc.generar_ficha_tecnica()
        
        # Retornar JSON
        print(json.dumps(ficha, indent=2, default=str))
        
    except Exception as e:
        import traceback
        error_data = {
            "error": str(e),
            "type": type(e).__name__,
            "trace": traceback.format_exc()
        }
        print(json.dumps(error_data))
        sys.exit(1)

if __name__ == '__main__':
    main()
