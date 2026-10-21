# Registro de decisiones de arquitectura (ADR)

Formato MADR. Plantilla: `docs/ai/templates/adr.md`. Índice corto de todas las decisiones: `docs/ai/07-decisiones.md`.

| ADR                                               | Título                                                 | Estado                        |
| ------------------------------------------------- | ------------------------------------------------------ | ----------------------------- |
| [001](001-prolog-unica-fuente-de-logica.md)       | Prolog como única fuente de lógica; Python solo puente | Aceptada                      |
| [002](002-puente-pyswip-con-alternativa-janus.md) | Puente con PySwip, aislado para poder cambiar a Janus  | Aceptada (provisional, F0-02) |
| [003](003-respuestas-como-lista-sin-estado.md)    | Respuestas como lista pasada a los predicados          | Aceptada                      |
| [004](004-encadenamiento-tres-niveles.md)         | Encadenamiento lógico en tres niveles                  | Aceptada                      |
| [005](005-certeza-entera-0-100-y-severidad.md)    | Certeza entera 0–100 (MYCIN) y severidad en 4 niveles  | Aceptada                      |
| [006](006-solo-consola-sin-gui.md)                | Interacción solo por consola (sin Tkinter)             | Aceptada (confirmar, F0-04)   |
