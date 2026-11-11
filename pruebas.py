"""
pruebas.py
==========
Suite de pruebas para DiagnostiPC (Entregables 1, 2 y 3).

Ejecuta 11 casos de prueba que verifican:
  1. Diagnóstico único claro         (RAM con síntomas canónicos)
  2. Múltiples diagnósticos          (síntomas de RAM + fuente de poder)
  3. Exclusión mutua (\\+ y !)        (síntomas de enfriamiento → excluye CPU)
  4. Datos insuficientes (borde)     (síntoma único, sin diagnóstico posible)
  5. Lista vacía (borde)             (entrada vacía, manejo elegante)
  6. Explicabilidad "¿Por qué?"      (hechos verdaderos, reglas N1-N3 y descartes)
  7. Recomendación "¿Qué falta?"     (hipótesis parciales y síntoma de desempate)
  8. DCG - Lenguaje Natural          (extracción sintáctica de síntomas con DCG)
  9. Adquisición Dinámica Caliente   (inyección en memoria viva con assertz/1)
  10. Persistencia de Reglas         (supervivencia de reglas tras reinicio limpio)
  11. Telemetría Numérica Híbrida    (variables continuas a hechos simbólicos)
"""

from __future__ import annotations

from pathlib import Path

from motor_inferencia import MotorInferencia

# ---------------------------------------------------------------------------
# Constantes de presentación
# ---------------------------------------------------------------------------
ANCHO = 60
LINEA_DOBLE_TOP  = "╔" + "═" * ANCHO + "╗"
LINEA_DOBLE_MID  = "╠" + "═" * ANCHO + "╣"
LINEA_DOBLE_BOT  = "╚" + "═" * ANCHO + "╝"
LINEA_SIMPLE     = "╟" + "─" * ANCHO + "╢"

VERDE  = "\033[92m"
ROJO   = "\033[91m"
RESET  = "\033[0m"


def fila(etiqueta: str, valor: str) -> str:
    """Formatea una fila de tabla con etiqueta y valor."""
    contenido = f"  {etiqueta:<11}: {valor}"
    max_val = ANCHO - 14
    if len(valor) > max_val:
        valor = valor[: max_val - 3] + "..."
        contenido = f"  {etiqueta:<11}: {valor}"
    padding = ANCHO - len(contenido)
    return f"║{contenido}{' ' * padding}║"


def encabezado(n: int, titulo: str) -> str:
    """Formatea la fila de encabezado del caso."""
    texto = f"  CASO {n}: {titulo}"
    padding = ANCHO - len(texto)
    return f"║{texto}{' ' * padding}║"


def resultado_str(resultado) -> str:
    """Convierte resultado a cadena legible."""
    if isinstance(resultado, list):
        if not resultado:
            return "[]"
        if isinstance(resultado[0], dict):
            if "diagnostico" in resultado[0] and "severidad" in resultado[0]:
                partes = [f"{r['diagnostico']} ({r['severidad']})" for r in resultado]
                return ", ".join(partes)
            if "diagnostico" in resultado[0] and "tipo" in resultado[0]:
                partes = [f"{r['diagnostico']}:{r['tipo']}" for r in resultado]
                return ", ".join(partes)
        return str(resultado)
    return str(resultado)


