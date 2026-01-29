from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "AVANCE_BIOCREDITOS_Y_AGROPROTECTOR.xlsx"
MODEL_FILE = Path(__file__).resolve().parents[1] / "data" / "modelo_crediticio.joblib"
SHEET_NAME = "COLOCACIONES_BIOCREDITOS"


@dataclass
class ModeloBundle:
    clf: Pipeline
    reg: Pipeline
    numerical_features: list
    categorical_features: list
    feature_columns: list


def _normalizar(serie: pd.Series) -> pd.Series:
    return (serie - serie.min()) / (serie.max() - serie.min() + 1e-8)


def _si_no(valor: Any) -> str:
    if isinstance(valor, str):
        v = valor.strip().lower()
        if v in {"si", "sí", "s", "true", "1", "yes"}:
            return "Sí"
        if v in {"no", "n", "false", "0"}:
            return "No"
    if isinstance(valor, (int, float)):
        return "Sí" if float(valor) >= 0.5 else "No"
    if isinstance(valor, bool):
        return "Sí" if valor else "No"
    return "No"


def _cargar_datos() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {DATA_FILE}")

    df = pd.read_excel(DATA_FILE, sheet_name=SHEET_NAME)
    df = df.rename(
        columns={
            "NUMERO": "ID",
            "REGION (1)": "REGION",
            "PROVINCIA (2)": "PROVINCIA",
            "DISTRITO (3)": "DISTRITO",
            "CASERIO/SECTOR (4)": "CASERIO_SECTOR",
            "AGENCIA ENTIDAD FINANCIERA (5)": "AGENCIA",
            "NOMBRES Y APELLIDOS DEL CLIENTE (6)": "NOMBRE_CLIENTE",
            "SEXO PROPIETARIO DEL NEGOCIO (7)": "SEXO",
            "MONTO DEL CRÉDITO (S/.) (8)": "MONTO_CREDITO",
            "DNI/RUC (9)": "DNI",
            "FECHA DESEMBOLSO (10)": "FECHA_DESEMBOLSO",
            "FECHA VENCIMIENTO (11)": "FECHA_VENCIMIENTO",
            "Meses": "PLAZO_MESES",
            "DESTINO DEL CRÉDITO : ACTIVO FIJO / CAPITAL DE TRABAJO (12)": "DESTINO_CREDITO",
            "ACTIVIDAD PRINCIPAL  DEL CLIENTE (13)": "ACTIVIDAD_PRINCIPAL",
            "TIPO DE CRÉDITO (15)": "TIPO_CREDITO",
            "TEA (16)": "TEA",
            "COORDENADAS UTM (17)": "COORDENADAS",
            "ÁREA TOTAL (HA) (18)": "AREA_TOTAL",
            "ÁREA A CULTIVAR (HA) (19)": "AREA_CULTIVAR",
            "PREDIO LIBRE DEFORESTACIÓN (20)": "PREDIO_LIBRE_DEFOREST",
            "PREDIO FUERA DE ZONAS DE ANP (21)": "PREDIO_FUERA_ANP",
            "PREDIO CON (SAF) (22)": "PREDIO_SAF",
            "EDAD DEL SAF (23)": "EDAD_SAF",
            "USO DE ABONOS SOSTENIBLES (24)": "USO_ABONOS",
            "MANEJO INTEGRADO DE PLAGAS (25)": "MANEJO_PLAGAS",
            "CLIENTE  NUEVO (28)": "CLIENTE_NUEVO",
        }
    )

    if "PAGARE" in df.columns:
        df = df.drop(columns=["PAGARE"])

    if "EDAD" not in df.columns:
        df["EDAD"] = 35

    df = df.dropna()
    return df


