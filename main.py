"""
main.py
=======
DiagnostiPC — Sistema Experto de Diagnostico de Hardware PC.

Interfaz interactiva desarrollada en Streamlit conectada a SWI-Prolog
mediante PySwip. Permite evaluar sintomas observados, auditar la traza
de deduccion paso a paso ("¿Por que?") y sugerir pruebas de desempate
cuando la evidencia no es concluyente ("¿Que falta?").
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import streamlit as st
    from streamlit.web import cli as stcli
except ImportError:
    print("Error: Streamlit no esta instalado. Ejecute: pip install streamlit")
    sys.exit(1)

from motor_inferencia import MotorInferencia

# ---------------------------------------------------------------------------
# Etiquetas legibles (sin emojis)
# ---------------------------------------------------------------------------
LABELS_SINTOMAS = {
    "pantalla_azul": "Pantalla azul de error critico (BSOD)",
    "reinicios_aleatorios": "Reinicios aleatorios e inesperados",
    "sobrecalentamiento": "Sobrecalentamiento termico excesivo",
    "throttling": "Thermal Throttling (reduccion forzada de frecuencia)",
    "errores_memoria": "Errores de lectura/escritura en memoria RAM",
    "artefactos_graficos": "Artefactos visuales o glitches en pantalla",
    "pantalla_negra": "Pantalla negra / perdida de senal de video",
    "no_arranca": "El equipo no enciende o no completa el POST",
    "pitidos_bios": "Secuencia de pitidos de advertencia de la BIOS",
    "rendimiento_lento": "Rendimiento general anormalmente lento",
    "disco_no_detectado": "Unidad de almacenamiento (SSD/HDD) no detectada",
    "ruidos_disco": "Ruidos mecanicos o chasquidos en la unidad",
    "voltaje_inestable": "Voltaje inestable / caidas en las lineas de poder",
    "apagado_brusco": "Apagado subito bajo carga o reposo",
    "puertos_usb_fallan": "Puertos USB sin energia o inoperables",
    "fps_bajos": "Tasa de cuadros por segundo (FPS) severamente reducida",
    "temperatura_alta_gpu": "Temperatura excesiva en el chip grafico (GPU)",
    "errores_io": "Errores continuos de entrada/salida (I/O)",
    "corrupcion_datos": "Corrupcion de archivos del sistema operativo",
    "ventilador_no_gira": "Ventilador del disipador no gira o bloqueado",
}

LABELS_DIAGNOSTICOS = {
    "falla_critica_cpu": "Falla Critica de Procesador (CPU)",
    "falla_ram": "Falla de Memoria RAM",
    "falla_gpu": "Falla de Tarjeta Grafica (GPU)",
    "falla_disco": "Falla Critica de Almacenamiento (Disco)",
    "falla_fuente": "Falla Critica de Fuente de Poder (PSU)",
    "falla_placa_madre": "Falla Critica de Placa Madre (Motherboard)",
    "falla_enfriamiento": "Falla del Sistema de Refrigeracion",
    "degradacion_disco": "Degradacion Progresiva de Almacenamiento",
    "inestabilidad_fuente": "Inestabilidad Electrica de Fuente de Poder",
    "rendimiento_general": "Rendimiento General Degradado",
}

LABELS_COMPONENTES = {
    "cpu": "Procesador (CPU)",
    "ram": "Memoria RAM",
    "gpu": "Tarjeta Grafica (GPU)",
    "disco": "Almacenamiento (Disco / SSD)",
    "fuente": "Fuente de Poder (PSU)",
    "placa_madre": "Placa Madre (Motherboard)",
    "enfriamiento": "Sistema de Refrigeracion",
}

COLORES_SEVERIDAD = {
    "critico": ("CRITICO", "#ff4d4f"),
    "alto":    ("ALTO",    "#fa8c16"),
    "medio":   ("MEDIO",   "#fadb14"),
    "bajo":    ("BAJO",    "#52c41a"),
    "desconocido": ("INDETERMINADO", "#8c8c8c"),
}


@st.cache_resource
def get_motor() -> MotorInferencia:
    """Instancia cacheada del motor de inferencia Prolog."""
    return MotorInferencia()


# ---------------------------------------------------------------------------
# Callbacks para mutación segura de estado en Streamlit
# (Se ejecutan ANTES de la instanciación de widgets, previniendo errores)
# ---------------------------------------------------------------------------
def cb_toggle_sintoma(sintoma: str):
    """Sincroniza el checkbox marcado con la lista de sintomas seleccionados."""
    esta_marcado = st.session_state.get(f"chk_{sintoma}", False)
    if esta_marcado and sintoma not in st.session_state.sintomas_seleccionados:
        st.session_state.sintomas_seleccionados.append(sintoma)
    elif not esta_marcado and sintoma in st.session_state.sintomas_seleccionados:
        st.session_state.sintomas_seleccionados.remove(sintoma)


def cb_agregar_sintoma(sintoma: str):
    """Agrega de forma segura un sintoma desde el modulo de recomendacion."""
    if sintoma not in st.session_state.sintomas_seleccionados:
        st.session_state.sintomas_seleccionados.append(sintoma)
    st.session_state[f"chk_{sintoma}"] = True


def cb_limpiar_sintomas(catalogo: list[str]):
    """Desmarca todos los checkboxes y limpia la lista activa."""
    st.session_state.sintomas_seleccionados = []
    for s in catalogo:
        st.session_state[f"chk_{s}"] = False


def cb_aplicar_sintomas_extra(nuevos_sintomas: list[str]):
    """Incorpora una lista de síntomas a los seleccionados y sincroniza sus checkboxes."""
    for s in nuevos_sintomas:
        if s not in st.session_state.sintomas_seleccionados:
            st.session_state.sintomas_seleccionados.append(s)
        st.session_state[f"chk_{s}"] = True


def cb_interpretar_dcg():
    """Callback seguro para analizar texto libre con DCG antes de instanciar widgets."""
    texto = st.session_state.get("input_texto_nl", "").strip()
    if not texto:
        st.session_state["feedback_dcg"] = ("info", "Por favor escriba una descripción antes de analizar.")
        return
    motor = get_motor()
    sintomas = motor.procesar_texto_libre(texto)
    if sintomas:
        for s in sintomas:
            if s not in st.session_state.sintomas_seleccionados:
                st.session_state.sintomas_seleccionados.append(s)
            st.session_state[f"chk_{s}"] = True
        st.session_state["feedback_dcg"] = ("success", f"DCG reconoció: {', '.join(sintomas)}")
    else:
        st.session_state["feedback_dcg"] = ("warning", "No se identificaron síntomas reconocibles en el texto.")


def cb_aplicar_telemetria():
    """Callback seguro para discretizar telemetría numérica antes de instanciar widgets."""
    t_cpu = float(st.session_state.get("in_t_cpu", 45.0))
    t_gpu = float(st.session_state.get("in_t_gpu", 50.0))
    v_12v = float(st.session_state.get("in_v_12v", 12.0))
    fps = float(st.session_state.get("in_fps", 65.0))
    lat = float(st.session_state.get("in_lat", 15.0))
    rpm = float(st.session_state.get("in_rpm", 1500.0))
    usar_ml = bool(st.session_state.get("in_usar_ml", True))

    datos = {
        "temperatura_cpu": t_cpu,
        "temperatura_gpu": t_gpu,
        "voltaje_12v": v_12v,
        "fps_promedio": fps,
        "latencia_disco_ms": lat,
        "rpm_ventilador": rpm,
    }
    motor = get_motor()
    sintomas = motor.discretizar_telemetria(datos, usar_ml=usar_ml)
    if sintomas:
        for s in sintomas:
            if s not in st.session_state.sintomas_seleccionados:
                st.session_state.sintomas_seleccionados.append(s)
            st.session_state[f"chk_{s}"] = True
        st.session_state["feedback_tele"] = ("success", f"Telemetría discretizada: {', '.join(sintomas)}")
    else:
        st.session_state["feedback_tele"] = ("info", "Valores dentro de los parámetros normales de funcionamiento.")


def render_app():
    st.set_page_config(
        page_title="DiagnostiPC",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    motor = get_motor()
    todos_sintomas = list(dict.fromkeys(motor.obtener_catalogo_sintomas()))

    if "sintomas_seleccionados" not in st.session_state:
        st.session_state.sintomas_seleccionados = []

    # Inicializar claves de checkboxes en session_state si no existen
    for s in todos_sintomas:
        if f"chk_{s}" not in st.session_state:
            st.session_state[f"chk_{s}"] = (s in st.session_state.sintomas_seleccionados)

    # -----------------------------------------------------------------------
    # Barra Lateral (Sidebar): 100% Dedicada a Seleccion y Busqueda de Sintomas
    # -----------------------------------------------------------------------
    with st.sidebar:
        st.subheader("Seleccion de Sintomas")

        # Buscador / filtro interactivo superior (fijo)
        filtro = st.text_input(
            "Buscar sintoma:",
            placeholder="Filtrar por nombre...",
            label_visibility="collapsed",
            key="filtro_sintomas",
        )

        col_c1, col_c2 = st.columns([0.55, 0.45])
        with col_c1:
            st.caption(f"Activos: {len(st.session_state.sintomas_seleccionados)}")
        with col_c2:
            st.button(
                "Limpiar",
                use_container_width=True,
                on_click=cb_limpiar_sintomas,
                args=(todos_sintomas,),
            )

        st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);'/>", unsafe_allow_html=True)

        # Filtrar lista de sintomas segun el texto ingresado
        f_txt = filtro.strip().lower()
        if f_txt:
            sintomas_a_mostrar = [
                s for s in todos_sintomas
                if f_txt in s.lower()
                or f_txt in LABELS_SINTOMAS.get(s, "").lower()
            ]
        else:
            sintomas_a_mostrar = todos_sintomas

        sintomas_a_mostrar = list(dict.fromkeys(sintomas_a_mostrar))

        # Contenedor con scroll vertical que ocupa el resto del sidebar
        with st.container(height=580):
            if not sintomas_a_mostrar:
                st.caption("No se encontraron sintomas coincidentes.")
            else:
                for s in sintomas_a_mostrar:
                    st.checkbox(
                        f"{s} — {LABELS_SINTOMAS.get(s, s)}",
                        key=f"chk_{s}",
                        on_change=cb_toggle_sintoma,
                        args=(s,),
                    )

    # -----------------------------------------------------------------------
    # Area Principal
    # -----------------------------------------------------------------------
    st.header("DiagnostiPC")
    st.caption("Sistema Experto de Diagnostico de Hardware PC")

    sintomas_activos = st.session_state.sintomas_seleccionados

    # Resumen visual de sintomas activos
    if sintomas_activos:
        st.markdown("##### Sintomas ingresados:")
        pills_html = " ".join([
            f"<span style='background-color:#1f2937;color:#93c5fd;padding:4px 10px;border-radius:12px;margin:2px;font-size:13px;border:1px solid #374151;display:inline-block;'>[+] {s}</span>"
            for s in sintomas_activos
        ])
        st.markdown(pills_html, unsafe_allow_html=True)
    else:
        st.info("No se ha seleccionado ningun sintoma. Marque los sintomas observados en la barra lateral para comenzar.")

    st.markdown("---")

    # -----------------------------------------------------------------------
    # Módulos Híbridos de Entrada: Lenguaje Natural (DCG) y Telemetría Numérica
    # -----------------------------------------------------------------------
    col_input_a, col_input_b = st.columns(2)

    with col_input_a:
        with st.expander("Entrada por Lenguaje Natural con DCG (Prolog)", expanded=False):
            st.caption(
                "Escriba libremente los problemas que presenta el equipo. "
                "La gramática DCG de Prolog extraerá los hechos canónicos automáticamente."
            )
            st.text_area(
                "Descripción libre del problema:",
                placeholder="Ejemplo: La máquina se calienta mucho, la pantalla se congela y se reinicia sola...",
                height=85,
                key="input_texto_nl",
            )
            st.button(
                "Interpretar con Gramática DCG",
                use_container_width=True,
                type="primary",
                on_click=cb_interpretar_dcg,
            )
            fb_dcg = st.session_state.get("feedback_dcg")
            if fb_dcg:
                tipo, msg = fb_dcg
                if tipo == "success":
                    st.success(msg)
                elif tipo == "warning":
                    st.warning(msg)
                elif tipo == "info":
                    st.info(msg)

    with col_input_b:
        with st.expander("Telemetría Numérica de Sensores (Pre-procesador Híbrido)", expanded=False):
            st.caption(
                "Inyecte mediciones continuas de hardware para que el clasificador "
                "las convierta a hechos simbólicos discretos."
            )
            c_t1, c_t2 = st.columns(2)
            with c_t1:
                st.number_input("Temp. CPU (°C):", min_value=25.0, max_value=115.0, value=45.0, step=1.0, key="in_t_cpu")
                st.number_input("Temp. GPU (°C):", min_value=25.0, max_value=115.0, value=50.0, step=1.0, key="in_t_gpu")
                st.number_input("Riel 12V (V):", min_value=9.0, max_value=14.0, value=12.0, step=0.1, key="in_v_12v")
            with c_t2:
                st.number_input("FPS Promedio:", min_value=0.0, max_value=360.0, value=65.0, step=5.0, key="in_fps")
                st.number_input("Latencia Disco (ms):", min_value=0.1, max_value=2000.0, value=15.0, step=5.0, key="in_lat")
                st.number_input("RPM Ventilador:", min_value=0.0, max_value=4000.0, value=1500.0, step=100.0, key="in_rpm")

            st.checkbox("Utilizar Clasificador Scikit-Learn (DecisionTree)", value=True, key="in_usar_ml")
            st.button(
                "Clasificar Telemetría a Síntomas",
                use_container_width=True,
                on_click=cb_aplicar_telemetria,
            )
            fb_tele = st.session_state.get("feedback_tele")
            if fb_tele:
                tipo, msg = fb_tele
                if tipo == "success":
                    st.success(msg)
                elif tipo == "info":
                    st.info(msg)

    st.markdown("---")

    # Ejecucion de inferencia en Prolog
    diagnosticos = motor.consultar_diagnosticos(sintomas_activos)
    componente_afectado = motor.obtener_componente_afectado(sintomas_activos)
    descartadas = motor.obtener_hipotesis_descartadas(sintomas_activos)
    parciales = motor.obtener_hipotesis_parciales(sintomas_activos)
    recomendacion = motor.recomendar_siguiente_sintoma(sintomas_activos)

    # Pestanas de trabajo
    tab_diag, tab_por_que, tab_que_falta, tab_experto = st.tabs([
        "Dictamen y Diagnosticos",
        "Modulo de Explicabilidad (\"¿Por que?\")",
        "Modulo de Recomendacion (\"¿Que falta?\")",
        "Modo Experto (Adquisición Dinámica)",
    ])

    # -----------------------------------------------------------------------
    # TAB 1: Dictamen y Diagnósticos
    # -----------------------------------------------------------------------
    with tab_diag:
        if diagnosticos:
            comp_cod = componente_afectado[0] if componente_afectado else "desconocido"
            comp_txt = LABELS_COMPONENTES.get(comp_cod, comp_cod.upper())
            st.markdown(f"**Componente de hardware dominante afectado:** `{comp_txt}`")
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            cols = st.columns(len(diagnosticos) if len(diagnosticos) <= 3 else 3)
            for idx, d in enumerate(diagnosticos):
                col = cols[idx % len(cols)]
                diag_id = d["diagnostico"]
                sev_id = d["severidad"]
                etiqueta_sev, color_hex = COLORES_SEVERIDAD.get(sev_id, COLORES_SEVERIDAD["desconocido"])
                desc_prolog = motor.obtener_descripcion_diagnostico(diag_id)
                nombre_diag = LABELS_DIAGNOSTICOS.get(diag_id, diag_id)

                with col:
                    st.markdown(
                        f"""
                        <div style="border: 2px solid {color_hex}; border-radius: 10px; padding: 15px; margin-bottom: 15px; background: rgba(255,255,255,0.03);">
                            <h4 style="margin:0; color:#ffffff;">{nombre_diag}</h4>
                            <p style="margin:5px 0 8px 0; font-size:12px; color:#aaa;">ID: <code>{diag_id}</code></p>
                            <span style="background:{color_hex}22; color:{color_hex}; border:1px solid {color_hex}; padding:3px 8px; border-radius:6px; font-weight:bold; font-size:11px;">
                                {etiqueta_sev}
                            </span>
                            <p style="margin:12px 0 0 0; font-size:13px; color:#cccccc; line-height:1.4;">
                                {desc_prolog}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            if not sintomas_activos:
                st.info("Marque sintomas en la barra lateral para evaluar el equipo.")
            else:
                st.warning(
                    "Evidencia insuficiente o no concluyente.\n\n"
                    "Los sintomas provistos no alcanzan el umbral para emitir un diagnostico definitivo. "
                    "Consulte la pestana 'Modulo de Recomendacion' para ver las hipotesis parciales "
                    "y el sintoma sugerido para desempate."
                )

    # -----------------------------------------------------------------------
    # TAB 2: Módulo de Explicabilidad ("¿Por qué?")
    # -----------------------------------------------------------------------
    with tab_por_que:
        st.subheader("Auditoria de Inferencia Logica (Caja Blanca)")
        st.write(
            "Detalle transparente de hechos comprobados, reglas logicas disparadas "
            "y motivos de exclusion o descarte de hipotesis alternativas."
        )

        if not sintomas_activos:
            st.info("Sin sintomas seleccionados para auditar.")
        else:
            if diagnosticos:
                for d in diagnosticos:
                    diag_id = d["diagnostico"]
                    explicacion = motor.explicar_diagnostico(diag_id, sintomas_activos)
                    nombre_diag = LABELS_DIAGNOSTICOS.get(diag_id, diag_id)

                    with st.expander(f"Justificacion logica: {nombre_diag} ({diag_id})", expanded=True):
                        # 1. Hechos comprobados
                        st.markdown("##### 1. Hechos Comprobados como Verdaderos")
                        hechos = explicacion.get("hechos_verdaderos", [])
                        if hechos:
                            for h in hechos:
                                st.markdown(f"- **`{h}`**: {LABELS_SINTOMAS.get(h, h)} (Unificado positivamente con el patron de falla)")
                        else:
                            st.write("No se unificaron hechos directos.")

                        # 2. Reglas disparadas
                        st.markdown("##### 2. Reglas Disparadas (Secuencia Jerarquica N1 a N3)")
                        reglas = explicacion.get("reglas_disparadas", [])
                        if reglas:
                            for r in reglas:
                                if "Nivel 1" in r:
                                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;[Nivel 1] `{r}`")
                                elif "Nivel 2" in r:
                                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;[Nivel 2] `{r}`")
                                elif "Nivel 3" in r:
                                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;[Nivel 3] **`{r}`**")
                                else:
                                    st.markdown(f"- `{r}`")
                        else:
                            st.write("No se registraron reglas intermedias.")

            # 3. Hipótesis alternativas descartadas
            st.markdown("##### 3. Hipotesis Alternativas Evaluadas y Descartadas")
            if descartadas:
                for desc in descartadas:
                    d_diag = desc["diagnostico"]
                    d_tipo = desc["tipo"]
                    d_detalle = desc["detalle"]
                    d_nombre = LABELS_DIAGNOSTICOS.get(d_diag, d_diag)
                    tipo_badge = "Exclusion Mutua" if d_tipo == "exclusion_mutua" else "Falta de Evidencia"

                    st.markdown(
                        f"""
                        <div style="border-left: 3px solid #ff7875; padding-left: 10px; margin-bottom: 8px;">
                            <strong>{d_nombre}</strong> (<code>{d_diag}</code>) — <em>[{tipo_badge}]</em><br/>
                            <span style="font-size: 13px; color: #bbb;">{d_detalle}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No hubo hipotesis concurrentes que requirieran descarte explicito.")

    # -----------------------------------------------------------------------
    # TAB 3: Módulo de Recomendación ("¿Qué falta?")
    # -----------------------------------------------------------------------
    with tab_que_falta:
        st.subheader("Modulo de Recomendacion y Desempate")
        st.write(
            "Cuando la evidencia no es concluyente o varias hipotesis compiten, Prolog "
            "evalua los sintomas faltantes y determina cual tiene el mayor peso para desempatar."
        )

        if not sintomas_activos:
            st.info("Para evaluar hipotesis y activar el modulo de recomendacion de desempate, marque al menos un sintoma en la barra lateral.")
        elif recomendacion and recomendacion.get("sintoma_sugerido"):
            sug = recomendacion["sintoma_sugerido"]
            mot = recomendacion["motivo"]
            sug_nombre = LABELS_SINTOMAS.get(sug, sug)

            st.markdown(
                f"""
                <div style="background: rgba(24, 144, 255, 0.1); border: 2px solid #1890ff; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                    <h4 style="margin: 0 0 8px 0; color: #69c0ff;">Sintoma Recomendado para Desempatar / Confirmar:</h4>
                    <h3 style="margin: 0 0 10px 0; color: #ffffff;">{sug_nombre} (<code>{sug}</code>)</h3>
                    <p style="margin: 0; color: #d9d9d9;"><strong>Fundamento en Prolog:</strong> {mot}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Botón interactivo con callback seguro
            if sug not in st.session_state.sintomas_seleccionados:
                st.button(
                    f"Incorporar '{sug}' a la consulta",
                    type="primary",
                    on_click=cb_agregar_sintoma,
                    args=(sug,),
                )
            else:
                st.success(f"El sintoma `{sug}` ya esta incorporado a la consulta actual.")
        else:
            st.info("No se requieren preguntas de desempate en el estado actual.")

        st.markdown("---")
        st.markdown("##### Hipotesis Parcialmente Activas en Competencia:")
        if parciales:
            for p in parciales:
                diag = p["diagnostico"]
                coinc = p["coincidentes"]
                falt = p["faltantes"]
                progreso = p["progreso"]
                tot = p["total_requeridos"]
                nombre_p = LABELS_DIAGNOSTICOS.get(diag, diag)

                st.markdown(f"**{nombre_p}** (`{diag}`)")
                st.progress(progreso / 100.0, text=f"Evidencia: {len(coinc)}/{tot} ({progreso}%)")
                st.caption(f"Observados: {coinc} | Faltan por verificar: {falt}")
                st.markdown("<br/>", unsafe_allow_html=True)
        else:
            if sintomas_activos:
                st.caption("No hay hipotesis con coincidencia parcial pendiente.")

    # -----------------------------------------------------------------------
    # TAB 4: Modo Experto (Adquisición Dinámica de Conocimiento)
    # -----------------------------------------------------------------------
    with tab_experto:
        st.subheader("Panel de Adquisición Dinámica de Conocimiento (Modo Experto)")
        st.write(
            "Permite a un técnico especialista formular nuevas reglas o diagnósticos "
            "e inyectarlos en caliente en la memoria lógica mediante `assertz/1`, "
            "escribiéndolos de forma persistente en `base_conocimiento.pl`."
        )

        with st.form("form_modo_experto"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                id_nuevo = st.text_input(
                    "ID del Diagnóstico (snake_case):",
                    placeholder="ej. falla_pasta_termica",
                    help="Identificador átomo de Prolog sin espacios ni tildes",
                )
                comp_nuevo = st.selectbox(
                    "Componente físico afectado:",
                    ["cpu", "gpu", "ram", "disco", "fuente", "placa_madre", "enfriamiento"],
                )
                sev_nueva = st.selectbox(
                    "Nivel de severidad:",
                    ["bajo", "medio", "alto", "critico"],
                    index=1,
                )
            with col_f2:
                sintomas_nuevos = st.multiselect(
                    "Síntomas que componen el patrón de falla:",
                    todos_sintomas,
                    help="Seleccione los síntomas requeridos para activar el nuevo diagnóstico",
                )
                persistir_disco = st.checkbox(
                    "Escribir persistentemente a base_conocimiento.pl",
                    value=True,
                    help="Si está activo, la regla se conservará tras reiniciar el programa.",
                )

            desc_nueva = st.text_area(
                "Descripción técnica y recomendación:",
                placeholder="Explique la causa raíz y las medidas de remediación recomendadas...",
                height=80,
            )

            btn_guardar = st.form_submit_button(
                "Inyectar y Persistir Diagnóstico",
                type="primary",
                use_container_width=True,
            )

            if btn_guardar:
                if not id_nuevo.strip():
                    st.error("Debe ingresar un ID para el diagnóstico.")
                elif not sintomas_nuevos:
                    st.error("Debe seleccionar al menos un síntoma para el patrón.")
                else:
                    res = motor.adquirir_nuevo_diagnostico(
                        id_diag=id_nuevo,
                        componente=comp_nuevo,
                        severidad=sev_nueva,
                        sintomas=sintomas_nuevos,
                        descripcion=desc_nueva,
                        persistir=persistir_disco,
                    )
                    if res.get("ok"):
                        st.success(res["mensaje"])
                        LABELS_DIAGNOSTICOS[res["id"]] = id_nuevo.replace("_", " ").title()
                    else:
                        st.error(res["mensaje"])

        st.markdown("---")
        st.markdown("##### Catálogo de Diagnósticos Registrados en la Base de Conocimiento:")
        diags_actuales = motor.obtener_diagnosticos_registrados()
        cols_d = st.columns(3)
        for i, d in enumerate(diags_actuales):
            with cols_d[i % 3]:
                st.markdown(f"- `{d}` ({LABELS_DIAGNOSTICOS.get(d, d)})")


def main():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
    except Exception:
        ctx = None

    if ctx is not None:
        render_app()
    else:
        print("Iniciando servidor Streamlit para DiagnostiPC...")
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())


if __name__ == "__main__":
    main()
