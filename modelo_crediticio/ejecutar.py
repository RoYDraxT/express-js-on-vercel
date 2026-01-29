import json
from .predictor import predecir_desde_stdin

if __name__ == "__main__":
    resultado = predecir_desde_stdin()
    print(json.dumps(resultado, ensure_ascii=False))
