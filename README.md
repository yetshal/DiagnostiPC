# DiagnostiPC

Sistema experto auditable ("Caja Blanca") para el diagnóstico de fallas de hardware y software en computadores personales.
**Prolog** (SWI-Prolog) contiene el 100% del conocimiento y el razonamiento lógico (inferencia, trazabilidad, explicabilidad y desempate); **Python** actúa como puente de comunicación (PySwip) e interfaz gráfica interactiva (Streamlit).

- **Asignatura:** Sistemas Expertos · Ingeniería de Software
- **Institución:** Fundación Escuela Tecnológica de Neiva (FET), sede Rivera-Huila
- **Docente:** Juan José Ramos Díaz
- **Integrantes:** Juan Carlos Bastidas Bernal & Julian Alfonso Montero Trujillo
- **Entregable Actual:** Entregable 3 — Procesamiento de Lenguaje Natural (DCG), Aprendizaje Dinámico en Caliente y Pre-procesamiento Numérico Híbrido

---

## Estado del Proyecto

- **Fase:** Entregable 3 — DCG en Prolog, Modo Experto (`assertz/1` + persistencia) y Telemetría Numérica (Scikit-Learn).
- **Implementación:** 100% operativa, conectada bidireccionalmente a SWI-Prolog y Streamlit.
- **Base de Conocimiento:** 66 hechos base estructurados, 27 reglas encadenadas en 3 niveles, analizador gramatical DCG (`extraer_sintomas_dcg/2`) y persistencia de reglas dinámicas.
- **Pruebas:** 11/11 casos de prueba pasando con éxito (100% PASS), cubriendo lenguaje natural libre, inyección en caliente en memoria viva, supervivencia de reglas tras reinicio y clasificación de telemetría de sensores.

---

## Qué hace

DiagnostiPC recibe los síntomas y observaciones reportadas por el usuario y proporciona una evaluación integral y auditable:

1. **Entrada por Lenguaje Natural con DCG (Prolog):** El usuario describe libremente las fallas en texto abierto; una gramática DCG en Prolog filtra ruido, analiza sintácticamente las frases y extrae los síntomas canónicos.
2. **Pre-procesamiento Numérico Híbrido:** Sensores continuos de hardware (temperatura CPU/GPU en °C, caídas de voltaje de riel 12V, FPS promedio, latencias de disco en ms) se discretizan a hechos simbólicos mediante un clasificador Scikit-learn (`DecisionTreeClassifier`) y heurísticas ATX.
3. **Diagnóstico Concluyente y Severidad:** Identifica el componente dominante afectado y emite diagnósticos con su nivel de criticidad (`critico`, `alto`, `medio`, `bajo`).
4. **Explicabilidad Simbólica ("¿Por qué?"):**
   - **Hechos comprobados:** Síntomas validados positivamente contra los patrones canónicos.
   - **Reglas disparadas:** Árbol secuencial de reglas activadas en 3 niveles (Nivel 1 $\to$ Nivel 2 $\to$ Nivel 3).
   - **Hipótesis descartadas:** Diagnósticos alternativos evaluados y descartados justificando el motivo (por exclusión mutua `\+` o por falta de evidencia).
5. **Módulo de Recomendación ("¿Qué falta?"):**
   - Ante evidencia incompleta o empates entre diagnósticos, Prolog evalúa las hipótesis parcialmente activas y determina qué síntoma adicional tiene mayor prioridad y peso discriminante para desempate con un clic.
6. **Modo Experto (Adquisición Dinámica en Caliente):**
   - Permite a un técnico formular nuevos diagnósticos en tiempo de ejecución.
   - Inyecta la regla en la memoria lógica viva mediante `assertz/1` (operativa al instante sin reiniciar).
   - Escribe de forma persistente la regla en `base_conocimiento.pl` para conservar el aprendizaje entre reinicios de la aplicación.

---

## Estructura del Repositorio

