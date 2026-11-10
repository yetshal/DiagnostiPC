"""Genera el informe técnico del Entregable 4 en PDF.

Herramienta de documentación, no forma parte del sistema (D-027): reportlab no
está en requirements.txt. Ejecutar desde la raíz del repositorio:

    uv run --with reportlab python docs/entregables/informe/generar_informe.py

Ejecuta las suites de pruebas y la base de conocimiento para que las cifras del
informe sean las reales del momento de generarlo.
"""
from __future__ import annotations

import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

RAIZ = Path(__file__).resolve().parents[3]
SALIDA = RAIZ / "docs" / "entregables" / "informe_tecnico_entregable4.pdf"
PY_VENV = RAIZ / ".venv" / "Scripts" / "python.exe"


def ejecutar(cmd: list[str]) -> str:
    r = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout + r.stderr


def resultados_pruebas() -> tuple[str, str, int]:
    py = str(PY_VENV) if PY_VENV.exists() else sys.executable
    salida_py = re.sub(r"\x1b\[[0-9;]*m", "", ejecutar([py, "pruebas.py"]))  # quita colores ANSI
    m = re.search(r"Resultado final:\s*(\d+)/(\d+)", salida_py)
    pruebas = f"{m.group(1)}/{m.group(2)}" if m else "no disponible"
    salida_pl = ejecutar(["swipl", "-q", "-g", "run_tests", "-t", "halt", "tests/tests_kb.pl"])
    pasadas = len(re.findall(r"passed", salida_pl))
    fallidas = len(re.findall(r"FAILED", salida_pl))
    plunit = f"{pasadas}/{pasadas + fallidas}"
    lineas_pl = sum(1 for _ in (RAIZ / "base_conocimiento.pl").open(encoding="utf-8"))
    return pruebas, plunit, lineas_pl


def estadisticas_kb() -> dict[str, int]:
    meta = (
        "consult('base_conocimiento.pl'),"
        "todos_los_sintomas(S), length(S, A),"
        "findall(D, patron_falla(D, _), Ds), sort(Ds, Du), length(Du, B),"
        "findall(x, excluye(_, _), Ex), length(Ex, C),"
        "findall(x, incompatible(_, _, _), In), length(In, I),"
        "findall(x, clause(frase_sintoma(_, _, _), _), Fr), length(Fr, F),"
        "format('~w ~w ~w ~w ~w~n', [A, B, C, I, F])"
    )
    out = ejecutar(["swipl", "-q", "-g", meta, "-t", "halt"])
    nums = [int(n) for n in re.findall(r"^(\d+) (\d+) (\d+) (\d+) (\d+)$", out, re.M)[-1]]
    return dict(zip(["sintomas", "diagnosticos", "exclusiones", "incompatibles", "frases_dcg"], nums))


# --- Estilos ----------------------------------------------------------------
est = getSampleStyleSheet()
H1 = est["Heading1"]
H2 = est["Heading2"]
N = ParagraphStyle("N", parent=est["Normal"], fontSize=10, leading=14, spaceAfter=6)
P = ParagraphStyle("P", parent=est["Normal"], fontSize=9, leading=12)
CODIGO = ParagraphStyle("C", parent=est["Code"], fontSize=8, leading=10,
                        backColor=colors.HexColor("#f4f4f4"), borderPadding=6)
AZUL = colors.HexColor("#1f3b5c")


def tabla(filas: list[list[str]], anchos: list[float]) -> Table:
    datos = [[Paragraph(c, P) for c in f] for f in filas]
    t = Table(datos, colWidths=[a * cm for a in anchos], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2f6")]),
    ]))
    return t


def encabezado_tabla(*cols: str) -> list[str]:
    return [f"<b>{c}</b>" for c in cols]


