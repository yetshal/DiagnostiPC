# 02 · Arquitectura de referencia

> Fuente de verdad técnica. Si el código y este documento difieren, **se detiene el trabajo y se pregunta al humano**.
> Reescrito el 2026-11-10 (F7-04) a partir del código real tras los Entregables 1–4. El diseño inicial (pares `Var-Valor`, FC numéricos, `Estado` en `diagnosticar_todos/3`) no se implementó; queda en el historial de Git.
> Diagramas: `docs/architecture/README.md`. Firmas exactas: `docs/entregables/03-diccionario-predicados.md`.

## 1. Vista general

```
Usuario (navegador)                        Evaluador (consola)
   │                                           │
   ▼                                           ▼
main.py (Streamlit)                        pruebas.py
   │   texto libre ─┐   telemetría ─┐          │
   ▼                ▼               ▼          ▼
motor_inferencia.py ──────────────────────► PySwip ──► SWI-Prolog
 (puente: arma consultas planas,            base_conocimiento.pl
  convierte resultados a dict/list)         (hechos, reglas N1–N3, DCG,
   │                                          explicabilidad, consistencia,
   ▼                                          adquisición en caliente)
preprocesador_numerico.py
 (°C, V, FPS, ms, RPM → átomos de síntoma)
```

- **Prolog decide:** inferencia, exclusiones, consistencia, explicación, desempate y análisis del lenguaje natural (DCG).
- **Python presenta:** tokeniza texto, discretiza telemetría, llama predicados y muestra resultados. No contiene reglas de diagnóstico.
- Sin base de datos ni red. La única escritura a disco es el Modo Experto, que agrega cláusulas al final del `.pl` (D-024).

## 2. Componentes

| Archivo                      | Responsabilidad                                                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `base_conocimiento.pl`       | Todo el conocimiento y el razonamiento (un solo archivo, secciones numeradas; §4)                                  |
| `motor_inferencia.py`        | Clase `MotorInferencia`: carga la base y expone un método por consulta (§5). Nunca propaga excepciones             |
| `preprocesador_numerico.py`  | `PreprocesadorTelemetria`: heurística por umbrales (ATX, especificaciones térmicas) o `DecisionTreeClassifier` (D-025) |
| `main.py`                    | Interfaz Streamlit (D-021): barra lateral de síntomas, texto libre, telemetría; 4 pestañas (dictamen, «¿Por qué?», «¿Qué falta?», Modo Experto) |
| `pruebas.py`                 | 16 casos por consola (objetivo, entrada, consulta, esperado, obtenido); sale con código 1 si alguno falla         |
| `tests/tests_kb.pl`          | Pruebas plunit de Prolog (hoy: consistencia de la entrada)                                                         |

## 3. Estructura del repositorio

```
.
├── base_conocimiento.pl
├── motor_inferencia.py
├── preprocesador_numerico.py
├── main.py
├── pruebas.py
├── tests/tests_kb.pl
├── requirements.txt
├── docs/                      # ai/, adr/, entregables/ (evidencia/ con capturas), product/, architecture/
├── AGENTS.md  CLAUDE.md  README.md  .gitignore
```

Estructura plana a propósito: el docente ejecuta los scripts desde la raíz (D-009).

## 4. Organización de `base_conocimiento.pl`

Los predicados de hechos son `dynamic` y `discontiguous` porque el Modo Experto agrega cláusulas al final del archivo (D-024).

| Sección    | Contenido                                     | Predicados principales                                                                   |
| ---------- | --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 1–5        | Hechos base                                   | `sintoma_valido/1`, `componente_sintoma/2`, `patron_falla/2`, `severidad_diagnostico/2`, `excluye/2`, `sintoma_critico/1` |
| Nivel 1    | Validación preliminar                         | `sintoma_en_lista/2`, `lista_contiene_minimo/3`, `subconjunto_valido/2`, `es_sintoma_critico/1` |
| Nivel 2    | Inferencia intermedia                         | `patron_presente/2`, `componente_sospechoso/2`, `diagnostico_excluido/2`, `tiene_sintomas_suficientes/1`, `componente_dominante/2` |
| Nivel 3    | Conclusión                                    | `diagnostico_posible/3`, `diagnosticar_todos/3`, `severidad_caso/2`, `componente_afectado/2` |
| Utilidades | Listas y textos                               | `validar_sintomas/2`, `conteo_sintomas_criticos/2`, `todos_los_sintomas/1`, `diagnostico_describe/2` |
| 11         | Explicabilidad («¿Por qué?»)                  | `hechos_comprobados/3`, `reglas_disparadas/3`, `hipotesis_descartada(s)/4,2`              |
| 12         | Recomendación («¿Qué falta?»)                 | `hipotesis_parcial(es)/5,2`, `sintoma_desempate/4`                                       |
| 13         | Lenguaje natural (DCG)                        | `extraer_sintomas_dcg/2`, `frase_sintoma//1`, `conector_opcional//0`                      |
| 14         | Adquisición en caliente                       | `registrar_diagnostico_dinamico/5`                                                       |
| 16         | Consistencia de la entrada (Entregable 4)     | `incompatible/3`, `par_contradictorio/4`, `contradicciones/2`, `estado_consistencia/2`    |
| 15 (final) | Cláusulas persistidas por el Modo Experto     | Bloques `%% [DINAMICO - ADQUIRIDO EN CALIENTE: id]`; siempre al final del archivo        |