```
.
├── base_conocimiento.pl        # Base de conocimiento Prolog (hechos, reglas 3 niveles, DCG y persistencia)
├── preprocesador_numerico.py   # Pre-procesador híbrido de telemetría (Scikit-learn + Heurística ATX)
├── motor_inferencia.py         # Módulo puente Python ↔ SWI-Prolog vía PySwip (consultas tipadas y seguras)
├── main.py                     # Interfaz gráfica interactiva web desarrollada en Streamlit (con Modo Experto)
├── pruebas.py                  # Suite de pruebas automatizadas por consola (11 casos, 100% PASS)
├── requirements.txt            # Dependencias del proyecto (pyswip, streamlit, scikit-learn)
├── entregable_1_sistema_experto_diagnostipc.md # Documento del Entregable 1
├── docs/                       # Documentación técnica y evidencias
│   ├── entregables/            # Artefactos de entrega del curso
│   │   ├── 01-ficha-definicion.md
│   │   ├── 02-matriz-cumplimiento.md
│   │   ├── 03-diccionario-predicados.md  # Diccionario actualizado con Entregable 2
│   │   ├── 04-evidencia-pruebas.md
│   │   └── evidencia/          # Capturas de pantalla de ejecuciones y consultas
│   ├── architecture/           # Diagramas de capas, niveles de reglas y flujo
│   ├── adr/                    # Registro de Decisiones de Arquitectura (ADRs 001–006)
│   ├── product/                # Alcance, cronograma y adquisición de conocimiento
│   └── ai/                     # Contexto técnico, hoja de ruta, bitácora y estado de sesión
├── AGENTS.md                   # Reglas de oro y protocolos para agentes IA
├── CLAUDE.md                   # Instrucciones para Claude Code
└── README.md                   # Documentación principal del proyecto
```

---

## Requisitos y Configuración Rápida

### 1. Requisitos Previos

- **SWI-Prolog:** 10.0.2 o superior instalado y disponible en el `PATH` del sistema.
- **Python:** 3.10 a 3.14 (64-bit compatible con SWI-Prolog).

### 2. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

_(O utilizando un entorno virtual con `uv pip install -r requirements.txt`)_

---

## Ejecución del Sistema

### 1. Interfaz Gráfica Interactiva (Streamlit)

Para iniciar la aplicación visual en el navegador web:

```bash
streamlit run main.py
# O alternativamente:
python main.py
```

La interfaz ofrece:

- **Botón Caso 1 (Inferencia Completa y ¿Por qué?):** Carga los síntomas canónicos de RAM y expone la traza completa de reglas N1-N3, hechos comprobados e hipótesis descartadas.
- **Botón Caso 2 (Evidencia Incompleta y ¿Qué falta?):** Carga un síntoma parcial y activa la consulta de desempate en Prolog, recomendando el siguiente síntoma a inspeccionar.

### 2. Suite de Pruebas Automatizadas

Verifica los 7 casos de prueba (100% PASS):

```bash
python pruebas.py
```

### 3. Verificación Limpia de SWI-Prolog

Comprueba que la base de conocimiento compila limpiamente sin advertencias ni errores:

```bash
swipl -q -g "consult('base_conocimiento.pl')" -t halt
```

---

## Mapa de Documentación y Entregables

| Documento                      | Ubicación                                                                                                                                | Descripción                                              |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------- |
| **Ficha de Definición**        | [`01-ficha-definicion.md`](file:///C:/Users/yetshal/DevelopmentProjects/DiagnostiPC/docs/entregables/01-ficha-definicion.md)             | Integrantes, justificación como SBR y alcance.           |
| **Matriz de Cumplimiento**     | [`02-matriz-cumplimiento.md`](file:///C:/Users/yetshal/DevelopmentProjects/DiagnostiPC/docs/entregables/02-matriz-cumplimiento.md)       | Trazabilidad 100% de requisitos del curso §3 y §4.       |
| **Diccionario de Predicados**  | [`03-diccionario-predicados.md`](file:///C:/Users/yetshal/DevelopmentProjects/DiagnostiPC/docs/entregables/03-diccionario-predicados.md) | Especificación de aridades, modos (+/-) y niveles N1–N3. |
| **Evidencias y Pruebas**       | [`04-evidencia-pruebas.md`](file:///C:/Users/yetshal/DevelopmentProjects/DiagnostiPC/docs/entregables/04-evidencia-pruebas.md)           | Detalle de casos probados y capturas de terminal.        |
| **Decisiones de Arquitectura** | [`docs/adr/`](file:///C:/Users/yetshal/DevelopmentProjects/DiagnostiPC/docs/adr/)                                                        | ADR 001 a ADR 006 aceptadas y vigentes.                  |
