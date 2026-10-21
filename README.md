# DiagnostiPC

Sistema experto para el diagnóstico de fallas de hardware y software en computadores personales.
**Prolog** (SWI-Prolog) guarda todo el conocimiento y el razonamiento; **Python** solo hace de puente y de consola.

Asignatura: Sistemas Expertos · Ingeniería de Software · Fundación Escuela Tecnológica de Neiva (FET), sede Rivera-Huila.
Docente: Juan José Ramos Díaz.

> Este repositorio parte de un **paquete de documentación y plan de desarrollo** (carpeta `docs/` + `AGENTS.md`). El código aún no existe: se construye tarea por tarea siguiendo `docs/ai/04-hoja-de-ruta.md`.

## Qué hace

Recibe una lista de respuestas sobre lo que el usuario observa en su equipo (enciende o no, pitidos, imagen, temperatura, software…) y devuelve los diagnósticos probables, ordenados por **severidad ajustada** y **certeza**, cada uno con su recomendación. Si no hay evidencia suficiente, lo dice (`datos_insuficientes` / `no_concluyente`) en lugar de inventar.

## Cómo usar este paquete

1. Crea un repositorio vacío y copia en su raíz: `AGENTS.md`, `CLAUDE.md`, `README.md`, `.gitignore` y la carpeta `docs/`.
2. Lee `docs/ai/09-guia-trabajo-con-ia.md` (cómo trabajar en pareja con agentes de IA) y `docs/ai/05-estado-sesion.md` (dónde estamos).
3. Responde las **preguntas abiertas** de `05` (fecha de entrega, nombres y códigos, confirmaciones con el docente).
4. Abre una sesión con tu agente usando `docs/ai/templates/prompt-inicio-sesion.md` y trabaja **una tarea por sesión** de `04-hoja-de-ruta.md`.
5. Al cerrar cada sesión, usa `templates/prompt-cierre-sesion.md`.

## Mapa de documentación

| Carpeta / archivo        | Contenido                                                                                                                     |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `AGENTS.md`, `CLAUDE.md` | Reglas de oro y protocolos para agentes de IA                                                                                 |
| `docs/ai/`               | Contexto, arquitectura, pautas, hoja de ruta, estado, bitácora, decisiones, glosario, errores conocidos y plantillas          |
| `docs/adr/`              | Decisiones de arquitectura (ADR 001–006)                                                                                      |
| `docs/architecture/`     | Diagramas: capas, niveles de reglas, flujo de una consulta                                                                    |
| `docs/entregables/`      | Los 4 artefactos de entrega: ficha, diccionario de predicados, evidencia de pruebas y la matriz de cumplimiento de requisitos |
| `docs/product/`          | Alcance, riesgos y guía de adquisición de conocimiento (fuentes y consulta con el técnico)                                    |

## Estructura final del repositorio (objetivo)

```
.
├── base_conocimiento.pl        # hechos + reglas (un solo archivo, secciones comentadas)
├── motor_inferencia.py         # puente a SWI-Prolog: carga la base y expone funciones
├── main.py                     # consola interactiva (cuestionario + resultados)
├── pruebas.py                  # ≥ 5 casos formateados + evidencia
├── tests/tests_kb.pl           # pruebas unitarias en Prolog (plunit)
├── evidencia/                  # salida de pruebas y capturas
├── docs/                       # este paquete
├── AGENTS.md  CLAUDE.md  README.md  requirements.txt
```

## Comandos (se confirman en la tarea F0-01/F0-03)

```bash
python -m pip install -r requirements.txt           # puente (PySwip o Janus, ver ADR-002)
swipl -q -g run_tests -t halt tests/tests_kb.pl     # pruebas de la base de conocimiento
python pruebas.py                                   # casos de prueba por consola
python main.py                                      # consulta interactiva
```

## Cumplimiento de requisitos

La trazabilidad requisito → implementación → prueba está en `docs/entregables/02-matriz-cumplimiento.md`.
