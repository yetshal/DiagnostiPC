# Arquitectura — diagramas

> Complementa `docs/ai/02-arquitectura.md` (fuente de verdad). Si hay diferencias, manda `02`.

## Capas y responsabilidades

```mermaid
flowchart LR
  U[Usuario<br/>consola] --> M[main.py<br/>cuestionario y resultados]
  T[pruebas.py<br/>casos y evidencia] --> P
  M --> P[motor_inferencia.py<br/>puente: cargar, consultar, formatear]
  P -->|PySwip o Janus| S[SWI-Prolog]
  S --> K[(base_conocimiento.pl<br/>hechos · reglas N1-N3 · certeza · severidad)]
  K -.->|catálogo de preguntas y textos| M
```

Todo lo que decide está a la derecha del puente; a la izquierda solo se captura, se muestra y se prueba.

## Estructura de `base_conocimiento.pl` y dependencias entre niveles

```mermaid
flowchart TD
  H[Hechos<br/>catálogo de variables · diagnósticos · escalas] --> L[Utilidades de listas<br/>respuesta, cumple_todas, contar_cumplidas, filtrar_validas]
  L --> N1[Nivel 1<br/>condiciones elementales]
  N1 --> N2[Nivel 2<br/>categorías e indicios]
  N2 --> N3[Nivel 3<br/>evidencia/4: reglas de diagnóstico]
  N3 --> C[Certeza<br/>combinar_certeza, nivel_certeza]
  N3 --> SV[Severidad<br/>severidad_ajustada]
  C --> API[diagnosticar_todos/3<br/>findall + orden + estados]
  SV --> API
```

La flecha es «es usado por». Ninguna dependencia sube de nivel: no hay ciclos por construcción (ADR-004).

## Ejemplo de encadenamiento (caso del Entregable 1)

```mermaid
flowchart LR
  A[enciende-si] --> N1a[equipo_enciende]
  B[imagen-no] --> N1b[sin_imagen]
  C[pitidos-largos] --> N1c[pitidos_largos]
  N1a --> CAT[categoria arranque]
  N1b --> CAT
  N1c --> CAT
  CAT --> R12[r12 · FC 80]
  N1b --> R12
  N1c --> R12
  D[cambio_hardware-si] --> R13[r13 · FC 50]
  CAT --> R13
  R12 --> FC[combinar: 80 + 50·20/100 = 90]
  R13 --> FC
  FC --> DX[falla_ram · muy_probable]
  DX --> SEV[severidad base alta → media<br/>por cambio de hardware]
```

## Flujo de una consulta

```mermaid
sequenceDiagram
  actor U as Usuario
  participant M as main.py
  participant P as motor_inferencia.py
  participant K as Prolog (base_conocimiento.pl)
  M->>P: catalogo()
  P->>K: catalogo_preguntas(P)
  K-->>P: [[Var, Grupo, Texto, Valores], ...]
  P-->>M: preguntas
  M->>U: formula preguntas y opciones
  U-->>M: respuestas (opciones numeradas)
  M->>P: diagnosticar([(var, valor), ...])
  P->>K: diagnosticar_todos([var-valor, ...], R, E)
  K->>K: validar, N1 → N2 → N3, combinar FC, severidad, findall, ordenar
  K-->>P: R (lista ordenada) y E (estado)
  P-->>M: {estado, resultados}
  M->>U: tabla de diagnósticos / mensaje por estado
```

## Decisión de estado (con cortes)

```mermaid
flowchart TD
  S[Respuestas] --> V{¿Hay valores fuera de catálogo?}
  V -- sí --> E1[entrada_invalida, resultados vacíos]
  V -- no --> I{¿Menos de N_MIN síntomas?}
  I -- sí --> E2[datos_insuficientes]
  I -- no --> D{¿Algún diagnóstico con FC ≥ 20?}
  D -- no --> E3[no_concluyente]
  D -- sí --> E4[ok: lista ordenada por severidad y certeza]
```

Cada rama es una cláusula de `estado_consulta/3` con corte; la última es el valor por defecto.
