# Ficha de regla

> Plantilla para documentar cada regla de Nivel 3 (y, si hace falta, de N1/N2). Se copia a `docs/product/adquisicion-conocimiento.md §4` o se usa para revisar con el técnico. El bloque equivalente va como comentario en `base_conocimiento.pl`.

| Campo                            | Valor                                                                    |
| -------------------------------- | ------------------------------------------------------------------------ |
| ID de regla                      | `r12`                                                                    |
| Diagnóstico (átomo)              | `falla_ram` (DX02)                                                       |
| Nivel                            | 3                                                                        |
| Categoría de la que depende (N2) | `arranque`                                                               |
| Condiciones N1 que usa           | `pitidos_largos`, `sin_imagen`                                           |
| Condiciones de exclusión (`\+`)  | —                                                                        |
| FC propuesto                     | 80                                                                       |
| Fuente                           | S3 (tabla de pitidos), T1                                                |
| Estado de validación             | `[PENDIENTE-VALIDAR]` / validada por el técnico el AAAA-MM-DD            |
| Pruebas                          | `test(r12_pitidos_largos_sin_imagen)`, `test(r12_no_aplica_sin_pitidos)` |
| Observaciones del técnico        | …                                                                        |

## Plantilla del comentario en el `.pl`

```prolog
%% r12 · falla_ram (DX02) · Nivel 3 · depende de categoria(arranque)
%% Fuente: S3, T1   FC: 80   Estado: [PENDIENTE-VALIDAR]
evidencia(R, falla_ram, r12, 80) :-
    categoria(R, arranque),
    pitidos_largos(R),
    sin_imagen(R).
```
