# 05 · Estado de la sesión (traspaso)

> Documento de estado del proyecto DiagnostiPC.

## Última actualización

- **Fecha:** 2026-11-04
- **Fase actual:** F5 / Entregable 2 (Puente Python–PySwip y Motor de Explicabilidad "Caja Blanca")
- **Estado general:** Implementación 100% completada, suite de 7 pruebas en verde (100% PASS), interfaz gráfica web interactiva con Streamlit (`main.py`) operativa, y documentación técnica sincronizada.

## Qué se hizo en la sesión de hoy

1. **Implementación de los Módulos de Explicabilidad y Recomendación en Prolog (`base_conocimiento.pl`):**
   - **Módulo de Explicabilidad ("¿Por qué?"):**
     - `hechos_comprobados/3`: Deduce los hechos verdaderos que unifican con el patrón canónico del diagnóstico.
     - `regla_disparada/4` y `reglas_disparadas/3`: Genera la traza paso a paso en 3 niveles de inferencia (N1 $\to$ N2 $\to$ N3).
     - `hipotesis_descartada/4` e `hipotesis_descartadas/2`: Evalúa y clasifica los diagnósticos alternativos descartados, identificando si fue por exclusión mutua (`\+`) o por falta de evidencia.
   - **Módulo de Recomendación ("¿Qué falta?"):**
     - `hipotesis_parcial/5` e `hipotesis_parciales/2`: Detecta hipótesis con evidencia parcial activa.
     - `peso_sintoma_candidato/4` y `sintoma_desempate/4`: Pondera los síntomas no ingresados según criticidad (+50 pts) y severidad (+10 a +40 pts) para sugerir la prueba de mayor peso discriminante.
2. **Ampliación del Puente Python en `motor_inferencia.py`:**
   - Métodos tipados para PySwip: `explicar_diagnostico()`, `obtener_hipotesis_descartadas()`, `obtener_hipotesis_parciales()`, `recomendar_siguiente_sintoma()`, `obtener_catalogo_sintomas()` y `obtener_sintomas_por_componente()`.
3. **Interfaz Interactiva en `main.py`:**
   - Desarrollada con Streamlit con layout de pestañas en el área central.
   - Barra lateral con lista directa de síntomas en contenedor con scroll vertical (sin menús desplegables), con buscador y botón de limpiar fijos arriba.
   - Esquema de colores original oscuro con tarjetas de fondo translúcido y bordes coloreados según severidad.
   - Cero emojis en toda la aplicación; tipografía técnica y badges sobrios.
   - Presets eliminados para una interacción 100% natural y guiada por el usuario.
   - Título único **DiagnostiPC** con su eslogan directamente debajo.
   - Arquitectura de callbacks (`on_click` y `on_change`) para mutación segura de checkboxes sin errores de instanciación (`StreamlitWidgetAlreadyInstantiatedError`).
   - Control de guardas: el módulo de recomendación exige al menos un síntoma ingresado para evaluar desempates entre hipótesis.
   - Panel de Auditoría ("¿Por qué?") con hechos verdaderos, reglas disparadas N1 a N3 y diagnósticos descartados.
   - Panel de Recomendación ("¿Qué falta?") con barras de progreso de evidencia y botón directo para agregar el síntoma sugerido.
4. **Actualización de la Suite de Pruebas (`pruebas.py`):**
   - Agregados los Casos 6 (Explicabilidad Caja Blanca) y 7 (Recomendación de desempate).
   - Ejecución 7/7 PASS (100%).
5. **Actualización de Documentación y Entregables:**
   - Creado `requirements.txt` con `pyswip` y `streamlit`.
   - Actualizado `README.md` con las instrucciones del Entregable 2.
   - Actualizado `docs/entregables/03-diccionario-predicados.md` con los nuevos predicados, aridades y modos.
   - Registradas decisiones D-021 y D-022 en `docs/ai/07-decisiones.md` y bitácora en `docs/ai/06-bitacora.md`.

## Estado del sistema

| Componente                                    | Estado      | Notas                                                                  |
| --------------------------------------------- | ----------- | ---------------------------------------------------------------------- |
| Base de conocimiento (`base_conocimiento.pl`) | ✅ Completo | 473 líneas, 66 hechos aridad 2, 27 reglas N1–N3, compila limpio en SWI |
| Motor de inferencia (`motor_inferencia.py`)   | ✅ Completo | 338 líneas, puente PySwip con métodos de auditoría y desempate         |
| Interfaz gráfica web (`main.py`)              | ✅ Completo | 273 líneas en Streamlit, ejecución dual (`streamlit run` / `python`)   |
| Suite de pruebas (`pruebas.py`)               | ✅ Completo | 330 líneas, 7/7 casos pasando en terminal (código 0)                   |
| Dependencias (`requirements.txt`)             | ✅ Completo | `pyswip>=0.3.3`, `streamlit>=1.30.0`                                   |
| Diccionario de predicados (`03`)              | ✅ Completo | Actualizado con secciones de Explicabilidad y Recomendación            |
| Documentación y README                        | ✅ Completo | Actualizado con arquitectura híbrida y guía del Entregable 2           |

- **SWI-Prolog:** 10.1.14 (x64-win64)
- **Python:** 3.14.7 (en `.venv`)
- **PySwip:** 0.3.3
- **Streamlit:** 1.66.1

## Próximos pasos sugeridos para el equipo humano

1. Ejecutar localmente `streamlit run main.py` o `python main.py` para visualizar la interfaz web interactiva.
2. Grabar el video corto de demostración (3 a 5 minutos) o preparar la sustentación en vivo:
   - **Demostración Caso 1:** Pulsar el botón preset "Caso 1 (Inferencia)" en la barra lateral $\to$ mostrar diagnóstico `falla_ram`, severidad alta $\to$ abrir panel "¿Por qué?" para mostrar los 3 hechos comprobados, las reglas N1-N3 disparadas y las hipótesis descartadas (ej. `falla_critica_cpu` excluida por `\+`).
   - **Demostración Caso 2:** Pulsar el botón preset "Caso 2 (Desempate)" en la barra lateral $\to$ mostrar advertencia de evidencia insuficiente $\to$ abrir panel "¿Qué falta?" para mostrar las hipótesis en competencia (CPU vs Enfriamiento) $\to$ observar el síntoma sugerido `throttling` $\to$ hacer clic en "➕ Agregar 'throttling' a la consulta" para evidenciar la re-evaluación en tiempo real.
