# Arquitectura — Diagramas y Estructura del Sistema

> Complementa la documentación técnica de DiagnostiPC y describe la arquitectura real implementada.

---

## 1. Capas y Responsabilidades

```mermaid
flowchart LR
  U[Usuario / Tester<br/>Terminal de Consola] --> T[pruebas.py<br/>Suite de pruebas y formateo]
  T --> P[motor_inferencia.py<br/>Puente Python: PySwip]
  P -->|PySwip C Foreign Interface| S[SWI-Prolog Engine]
  S --> K[(base_conocimiento.pl<br/>66 hechos · 17 reglas N1-N3 · Severidad)]
```

- **Lógica de Inferencia (Prolog):** El 100% de la deducción, descarte, agregación sin duplicados y severidad reside en `base_conocimiento.pl`.
- **Puente y Presentación (Python):** `motor_inferencia.py` encapsula la comunicación con SWI-Prolog, convierte términos y tipos, y entrega resultados estructurados a `pruebas.py`.

---

## 2. Dependencias entre Niveles de Reglas

```mermaid
flowchart TD
  H[Hechos Base<br/>sintoma_valido, componente_sintoma, patron_falla,<br/>severidad_diagnostico, excluye, diagnostico_describe]

  H --> N1[Nivel 1: Validación y Condiciones Elementales<br/>sintoma_en_lista/2, lista_contiene_minimo/3,<br/>subconjunto_valido/2, es_sintoma_critico/1]

  N1 --> N2[Nivel 2: Inferencia Intermedia y Patrones<br/>patron_presente/2, componente_sospechoso/2,<br/>diagnostico_excluido/2, tiene_sintomas_suficientes/1,<br/>componente_dominante/2]

  N2 --> N3[Nivel 3: Conclusión Final y Recolección<br/>diagnostico_candidato/3, diagnostico_con_severidad/3,<br/>diagnosticar_todos/3 con findall y list_to_set]

  H --> SV[Severidad Determinista<br/>severidad_caso/2]
  SV --> N3
```

> **Garantía sin ciclos:** El flujo de dependencia es estrictamente descendente ($H \rightarrow N1 \rightarrow N2 \rightarrow N3$). No existe recursión izquierda ni referencias circulares.

---

## 3. Flujo de una Consulta de Diagnóstico

```mermaid
sequenceDiagram
  actor T as Suite pruebas.py
  participant M as motor_inferencia.py
  participant P as SWI-Prolog Engine
  participant K as base_conocimiento.pl

  T->>M: consultar_diagnosticos(sintomas, comp)
  M->>P: Prolog.query("diagnosticar_todos([...], Comp, Diags)")
  P->>K: tiene_sintomas_suficientes(Sintomas)
  alt Síntomas insuficientes (< 2)
    K-->>P: Fallback con corte (!) -> Diags = []
  else Síntomas suficientes
    K->>K: Nivel 1: validar pertenencia de síntomas
    K->>K: Nivel 2: patron_presente y \+ diagnostico_excluido
    K->>K: Nivel 3: diagnostico_con_severidad (Diag-Sev)
    K->>K: findall/3 + list_to_set/2 (elimina duplicados)
    K-->>P: Diags = [falla_ram-alto, ...]
  end
  P-->>M: Generador de soluciones PySwip
  M->>M: Parseo de términos Functor/Str a tuplas Python
  M-->>T: Lista de tuplas [(diagnostico, severidad), ...]
  T->>T: Formateo visual y verificación PASS/FAIL
```

---

## 4. Mecanismo de Exclusión y Casos Borde

```mermaid
flowchart TD
  In[Lista de Síntomas Observados] --> Suf{¿Tiene al menos 2 síntomas válidos?}
  Suf -- No --> FB[Fallback con corte ! y \+<br/>Retorna lista vacía [] sin error]
  Suf -- Sí --> Pat{¿Coincide con patron_falla/2?}
  Pat -- No --> Disc[No concluyente / Descartado]
  Pat -- Sí --> Exc{¿Está excluido por otro diagnóstico?<br/>\+ diagnostico_excluido/2}
  Exc -- Sí --> Disc
  Exc -- No --> Cand[Diagnóstico Candidato Válido]
  Cand --> Sev[Asignar Severidad Determinista<br/>severidad_diagnostico/2]
  Sev --> Coll[Recolección findall/3 + list_to_set/2]
  Coll --> Out[Lista Final de Diagnósticos Ordenada y Única]
```
