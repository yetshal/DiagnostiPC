"""
preprocesador_numerico.py
=========================
Módulo de Pre-procesamiento Numérico Híbrido para DiagnostiPC.

Convierte variables continuas de telemetría del mundo real (temperaturas en °C,
voltajes en V, latencias en ms, cuadros por segundo FPS y revoluciones RPM)
en hechos simbólicos discretos reconocidos por la base de conocimiento en Prolog.

Incorpora dos motores de discretización:
  1. Motor heurístico basado en estándares de la industria (especificaciones ATX e Intel/AMD).
  2. Motor de aprendizaje supervisado con Scikit-Learn (DecisionTreeClassifier).
"""

from __future__ import annotations

from typing import Any, Optional
import numpy as np
from sklearn.tree import DecisionTreeClassifier


# ---------------------------------------------------------------------------
# Especificaciones y umbrales estándar de la industria de hardware PC
# ---------------------------------------------------------------------------
UMBRALES_TELEMETRIA = {
    "temperatura_cpu": {
        "unidad": "°C",
        "normal": (30.0, 75.0),
        "alerta": 80.0,      # -> sobrecalentamiento
        "critico": 90.0,     # -> throttling
    },
    "temperatura_gpu": {
        "unidad": "°C",
        "normal": (30.0, 78.0),
        "alerta": 82.0,      # -> temperatura_alta_gpu
        "critico": 90.0,
    },
    "voltaje_12v": {
        "unidad": "V",
        "normal": (11.4, 12.6),  # Norma ATX ±5%
        "inestable_bajo": 11.4,  # -> voltaje_inestable
        "inestable_alto": 12.6,
    },
    "fps_promedio": {
        "unidad": "FPS",
        "normal": (60.0, 240.0),
        "alerta": 30.0,      # < 30 -> fps_bajos
    },
    "latencia_disco_ms": {
        "unidad": "ms",
        "normal": (0.1, 50.0),
        "alerta": 150.0,     # -> rendimiento_lento
        "critico": 600.0,    # -> errores_io
    },
    "rpm_ventilador": {
        "unidad": "RPM",
        "normal": (800.0, 3000.0),
        "critico": 0.0,      # -> ventilador_no_gira (si temp > 50°C)
    },
}