def _simular_targets(df: pd.DataFrame) -> pd.DataFrame:
    np.random.seed(2025)

    monto_norm = _normalizar(df["MONTO_CREDITO"].astype(float))
    plazo_norm = _normalizar(df["PLAZO_MESES"].astype(float))
    edad_norm = _normalizar(df["EDAD"].astype(float))
    area_norm = _normalizar(df["AREA_CULTIVAR"].astype(float))

    cliente_nuevo_riesgo = (df["CLIENTE_NUEVO"] == "Sí").astype(int)

    practicas_buenas = (
        (df["USO_ABONOS"] == "Sí").astype(int)
        + (df["MANEJO_PLAGAS"] == "Sí").astype(int)
        + (df["PREDIO_SAF"] == "Sí").astype(int)
        + (df["PREDIO_LIBRE_DEFOREST"] == "Sí").astype(int)
    ) / 4.0
    practicas_riesgo = 1 - practicas_buenas

    riesgo_score = (
        0.30 * monto_norm
        + 0.20 * plazo_norm
        + 0.15 * cliente_nuevo_riesgo
        + 0.15 * practicas_riesgo
        + 0.10 * (1 - edad_norm)
        + 0.10 * (1 - area_norm)
    )

    riesgo_score = np.clip(riesgo_score + np.random.normal(0, 0.08, len(df)), 0, 1)
    umbral = np.percentile(riesgo_score, 80)
    df["incumplio_90d"] = (riesgo_score >= umbral).astype(int)

    df["PD"] = riesgo_score

    area_norm = _normalizar(df["AREA_CULTIVAR"].astype(float))
    practicas_buenas = (
        (df["USO_ABONOS"] == "Sí").astype(int)
        + (df["MANEJO_PLAGAS"] == "Sí").astype(int)
        + (df["PREDIO_SAF"] == "Sí").astype(int)
    ) / 3.0

    lgd_base = 0.60
    ajuste = -0.2 * (area_norm + practicas_buenas) / 2
    lgd = np.clip(lgd_base + ajuste + np.random.normal(0, 0.05, len(df)), 0.3, 0.9)
    df["LGD"] = lgd

    df["EAD"] = df["MONTO_CREDITO"].astype(float)
    df["EL"] = df["PD"] * df["LGD"] * df["EAD"]

    return df


def _entrenar_modelo() -> ModeloBundle:
    df = _cargar_datos()
    df = _simular_targets(df)

    cols_no_predictoras = [
        "ID",
        "NOMBRE_CLIENTE",
        "DNI",
        "FECHA_DESEMBOLSO",
        "FECHA_VENCIMIENTO",
        "PD",
        "LGD",
        "EAD",
        "incumplio_90d",
        "EL",
    ]

    X = df.drop(columns=cols_no_predictoras, errors="ignore")
    y_clf = df["incumplio_90d"]
    y_reg = df["EL"]

    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()
    numerical_features = X.select_dtypes(include=[np.number]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numerical_features),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
        ]
    )

    clf_pipeline = Pipeline(
        steps=[
            ("preprocessor", clone(preprocessor)),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=150, random_state=42, class_weight="balanced"
                ),
            ),
        ]
    )

    X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
        X, y_clf, test_size=0.3, stratify=y_clf, random_state=42
    )
    clf_pipeline.fit(X_train_clf, y_train_clf)

    reg_pipeline = Pipeline(
        steps=[
            ("preprocessor", clone(preprocessor)),
            ("regressor", RandomForestRegressor(n_estimators=150, random_state=42)),
        ]
    )

    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X, y_reg, test_size=0.3, random_state=42
    )
    reg_pipeline.fit(X_train_reg, y_train_reg)

    bundle = ModeloBundle(
        clf=clf_pipeline,
        reg=reg_pipeline,
        numerical_features=numerical_features,
        categorical_features=categorical_features,
        feature_columns=X.columns.tolist(),
    )

    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, MODEL_FILE)
    return bundle


def _cargar_modelo() -> ModeloBundle:
    if MODEL_FILE.exists():
        try:
            return joblib.load(MODEL_FILE)
        except Exception:
            return _entrenar_modelo()
    return _entrenar_modelo()


