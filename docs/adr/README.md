# Registro de decisiones de arquitectura (ADR)

Formato MADR. Plantilla: `docs/ai/templates/adr.md`. Índice corto de todas las decisiones: `docs/ai/07-decisiones.md`.

| ADR                                               | Título                                                 | Estado   | Notas de Implementación                                                |
| ------------------------------------------------- | ------------------------------------------------------ | -------- | ---------------------------------------------------------------------- |
| [001](001-prolog-unica-fuente-de-logica.md)       | Prolog como única fuente de lógica; Python solo puente | Aceptada | Reglas, deducción y severidad 100% en `base_conocimiento.pl`.          |
| [002](002-puente-pyswip-con-alternativa-janus.md) | Puente con PySwip, aislado para poder cambiar a Janus  | Aceptada | Implementado con PySwip 0.3.3 en `motor_inferencia.py`.                |
| [003](003-respuestas-como-lista-sin-estado.md)    | Respuestas como lista pasada a los predicados          | Aceptada | Consultas funcionales puras sin efectos colaterales.                   |
| [004](004-encadenamiento-tres-niveles.md)         | Encadenamiento lógico en tres niveles                  | Aceptada | Nivel 1 (hechos) → Nivel 2 (patrones) → Nivel 3 (conclusión).          |
| [005](005-certeza-entera-0-100-y-severidad.md)    | Certeza entera 0–100 (MYCIN) y severidad en 4 niveles  | Aceptada | Escala de severidad en 4 niveles (`bajo`, `medio`, `alto`, `critico`). |
| [006](006-solo-consola-sin-gui.md)                | Interacción solo por consola (sin Tkinter)             | Aceptada | Salida y ejecución por terminal en `pruebas.py`.                       |
