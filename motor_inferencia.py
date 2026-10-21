"""
motor_inferencia.py
===================
Puente Python ↔ SWI-Prolog para DiagnostiPC.

Carga la base de conocimiento Prolog y expone los predicados principales
a través de la clase MotorInferencia. Toda la lógica de inferencia reside
en base_conocimiento.pl; Python sólo convierte tipos y formatea resultados.

Dependencias:
    pip install pyswip
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pyswip import Prolog, Atom, Functor, Variable, Query

# ---------------------------------------------------------------------------
# Ruta absoluta a la base de conocimiento (misma carpeta que este módulo)
# ---------------------------------------------------------------------------
_BASE_DIR = Path(__file__).resolve().parent
_KB_PATH   = _BASE_DIR / "base_conocimiento.pl"


def _atom_str(term) -> str:
    """Convierte un término PySwip (Atom, Functor, bytes o str) a cadena Python."""
    if isinstance(term, bytes):
        return term.decode("utf-8")
    if isinstance(term, Atom):
        return str(term)
    return str(term)


def _parse_par_diag_sev(item) -> tuple[str, str]:
    """
    Extrae (diagnostico, severidad) de un elemento de la lista devuelta
    por diagnosticar_todos/3.

    PySwip puede devolver el par ``Diag-Sev`` como:
    - Un objeto ``Functor`` con ``.args[0]`` y ``.args[1]``.
    - Una cadena con formato ``'-(Diag, Sev)'`` (comportamiento en SWI-Prolog 10).

    Returns
    -------
    Tupla (diagnostico, severidad) como strings.
    """
    # Caso 1: Functor PySwip con atributo args
    if hasattr(item, "args") and len(item.args) >= 2:
        return _atom_str(item.args[0]), _atom_str(item.args[1])

    # Caso 2: string con formato '-(Diag, Sev)'
    s = _atom_str(item)
    if s.startswith("-(") and s.endswith(")"):
        interior = s[2:-1]
        partes = [p.strip() for p in interior.split(",", 1)]
        if len(partes) == 2:
            return partes[0], partes[1]

    # Fallback genérico: intentar split por '-'
    partes = s.split("-", 1)
    if len(partes) == 2:
        return partes[0].strip(), partes[1].strip()

    return s, "desconocido"


def _prolog_list(items: list[str]) -> list[Atom]:
    """Convierte una lista de strings Python en una lista de Atoms PySwip."""
    return [Atom(s) for s in items]


class MotorInferencia:
    """
    Motor de inferencia de DiagnostiPC.

    Encapsula la conexión a SWI-Prolog y expone métodos de alto nivel
    para consultar la base de conocimiento de diagnóstico de hardware.

    Ejemplo de uso::

        motor = MotorInferencia()
        resultados = motor.consultar_diagnosticos(
            ["pantalla_azul", "errores_memoria", "reinicios_aleatorios"]
        )
        for r in resultados:
            print(r["diagnostico"], r["severidad"])
    """

    def __init__(self) -> None:
        """Inicializa la instancia cargando la base de conocimiento Prolog."""
        if not _KB_PATH.exists():
            raise FileNotFoundError(f"Base de conocimiento no encontrada: {_KB_PATH}")

        self._prolog = Prolog()
        # consultar con ruta absoluta evita problemas de directorio de trabajo
        self._prolog.consult(str(_KB_PATH))

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------

    def consultar_diagnosticos(
        self,
        sintomas: list[str],
        componente: Optional[str] = None,
    ) -> list[dict]:
        """
        Llama a ``diagnosticar_todos/3`` y devuelve todos los diagnósticos
        posibles para la lista de síntomas dada.

        Parameters
        ----------
        sintomas:    Lista de síntomas (strings en español, formato átomo Prolog).
        componente:  Componente de filtro opcional (p. ej. ``'cpu'``).
                     Si es ``None`` se usa ``'cualquiera'``.

        Returns
        -------
        Lista de dicts con claves ``diagnostico`` y ``severidad``.
        Devuelve lista vacía si no hay diagnósticos posibles.
        """
        comp_atom = componente if componente is not None else "cualquiera"

        resultados: list[dict] = []
        try:
            query_str = (
                f"diagnosticar_todos({self._lista_pl(sintomas)}, "
                f"{comp_atom}, Diagnosticos)"
            )
            for sol in self._prolog.query(query_str):
                diags = sol.get("Diagnosticos", [])
                for par in diags:
                    diag, sev = _parse_par_diag_sev(par)
                    resultados.append({"diagnostico": diag, "severidad": sev})
                break  # diagnosticar_todos es determinista por diseño
        except Exception as exc:
            # Ante cualquier fallo Prolog, devolver lista vacía con log
            print(f"[MotorInferencia] Error en consultar_diagnosticos: {exc}")
        return resultados

    def validar_sintomas(self, sintomas: list[str]) -> list[str]:
        """
        Llama a ``validar_sintomas/2`` y devuelve sólo los síntomas
        reconocidos por la base de conocimiento.

        Parameters
        ----------
        sintomas: Lista de candidatos a síntoma.

        Returns
        -------
        Sub-lista con únicamente los síntomas válidos.
        """
        if not sintomas:
            return []
        validos: list[str] = []
        try:
            query_str = f"validar_sintomas({self._lista_pl(sintomas)}, Validos)"
            for sol in self._prolog.query(query_str):
                raw = sol.get("Validos", [])
                validos = [_atom_str(s) for s in raw]
                break
        except Exception as exc:
            print(f"[MotorInferencia] Error en validar_sintomas: {exc}")
        return validos

    def obtener_componente_afectado(self, sintomas: list[str]) -> list[str]:
        """
        Llama a ``componente_afectado/2`` e infiere qué componente es el
        más probable responsable de los síntomas dados.

        Parameters
        ----------
        sintomas: Lista de síntomas observados.

        Returns
        -------
        Lista con el nombre del componente (normalmente un solo elemento)
        o ``['desconocido']`` si no puede determinarse.
        """
        if not sintomas:
            return ["desconocido"]
        componentes: list[str] = []
        try:
            query_str = f"componente_afectado({self._lista_pl(sintomas)}, Componente)"
            for sol in self._prolog.query(query_str):
                comp = _atom_str(sol.get("Componente", "desconocido"))
                componentes.append(comp)
                break
        except Exception as exc:
            print(f"[MotorInferencia] Error en obtener_componente_afectado: {exc}")
        return componentes if componentes else ["desconocido"]

    def contar_sintomas_criticos(self, sintomas: list[str]) -> int:
        """
        Llama a ``conteo_sintomas_criticos/2`` y cuenta cuántos síntomas
        de la lista pertenecen a la categoría crítica.

        Parameters
        ----------
        sintomas: Lista de síntomas a evaluar.

        Returns
        -------
        Número entero de síntomas críticos presentes.
        """
        if not sintomas:
            return 0
        conteo = 0
        try:
            query_str = f"conteo_sintomas_criticos({self._lista_pl(sintomas)}, Conteo)"
            for sol in self._prolog.query(query_str):
                conteo = int(sol.get("Conteo", 0))
                break
        except Exception as exc:
            print(f"[MotorInferencia] Error en contar_sintomas_criticos: {exc}")
        return conteo

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------

    @staticmethod
    def _lista_pl(items: list[str]) -> str:
        """
        Convierte una lista Python de strings a la representación textual
        de una lista Prolog para inyectar en strings de consulta.

        Ejemplo: ``['a', 'b']``  →  ``'[a,b]'``
        """
        if not items:
            return "[]"
        atoms = ",".join(items)
        return f"[{atoms}]"
