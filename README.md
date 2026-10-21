# DiagnostiPC

Sistema experto para el diagnóstico de fallas de hardware y software en computadores personales.
**Prolog** (SWI-Prolog) contiene el 100% del conocimiento y el razonamiento lógico; **Python** actúa exclusivamente como puente de comunicación e interfaz de consola.

- **Asignatura:** Sistemas Expertos · Ingeniería de Software
- **Institución:** Fundación Escuela Tecnológica de Neiva (FET), sede Rivera-Huila
- **Docente:** Juan José Ramos Díaz
- **Integrantes:** Juan Carlos Bastidas Bernal & Julian Alfonso Montero Trujillo

---

## Estado del Proyecto

- **Fase:** F4 — Cierre de Entregables y Documentación Completa.
- **Implementación:** 100% operativa y probada.
- **Base de Conocimiento:** 66 hechos estructurados (aridad 2) y 17 reglas encadenadas en 3 niveles estrictos.
- **Pruebas:** 5/5 casos de prueba pasando con éxito (100% PASS) y evidencias fotográficas integradas.

---

## Qué hace

DiagnostiPC recibe un conjunto de síntomas y observaciones reportadas por el usuario (pantalla azul, ruidos extraños, sobrecalentamiento, reinicios aleatorios, artefactos gráficos, etc.) y genera un diagnóstico estructurado:

1. **Identifica el componente dominante** afectado (CPU, RAM, GPU, Almacenamiento, Fuente, Placa Base, Refrigeración).
2. **Genera diagnósticos específicos** asociados con su nivel de **severidad** (`bajo`, `medio`, `alto`, `critico`).
3. **Aplica reglas de exclusión mutua** mediante corte (`!`) y negación por fallo (`\+`) para descartar diagnósticos incompatibles.
4. **Maneja casos borde** con robustez (listas vacías o datos insuficientes no lanzan excepciones ni fallan, devolviendo estados consistentes).

---

## Estructura del Repositorio

```
.
├── base_conocimiento.pl        # Base de conocimiento Prolog (66 hechos, 17 reglas en 3 niveles)
├── motor_inferencia.py         # Módulo puente Python ↔ SWI-Prolog vía PySwip
├── pruebas.py                  # Suite de pruebas automatizadas por consola (5 casos, 100% PASS)
├── entregable_1_sistema_experto_diagnostipc.md # Documento del Entregable 1
├── docs/                       # Documentación técnica y evidencias
│   ├── entregables/            # Los 4 artefactos de entrega + evidencias fotográficas
│   │   ├── 01-ficha-definicion.md
│   │   ├── 02-matriz-cumplimiento.md
│   │   ├── 03-diccionario-predicados.md
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

## Requisitos y Entorno de Ejecución

- **SWI-Prolog:** 10.0.2 o superior (agregado al `PATH` del sistema).
- **Python:** 3.10 a 3.14.
- **PySwip:** 0.3.3 (`pip install pyswip`).

---

## Comandos de Ejecución y Verificación

### 1. Ejecutar la Suite de Pruebas Automatizada (Python)

Ejecuta los 5 casos de prueba obligatorios (normales, exclusión, datos insuficientes y lista vacía):

```bash
python pruebas.py
# o en Windows si python apunta al launcher:
py pruebas.py
```

### 2. Verificar la Base de Conocimiento en SWI-Prolog

Comprueba que la base de conocimiento compila limpiamente sin advertencias ni errores:

```bash
swipl -q -g "consult('base_conocimiento.pl')" -t halt
```

### 3. Consultar Directamente en Consola Prolog

```bash
swipl -q base_conocimiento.pl
```

Ejemplo de consulta interactiva:

```prolog
?- diagnosticar_todos([pantalla_azul, errores_memoria, reinicios_aleatorios], cualquiera, Diags).
Diags = [falla_ram-alto].
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