def imprimir_caso(
    n: int,
    titulo: str,
    objetivo: str,
    entrada: str,
    consulta: str,
    esperado: str,
    obtenido,
    ok: bool,
) -> None:
    """Imprime el bloque formateado de un caso de prueba."""
    estado = f"{VERDE}✔ PASS{RESET}" if ok else f"{ROJO}✘ FAIL{RESET}"
    print(LINEA_DOBLE_TOP)
    print(encabezado(n, titulo))
    print(LINEA_DOBLE_MID)
    print(fila("Objetivo", objetivo))
    print(fila("Entrada", entrada))
    print(fila("Consulta", consulta))
    print(fila("Esperado", esperado))
    print(fila("Obtenido", resultado_str(obtenido)))
    print(fila("Estado", estado))
    print(LINEA_DOBLE_BOT)
    print()


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n" + "=" * 62)
    print("   DiagnostiPC — Suite de Pruebas del Motor de Inferencia")
    print("=" * 62 + "\n")

    motor = MotorInferencia()
    total = 0
    pasados = 0

    # -----------------------------------------------------------------------
    # CASO 1: Diagnóstico Único Claro
    # -----------------------------------------------------------------------
    total += 1
    sintomas_1 = ["pantalla_azul", "errores_memoria", "reinicios_aleatorios"]
    resultado_1 = motor.consultar_diagnosticos(sintomas_1)
    ok_1 = (
        len(resultado_1) == 1
        and resultado_1[0]["diagnostico"] == "falla_ram"
        and resultado_1[0]["severidad"] == "alto"
    )
    if ok_1:
        pasados += 1
    imprimir_caso(
        n=1,
        titulo="Diagnóstico Único Claro",
        objetivo="Tres síntomas canónicos de RAM → un solo diagnóstico falla_ram (alto)",
        entrada=str(sintomas_1),
        consulta="consultar_diagnosticos(sintomas)",
        esperado="[falla_ram (alto)]",
        obtenido=resultado_1,
        ok=ok_1,
    )

    # -----------------------------------------------------------------------
    # CASO 2: Múltiples Diagnósticos / Recolección con findall
    # -----------------------------------------------------------------------
    total += 1
    sintomas_2 = [
        "pantalla_azul", "errores_memoria", "reinicios_aleatorios",
        "voltaje_inestable", "apagado_brusco",
    ]
    resultado_2 = motor.consultar_diagnosticos(sintomas_2)
    diagnosticos_2 = {r["diagnostico"] for r in resultado_2}
    ok_2 = (
        len(resultado_2) >= 2
        and "falla_ram"    in diagnosticos_2
        and "falla_fuente" in diagnosticos_2
    )
    if ok_2:
        pasados += 1
    imprimir_caso(
        n=2,
        titulo="Múltiples Diagnósticos / Recolección",
        objetivo="Síntomas de RAM y fuente → al menos 2 diagnósticos distintos (findall)",
        entrada=str(sintomas_2),
        consulta="consultar_diagnosticos(sintomas)",
        esperado="falla_ram + falla_fuente (al menos 2 diagnósticos)",
        obtenido=resultado_2,
        ok=ok_2,
    )

    # -----------------------------------------------------------------------
    # CASO 3: Exclusión mutua (\+ y !)
    # -----------------------------------------------------------------------
    total += 1
    sintomas_3 = ["sobrecalentamiento", "ventilador_no_gira", "throttling"]
    resultado_3 = motor.consultar_diagnosticos(sintomas_3)
    diagnosticos_3 = {r["diagnostico"] for r in resultado_3}
    ok_3 = (
        "falla_enfriamiento" in diagnosticos_3
        and "falla_critica_cpu" not in diagnosticos_3
    )
    if ok_3:
        pasados += 1
    imprimir_caso(
        n=3,
        titulo="Exclusión Mutua (\\+ y !)",
        objetivo="Síntomas de enfriamiento: falla_enfriamiento excluye falla_critica_cpu",
        entrada=str(sintomas_3),
        consulta="consultar_diagnosticos(sintomas)",
        esperado="falla_enfriamiento presente, falla_critica_cpu AUSENTE",
        obtenido=resultado_3,
        ok=ok_3,
    )

    # -----------------------------------------------------------------------
    # CASO 4: Datos Insuficientes (Borde)
    # -----------------------------------------------------------------------
    total += 1
    sintomas_4 = ["pantalla_azul"]
    resultado_4 = motor.consultar_diagnosticos(sintomas_4)
    validos_4   = motor.validar_sintomas(sintomas_4)
    criticos_4  = motor.contar_sintomas_criticos(sintomas_4)
    ok_4 = (
        resultado_4 == []
        and validos_4 == ["pantalla_azul"]
        and criticos_4 == 1
    )
    if ok_4:
        pasados += 1
    imprimir_caso(
        n=4,
        titulo="Datos Insuficientes (Borde)",
        objetivo="Un solo síntoma: sin diagnóstico, pero síntoma validado y contado",
        entrada=str(sintomas_4),
        consulta="consultar_diagnosticos + validar_sintomas + contar_criticos",
        esperado="diagnósticos=[], válidos=[pantalla_azul], críticos=1",
        obtenido=f"diags={resultado_4}, válidos={validos_4}, críticos={criticos_4}",
        ok=ok_4,
    )

    # -----------------------------------------------------------------------
    # CASO 5: Lista Vacía (Borde)
    # -----------------------------------------------------------------------
    total += 1
    sintomas_5 = []
    resultado_5   = motor.consultar_diagnosticos(sintomas_5)
    validos_5     = motor.validar_sintomas(sintomas_5)
    componente_5  = motor.obtener_componente_afectado(sintomas_5)
    criticos_5    = motor.contar_sintomas_criticos(sintomas_5)
    ok_5 = (
        resultado_5  == []
        and validos_5    == []
        and componente_5 == ["desconocido"]
        and criticos_5   == 0
    )
    if ok_5:
        pasados += 1
    imprimir_caso(
        n=5,
        titulo="Lista Vacía (Borde)",
        objetivo="Entrada vacía: todos los predicados devuelven vacío/desconocido",
        entrada="[]",
        consulta="todos los predicados con entrada vacía",
        esperado="diags=[], válidos=[], componente=desconocido, críticos=0",
        obtenido=f"diags={resultado_5}, válidos={validos_5}, comp={componente_5}, críticos={criticos_5}",
        ok=ok_5,
    )

    # -----------------------------------------------------------------------
    # CASO 6: Explicabilidad "¿Por qué?" (Entregable 2)
    # -----------------------------------------------------------------------
    total += 1
    sintomas_6 = ["pantalla_azul", "errores_memoria", "reinicios_aleatorios"]
    exp_6 = motor.explicar_diagnostico("falla_ram", sintomas_6)
    descartadas_6 = motor.obtener_hipotesis_descartadas(sintomas_6)
    descartados_nombres = {d["diagnostico"] for d in descartadas_6}
    ok_6 = (
        len(exp_6["hechos_verdaderos"]) == 3
        and any("Nivel 1" in r for r in exp_6["reglas_disparadas"])
        and any("Nivel 2" in r for r in exp_6["reglas_disparadas"])
        and any("Nivel 3" in r for r in exp_6["reglas_disparadas"])
        and "falla_critica_cpu" in descartados_nombres
    )
    if ok_6:
        pasados += 1
    imprimir_caso(
        n=6,
        titulo="Explicabilidad '¿Por qué?' (Caja Blanca)",
        objetivo="Auditar traza: 3 hechos verdaderos, reglas N1->N3 y descarte de CPU",
        entrada=str(sintomas_6),
        consulta="explicar_diagnostico + obtener_hipotesis_descartadas",
        esperado="3 hechos, reglas N1-N3 activas, falla_critica_cpu descartada",
        obtenido=f"hechos={len(exp_6['hechos_verdaderos'])}, reglas={len(exp_6['reglas_disparadas'])}, descartadas={len(descartadas_6)}",
        ok=ok_6,
    )

    # -----------------------------------------------------------------------
    # CASO 7: Recomendación de Desempate "¿Qué falta?" (Entregable 2)
    # -----------------------------------------------------------------------
    total += 1
    sintomas_7 = ["sobrecalentamiento"]
    parciales_7 = motor.obtener_hipotesis_parciales(sintomas_7)
    recom_7 = motor.recomendar_siguiente_sintoma(sintomas_7)
    parciales_nombres = {p["diagnostico"] for p in parciales_7}
    ok_7 = (
        "falla_critica_cpu" in parciales_nombres
        and "falla_enfriamiento" in parciales_nombres
        and recom_7 is not None
        and recom_7["sintoma_sugerido"] == "throttling"
    )
    if ok_7:
        pasados += 1
    sug_str = f"{recom_7['sintoma_sugerido']} ({recom_7['motivo']})" if recom_7 else "None"
    # -----------------------------------------------------------------------
    # CASO 8: Procesamiento de Lenguaje Natural con DCG (Entregable 3)
    # -----------------------------------------------------------------------
    total += 1
    texto_8 = "El equipo presenta sobrecalentamiento excesivo, la pantalla se pone azul y se reinicia sola"
    sintomas_dcg_8 = motor.procesar_texto_libre(texto_8)
    diags_dcg_8 = motor.consultar_diagnosticos(sintomas_dcg_8)
    ok_8 = (
        "sobrecalentamiento" in sintomas_dcg_8
        and "pantalla_azul" in sintomas_dcg_8
        and "reinicios_aleatorios" in sintomas_dcg_8
        and any(d["diagnostico"] == "falla_ram" for d in diags_dcg_8)
    )
    if ok_8:
        pasados += 1
    imprimir_caso(
        n=8,
        titulo="Entrada Lenguaje Natural con DCG (Prolog)",
        objetivo="Texto libre con ruido y conectores → DCG extrae síntomas y emite diagnóstico",
        entrada=f"\"{texto_8}\"",
        consulta="procesar_texto_libre + consultar_diagnosticos",
        esperado="síntomas=[sobrecalentamiento, pantalla_azul, reinicios_aleatorios] → falla_ram",
        obtenido=f"síntomas={sintomas_dcg_8}, diags={[d['diagnostico'] for d in diags_dcg_8]}",
        ok=ok_8,
    )

    # -----------------------------------------------------------------------
    # CASO 9: Adquisición Dinámica de Conocimiento en Caliente (Entregable 3)
    # -----------------------------------------------------------------------
    total += 1
    id_test_9 = "falla_pasta_termica"
    res_inyeccion_9 = motor.adquirir_nuevo_diagnostico(
        id_diag=id_test_9,
        componente="cpu",
        severidad="alto",
        sintomas=["sobrecalentamiento", "throttling"],
        descripcion="Degradacion termica por pasta seca o disipador mal fijado.",
        persistir=False,
    )
    # Inferencia inmediata en memoria viva
    diags_9 = motor.consultar_diagnosticos(["sobrecalentamiento", "throttling"])
    diags_ids_9 = {d["diagnostico"] for d in diags_9}
    ok_9 = (
        res_inyeccion_9.get("ok") is True
        and id_test_9 in diags_ids_9
    )
    if ok_9:
        pasados += 1
    imprimir_caso(
        n=9,
        titulo="Adquisición Dinámica en Caliente (assertz)",
        objetivo="Inyectar nueva regla en memoria viva → inferencia inmediata sin reiniciar",
        entrada="id=falla_pasta_termica, sev=alto, síntomas=[sobrecalentamiento, throttling]",
        consulta="adquirir_nuevo_diagnostico + consultar_diagnosticos([sobrec., thrott.])",
        esperado="falla_pasta_termica incorporada inmediatamente en la inferencia",
        obtenido=f"inyectado={res_inyeccion_9.get('ok')}, diagnósticos={[d['diagnostico'] for d in diags_9]}",
        ok=ok_9,
    )

    # -----------------------------------------------------------------------
    # CASO 10: Persistencia de Conocimiento a Disco (Entregable 3)
    # -----------------------------------------------------------------------
    total += 1
    id_test_10 = "falla_vrm_placa"
    res_inyeccion_10 = motor.adquirir_nuevo_diagnostico(
        id_diag=id_test_10,
        componente="placa_madre",
        severidad="critico",
        sintomas=["voltaje_inestable", "apagado_brusco"],
        descripcion="Falla en modulo regulador de voltaje (VRM) de la placa madre.",
        persistir=True,
    )

    # Instanciar un motor limpio para comprobar que la regla persiste tras reinicio
    motor_nuevo = MotorInferencia()
    diags_10 = motor_nuevo.consultar_diagnosticos(["voltaje_inestable", "apagado_brusco"])
    diags_ids_10 = {d["diagnostico"] for d in diags_10}

    ok_10 = (
        res_inyeccion_10.get("ok") is True
        and id_test_10 in diags_ids_10
    )
    if ok_10:
        pasados += 1

    imprimir_caso(
        n=10,
        titulo="Persistencia de Conocimiento (.pl en Disco)",
        objetivo="Inyectar regla persistente → verificar que sobrevive a una nueva instancia limpia",
        entrada="id=falla_vrm_placa, persistir=True, síntomas=[voltaje_inestable, apagado_brusco]",
        consulta="MotorInferencia().consultar_diagnosticos(...) en instancia reiniciada",
        esperado="falla_vrm_placa persiste y es diagnosticada tras recargar la base",
        obtenido=f"instancia_nueva_diags={[d['diagnostico'] for d in diags_10]}",
        ok=ok_10,
    )

    # -----------------------------------------------------------------------
    # CASO 11: Pre-procesamiento Numérico Híbrido (Entregable 3)
    # -----------------------------------------------------------------------
    total += 1
    telemetria_11 = {
        "temperatura_cpu": 93.0,
        "voltaje_12v": 11.0,
        "fps_promedio": 19.0,
        "latencia_disco_ms": 25.0,
    }
    sintomas_num_11 = motor.discretizar_telemetria(telemetria_11, usar_ml=True)
    diags_num_11 = motor.consultar_diagnosticos(sintomas_num_11)
    ok_11 = (
        "sobrecalentamiento" in sintomas_num_11
        and "throttling" in sintomas_num_11
        and "voltaje_inestable" in sintomas_num_11
        and "fps_bajos" in sintomas_num_11
        and len(diags_num_11) > 0
    )
    if ok_11:
        pasados += 1
    imprimir_caso(
        n=11,
        titulo="Pre-procesamiento Numérico Híbrido (ML)",
        objetivo="Variables continuas (°C, V, FPS) → Clasificador Scikit-Learn discretiza a síntomas",
        entrada=str(telemetria_11),
        consulta="discretizar_telemetria(usar_ml=True) + consultar_diagnosticos",
        esperado="[fps_bajos, sobrecalentamiento, throttling, voltaje_inestable] → diagnósticos activos",
        obtenido=f"sintomas={sintomas_num_11}, diags={[d['diagnostico'] for d in diags_num_11]}",
        ok=ok_11,
    )

    # -----------------------------------------------------------------------
    # CASOS 12-16: Pruebas de estrés y contradicciones (Entregable 4)
    # -----------------------------------------------------------------------
    def ids(diags: list[dict]) -> list[str]:
        return [d["diagnostico"] for d in diags]

    # CASO 12: contradicción directa en la entrada manual
    total += 1
    entrada_12 = ["no_arranca", "pitidos_bios", "puertos_usb_fallan", "fps_bajos"]
    cons_12 = motor.verificar_consistencia(entrada_12)
    diags_12 = motor.consultar_diagnosticos(entrada_12)
    ok_12 = (
        cons_12["estado"] == "contradictoria"
        and [(c["a"], c["b"]) for c in cons_12["conflictos"]] == [("no_arranca", "fps_bajos")]
        and diags_12 == []
    )
    pasados += ok_12
    imprimir_caso(
        n=12,
        titulo="Contradicción Directa (Bloqueo)",
        objetivo="Patrón completo de placa madre + síntoma imposible → se bloquea el diagnóstico",
        entrada=str(entrada_12),
        consulta="verificar_consistencia + consultar_diagnosticos",
        esperado="contradictoria, conflicto (no_arranca, fps_bajos), diagnósticos=[]",
        obtenido=f"{cons_12['estado']}, {[(c['a'], c['b']) for c in cons_12['conflictos']]}, diags={ids(diags_12)}",
        ok=ok_12,
    )

    # CASO 13: contradicción escrita en lenguaje natural (DCG)
    total += 1
    texto_13 = "El equipo no enciende y tiene fps bajos"
    sint_13 = motor.procesar_texto_libre(texto_13)
    cons_13 = motor.verificar_consistencia(sint_13)
    ok_13 = sorted(sint_13) == ["fps_bajos", "no_arranca"] and cons_13["estado"] == "contradictoria"
    pasados += ok_13
    imprimir_caso(
        n=13,
        titulo="Contradicción por Lenguaje Natural (DCG)",
        objetivo="La DCG extrae dos síntomas incompatibles → Prolog los detecta",
        entrada=repr(texto_13),
        consulta="procesar_texto_libre + verificar_consistencia",
        esperado="[no_arranca, fps_bajos] → contradictoria",
        obtenido=f"{sint_13} → {cons_13['estado']}",
        ok=ok_13,
    )

    # CASO 14: entradas ambiguas, vacías o basura en la DCG (auditoría cruzada)
    total += 1
    textos_14 = ["", "   ", "asdf qwe !!! 123", "la computadora esta rara", "y y y pero ademas"]
    try:
        salidas_14 = []
        for t in textos_14:
            s = motor.procesar_texto_libre(t)
            salidas_14.append((s, motor.verificar_consistencia(s)["estado"], ids(motor.consultar_diagnosticos(s))))
        ok_14 = all(s == [] and e == "consistente" and d == [] for s, e, d in salidas_14)
        obtenido_14 = str(salidas_14)
    except Exception as exc:  # cualquier excepción es un fallo de robustez
        ok_14 = False
        obtenido_14 = f"EXCEPCION {type(exc).__name__}: {exc}"
    pasados += ok_14
    imprimir_caso(
        n=14,
        titulo="Entradas Ambiguas o Basura en la DCG",
        objetivo="Texto vacío, ruido o vago → sin síntomas, sin diagnóstico y sin excepciones",
        entrada=str(textos_14),
        consulta="procesar_texto_libre + verificar_consistencia + consultar_diagnosticos",
        esperado="[] / consistente / [] para cada texto",
        obtenido=obtenido_14,
        ok=ok_14,
    )

    # CASO 15: combinación no prevista entre telemetría y texto
    total += 1
    sint_15 = sorted(set(motor.discretizar_telemetria(telemetria_11, usar_ml=True))
                     | set(motor.procesar_texto_libre("no pasa del post")))
    cons_15 = motor.verificar_consistencia(sint_15)
    diags_15 = motor.consultar_diagnosticos(sint_15)
    pares_15 = sorted((c["a"], c["b"]) for c in cons_15["conflictos"])
    ok_15 = (
        cons_15["estado"] == "contradictoria"
        and pares_15 == [("no_arranca", "fps_bajos"), ("no_arranca", "throttling")]
        and diags_15 == []
    )
    pasados += ok_15
    imprimir_caso(
        n=15,
        titulo="Telemetría + Texto Incompatibles",
        objetivo="Sensores en ejecución (FPS, throttling) + usuario dice que no arranca → bloqueo",
        entrada=f"telemetría caso 11 + 'no pasa del post' → {sint_15}",
        consulta="discretizar_telemetria + procesar_texto_libre + verificar_consistencia",
        esperado="contradictoria, 2 conflictos con no_arranca, diagnósticos=[]",
        obtenido=f"{cons_15['estado']}, {pares_15}, diags={ids(diags_15)}",
        ok=ok_15,
    )

    # CASO 16: el Modo Experto rechaza un patrón contradictorio sin tocar el .pl
    total += 1
    kb_path = Path(__file__).resolve().parent / "base_conocimiento.pl"
    kb_antes = kb_path.read_text(encoding="utf-8")
    res_16 = motor.adquirir_nuevo_diagnostico(
        id_diag="falla_imposible",
        componente="cpu",
        severidad="alto",
        sintomas=["no_arranca", "throttling"],
        descripcion="Patrón contradictorio de prueba",
        persistir=True,
    )
    ok_16 = res_16["ok"] is False and kb_path.read_text(encoding="utf-8") == kb_antes
    pasados += ok_16
    imprimir_caso(
        n=16,
        titulo="Modo Experto Rechaza Regla Contradictoria",
        objetivo="Un patrón con síntomas incompatibles no entra en memoria ni en disco",
        entrada="id=falla_imposible, síntomas=[no_arranca, throttling]",
        consulta="adquirir_nuevo_diagnostico(persistir=True)",
        esperado="ok=False y base_conocimiento.pl sin cambios",
        obtenido=f"ok={res_16['ok']}, archivo_intacto={kb_path.read_text(encoding='utf-8') == kb_antes}",
        ok=ok_16,
    )

    # -----------------------------------------------------------------------
    # CASO 17: el Modo Experto crea un síntoma nuevo y la barra lateral lo lista
    # -----------------------------------------------------------------------
    total += 1
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(Path(__file__).resolve().parent / "main.py"), default_timeout=30)
    app.run()
    form_inputs = [w for w in app.text_input if w.label.startswith("ID del Diagn")]
    form_inputs[0].input("falla_bobina_prueba")
    [w for w in app.text_input if w.label.startswith("Síntomas nuevos")][0].input("ruido_bobina_prueba")
    [w for w in app.checkbox if w.label.startswith("Escribir persistentemente")][0].uncheck()
    [b for b in app.button if b.label.startswith("Inyectar")][0].click()
    app.run()
    claves = {c.key for c in app.checkbox}
    ok_17 = not app.exception and "chk_ruido_bobina_prueba" in claves
    pasados += ok_17
    imprimir_caso(
        n=17,
        titulo="Modo Experto Crea Síntoma Nuevo",
        objetivo="Un síntoma escrito en el formulario aparece en la lista lateral",
        entrada="id=falla_bobina_prueba, síntomas nuevos=ruido_bobina_prueba",
        consulta="AppTest(main.py) → enviar formulario (persistir=False)",
        esperado="checkbox chk_ruido_bobina_prueba presente, sin excepción",
        obtenido=f"presente={'chk_ruido_bobina_prueba' in claves}, excepcion={bool(app.exception)}",
        ok=ok_17,
    )

    # CASO 18: borrar un diagnóstico adquirido (Prolog + archivo) sobre una copia del .pl
    # -----------------------------------------------------------------------
    total += 1
    import shutil
    import tempfile
    import motor_inferencia as _mi

    kb_real = _mi._KB_PATH
    with tempfile.TemporaryDirectory() as tmp:
        kb_copia = Path(tmp) / "base_conocimiento.pl"
        shutil.copy(kb_real, kb_copia)
        _mi._KB_PATH = kb_copia
        try:
            m18 = motor  # misma instancia: PySwip comparte un único motor Prolog
            reg = m18.adquirir_nuevo_diagnostico(
                "falla_borrable_prueba", "cpu", "alto", ["ruido_borrable_prueba", "throttling"], "prueba"
            )
            en_disco = "falla_borrable_prueba" in kb_copia.read_text(encoding="utf-8")
            res_base = m18.eliminar_diagnostico("falla_ram")
            res_del = m18.eliminar_diagnostico("falla_borrable_prueba")
            texto_final = kb_copia.read_text(encoding="utf-8")
            ok_18 = (
                reg["ok"] and en_disco
                and not res_base["ok"] and "falla_ram" in m18.obtener_diagnosticos_registrados()
                and res_del["ok"]
                and "falla_borrable_prueba" not in m18.obtener_diagnosticos_registrados()
                and "ruido_borrable_prueba" not in m18.obtener_catalogo_sintomas()
                and "falla_borrable_prueba" not in texto_final
                and "ruido_borrable_prueba" not in texto_final
                and "throttling" in m18.obtener_catalogo_sintomas()
            )
        finally:
            _mi._KB_PATH = kb_real
    pasados += ok_18
    imprimir_caso(
        n=18,
        titulo="Modo Experto Borra Diagnóstico Adquirido",
        objetivo="Se borra lo adquirido (memoria, síntoma huérfano y archivo); lo base se rechaza",
        entrada="registrar falla_borrable_prueba; eliminar falla_borrable_prueba y falla_ram",
        consulta="eliminar_diagnostico (copia temporal de base_conocimiento.pl)",
        esperado="adquirido eliminado de memoria y archivo; falla_ram rechazada",
        obtenido=f"base_rechazada={not res_base['ok']}, eliminado={res_del['ok']}, ok={ok_18}",
        ok=ok_18,
    )

    # CASO 19: botón de borrado en Streamlit (borra lo creado en el caso 17)
    # -----------------------------------------------------------------------
    total += 1
    app.run()
    app.checkbox(key="chk_confirmar_borrado").check()
    app.run()
    sel = app.selectbox(key="sel_borrar_experto")
    sel.select("falla_bobina_prueba")
    app.run()
    app.button(key="btn_borrar_experto").click()
    app.run()
    claves_19 = {c.key for c in app.checkbox}
    ok_19 = not app.exception and "chk_ruido_bobina_prueba" not in claves_19
    pasados += ok_19
    imprimir_caso(
        n=19,
        titulo="Botón Eliminar del Modo Experto",
        objetivo="Confirmar y eliminar quita el diagnóstico y su síntoma de la barra lateral",
        entrada="selectbox=falla_bobina_prueba + confirmación",
        consulta="AppTest(main.py) → botón «Eliminar diagnóstico»",
        esperado="checkbox chk_ruido_bobina_prueba ausente, sin excepción",
        obtenido=f"ausente={'chk_ruido_bobina_prueba' not in claves_19}, excepcion={bool(app.exception)}",
        ok=ok_19,
    )

    # -----------------------------------------------------------------------
    # Resumen final
    # -----------------------------------------------------------------------
    print("=" * 62)
    color = VERDE if pasados == total else ROJO
    print(f"  Resultado final: {color}{pasados}/{total} pruebas pasadas{RESET}")
    print("=" * 62 + "\n")

    if pasados < total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