class PreprocesadorTelemetria:
    """
    Preprocesador híbrido de variables continuas de hardware a hechos simbólicos.
    """

    def __init__(self) -> None:
        self._clf_cpu: Optional[DecisionTreeClassifier] = None
        self._clf_gpu: Optional[DecisionTreeClassifier] = None
        self._clf_voltaje: Optional[DecisionTreeClassifier] = None
        self._clf_disco: Optional[DecisionTreeClassifier] = None
        self._entrenar_clasificadores()

    def _entrenar_clasificadores(self) -> None:
        """
        Entrena clasificadores ligeros de Scikit-learn utilizando datos
        sintéticos calibrados contra especificaciones físicas reales.
        """
        np.random.seed(42)

        # 1. Clasificador Térmico CPU: [Temp, RPM] -> 0: Normal, 1: Sobrecalentamiento, 2: Throttling, 3: Fan Parado
        # Generar perfiles normales (40 a 70°C, RPM 1000 a 2000)
        n_samples = 150
        x_cpu_norm = np.column_stack([
            np.random.uniform(35.0, 75.0, n_samples),
            np.random.uniform(900.0, 2200.0, n_samples),
        ])
        y_cpu_norm = np.zeros(n_samples, dtype=int)

        # Perfiles sobrecalentamiento (80 a 89°C)
        x_cpu_warm = np.column_stack([
            np.random.uniform(80.0, 89.9, n_samples),
            np.random.uniform(1200.0, 2500.0, n_samples),
        ])
        y_cpu_warm = np.ones(n_samples, dtype=int)

        # Perfiles throttling (90 a 105°C)
        x_cpu_hot = np.column_stack([
            np.random.uniform(90.0, 105.0, n_samples),
            np.random.uniform(1500.0, 3000.0, n_samples),
        ])
        y_cpu_hot = np.full(n_samples, 2, dtype=int)

        # Perfiles ventilador detenido (Temp > 55°C, RPM = 0)
        x_cpu_fan = np.column_stack([
            np.random.uniform(55.0, 95.0, n_samples),
            np.zeros(n_samples),
        ])
        y_cpu_fan = np.full(n_samples, 3, dtype=int)

        x_cpu = np.vstack([x_cpu_norm, x_cpu_warm, x_cpu_hot, x_cpu_fan])
        y_cpu = np.concatenate([y_cpu_norm, y_cpu_warm, y_cpu_hot, y_cpu_fan])

        self._clf_cpu = DecisionTreeClassifier(max_depth=4, random_state=42)
        self._clf_cpu.fit(x_cpu, y_cpu)

        # 2. Clasificador Eléctrico Voltaje 12V: [Voltaje] -> 0: Estable, 1: Inestable
        x_v_ok = np.random.uniform(11.45, 12.55, (n_samples, 1))
        y_v_ok = np.zeros(n_samples, dtype=int)
        x_v_low = np.random.uniform(10.0, 11.39, (n_samples // 2, 1))
        x_v_high = np.random.uniform(12.61, 13.8, (n_samples // 2, 1))
        x_v_bad = np.vstack([x_v_low, x_v_high])
        y_v_bad = np.ones(n_samples, dtype=int)

        x_volt = np.vstack([x_v_ok, x_v_bad])
        y_volt = np.concatenate([y_v_ok, y_v_bad])

        self._clf_voltaje = DecisionTreeClassifier(max_depth=3, random_state=42)
        self._clf_voltaje.fit(x_volt, y_volt)

    def discretizar_heuristica(self, datos: dict[str, float]) -> list[str]:
        """
        Discretiza valores continuos a síntomas discretos mediante reglas
        heurísticas deterministas basadas en tolerancias ATX y térmicas.
        """
        sintomas: set[str] = set()

        temp_cpu = datos.get("temperatura_cpu")
        temp_gpu = datos.get("temperatura_gpu")
        voltaje_12v = datos.get("voltaje_12v")
        fps = datos.get("fps_promedio")
        latencia_disco = datos.get("latencia_disco_ms")
        rpm_fan = datos.get("rpm_ventilador")

        # CPU y ventilador
        if temp_cpu is not None:
            if temp_cpu >= 80.0:
                sintomas.add("sobrecalentamiento")
            if temp_cpu >= 90.0:
                sintomas.add("throttling")

        if rpm_fan is not None and rpm_fan <= 0.0:
            if temp_cpu is not None and temp_cpu >= 50.0:
                sintomas.add("ventilador_no_gira")
            elif temp_cpu is None:
                sintomas.add("ventilador_no_gira")

        # GPU
        if temp_gpu is not None and temp_gpu >= 82.0:
            sintomas.add("temperatura_alta_gpu")

        # Voltaje
        if voltaje_12v is not None:
            if voltaje_12v < 11.4 or voltaje_12v > 12.6:
                sintomas.add("voltaje_inestable")
            if voltaje_12v < 10.8:
                sintomas.add("apagado_brusco")

        # FPS
        if fps is not None and fps < 30.0:
            sintomas.add("fps_bajos")

        # Latencia disco
        if latencia_disco is not None:
            if latencia_disco >= 150.0:
                sintomas.add("rendimiento_lento")
            if latencia_disco >= 600.0:
                sintomas.add("errores_io")

        return sorted(list(sintomas))

    def discretizar_ml(self, datos: dict[str, float]) -> list[str]:
        """
        Discretiza variables continuas utilizando los modelos de Scikit-Learn
        entrenados con perfiles de telemetría física.
        """
        sintomas: set[str] = set()

        # Inferencia CPU + Fan con DecisionTree
        temp_cpu = datos.get("temperatura_cpu")
        rpm_fan = datos.get("rpm_ventilador", 1500.0)
        if temp_cpu is not None and self._clf_cpu is not None:
            pred = self._clf_cpu.predict([[temp_cpu, rpm_fan]])[0]
            if pred == 1:
                sintomas.add("sobrecalentamiento")
            elif pred == 2:
                sintomas.add("sobrecalentamiento")
                sintomas.add("throttling")
            elif pred == 3:
                sintomas.add("ventilador_no_gira")
                if temp_cpu >= 80.0:
                    sintomas.add("sobrecalentamiento")

        # Inferencia Voltaje 12V con DecisionTree
        voltaje_12v = datos.get("voltaje_12v")
        if voltaje_12v is not None and self._clf_voltaje is not None:
            pred_v = self._clf_voltaje.predict([[voltaje_12v]])[0]
            if pred_v == 1:
                sintomas.add("voltaje_inestable")
            if voltaje_12v < 10.8:
                sintomas.add("apagado_brusco")

        # Fallback/complemento para variables univariadas
        temp_gpu = datos.get("temperatura_gpu")
        if temp_gpu is not None and temp_gpu >= 82.0:
            sintomas.add("temperatura_alta_gpu")

        fps = datos.get("fps_promedio")
        if fps is not None and fps < 30.0:
            sintomas.add("fps_bajos")

        latencia = datos.get("latencia_disco_ms")
        if latencia is not None:
            if latencia >= 150.0:
                sintomas.add("rendimiento_lento")
            if latencia >= 600.0:
                sintomas.add("errores_io")

        return sorted(list(sintomas))

    def discretizar(self, datos: dict[str, float], usar_ml: bool = True) -> list[str]:
        """
        Método de alto nivel: discretiza un diccionario de telemetría a hechos simbólicos.
        """
        if usar_ml and self._clf_cpu is not None:
            return self.discretizar_ml(datos)
        return self.discretizar_heuristica(datos)

    @staticmethod
    def obtener_umbrales() -> dict[str, dict]:
        """Retorna el catálogo de umbrales para presentación en la UI."""
        return UMBRALES_TELEMETRIA