def _preparar_input(payload: Dict[str, Any], bundle: ModeloBundle) -> pd.DataFrame:
    base = {
        "REGION": payload.get("region", "Cusco"),
        "PROVINCIA": payload.get("provincia", "La Convención"),
        "DISTRITO": payload.get("distrito", "Echarati"),
        "CASERIO_SECTOR": payload.get("caserio_sector", "N/A"),
        "AGENCIA": payload.get("agencia", "Agencia Echarati"),
        "SEXO": payload.get("sexo", "Masculino"),
        "MONTO_CREDITO": float(payload.get("monto_credito", 0)),
        "PLAZO_MESES": float(payload.get("plazo_meses", 12)),
        "DESTINO_CREDITO": payload.get("destino_credito", "Capital de trabajo"),
        "ACTIVIDAD_PRINCIPAL": payload.get("actividad_principal", "Café"),
        "TIPO_CREDITO": payload.get("tipo_credito", "Convencional"),
        "TEA": float(payload.get("tea", 0)),
        "COORDENADAS": payload.get("coordenadas", "0,0"),
        "AREA_TOTAL": float(payload.get("area_total", payload.get("area_cultivar", 1) or 1)),
        "AREA_CULTIVAR": float(payload.get("area_cultivar", 1)),
        "PREDIO_LIBRE_DEFOREST": _si_no(payload.get("predio_libre_deforest", "No")),
        "PREDIO_FUERA_ANP": _si_no(payload.get("predio_fuera_anp", "No")),
        "PREDIO_SAF": _si_no(payload.get("predio_saf", "No")),
        "EDAD_SAF": float(payload.get("edad_saf", 1)),
        "USO_ABONOS": _si_no(payload.get("uso_abonos", "No")),
        "MANEJO_PLAGAS": _si_no(payload.get("manejo_plagas", "No")),
        "CLIENTE_NUEVO": _si_no(payload.get("cliente_nuevo", "No")),
        "EDAD": float(payload.get("edad", 35)),
    }

    fila = {}
    for col in bundle.feature_columns:
        if col in base:
            fila[col] = base[col]
        else:
            if col in bundle.numerical_features:
                fila[col] = 0
            else:
                fila[col] = "N/A"

    return pd.DataFrame([fila])


def _eco_score(payload: Dict[str, Any]) -> Tuple[int, bool]:
    campos = [
        payload.get("predio_saf"),
        payload.get("predio_libre_deforest"),
        payload.get("predio_fuera_anp"),
        payload.get("uso_abonos"),
        payload.get("manejo_plagas"),
    ]
    completos = all(valor is not None and str(valor) != "" for valor in campos)
    valores = [
        _si_no(payload.get("predio_saf")) == "Sí",
        _si_no(payload.get("predio_libre_deforest")) == "Sí",
        _si_no(payload.get("predio_fuera_anp")) == "Sí",
        _si_no(payload.get("uso_abonos")) == "Sí",
        _si_no(payload.get("manejo_plagas")) == "Sí",
    ]
    score = int(round(sum(valores) / len(valores) * 100))
    return score, completos


def predecir(payload: Dict[str, Any]) -> Dict[str, Any]:
    bundle = _cargar_modelo()
    X = _preparar_input(payload, bundle)

    try:
        prob_impago = float(bundle.clf.predict_proba(X)[0, 1])
        perdida_esperada = float(bundle.reg.predict(X)[0])
    except ValueError as exc:
        mensaje = str(exc).lower()
        if "n_features" in mensaje or "feature" in mensaje:
            if MODEL_FILE.exists():
                MODEL_FILE.unlink(missing_ok=True)
            bundle = _entrenar_modelo()
            X = _preparar_input(payload, bundle)
            prob_impago = float(bundle.clf.predict_proba(X)[0, 1])
            perdida_esperada = float(bundle.reg.predict(X)[0])
        else:
            raise

    eco_score, completos = _eco_score(payload)

    if prob_impago >= 0.5:
        decision = "RECHAZADO"
    elif prob_impago >= 0.35:
        decision = "OBSERVACIÓN"
    else:
        decision = "APROBADO"

    if not completos:
        resumen = "Complete los datos ambientales para activar la IA."
        eco_tip = "Complete los datos ambientales para activar la IA."
    else:
        if prob_impago >= 0.5:
            resumen = "Riesgo elevado detectado. Se recomienda revisar garantías y plan de manejo."
        elif prob_impago >= 0.35:
            resumen = "Riesgo moderado. Considere ajustar condiciones y acompañamiento técnico."
        else:
            resumen = "Perfil saludable con buenas prácticas ambientales."

        eco_tip = "Mejore prácticas sostenibles para reducir riesgo y costo financiero." if eco_score < 60 else "Mantenga las buenas prácticas ambientales para sostener el score."

    return {
        "eco_score": eco_score,
        "decision": decision,
        "perdida_esperada": round(perdida_esperada, 2),
        "prob_impago": round(prob_impago * 100, 2),
        "resumen_ia": resumen,
        "eco_tip": eco_tip,
    }


def predecir_desde_stdin() -> Dict[str, Any]:
    import sys

    raw = sys.stdin.read().strip()
    if not raw:
        raw = "{}"
    payload = json.loads(raw)
    return predecir(payload)
