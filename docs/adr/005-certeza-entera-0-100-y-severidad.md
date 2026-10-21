# ADR-005: Certeza como entero 0–100 (modelo MYCIN) y severidad en 4 niveles

- **Estado:** Aceptada
- **Fecha:** 2026-10-21
- **Decisores:** Pareja
- **Tarea relacionada:** F2-01, F2-07

## Contexto y problema

El Entregable 1 adoptó factores de certeza (FC) entre 0 y 1 con la combinación `FC = FC1 + FC2 × (1 − FC1)`, etiquetas (muy probable ≥ 0,70; probable 0,40–0,69; posible 0,20–0,39; descartado < 0,20) y una escala de severidad de 4 niveles ajustable por contexto. En coma flotante, `0.8 + 0.5 * 0.2` no es exactamente `0.9`, lo que rompe comparaciones y pruebas.

## Factores de decisión

- Pruebas con resultados exactos.
- Mantener el modelo ya entregado.
- Umbrales en los bordes (0,70; 0,40; 0,20) sin errores de redondeo.

## Opciones consideradas

1. FC enteros de 0 a 100 (porcentaje); combinación `FC is FC1 + (FC2 * (100 - FC1)) // 100`.
2. FC en coma flotante con comparación por tolerancia.
3. Contar condiciones cumplidas (sin FC).

## Decisión

**Opción 1.** El ejemplo del Entregable 1 (0,80 y 0,50 → 0,90) se vuelve 80 y 50 → 90. Etiquetas: `muy_probable` ≥ 70, `probable` 40–69, `posible` 20–39, descartado < 20. Severidad: 4 `critica`, 3 `alta`, 2 `media`, 1 `baja`, limitada a [1, 4]. Orden final: severidad ajustada descendente y, a igual severidad, certeza descendente.

## Consecuencias

- **Positivas:** aritmética exacta; umbrales sin ambigüedad; fácil de explicar.
- **Negativas / deuda aceptada:** el redondeo de la división entera trunca; se documenta y se prueba. Los FC por regla son estimaciones que deben validarse con el técnico.
- **Cuándo revisarla:** si el técnico propone escalas distintas o el docente exige coma flotante.

## Pros y contras de las opciones

### Coma flotante

- ➕ Idéntico al texto del Entregable 1.
- ➖ Pruebas frágiles; errores en los bordes.

### Solo conteo

- ➕ Más simple.
- ➖ Pierde la fortaleza distinta de cada regla que el Entregable 1 justificó.
