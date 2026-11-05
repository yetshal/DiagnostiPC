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
