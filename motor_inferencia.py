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
import re
import unicodedata
from pathlib import Path
from typing import Optional

from pyswip import Prolog, Atom, Functor, Variable, Query
from preprocesador_numerico import PreprocesadorTelemetria

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


def normalizar_texto_a_tokens(texto: str) -> list[str]:
    """
    Normaliza un texto en lenguaje natural para la gramática DCG en Prolog:
    - Convierte a minúsculas.
    - Elimina tildes y diacríticos (á -> a, etc.).
    - Reemplaza signos de puntuación y caracteres especiales por espacios.
    - Retorna lista de palabras/tokens.
    """
    if not texto or not texto.strip():
        return []
    t_sin_acentos = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    t_limpio = t_sin_acentos.lower()
    return re.findall(r"[a-z0-9_]+", t_limpio)


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
        self._telemetria = PreprocesadorTelemetria()

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
    # Métodos de Explicabilidad y Recomendación (Entregable 2 - Caja Blanca)
    # ------------------------------------------------------------------

    def explicar_diagnostico(self, diagnostico: str, sintomas: list[str]) -> dict:
        """
        Obtiene la justificación lógica paso a paso para un diagnóstico emitido:
        - Hechos verdaderos comprobados (síntomas que unifican con el patrón)
        - Reglas disparadas en los tres niveles de inferencia (N1 -> N2 -> N3).
        """
        resultado = {
            "diagnostico": diagnostico,
            "hechos_verdaderos": [],
            "reglas_disparadas": [],
        }
        if not sintomas:
            return resultado
        try:
            q = (
                f"hechos_comprobados({diagnostico}, {self._lista_pl(sintomas)}, H), "
                f"reglas_disparadas({diagnostico}, {self._lista_pl(sintomas)}, R)"
            )
            for sol in self._prolog.query(q):
                resultado["hechos_verdaderos"] = [_atom_str(s) for s in sol.get("H", [])]
                resultado["reglas_disparadas"] = [_atom_str(r) for r in sol.get("R", [])]
                break
        except Exception as exc:
            print(f"[MotorInferencia] Error en explicar_diagnostico: {exc}")
        return resultado

    def obtener_hipotesis_descartadas(self, sintomas: list[str]) -> list[dict]:
        """
        Retorna las hipótesis evaluadas pero descartadas para la lista de síntomas dada,
        especificando si fue por exclusión mutua (\\+) o por falta de evidencia.
        """
        descartadas = []
        if not sintomas:
            return descartadas
        try:
            q = f"hipotesis_descartada({self._lista_pl(sintomas)}, Diag, Tipo, Detalle)"
            for sol in self._prolog.query(q):
                descartadas.append({
                    "diagnostico": _atom_str(sol["Diag"]),
                    "tipo": _atom_str(sol["Tipo"]),
                    "detalle": _atom_str(sol["Detalle"]),
                })
        except Exception as exc:
            print(f"[MotorInferencia] Error en obtener_hipotesis_descartadas: {exc}")
        return descartadas

    def obtener_hipotesis_parciales(self, sintomas: list[str]) -> list[dict]:
        """
        Retorna las hipótesis que presentan síntomas coincidentes pero aún no
        alcanzan el umbral de activación suficiente.
        """
        if not sintomas:
            return []
        parciales = []
        try:
            q = f"hipotesis_parcial({self._lista_pl(sintomas)}, Diag, Coinc, Falt, Tot)"
            for sol in self._prolog.query(q):
                coinc = [_atom_str(s) for s in sol.get("Coinc", [])]
                falt = [_atom_str(s) for s in sol.get("Falt", [])]
                tot = int(sol.get("Tot", 1))
                parciales.append({
                    "diagnostico": _atom_str(sol["Diag"]),
                    "coincidentes": coinc,
                    "faltantes": falt,
                    "total_requeridos": tot,
                    "progreso": round((len(coinc) / max(1, tot)) * 100, 1),
                })
        except Exception as exc:
            print(f"[MotorInferencia] Error en obtener_hipotesis_parciales: {exc}")
        return parciales

    def recomendar_siguiente_sintoma(self, sintomas: list[str]) -> Optional[dict]:
        """
        Consulta en Prolog el síntoma no ingresado que tiene mayor peso para
        desempatar o aproximar la conclusión de una hipótesis diagnóstica.
        """
        if not sintomas:
            return None
        try:
            q = f"sintoma_desempate({self._lista_pl(sintomas)}, Sugerido, Hips, Motivo)"
            for sol in self._prolog.query(q):
                return {
                    "sintoma_sugerido": _atom_str(sol["Sugerido"]),
                    "hipotesis_beneficiadas": [_atom_str(h) for h in sol.get("Hips", [])],
                    "motivo": _atom_str(sol["Motivo"]),
                }
        except Exception as exc:
            print(f"[MotorInferencia] Error en recomendar_siguiente_sintoma: {exc}")
        return None

    def obtener_catalogo_sintomas(self) -> list[str]:
        """Devuelve el catálogo completo de todos los síntomas válidos (sin duplicados)."""
        sintomas: set[str] = set()
        try:
            for sol in self._prolog.query("todos_los_sintomas(Lista)"):
                for s in sol.get("Lista", []):
                    sintomas.add(_atom_str(s))
                break
        except Exception as exc:
            print(f"[MotorInferencia] Error en obtener_catalogo_sintomas: {exc}")
        return sorted(list(sintomas))

    def obtener_sintomas_por_componente(self) -> dict[str, list[str]]:
        """Mapea cada componente de hardware con su lista de síntomas asociados."""
        mapping = {}
        try:
            for sol in self._prolog.query("componente_sintoma(Comp, Sintoma)"):
                comp = _atom_str(sol["Comp"])
                sint = _atom_str(sol["Sintoma"])
                mapping.setdefault(comp, []).append(sint)
        except Exception as exc:
            print(f"[MotorInferencia] Error en obtener_sintomas_por_componente: {exc}")
        return mapping

    def obtener_descripcion_diagnostico(self, diagnostico: str) -> str:
        """Consulta en Prolog el texto descriptivo asociado al diagnóstico."""
        try:
            for sol in self._prolog.query(f"diagnostico_describe({diagnostico}, Desc)"):
                return _atom_str(sol.get("Desc", ""))
        except Exception as exc:
            print(f"[MotorInferencia] Error en obtener_descripcion_diagnostico: {exc}")
        return ""

    # ------------------------------------------------------------------
    # Métodos de Procesamiento de Lenguaje Natural y Aprendizaje (Entregable 3)
    # ------------------------------------------------------------------

    def procesar_texto_libre(self, texto: str) -> list[str]:
        """
        Analiza un texto en lenguaje natural usando la gramática DCG de Prolog
        y extrae los síntomas simbólicos reconocidos.

        Parameters
        ----------
        texto: Cadena de texto libre ingresada por el usuario.

        Returns
        -------
        Lista de identificadores de síntomas reconocidos (sin duplicados).
        """
        tokens = normalizar_texto_a_tokens(texto)
        if not tokens:
            return []
        sintomas: list[str] = []
        try:
            q = f"extraer_sintomas_dcg({self._lista_pl(tokens)}, Sintomas)"
            for sol in self._prolog.query(q):
                raw = sol.get("Sintomas", [])
                sintomas = [_atom_str(s) for s in raw]
                break
        except Exception as exc:
            print(f"[MotorInferencia] Error en procesar_texto_libre: {exc}")
        return sintomas

    def adquirir_nuevo_diagnostico(
        self,
        id_diag: str,
        componente: str,
        severidad: str,
        sintomas: list[str],
        descripcion: str,
        persistir: bool = True,
    ) -> dict:
        """
        Inyecta en caliente un nuevo diagnóstico en la base de conocimiento Prolog
        mediante assertz/1 y lo persiste al final de base_conocimiento.pl.

        Parameters
        ----------
        id_diag:      Identificador del diagnóstico (alfanumérico snake_case).
        componente:   Componente físico afectado (ej. 'cpu', 'gpu', 'ram', etc.).
        severidad:    Nivel de severidad ('bajo', 'medio', 'alto', 'critico').
        sintomas:     Lista de síntomas que componen el patrón de falla.
        descripcion:  Texto explicativo del diagnóstico.
        persistir:    Si True, escribe las cláusulas a disco en base_conocimiento.pl.

        Returns
        -------
        Diccionario con el resultado de la operación: {'ok': bool, 'id': str, 'mensaje': str}.
        """
        # Sanitizar y normalizar identificadores a formato átomo de Prolog
        diag_clean = re.sub(r"[^a-z0-9_]", "_", id_diag.strip().lower())
        comp_clean = re.sub(r"[^a-z0-9_]", "_", componente.strip().lower())
        sev_clean = severidad.strip().lower()
        if sev_clean not in {"bajo", "medio", "alto", "critico"}:
            sev_clean = "medio"

        sintomas_limpios = [
            re.sub(r"[^a-z0-9_]", "_", s.strip().lower())
            for s in sintomas if s.strip()
        ]
        if not diag_clean or not sintomas_limpios:
            return {
                "ok": False,
                "id": diag_clean,
                "mensaje": "El ID del diagnóstico y al menos un síntoma son obligatorios.",
            }

        desc_escaped = descripcion.replace("'", "''").strip()
        if not desc_escaped:
            desc_escaped = f"Diagnostico adquirido en caliente para {comp_clean}"

        # 1. Inyección en memoria viva mediante SWI-Prolog
        try:
            q = (
                f"registrar_diagnostico_dinamico({diag_clean}, {comp_clean}, {sev_clean}, "
                f"{self._lista_pl(sintomas_limpios)}, '{desc_escaped}')"
            )
            # Consumir la consulta para efectuar el assertz; si Prolog la rechaza
            # (p. ej. patrón contradictorio, Sección 16) no se persiste nada.
            if not list(self._prolog.query(q)):
                return {
                    "ok": False,
                    "id": diag_clean,
                    "mensaje": "Prolog rechazó la regla: el patrón contiene síntomas incompatibles entre sí.",
                }
        except Exception as exc:
            return {
                "ok": False,
                "id": diag_clean,
                "mensaje": f"Error al inyectar regla en Prolog: {exc}",
            }

        # 2. Persistencia en disco (base_conocimiento.pl)
        if persistir and _KB_PATH.exists():
            try:
                content = _KB_PATH.read_text(encoding="utf-8")
                # Evitar escribir duplicados si el diagnóstico ya está persistido en el archivo
                if f"patron_falla({diag_clean}," not in content:
                    bloque_pl = (
                        f"\n%% [DINAMICO - ADQUIRIDO EN CALIENTE: {diag_clean}]\n"
                        f"patron_falla({diag_clean}, {self._lista_pl(sintomas_limpios)}).\n"
                        f"severidad_diagnostico({diag_clean}, {sev_clean}).\n"
                        f"diagnostico_describe({diag_clean}, '{desc_escaped}').\n"
                    )
                    for s in sintomas_limpios:
                        if f"componente_sintoma({comp_clean}, {s})" not in content:
                            bloque_pl += f"componente_sintoma({comp_clean}, {s}).\n"
                        if f"sintoma_valido({s})" not in content:
                            bloque_pl += f"sintoma_valido({s}).\n"

                    with open(_KB_PATH, "a", encoding="utf-8") as f:
                        f.write(bloque_pl)
            except Exception as exc:
                return {
                    "ok": True,
                    "id": diag_clean,
                    "mensaje": f"Regla inyectada en memoria pero ocurrió un error al persistir a disco: {exc}",
                }

        return {
            "ok": True,
            "id": diag_clean,
            "mensaje": f"Diagnóstico '{diag_clean}' inyectado exitosamente en memoria viva y persistido en base_conocimiento.pl.",
        }

    def obtener_diagnosticos_registrados(self) -> list[str]:
        """Devuelve la lista de todos los diagnósticos registrados en la base (estáticos y dinámicos)."""
        diags: list[str] = []
        try:
            for sol in self._prolog.query("patron_falla(Diag, _)"):
                d = _atom_str(sol["Diag"])
                if d not in diags:
                    diags.append(d)
        except Exception as exc:
            print(f"[MotorInferencia] Error en obtener_diagnosticos_registrados: {exc}")
        return sorted(diags)

    def discretizar_telemetria(
        self, datos_telemetria: dict[str, float], usar_ml: bool = True
    ) -> list[str]:
        """
        Convierte variables continuas de sensores a hechos simbólicos de síntomas.
        """
        return self._telemetria.discretizar(datos_telemetria, usar_ml=usar_ml)

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
