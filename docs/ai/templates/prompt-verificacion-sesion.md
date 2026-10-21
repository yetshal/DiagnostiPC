# Prompt de verificación de la sesión

Úsalo **antes de fusionar** el PR, sobre todo en tareas de certeza, severidad, recolección, puente y auditoría.

```text
Audita tu trabajo de esta sesión. Para cada punto, ejecuta el comando o lee el archivo (no respondas de memoria) y marca ✅, ⚠️ o ❌ con la evidencia:

1. AC de la tarea: ¿se cumple cada criterio? Muestra cómo lo comprobaste.
2. `swipl -q -g run_tests -t halt tests/tests_kb.pl` y, si aplica, `python pruebas.py`: salida real.
3. Carga de `base_conocimiento.pl`: ¿cero advertencias (singleton, discontiguous)?
4. Niveles: ¿algún predicado de N3 consulta solo `respuesta/3`? ¿Alguna llamada ascendente o recursiva? Muestra el grafo de llamadas de lo que tocaste.
5. Cortes: lista cada `!` nuevo, qué ramas descarta y su comentario `% CORTE:`. ¿Alguno es "rojo"? ¿Hay prueba que lo demuestre?
6. Negaciones: lista cada `\+` nuevo y confirma que sus variables están ligadas.
7. Listas y recolección: ¿hay duplicados posibles en los resultados? ¿Qué pasa con `[]`, un solo elemento y listas con variables desconocidas?
8. Certeza y severidad: bordes de umbral, límites 1–4 y precedencias probados.
9. Frontera: ¿algo de dominio en Python? ¿Algún término compuesto cruza el puente? ¿La base imprime algo?
10. Conocimiento: ¿cada regla nueva cita fuente o está `[PENDIENTE-VALIDAR]`? ¿Algún FC o umbral sin respaldo?
11. Tamaño: líneas nuevas de Prolog y de Python frente al límite de `AGENTS.md`.
12. Documentación: `04`, `05`, `06` (y `07`, `08`, `10`, diccionario si aplican) coherentes con el código.
13. Git: rama, commits convencionales, `git status` y `git diff --stat` sin archivos sueltos.
14. Pendientes: ¿cada uno está en el grupo correcto de `04 §Pendientes` con recomendación?

Cierra con una tabla resumen y la lista de lo que hay que corregir antes del merge.
```

## Variante: después de fusionar el PR

```text
El PR de <ID> ya está fusionado. Verifica: `main` coincide con `origin/main`, la rama fue borrada, `05-estado-sesion.md` apunta a la tarea siguiente y las pruebas pasan sobre `main` recién clonado.
```

## Por qué existe

Los agentes tienden a declarar "terminado" con pruebas verdes pero con huecos de fondo: cortes sin justificar, reglas que se saltan niveles, lógica que se filtra a Python o conocimiento inventado. Esta verificación fuerza evidencia concreta justo en esos puntos.