def construir() -> None:
    pruebas, plunit, lineas_pl = resultados_pruebas()
    kb = estadisticas_kb()
    hoy = dt.date.today().strftime("%d/%m/%Y")
    h: list = []

    # Portada
    h += [Spacer(1, 4 * cm),
          Paragraph("DiagnostiPC", ParagraphStyle("T", parent=est["Title"], fontSize=28, leading=36, spaceAfter=10)),
          Paragraph("Sistema experto para el diagnóstico de fallas de hardware en PC", est["Title"]),
          Spacer(1, 1 * cm),
          Paragraph("<b>Informe técnico — Entregable 4</b><br/>"
                    "Pruebas de estrés, manejo de contradicciones y auditoría cruzada",
                    ParagraphStyle("S", parent=N, alignment=1, fontSize=13, leading=18)),
          Spacer(1, 2 * cm),
          Paragraph("Juan Carlos Bastidas Bernal (Integrante A — motor simbólico)<br/>"
                    "Julian Alfonso Montero Trujillo (Integrante B — integración)<br/><br/>"
                    "Asesor: Juan José Ramos Díaz<br/>"
                    "Sistemas Expertos · Ingeniería de Software<br/>"
                    "Fundación Escuela Tecnológica de Neiva Jesús Oviedo Pérez — FET<br/>"
                    f"Rivera, Huila · {hoy}",
                    ParagraphStyle("A", parent=N, alignment=1, fontSize=11, leading=16)),
          PageBreak()]

    # 1. Resumen
    h += [Paragraph("1. Resumen", H1),
          Paragraph(
              "DiagnostiPC recibe síntomas de una computadora (marcados a mano, escritos en lenguaje "
              "natural o derivados de sensores) y concluye qué componente falla y con qué severidad. "
              "Toda la lógica vive en Prolog; Python solo captura datos y muestra resultados. "
              "En este entregable se añadió una capa de consistencia que detecta síntomas que no "
              "pueden presentarse a la vez y bloquea el diagnóstico antes de emitirlo, y se "
              "sometió el sistema a pruebas de estrés.", N),
          tabla([
              encabezado_tabla("Indicador", "Valor"),
              ["Pruebas por consola (<font face='Courier'>pruebas.py</font>)", f"{pruebas} PASS"],
              ["Pruebas unitarias Prolog (plunit)", f"{plunit} PASS"],
              ["Síntomas reconocidos", str(kb["sintomas"])],
              ["Diagnósticos (patrones de falla)", str(kb["diagnosticos"])],
              ["Exclusiones mutuas / pares incompatibles", f"{kb['exclusiones']} / {kb['incompatibles']}"],
              ["Frases de la gramática DCG", str(kb["frases_dcg"])],
              ["Líneas de <font face='Courier'>base_conocimiento.pl</font>", str(lineas_pl)],
          ], [9, 6])]

    # 2. Arquitectura
    h += [Paragraph("2. Arquitectura final", H1),
          Preformatted(
              "Usuario (navegador)                      Evaluador (consola)\n"
              "      |                                          |\n"
              "  main.py (Streamlit)                       pruebas.py\n"
              "      |  texto libre / telemetria                |\n"
              "      v                                          v\n"
              "  motor_inferencia.py  ---- PySwip ---->  SWI-Prolog: base_conocimiento.pl\n"
              "  (consultas planas, sin excepciones)     (hechos, N1-N3, DCG, explicacion,\n"
              "      |                                     consistencia, aprendizaje)\n"
              "      v\n"
              "  preprocesador_numerico.py (C, V, FPS, ms, RPM -> atomos de sintoma)", CODIGO),
          Spacer(1, 6),
          tabla([
              encabezado_tabla("Archivo", "Responsabilidad"),
              ["base_conocimiento.pl", "Conocimiento y razonamiento: hechos, reglas en 3 niveles, "
               "explicabilidad, desempate, DCG, adquisición en caliente y consistencia (Sección 16)."],
              ["motor_inferencia.py", "Puente PySwip. Un método por consulta; sanea átomos, nunca "
               "propaga excepciones y solo persiste reglas que Prolog aceptó."],
              ["preprocesador_numerico.py", "Convierte telemetría continua en síntomas: heurística por "
               "umbrales o árbol de decisión (scikit-learn)."],
              ["main.py", "Interfaz Streamlit: captura (checkboxes, texto, sensores), aviso de "
               "contradicciones, dictamen, «¿Por qué?», «¿Qué falta?» y Modo Experto."],
              ["pruebas.py / tests/tests_kb.pl", "16 casos por consola y 11 pruebas plunit."],
          ], [4.5, 11.5]),
          Spacer(1, 6),
          Paragraph("<b>Contrato.</b> La frontera solo usa átomos y listas de átomos. "
                    "<font face='Courier'>diagnosticar_todos(+Sintomas, cualquiera, -Pares)</font> devuelve "
                    "pares <font face='Courier'>Diagnostico-Severidad</font>, o <font face='Courier'>[]</font> "
                    "si la evidencia no alcanza o si la entrada es contradictoria. El motivo de una "
                    "contradicción se consulta con <font face='Courier'>par_contradictorio/4</font>.", N)]

    # 3. Árbol lógico
    h += [PageBreak(), KeepTogether([Paragraph("3. Árbol lógico principal", H1),
          Paragraph("Cada nivel solo usa niveles inferiores; la única recursión es sobre la cola de "
                    "una lista, por lo que la inferencia siempre termina.", N),
          Preformatted(
              "diagnosticar_todos(S, _, D)                          [API / Nivel 3]\n"
              "|\n"
              "+-- entrada_contradictoria(S), !  -> D = []          [Seccion 16]\n"
              "|     +-- par_contradictorio(S, A, B, Motivo)        [Nivel 1]\n"
              "|           +-- incompatible(A, B, Motivo)           [hecho]\n"
              "|           +-- memberchk(A, S), memberchk(B, S)\n"
              "|\n"
              "+-- findall(Diag-Sev, ...)\n"
              "      +-- diagnostico_posible(Diag, S, _)            [Nivel 3]\n"
              "      |     +-- patron_presente(Diag, S)             [Nivel 2]\n"
              "      |     |     +-- patron_falla(Diag, Req)        [hecho]\n"
              "      |     |     +-- lista_contiene_minimo(S, Req, max(2, |Req|-1))  [Nivel 1]\n"
              "      |     +-- tiene_sintomas_suficientes(S)        [Nivel 2]\n"
              "      |     |     +-- subconjunto_valido(S, V), |V| >= 2            [Nivel 1]\n"
              "      |     +-- \\+ diagnostico_excluido(Diag, S)     [Nivel 2]\n"
              "      |           +-- excluye(Otro, Diag)            [hecho]\n"
              "      |           +-- patron_presente(Otro, S)       [Nivel 2]\n"
              "      +-- severidad_diagnostico(Diag, Sev)           [hecho]", CODIGO)]),
          Spacer(1, 6),
          Paragraph("<b>Ejemplo.</b> Con <font face='Courier'>[pantalla_azul, errores_memoria, "
                    "reinicios_aleatorios]</font> no hay conflictos, el patrón de "
                    "<font face='Courier'>falla_ram</font> está completo y nada lo excluye: resultado "
                    "<font face='Courier'>[falla_ram-alto]</font>. Si se agrega "
                    "<font face='Courier'>no_arranca</font> y <font face='Courier'>fps_bajos</font>, "
                    "la primera rama corta la búsqueda y devuelve <font face='Courier'>[]</font>.", N),
          PageBreak()]

    # 4. Contradicciones
    h += [Paragraph("4. Manejo de contradicciones", H1),
          Paragraph("Un hecho <font face='Courier'>incompatible(A, B, Motivo)</font> declara que dos "
                    "síntomas no pueden observarse a la vez. <font face='Courier'>no_arranca</font> "
                    "significa que el equipo no enciende o no pasa del POST; los síntomas que exigen el "
                    "sistema operativo en ejecución no pueden coexistir con él.", N),
          tabla([
              encabezado_tabla("Síntoma A", "Síntoma B", "Motivo"),
              ["no_arranca", "fps_bajos", "Medir FPS exige ejecutar una aplicación gráfica."],
              ["no_arranca", "throttling", "Solo se observa con el procesador bajo carga en el SO."],
              ["no_arranca", "rendimiento_lento", "Evaluar rendimiento exige el SO en ejecución."],
          ], [3.5, 3.5, 9]),
          Spacer(1, 6),
          Paragraph("<b>Dónde se aplica el bloqueo:</b> (1) <font face='Courier'>diagnosticar_todos/3</font> "
                    "devuelve <font face='Courier'>[]</font> ante entrada contradictoria; (2) "
                    "<font face='Courier'>sintoma_desempate/4</font> no recomienda síntomas que "
                    "contradigan lo ya reportado; (3) <font face='Courier'>registrar_diagnostico_dinamico/5</font> "
                    "rechaza patrones contradictorios y Python no los escribe a disco; (4) la interfaz "
                    "muestra el motivo de cada conflicto. Los tres pares están marcados "
                    "<b>[PENDIENTE-VALIDAR]</b>: se derivan de la definición del síntoma y falta "
                    "confirmarlos con el técnico de mantenimiento.", N)]

    # 5. Pruebas de estrés
    h += [Paragraph("5. Reporte de pruebas de estrés", H1),
          tabla([
              encabezado_tabla("Caso", "Escenario", "Entrada", "Esperado", "Res."),
              ["12", "Contradicción directa", "no_arranca, pitidos_bios, puertos_usb_fallan, fps_bajos",
               "Conflicto (no_arranca, fps_bajos); sin diagnóstico aunque el patrón de placa madre está completo", "PASS"],
              ["13", "Contradicción en lenguaje natural", "«El equipo no enciende y tiene fps bajos»",
               "La DCG extrae ambos síntomas; contradictoria", "PASS"],
              ["14", "Entradas ambiguas o basura", "vacío, espacios, «asdf qwe !!! 123», «la computadora esta rara», «y y y pero ademas»",
               "Sin síntomas, sin diagnóstico, sin excepciones", "PASS"],
              ["15", "Telemetría + texto", "92 °C, 11 V, 19 FPS + «no pasa del post»",
               "Dos conflictos con no_arranca; bloqueo", "PASS"],
              ["16", "Modo Experto contradictorio", "falla_imposible = [no_arranca, throttling]",
               "Regla rechazada; archivo .pl sin cambios", "PASS"],
          ], [1.4, 3.1, 4.7, 5.5, 1.3]),
          Spacer(1, 6),
          Paragraph(f"Resultado de la suite completa al generar este informe: <b>{pruebas}</b> casos "
                    f"por consola y <b>{plunit}</b> pruebas plunit. Las pruebas plunit cubren además "
                    "el orden inverso de los síntomas, varios conflictos simultáneos, la lista vacía, "
                    "una entrada que no es lista y que el desempate no sugiera síntomas incompatibles. "
                    "El aviso de la interfaz se verificó con <font face='Courier'>streamlit.testing.v1.AppTest</font>.", N),
          Paragraph("<b>Hallazgo corregido durante las pruebas:</b> el Modo Experto escribía en "
                    "<font face='Courier'>base_conocimiento.pl</font> aunque Prolog rechazara la regla, "
                    "porque en PySwip un fallo no es una excepción. Ahora se comprueba que la consulta "
                    "tuvo solución antes de persistir.", N)]

    # 6. Limitaciones
    h += [Paragraph("6. Limitaciones conocidas", H1),
          Paragraph("• La gramática DCG no interpreta negaciones: «no se calienta» se ignora en lugar de "
                    "descartar <font face='Courier'>sobrecalentamiento</font>.<br/>"
                    "• Solo hay tres pares incompatibles y aún no están validados por el experto.<br/>"
                    "• No se modelan factores de certeza numéricos; la fuerza de la evidencia depende del "
                    "umbral de coincidencia del patrón.", N)]

    def pie(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(2 * cm, 1.2 * cm, "DiagnostiPC — Informe técnico Entregable 4")
        canvas.drawRightString(letter[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(str(SALIDA), pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm,
                            title="DiagnostiPC - Informe técnico Entregable 4",
                            author="J. C. Bastidas Bernal; J. A. Montero Trujillo")
    doc.build(h, onLaterPages=pie)
    print(f"PDF generado: {SALIDA} (pruebas {pruebas}, plunit {plunit})")


if __name__ == "__main__":
    construir()
