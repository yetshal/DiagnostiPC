# 08 · Glosario del dominio (español ↔ código)

> Usa **siempre** estos nombres en Prolog y Python; en la consola, el texto en español. Si falta un término, agrégalo aquí antes de usarlo.
> Los átomos van en minúsculas, `snake_case`, sin tildes ni ñ.

## 1. Variables de entrada (38) — `Var-Valor`

Códigos del Entregable 1 (Tabla 2). Valores: `si`/`no` salvo indicación. «ns» = `no_sabe`.

### Grupo A · Energía y encendido (`grupo_variable(_, energia)`)

| Cód. | Átomo                    | Pregunta (resumen)                         | Valores           |
| ---- | ------------------------ | ------------------------------------------ | ----------------- |
| A1   | `enciende`               | ¿El equipo enciende (luces, ventiladores)? | si, no            |
| A2   | `apagado_repentino`      | ¿Se apaga de forma repentina?              | si, no            |
| A3   | `reinicio_inesperado`    | ¿Se reinicia solo?                         | si, no            |
| A4   | `olor_quemado`           | ¿Olor a quemado o chispas?                 | si, no            |
| A5   | `solo_con_cargador`      | ¿Solo enciende con el cargador? (portátil) | si, no, no_aplica |
| A6   | `corte_energia_reciente` | ¿Corte de energía o tormenta reciente?     | si, no            |

### Grupo B · Arranque

| Cód. | Átomo                  | Pregunta                                           | Valores                      |
| ---- | ---------------------- | -------------------------------------------------- | ---------------------------- |
| B1   | `pitidos`              | ¿Pitidos al encender?                              | no, cortos, largos           |
| B2   | `imagen`               | ¿Aparece imagen al encender?                       | si, no                       |
| B3   | `disco_no_detectado`   | ¿Mensaje de disco no detectado / No boot device?   | si, no                       |
| B4   | `atascado_en_logo`     | ¿Se queda en el logo o en «Reparación automática»? | si, no                       |
| B5   | `pantalla_azul`        | ¿Pantalla azul (BSOD)?                             | no, al_arrancar, durante_uso |
| B6   | `hora_se_desconfigura` | ¿Fecha y hora se desconfiguran al desconectar?     | si, no                       |

### Grupo C · Video y pantalla

| Cód. | Átomo                      | Pregunta                                    | Valores |
| ---- | -------------------------- | ------------------------------------------- | ------- |
| C1   | `imagen_artefactos`        | ¿Líneas, cuadros o colores extraños?        | si, no  |
| C2   | `pantalla_negra_encendido` | ¿Pantalla negra con el equipo encendido?    | si, no  |
| C3   | `fallas_en_graficos`       | ¿Fallas al jugar o usar programas gráficos? | si, no  |
| C4   | `imagen_parpadea`          | ¿La imagen parpadea o se pierde la señal?   | si, no  |

### Grupo D · Rendimiento y temperatura

| Cód. | Átomo                       | Pregunta                                        | Valores         |
| ---- | --------------------------- | ----------------------------------------------- | --------------- |
| D1   | `equipo_lento`              | ¿Lento en general?                              | si, no          |
| D2   | `ventilador_ruidoso`        | ¿Ventilador fuerte o constante?                 | si, no          |
| D3   | `carcasa_caliente`          | ¿Carcasa muy caliente?                          | si, no          |
| D4   | `congela_con_carga`         | ¿Se congela o apaga con tareas pesadas?         | si, no          |
| D5   | `disco_al_100`              | ¿Disco al 100 % en el Administrador de tareas?  | si, no, no_sabe |
| D6   | `cpu_ocupada_sin_programas` | ¿Procesador muy ocupado sin programas abiertos? | si, no, no_sabe |

### Grupo E · Almacenamiento

| Cód. | Átomo              | Pregunta                                  | Valores         |
| ---- | ------------------ | ----------------------------------------- | --------------- |
| E1   | `clics_en_disco`   | ¿Clics o rasgueos en el disco?            | si, no          |
| E2   | `archivos_danados` | ¿Archivos dañados o que desaparecen?      | si, no          |
| E3   | `alerta_smart`     | ¿Advertencia de estado del disco (SMART)? | si, no, no_sabe |

### Grupo F · Software y seguridad

| Cód. | Átomo                         | Pregunta                                         | Valores |
| ---- | ----------------------------- | ------------------------------------------------ | ------- |
| F1   | `ventanas_emergentes`         | ¿Ventanas emergentes o publicidad no solicitada? | si, no  |
| F2   | `programas_desconocidos`      | ¿Programas o extensiones que no instaló?         | si, no  |
| F3   | `navegador_redirige`          | ¿Redirecciones o página de inicio cambiada?      | si, no  |
| F4   | `antivirus_inactivo`          | ¿Antivirus desactivado o no se puede activar?    | si, no  |
| F5   | `problema_tras_actualizacion` | ¿Empezó tras una actualización o controlador?    | si, no  |

### Grupo G · Contexto (no apunta a un diagnóstico; ajusta certeza y severidad)