## 5. Contrato Python ↔ Prolog (fronteras planas)

**Entrada:** una lista de átomos de síntoma, p. ej. `[pantalla_azul, errores_memoria, reinicios_aleatorios]`. Sale de los checkboxes, de `extraer_sintomas_dcg/2` o de `PreprocesadorTelemetria`.

**Consultas principales**

| Python (`MotorInferencia`)          | Prolog                                         | Devuelve a Python                                  |
| ----------------------------------- | ---------------------------------------------- | -------------------------------------------------- |
| `consultar_diagnosticos(s)`         | `diagnosticar_todos(S, cualquiera, D)`         | `[{'diagnostico', 'severidad'}]`; `[]` si no hay evidencia suficiente o la entrada es contradictoria |
| `verificar_consistencia(s)`         | `estado_consistencia/2` + `par_contradictorio/4` | `{'estado': 'consistente'|'contradictoria', 'conflictos': [{'a','b','motivo'}]}` |
| `explicar_diagnostico(d, s)`        | `hechos_comprobados/3`, `reglas_disparadas/3`  | dict con hechos y reglas por nivel                 |
| `obtener_hipotesis_descartadas(s)`  | `hipotesis_descartada/4`                       | `[{'diagnostico','tipo','detalle'}]`               |
| `obtener_hipotesis_parciales(s)`    | `hipotesis_parcial/5`                          | lista de dicts                                     |
| `recomendar_siguiente_sintoma(s)`   | `sintoma_desempate/4`                          | dict o `None`                                      |
| `procesar_texto_libre(t)`           | `extraer_sintomas_dcg/2`                       | lista de síntomas (`[]` ante texto vacío o ruido)  |
| `adquirir_nuevo_diagnostico(...)`   | `registrar_diagnostico_dinamico/5`             | `{'ok','id','mensaje'}`; solo persiste si Prolog aceptó |
| `eliminar_diagnostico(id)`          | `eliminar_diagnostico_dinamico/1`              | `{'ok','id','mensaje'}`; solo borra lo marcado `diagnostico_adquirido/1`, luego quita el bloque del `.pl` |
| `discretizar_telemetria(d)`         | — (Python, `preprocesador_numerico.py`)        | lista de síntomas                                  |

**Reglas del puente**

1. Los átomos se sanitizan a `[a-z0-9_]` antes de construir la consulta; el texto libre se tokeniza en Python y se analiza en Prolog, nunca se inserta tal cual.
2. Se consultan predicados con variables planas (átomos, listas de átomos); los términos compuestos se evitan en la frontera.
3. Una consulta con efectos (`assertz`) debe comprobar que tuvo solución antes de continuar (E-003).
4. Toda excepción del puente se captura en `motor_inferencia.py`; el usuario nunca ve un traceback.
5. Prolog no imprime; solo devuelve datos.

## 6. Razonamiento en tres niveles

```prolog
% Nivel 1: condición elemental sobre la lista
lista_contiene_minimo(Lista, Requeridos, N) :-
    include(contiene_sintoma(Lista), Requeridos, Presentes),
    length(Presentes, Cuenta), Cuenta >= N.

% Nivel 2: el patrón de una falla está presente (usa Nivel 1)
patron_presente(Patron, Lista) :-
    patron_falla(Patron, Sintomas), length(Sintomas, Total),
    Minimo is max(2, Total - 1),
    lista_contiene_minimo(Lista, Sintomas, Minimo).

% Nivel 3: diagnóstico (usa Nivel 2)
diagnostico_posible(Patron, Lista, _) :-
    patron_presente(Patron, Lista),
    tiene_sintomas_suficientes(Lista),
    \+ diagnostico_excluido(Patron, Lista).
```

Dependencias estrictamente descendentes (N3 → N2 → N1 → hechos). La única recursión es sobre la cola de una lista (`subconjunto_valido/2`, `max_par/2`, la DCG), así que siempre termina.

## 7. Severidad y orden

- La severidad es un hecho por diagnóstico (`severidad_diagnostico/2`: `bajo`, `medio`, `alto`, `critico`); `severidad_caso/2` devuelve `desconocido` si falta.
- No hay factores de certeza numéricos; la fuerza de la evidencia se expresa con el umbral de `patron_presente/2` y con `sintoma_critico/1`.
- `sintoma_desempate/4` pondera los síntomas faltantes: +50 si es crítico, +10 a +40 según la severidad de cada hipótesis que ayuda, y +20 por hipótesis.

