"""
pruebas.py
==========
Suite de pruebas para DiagnostiPC.

Ejecuta 5 casos de prueba que verifican el comportamiento del motor
de inferencia y muestran cada resultado en una tabla formateada en consola.

Casos:
  1. Diagnóstico único claro         (RAM con síntomas canónicos)
  2. Múltiples diagnósticos          (síntomas de RAM + fuente de poder)
  3. Exclusión mutua (\\+ y !)        (síntomas de enfriamiento → excluye CPU)
  4. Datos insuficientes (borde)     (síntoma único, sin diagnóstico posible)
  5. Lista vacía (borde)             (entrada vacía, manejo elegante)
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
    # truncar si excede el ancho disponible
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
            partes = [f"{r['diagnostico']} ({r['severidad']})" for r in resultado]
            return ", ".join(partes)
        return str(resultado)
    return str(resultado)


def verificar(obtenido, esperado_fn) -> tuple[bool, str]:
    """Evalúa si el resultado cumple la condición esperada."""
    ok = esperado_fn(obtenido)
    estado = f"{VERDE}PASS{RESET}" if ok else f"{ROJO}FAIL{RESET}"
    return ok, estado


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
    # Síntomas de enfriamiento puro: el patrón falla_critica_cpu TAMBIÉN
    # matchea parcialmente pero es excluido porque falla_enfriamiento lo excluye.
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
        resultado_4 == []          # sin diagnóstico con 1 síntoma
        and validos_4 == ["pantalla_azul"]  # el síntoma sí es válido
        and criticos_4 == 1        # es crítico
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