| Cód. | Átomo                  | Pregunta                                      | Valores                          |
| ---- | ---------------------- | --------------------------------------------- | -------------------------------- |
| G1   | `tipo_equipo`          | Tipo de equipo                                | portatil, escritorio             |
| G2   | `antiguedad_anios`     | Antigüedad                                    | entero ≥ 0                       |
| G3   | `meses_desde_limpieza` | Meses desde la última limpieza interna        | entero ≥ 0, nunca                |
| G4   | `cambio_hardware`      | ¿Cambió o agregó un componente recientemente? | si, no                           |
| G5   | `frecuencia`           | Frecuencia del problema                       | ocasional, frecuente, permanente |
| G6   | `tiene_respaldo`       | ¿Tiene copia de seguridad?                    | si, no                           |
| G7   | `ram_gb`               | RAM instalada                                 | entero > 0, no_sabe              |
| G8   | `tipo_almacenamiento`  | Tipo de unidad                                | hdd, ssd, no_sabe                |

> Pendiente (F1-02): confirmar con el docente si `no_sabe` cuenta como respuesta o como ausencia de dato (propuesta: respuesta válida que **no** aporta evidencia).

## 2. Diagnósticos (10)

| Cód. | Átomo                     | Nombre                                                | Sev. base |
| ---- | ------------------------- | ----------------------------------------------------- | --------- |
| DX01 | `falla_fuente_poder`      | Falla de la fuente de poder o del adaptador           | alta (3)  |
| DX02 | `falla_ram`               | Falla o mala conexión de la RAM                       | alta (3)  |
| DX03 | `falla_disco`             | Falla inminente del disco duro o SSD                  | alta (3)  |
| DX04 | `sobrecalentamiento`      | Sobrecalentamiento (polvo, pasta térmica, ventilador) | alta (3)  |
| DX05 | `falla_grafica`           | Falla de la tarjeta gráfica o del subsistema de video | alta (3)  |
| DX06 | `corrupcion_so`           | Corrupción del sistema operativo o del arranque       | media (2) |
| DX07 | `malware`                 | Infección por software malicioso                      | alta (3)  |
| DX08 | `conflicto_controladores` | Conflicto de controladores o actualización defectuosa | media (2) |
| DX09 | `pila_cmos`               | Pila de la BIOS (CMOS) agotada                        | baja (1)  |
| DX10 | `recursos_insuficientes`  | Recursos insuficientes para el uso actual             | baja (1)  |

## 3. Categorías (Nivel 2)

`energia` · `arranque` · `video` · `rendimiento` · `almacenamiento` · `software`

## 4. Escalas

| Severidad | Número | Átomo     | Criterio                                                        |
| --------- | ------ | --------- | --------------------------------------------------------------- |
| Crítica   | 4      | `critica` | Riesgo de daño físico, incendio o pérdida irreversible de datos |
| Alta      | 3      | `alta`    | Hardware inutilizado o que tiende a empeorar                    |
| Media     | 2      | `media`   | Funciona con fallas; causa probable corregible por software     |
| Baja      | 1      | `baja`    | Rendimiento o comodidad, sin riesgo                             |

| Certeza (FC entero) | Etiqueta                   |
| ------------------- | -------------------------- |
| 70–100              | `muy_probable`             |
| 40–69               | `probable`                 |
| 20–39               | `posible`                  |
| 0–19                | descartado (no se informa) |

## 5. Estados de consulta

| Átomo                 | Significado                                                 |
| --------------------- | ----------------------------------------------------------- |
| `ok`                  | Hay ≥ 1 diagnóstico                                         |
| `no_concluyente`      | Datos suficientes, ningún diagnóstico llega a FC 20         |
| `datos_insuficientes` | Menos de `N_MIN` síntomas respondidos (incluye lista vacía) |
| `entrada_invalida`    | Variable o valor fuera de catálogo                          |

## 6. Términos técnicos

| Término                    | Significado                                                               |
| -------------------------- | ------------------------------------------------------------------------- |
| Hecho                      | Cláusula sin cuerpo (`severidad_base(falla_ram, 3).`)                     |
| Regla                      | Cláusula con cuerpo (`cabeza :- metas.`)                                  |
| Nivel 1 / 2 / 3            | Validación elemental / inferencia intermedia / conclusión final (ADR-004) |
| FC                         | Factor de certeza, entero 0–100 (ADR-005)                                 |
| Corte (`!`)                | Poda del backtracking; solo en exclusión mutua, fallback o determinismo   |
| Negación por fallo (`\+`)  | Éxito si la meta no se puede probar; requiere variables ligadas           |
| Fallback                   | Cláusula final por defecto cuando ninguna condición específica se cumple  |
| Frontera                   | Datos que cruzan Python↔Prolog: listas, átomos, enteros                   |
| Puente                     | PySwip o Janus                                                            |
| plunit                     | Biblioteca de pruebas unitarias de SWI-Prolog                             |
| AC                         | Criterio de aceptación de una tarea                                       |
| DoD                        | Definición de terminado                                                   |
| Fuente `S?` / técnico `T?` | IDs de `docs/product/adquisicion-conocimiento.md`                         |