## 8. Dónde aparece cada requisito técnico

| Requisito                     | Mecanismo                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Listas                        | `subconjunto_valido/2`, `lista_contiene_minimo/3`, `include/3`, `subtract/3`, `list_to_set/2`                |
| Corte `!`                     | `subconjunto_valido/2`, `severidad_caso/2`, `max_par/2`, `extraer_sintomas_dcg/2`, `diagnosticar_todos/3` (bloqueo por contradicción), `estado_consistencia/2` |
| Negación `\+`                 | `diagnostico_posible/3` (exclusión mutua), `hipotesis_parcial/5`, `sintoma_desempate/4`, `registrar_diagnostico_dinamico/5` |
| `findall`                     | `diagnosticar_todos/3`, `hipotesis_descartadas/2`, `contradicciones/2`                                       |
| Severidad                     | `severidad_diagnostico/2`, `severidad_caso/2`, `peso_severidad/2`                                            |
| Explicabilidad (E2)           | Sección 11 + pestaña «¿Por qué?»                                                                             |
| DCG (E3)                      | Sección 13                                                                                                   |
| Aprendizaje en caliente (E3)  | Sección 14 + persistencia en `motor_inferencia.py`                                                           |
| Contradicciones (E4)          | Sección 16 + aviso en `main.py` + casos 12–16                                                                |

## 9. Estados de error y manejo

| Situación                                       | Dónde se detecta                         | Resultado                                                  |
| ----------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------- |
| `base_conocimiento.pl` no existe                | `MotorInferencia.__init__`               | `FileNotFoundError` con la ruta (antes de abrir la interfaz) |
| Síntoma fuera de catálogo                       | Prolog (`subconjunto_valido/2`)          | Se ignora para el conteo de evidencia                      |
| Lista vacía o menos de 2 síntomas válidos       | Prolog (`tiene_sintomas_suficientes/1`)  | `[]`; la interfaz muestra «evidencia insuficiente»         |
| Síntomas incompatibles                          | Prolog (Sección 16)                      | `[]`; la interfaz muestra el aviso con el motivo           |
| Texto libre vacío o sin síntomas reconocibles   | Prolog (DCG)                             | `[]`, sin excepción                                        |
| Regla del Modo Experto rechazada por Prolog     | `adquirir_nuevo_diagnostico`             | `ok=False`; no se escribe el `.pl`                         |
| Excepción inesperada del puente                 | `motor_inferencia.py`                    | Mensaje en consola y valor vacío; la interfaz sigue viva   |

## 10. Stack aprobado (no agregar fuera de esto sin decisión registrada)

| Capa                 | Tecnología                                                | Nota                                   |
| -------------------- | --------------------------------------------------------- | -------------------------------------- |
| Motor lógico         | **SWI-Prolog** ≥ 10.0.2 (Windows 10.1.14)                  | Versión exacta en `05`                 |
| Lenguaje puente      | **Python** 3.12+ (Windows: 3.14 en `.venv`)               |                                        |
| Puente               | **PySwip** ≥ 0.3.3 (ADR-002)                              |                                        |
| Interfaz             | **Streamlit** ≥ 1.30 (D-021)                              | Sin otras GUI                          |
| Telemetría           | **scikit-learn** ≥ 1.4 (D-025)                            | Solo `DecisionTreeClassifier`          |
| Pruebas Prolog       | **plunit** (incluida en SWI-Prolog)                       | `tests/tests_kb.pl`                    |
| Pruebas Python       | Script propio `pruebas.py`                                | Sin pytest; `AppTest` de Streamlit para comprobar la interfaz |
| Control de versiones | Git + GitHub                                              | Una rama por tarea; commits sin atribución a IA (`03 §6`) |

**No usar:** otras GUI o frameworks web, bases de datos, redes neuronales u otras librerías de IA, `assert`/`retract` para respuestas de la sesión (el Modo Experto sí usa `assertz` para reglas, D-024).

## 11. Entorno local

Requisitos: SWI-Prolog en el `PATH`, Python 3.12+, Git. En Windows, Python y SWI-Prolog deben ser ambos de 64 bits.

```powershell
swipl --version
py -3.14 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
swipl -q -g run_tests -t halt tests/tests_kb.pl
.venv\Scripts\python.exe pruebas.py
.venv\Scripts\streamlit.exe run main.py
```

Codificación: UTF-8 en archivos y en consola (ver `10` T-10).

## 12. Convenciones de nombres

- Predicados, átomos y funciones: **español, minúsculas, `snake_case`, sin tildes ni ñ** (`falla_ram`, `no_arranca`).
- Los textos para el usuario (descripciones, motivos) son átomos entre comillas simples; dentro del `.pl` se escriben sin tildes cuando cruzan el puente.
- Los ID de diagnóstico del Modo Experto se sanitizan a `[a-z0-9_]`.
