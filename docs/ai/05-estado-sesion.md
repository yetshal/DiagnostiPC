# 05 · Estado de la sesión (traspaso)

> Documento de estado del proyecto DiagnostiPC.

## Última actualización

- **Fecha:** 2026-11-05
- **Fase actual:** F6 / Entregable 3 (Procesamiento de Lenguaje Natural con DCG, Aprendizaje Dinámico en Caliente y Pre-procesamiento Numérico Híbrido)
- **Estado general:** Implementación 100% completada, suite de 11 pruebas en verde (100% PASS), interfaz gráfica web interactiva con Streamlit (`main.py`) con Modo Experto y entrada DCG operativa, y documentación técnica sincronizada.

## Qué se hizo en la sesión de hoy

1. **Implementación de la Gramática DCG en Prolog (`base_conocimiento.pl`):**
   - Directivas dinámicas `:- dynamic` y `:- discontiguous` para los predicados de reglas, diagnósticos y componentes.
   - Gramática DCG completa (`extraer_sintomas_dcg/2`) con lexicón de frases compuestas, sinónimos técnicos y filtrado recursivo de ruido/conectores (`y`, `ademas`, `tambien`, `con`, `pero`).
   - Mapeo robusto a los 20 síntomas canónicos del sistema de hardware.

2. **Módulo de Adquisición Dinámica de Conocimiento (Modo Experto):**
   - Predicado `registrar_diagnostico_dinamico/5` en Prolog para enlazar en memoria viva (`assertz/1`) el patrón de falla, severidad, descripción y componente sin reiniciar.
   - Persistencia dual en `motor_inferencia.py`: escribe las cláusulas aprendidas al final de `base_conocimiento.pl` dentro de una sección estructurada para asegurar su supervivencia entre reinicios.

3. **Pre-procesador Numérico Híbrido (`preprocesador_numerico.py`):**
   - Conversión de variables continuas de sensores (temperaturas CPU/GPU en °C, riel de 12V en V, FPS promedio, latencias de almacenamiento en ms y RPM de ventiladores) a hechos simbólicos discretos.
   - Motor dual:
     - Clasificador supervisado ligero con Scikit-learn (`DecisionTreeClassifier`).
     - Heurística determinista basada en tolerancias ATX y especificaciones térmicas Intel/AMD.

4. **Interfaz Interactiva Streamlit (`main.py`):**
   - Expansor de entrada por Lenguaje Natural libre conectada a la DCG de Prolog.
   - Expansor de Telemetría Numérica con sliders para sensores y botón de discretización.
   - Pestaña dedicada "Modo Experto (Adquisición Dinámica)" con formulario completo para dar de alta diagnósticos en caliente, inyección a memoria viva, persistencia y visualización del catálogo registrado.

5. **Suite de Pruebas Automatizadas (`pruebas.py`):**
   - Ampliada de 7 a 11 casos cubriendo DCG en Prolog (Caso 8), inyección en caliente con `assertz` (Caso 9), persistencia y recarga limpia tras reinicio (Caso 10) y telemetría ML (Caso 11).
   - Ejecución 11/11 PASS (100%).

6. **Actualización de Documentación:**
   - Actualizados `requirements.txt`, `README.md`, `docs/entregables/03-diccionario-predicados.md`, `docs/ai/04-hoja-de-ruta.md`, `docs/ai/07-decisiones.md` (D-023, D-024, D-025) y bitácora `06`.

## Estado del sistema

| Componente                                    | Estado      | Notas                                                                  |
| --------------------------------------------- | ----------- | ---------------------------------------------------------------------- |
| Base de conocimiento (`base_conocimiento.pl`) | ✅ Completo | 790+ líneas, hechos base, 27 reglas N1–N3, DCG, dinámicos y persistencia |
| Preprocesador numérico (`preprocesador_numerico.py`) | ✅ Completo | 220 líneas, motor Scikit-Learn y heurística estándar ATX |
| Motor de inferencia (`motor_inferencia.py`)   | ✅ Completo | 470+ líneas, métodos de DCG, adquisición en caliente y telemetría      |
| Interfaz gráfica web (`main.py`)              | ✅ Completo | 490+ líneas en Streamlit, 4 pestañas, entrada DCG y panel Modo Experto |
| Suite de pruebas (`pruebas.py`)               | ✅ Completo | 420+ líneas, 11/11 casos pasando en terminal (código 0)                |
| Dependencias (`requirements.txt`)             | ✅ Completo | `pyswip>=0.3.3`, `streamlit>=1.30.0`, `scikit-learn>=1.4.0`           |
| Diccionario de predicados (`03`)              | ✅ Completo | Actualizado con DCG y adquisición en caliente                          |
| Documentación y README                        | ✅ Completo | Actualizado con guía de Entregables 1, 2 y 3                           |

- **SWI-Prolog:** 10.1.14 (x64-win64)
- **Python:** 3.14.7 (en `.venv`)
- **PySwip:** 0.3.3
- **Streamlit:** 1.66.1
- **Scikit-Learn:** 1.9.1

## Próximos pasos sugeridos para el equipo humano

1. Ejecutar localmente `streamlit run main.py` o `.venv\Scripts\python.exe main.py` para interactuar con las nuevas funciones:
   - Probar la entrada de texto libre en el expansor DCG: *"El equipo se calienta mucho, la pantalla se pone azul y se reinicia sola"*.
   - Probar el clasificador de telemetría: subir temperatura a 92°C y bajar voltaje a 11.1V.
   - Ir a la pestaña **Modo Experto**, registrar un diagnóstico personalizado (ej. `falla_pasta_termica`) y comprobar cómo se evalúa de inmediato y se escribe al archivo `.pl`.
2. Grabar el video demostrativo o ensayar la sustentación del Entregable 3 cubriendo los 3 requisitos clave del docente.
