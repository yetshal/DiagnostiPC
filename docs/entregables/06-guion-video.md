# Guion del video · DiagnostiPC

> Solo el texto que se dice, por fases. Cada fase es una grabación aparte.
> Las acciones van entre paréntesis dentro del texto, para que sepas qué hacer mientras hablas.

---

## FASE 1 · Presentación

Muy buenas, mi nombre es Julian Alfonso Montero Trujillo y presento este trabajo junto con mi compañero Juan Carlos Bastidas Bernal. El proyecto se llama DiagnostiPC.

---

## FASE 2 · De qué se trata

DiagnostiPC es un sistema experto para diagnosticar fallas de un computador. Uno le marca los síntomas que ve, por ejemplo que la pantalla se pone azul o que el equipo se reinicia solo, y el sistema dice qué componente puede estar fallando y qué tan grave es.

La lógica está escrita en Prolog. Python solo se encarga de mostrar la interfaz.

---

## FASE 3 · Entrega 3: lenguaje natural

Para la entrega 3 teníamos que incorporar procesamiento de lenguaje natural. Eso significa que ya no hace falta marcar casillas: se puede escribir como hablaría una persona.

(Hacer clic en el cuadro de texto y escribir: *el equipo se calienta mucho y la pantalla se pone azul*)

Ahora doy clic en "Interpretar con Gramática DCG".

(Clic en el botón)

Los síntomas aparecen marcados en la barra lateral. Esto lo hace una gramática escrita en Prolog, no Python.

---

## FASE 4 · Entrega 3: sensores

La otra parte nueva de la entrega 3 es la telemetría. Aquí tenemos valores de sensores: temperatura del procesador, voltaje, FPS y latencia del disco.

(Mover el control de temperatura del procesador a 92 grados y el de FPS a 19)

Subo la temperatura a 92 grados y bajo los FPS a 19. Luego doy clic en "Clasificar Telemetría a Síntomas".

(Clic en el botón)

El sistema convierte esos números en síntomas. Para eso usamos un clasificador de scikit-learn, y también una regla de umbrales que sigue los estándares de los fabricantes.

---

## FASE 5 · Entrega 3: modo experto

También agregamos el modo experto. Aquí un usuario le puede enseñar al sistema un diagnóstico nuevo, sin reiniciar la aplicación.

(Ir a la pestaña "Modo Experto (Adquisición Dinámica)")

Por ejemplo, registro una falla de pasta térmica con sobrecalentamiento y throttling. Ahora el sistema ya la puede diagnosticar en la siguiente consulta, y además queda guardada en el archivo de la base de conocimiento.

---

## FASE 6 · Entrega 4: el problema

Para la entrega 4, el reto era que el sistema no diga cosas imposibles.

Por ejemplo, si el equipo no enciende, no puede tener FPS bajos, porque no hay ningún juego corriendo. Pero antes el sistema no se daba cuenta y podía dar un diagnóstico igual.

---

## FASE 7 · Entrega 4: demostración del bloqueo

Voy a marcar dos síntomas que no pueden ir juntos: el equipo no enciende y los FPS bajos.

(Marcar en la barra lateral "no_arranca" y "fps_bajos")

Y aparece el aviso: entrada contradictoria, diagnóstico bloqueado. Dice el motivo, y no muestra ningún diagnóstico.

---

## FASE 8 · Entrega 4: el modo experto también se protege

Lo mismo pasa en el modo experto. Si intento registrar un diagnóstico con síntomas que se contradicen, el sistema lo rechaza.

(Ir a "Modo Experto", escribir un ID y elegir "no_arranca" y "throttling", y dar clic en el botón de registrar)

Aparece el error, y el archivo de la base de conocimiento no cambia.

---

## FASE 9 · Entrega 4: pruebas

Tenemos dieciséis casos de prueba por consola, y once pruebas unitarias en Prolog. Incluyen texto vacío, texto sin sentido, y telemetría mezclada con texto contradictorio.

(Ejecutar `python pruebas.py` y mostrar el resultado final)

Aquí están: dieciséis de dieciséis pasan.

---

## FASE 10 · Entrega 4: informe

También entregamos un informe técnico en PDF, con la arquitectura final, el árbol lógico y el reporte de las pruebas de estrés.

(Abrir el PDF y pasar por la portada y la página del árbol lógico)

---

## FASE 11 · Lo que todavía no hace

Quiero ser claros con las limitaciones. La gramática no entiende negaciones: si escribo "no se calienta", el sistema no lo toma como ausencia del síntoma.

Además, por ahora solo tenemos tres pares de síntomas incompatibles, y todavía los estamos validando con un técnico de mantenimiento.

---

## FASE 12 · Cierre

Eso es DiagnostiPC. Muchas gracias por su atención.
