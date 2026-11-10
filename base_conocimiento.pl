%% =============================================================================
%% DiagnostiPC - Base de Conocimiento
%% Sistema Experto de Diagnóstico de Hardware de PC
%% Versión 1.0
%% =============================================================================

:- use_module(library(lists)).
:- use_module(library(apply)).

%% Directivas de predicados dinamicos para permitir adquisicion en caliente
:- dynamic sintoma_valido/1.
:- dynamic componente_sintoma/2.
:- dynamic patron_falla/2.
:- dynamic severidad_diagnostico/2.
:- dynamic diagnostico_describe/2.
:- dynamic excluye/2.

%% Cláusulas dinámicas pueden aparecer al final del archivo al persistir
:- discontiguous sintoma_valido/1.
:- discontiguous componente_sintoma/2.
:- discontiguous patron_falla/2.
:- discontiguous severidad_diagnostico/2.
:- discontiguous diagnostico_describe/2.

%% =============================================================================
%% SECCIÓN 1: HECHOS BASE - SÍNTOMAS CONOCIDOS
%% =============================================================================
%% Cada síntoma válido que el sistema puede reconocer y procesar.

sintoma_valido(pantalla_azul).
sintoma_valido(reinicios_aleatorios).
sintoma_valido(sobrecalentamiento).
sintoma_valido(throttling).
sintoma_valido(errores_memoria).
sintoma_valido(artefactos_graficos).
sintoma_valido(pantalla_negra).
sintoma_valido(no_arranca).
sintoma_valido(pitidos_bios).
sintoma_valido(rendimiento_lento).
sintoma_valido(disco_no_detectado).
sintoma_valido(ruidos_disco).
sintoma_valido(voltaje_inestable).
sintoma_valido(apagado_brusco).
sintoma_valido(puertos_usb_fallan).
sintoma_valido(fps_bajos).
sintoma_valido(temperatura_alta_gpu).
sintoma_valido(errores_io).
sintoma_valido(corrupcion_datos).
sintoma_valido(ventilador_no_gira).

%% =============================================================================
%% SECCIÓN 2: HECHOS BASE - COMPONENTES Y SUS SÍNTOMAS ASOCIADOS
%% =============================================================================
%% Relación entre cada componente y los síntomas que puede provocar.

componente_sintoma(cpu, sobrecalentamiento).
componente_sintoma(cpu, reinicios_aleatorios).
componente_sintoma(cpu, throttling).
componente_sintoma(cpu, rendimiento_lento).
componente_sintoma(cpu, pantalla_azul).

componente_sintoma(ram, pantalla_azul).
componente_sintoma(ram, errores_memoria).
componente_sintoma(ram, reinicios_aleatorios).
componente_sintoma(ram, no_arranca).
componente_sintoma(ram, rendimiento_lento).

componente_sintoma(gpu, artefactos_graficos).
componente_sintoma(gpu, pantalla_negra).
componente_sintoma(gpu, fps_bajos).
componente_sintoma(gpu, temperatura_alta_gpu).
componente_sintoma(gpu, pantalla_azul).

componente_sintoma(disco, disco_no_detectado).
componente_sintoma(disco, ruidos_disco).
componente_sintoma(disco, rendimiento_lento).
componente_sintoma(disco, errores_io).
componente_sintoma(disco, corrupcion_datos).

componente_sintoma(fuente, voltaje_inestable).
componente_sintoma(fuente, apagado_brusco).
componente_sintoma(fuente, reinicios_aleatorios).
componente_sintoma(fuente, no_arranca).
componente_sintoma(fuente, puertos_usb_fallan).

componente_sintoma(placa_madre, pitidos_bios).
componente_sintoma(placa_madre, no_arranca).
componente_sintoma(placa_madre, puertos_usb_fallan).
componente_sintoma(placa_madre, reinicios_aleatorios).
componente_sintoma(placa_madre, errores_io).

componente_sintoma(enfriamiento, sobrecalentamiento).
componente_sintoma(enfriamiento, ventilador_no_gira).
componente_sintoma(enfriamiento, throttling).
componente_sintoma(enfriamiento, reinicios_aleatorios).

%% =============================================================================
%% SECCIÓN 3: HECHOS BASE - PATRONES DE FALLA
%% =============================================================================
%% Cada patrón de falla define el conjunto mínimo de síntomas que lo identifican.

patron_falla(falla_critica_cpu,    [sobrecalentamiento, reinicios_aleatorios, throttling, rendimiento_lento]).
patron_falla(falla_ram,            [pantalla_azul, errores_memoria, reinicios_aleatorios]).
patron_falla(falla_gpu,            [artefactos_graficos, fps_bajos, temperatura_alta_gpu]).
patron_falla(falla_disco,          [disco_no_detectado, ruidos_disco, errores_io]).
patron_falla(falla_fuente,         [voltaje_inestable, apagado_brusco, reinicios_aleatorios]).
patron_falla(falla_placa_madre,    [pitidos_bios, no_arranca, puertos_usb_fallan]).
patron_falla(falla_enfriamiento,   [sobrecalentamiento, ventilador_no_gira, throttling]).
patron_falla(degradacion_disco,    [rendimiento_lento, corrupcion_datos, errores_io]).
patron_falla(inestabilidad_fuente, [voltaje_inestable, reinicios_aleatorios, apagado_brusco]).

%% =============================================================================
%% SECCIÓN 4: HECHOS BASE - SEVERIDAD DE DIAGNÓSTICOS
%% =============================================================================
%% Nivel de severidad: bajo < medio < alto < critico

severidad_diagnostico(falla_critica_cpu,    critico).
severidad_diagnostico(falla_ram,            alto).
severidad_diagnostico(falla_gpu,            alto).
severidad_diagnostico(falla_disco,          critico).
severidad_diagnostico(falla_fuente,         critico).
severidad_diagnostico(falla_placa_madre,    critico).
severidad_diagnostico(falla_enfriamiento,   medio).
severidad_diagnostico(degradacion_disco,    medio).
severidad_diagnostico(inestabilidad_fuente, alto).
severidad_diagnostico(rendimiento_general,  bajo).

%% =============================================================================
%% SECCIÓN 5: HECHOS BASE - EXCLUSIONES MUTUAS
%% =============================================================================
%% excluye(DiagA, DiagB): si DiagA aplica, no emitir DiagB simultáneamente.

excluye(falla_critica_cpu,    rendimiento_general).
excluye(falla_critica_cpu,    falla_enfriamiento).
excluye(falla_ram,            falla_critica_cpu).
excluye(falla_fuente,         inestabilidad_fuente).
excluye(falla_disco,          degradacion_disco).

%% Síntomas considerados críticos para conteo especial.
sintoma_critico(pantalla_azul).
sintoma_critico(no_arranca).
sintoma_critico(voltaje_inestable).
sintoma_critico(apagado_brusco).
sintoma_critico(corrupcion_datos).
sintoma_critico(disco_no_detectado).
sintoma_critico(pitidos_bios).

%% =============================================================================
%% NIVEL 1: REGLAS DE VALIDACIÓN PRELIMINAR
%% =============================================================================

%% sintoma_en_lista/2
%% Verdadero si Sintoma pertenece a ListaSintomas Y es un síntoma conocido.
sintoma_en_lista(Sintoma, ListaSintomas) :-
    member(Sintoma, ListaSintomas),
    sintoma_valido(Sintoma).

%% lista_contiene_minimo/3
%% Verdadero si ListaSintomas contiene al menos N elementos de Requeridos.
lista_contiene_minimo(ListaSintomas, Requeridos, N) :-
    include(contiene_sintoma(ListaSintomas), Requeridos, Presentes),
    length(Presentes, Cuenta),
    Cuenta >= N.

%% Auxiliar: comprueba si Sintoma está en la lista.
contiene_sintoma(Lista, Sintoma) :-
    member(Sintoma, Lista).

%% es_sintoma_critico/1
%% Verdadero si el síntoma tiene clasificación crítica.
es_sintoma_critico(Sintoma) :-
    sintoma_critico(Sintoma).

%% sintomas_del_componente/2
%% Obtiene todos los síntomas asociados a un componente.
sintomas_del_componente(Componente, Sintomas) :-
    findall(S, componente_sintoma(Componente, S), Sintomas).

%% subconjunto_valido/2
%% Filtra una lista dejando solo los síntomas válidos.
subconjunto_valido([], []).
subconjunto_valido([H|T], [H|Validos]) :-
    sintoma_valido(H), !,
    % CORTE: H es válido; impide que la 3.ª cláusula lo descarte al reintentar.
    subconjunto_valido(T, Validos).
subconjunto_valido([_|T], Validos) :-
    subconjunto_valido(T, Validos).

%% =============================================================================
%% NIVEL 2: REGLAS DE INFERENCIA INTERMEDIA
%% =============================================================================

%% patron_presente/2
%% Verdadero si los síntomas del patrón están presentes en ListaSintomas.
%% Requiere al menos 2 de los 3 síntomas del patrón para activarse.
patron_presente(Patron, ListaSintomas) :-
    patron_falla(Patron, SintomasPatron),
    length(SintomasPatron, Total),
    Minimo is max(2, Total - 1),
    lista_contiene_minimo(ListaSintomas, SintomasPatron, Minimo).

%% componente_sospechoso/2
%% Sospecha de un componente si al menos 2 de sus síntomas están presentes.
componente_sospechoso(Componente, ListaSintomas) :-
    sintomas_del_componente(Componente, SintomasComp),
    lista_contiene_minimo(ListaSintomas, SintomasComp, 2).

%% diagnostico_excluido/2
%% Verdadero si el diagnóstico está excluido por algún otro diagnóstico
%% ya establecido para la misma lista de síntomas.
diagnostico_excluido(Diagnostico, ListaSintomas) :-
    excluye(OtroDiag, Diagnostico),
    patron_presente(OtroDiag, ListaSintomas).

%% tiene_sintomas_suficientes/2
%% Verifica que la lista no esté vacía y tenga al menos 2 síntomas válidos.
tiene_sintomas_suficientes(ListaSintomas) :-
    subconjunto_valido(ListaSintomas, Validos),
    length(Validos, N),
    N >= 2.

%% componente_dominante/2
%% Determina el componente con más síntomas presentes en la lista.
componente_dominante(ListaSintomas, Componente) :-
    findall(
        Cuenta-Comp,
        (
            member(Comp, [cpu, ram, gpu, disco, fuente, placa_madre, enfriamiento]),
            sintomas_del_componente(Comp, SC),
            include(contiene_sintoma(ListaSintomas), SC, Match),
            length(Match, Cuenta),
            Cuenta > 0
        ),
        Pares
    ),
    Pares \= [],
    max_par(Pares, _-Componente).

%% max_par/2 — obtiene el par con mayor clave numérica.
max_par([X], X) :- !.
% CORTE: con un solo elemento no se prueba la cláusula recursiva (evita max_par([], _)).
max_par([H|T], Max) :-
    max_par(T, MaxT),
    H = N1-_,
    MaxT = N2-_,
    ( N1 >= N2 -> Max = H ; Max = MaxT ).

%% =============================================================================
%% NIVEL 3: REGLAS DE CONCLUSIÓN FINAL
%% =============================================================================

%% diagnostico_posible/3
%% Genera un diagnóstico posible dado un patrón, una lista de síntomas
%% y un componente objetivo (puede ser 'cualquiera' para no filtrar).
diagnostico_posible(Patron, ListaSintomas, _Componente) :-
    patron_presente(Patron, ListaSintomas),
    tiene_sintomas_suficientes(ListaSintomas),
    \+ diagnostico_excluido(Patron, ListaSintomas).

%% diagnosticar_todos/3
%% +ListaSintomas, +Componente, -Diagnosticos
%% Recopila todos los diagnósticos posibles en una lista de pares Diag-Severidad.
%% El parámetro Componente puede ser 'cualquiera' para no filtrar por componente.
diagnosticar_todos(ListaSintomas, _Componente, []) :-
    entrada_contradictoria(ListaSintomas), !.
% CORTE: entrada con síntomas incompatibles (Sección 16); se bloquea antes de
% inferir para no emitir un diagnóstico sobre hechos imposibles.
diagnosticar_todos(ListaSintomas, _Componente, Diagnosticos) :-
    findall(
        Diag-Sev,
        (
            patron_falla(Diag, _),
            diagnostico_posible(Diag, ListaSintomas, _),
            severidad_diagnostico(Diag, Sev)
        ),
        DiagsBrutos
    ),
    list_to_set(DiagsBrutos, Diagnosticos).

%% diagnosticar_todos/3 - caso base: lista vacía o sin síntomas suficientes.
%% (cut para evitar ambigüedad cuando la lista está vacía)
diagnosticar_todos(ListaSintomas, _Componente, []) :-
    \+ tiene_sintomas_suficientes(ListaSintomas), !.

%% severidad_caso/2
%% +Diagnostico, -Nivel
%% Devuelve el nivel de severidad de un diagnóstico.
severidad_caso(Diagnostico, Nivel) :-
    severidad_diagnostico(Diagnostico, Nivel), !.
% CORTE: si hay severidad registrada, se excluye el valor por defecto 'desconocido'.
severidad_caso(_, desconocido).

%% componente_afectado/2
%% +ListaSintomas, -Componente
%% Infiere qué componente es el más probable causante de los síntomas.
componente_afectado(ListaSintomas, Componente) :-
    tiene_sintomas_suficientes(ListaSintomas),
    componente_dominante(ListaSintomas, Componente), !.
% CORTE: un solo componente dominante; excluye el valor por defecto 'desconocido'.
componente_afectado(_, desconocido).

%% =============================================================================
%% PREDICADOS DE LISTAS Y UTILIDADES
%% =============================================================================

%% validar_sintomas/2
%% +Lista, -Validos
%% Filtra la lista de entrada dejando únicamente síntomas reconocidos.
validar_sintomas(Lista, Validos) :-
    subconjunto_valido(Lista, Validos).

%% conteo_sintomas_criticos/2
%% +Lista, -Conteo
%% Cuenta cuántos síntomas críticos hay en la lista de entrada.
conteo_sintomas_criticos(Lista, Conteo) :-
    include(es_sintoma_critico, Lista, Criticos),
    length(Criticos, Conteo).

%% include/3 con predicado de orden superior (es_sintoma_critico).
%% SWI-Prolog ya provee include/3, pero necesitamos el wrapper de aridad 2.
% meta_predicate removido para compatibilidad con library(apply)

%% todos_los_sintomas/1
%% Devuelve la lista completa de síntomas válidos.
todos_los_sintomas(Lista) :-
    findall(S, sintoma_valido(S), Brutos),
    list_to_set(Brutos, Lista).

%% diagnostico_describe/2
%% Texto descriptivo para cada diagnóstico (para reportes).
diagnostico_describe(falla_critica_cpu,
    'El procesador presenta falla crítica por sobrecalentamiento y throttling severo.').
diagnostico_describe(falla_ram,
    'La memoria RAM presenta errores que causan BSOD y reinicios aleatorios.').
diagnostico_describe(falla_gpu,
    'La tarjeta gráfica falla produciendo artefactos, bajo FPS y alta temperatura.').
diagnostico_describe(falla_disco,
    'El disco duro/SSD no es detectado o presenta ruidos y errores de E/S.').
diagnostico_describe(falla_fuente,
    'La fuente de poder entrega voltaje inestable causando apagados y reinicios.').
diagnostico_describe(falla_placa_madre,
    'La placa madre falla: pitidos POST, no arranca, puertos USB inoperables.').
diagnostico_describe(falla_enfriamiento,
    'El sistema de enfriamiento es deficiente: ventilador parado y throttling.').
diagnostico_describe(degradacion_disco,
    'El disco presenta degradación progresiva con corrupción y errores de E/S.').
diagnostico_describe(inestabilidad_fuente,
    'La fuente genera inestabilidad de voltaje con reinicios y apagados esporádicos.').
diagnostico_describe(rendimiento_general,
    'Rendimiento general degradado sin falla crítica identificada.').


%% =============================================================================
%% SECCIÓN 11: MÓDULO DE EXPLICABILIDAD ("CAJA BLANCA" / ¿POR QUÉ?)
%% =============================================================================
%% Permite auditar el razonamiento lógico del sistema experto en tres aspectos:
%% 1. Hechos verdaderos comprobados (síntomas que unifican con el patrón).
%% 2. Reglas disparadas en los 3 niveles lógicos (N1 -> N2 -> N3).
%% 3. Hipótesis alternativas descartadas y su justificación (falta de evidencia o \+).
%% =============================================================================

%% hechos_comprobados/3
%% +Diagnostico, +ListaSintomas, -HechosVerdaderos
%% % Fuente: S1, T1
%% Obtiene los síntomas provistos por el usuario que unifican con el patrón del diagnóstico.
hechos_comprobados(Diagnostico, ListaSintomas, HechosVerdaderos) :-
    patron_falla(Diagnostico, SintomasPatron),
    include(contiene_sintoma(ListaSintomas), SintomasPatron, HechosVerdaderos).

%% regla_disparada/4
%% +Nivel, +Diagnostico, +ListaSintomas, -Descripcion
%% Deduce qué reglas se activaron en cada nivel de inferencia.
%% Nivel 1: hechos y síntomas validados individualmente.
regla_disparada(1, Diagnostico, ListaSintomas, Regla) :-
    hechos_comprobados(Diagnostico, ListaSintomas, Hechos),
    member(S, Hechos),
    format(atom(Regla), 'sintoma_valido(~w) comprobado como hecho verdadero', [S]).

%% Nivel 2: patrones presentes y confirmación de subsistema.
regla_disparada(2, Diagnostico, ListaSintomas, Regla) :-
    patron_presente(Diagnostico, ListaSintomas),
    format(atom(Regla), 'patron_presente(~w) satisface umbral minimo de activacion', [Diagnostico]).

regla_disparada(2, Diagnostico, ListaSintomas, Regla) :-
    hechos_comprobados(Diagnostico, ListaSintomas, Hechos),
    member(S, Hechos),
    componente_sintoma(Comp, S),
    componente_sospechoso(Comp, ListaSintomas),
    format(atom(Regla), 'componente_sospechoso(~w) confirmado con >= 2 sintomas observados', [Comp]).

regla_disparada(2, Diagnostico, ListaSintomas, Regla) :-
    % Justificación de \+: seguro porque Diagnostico y ListaSintomas están ligados.
    % Excluye ramas donde otro diagnóstico inhibe al actual por regla de exclusión mutua.
    \+ diagnostico_excluido(Diagnostico, ListaSintomas),
    format(atom(Regla), 'no_excluido(~w) sin inhibiciones activas de exclusion mutua', [Diagnostico]).

%% Nivel 3: conclusión y dictamen final.
regla_disparada(3, Diagnostico, ListaSintomas, Regla) :-
    diagnostico_posible(Diagnostico, ListaSintomas, _),
    severidad_diagnostico(Diagnostico, Sev),
    format(atom(Regla), 'diagnostico_posible(~w, severidad: ~w) activado exitosamente', [Diagnostico, Sev]).

%% reglas_disparadas/3
%% +Diagnostico, +ListaSintomas, -ReglasOrdenadas
%% Recolecta la lista de reglas disparadas en orden N1 -> N2 -> N3 sin duplicados.
reglas_disparadas(Diagnostico, ListaSintomas, ReglasOrdenadas) :-
    findall(
        Nivel-Texto,
        regla_disparada(Nivel, Diagnostico, ListaSintomas, Texto),
        Pares
    ),
    list_to_set(Pares, ParesUnicos),
    keysort(ParesUnicos, ParesOrdenados),
    formatear_reglas(ParesOrdenados, ReglasOrdenadas).

formatear_reglas([], []).
formatear_reglas([N-Txt | T], [Formateada | Resto]) :-
    format(atom(Formateada), 'Nivel ~w: ~w', [N, Txt]),
    formatear_reglas(T, Resto).

%% hipotesis_descartada/4
%% +ListaSintomas, -Diagnostico, -TipoDescarte, -Detalle
%% % Fuente: S1, T1
%% Identifica diagnósticos que compartían síntomas con la entrada pero no concluyeron.
%% Caso A: Descartado por regla de exclusión mutua (\+).
hipotesis_descartada(ListaSintomas, Diagnostico, exclusion_mutua, Detalle) :-
    patron_falla(Diagnostico, _),
    excluye(DiagCausante, Diagnostico),
    patron_presente(DiagCausante, ListaSintomas),
    format(atom(Detalle), 'Inhibido por exclusion mutua ante presencia confirmada de ~w', [DiagCausante]).

%% Caso B: Descartado por evidencia insuficiente (comparte síntomas pero no alcanza el umbral de activación).
hipotesis_descartada(ListaSintomas, Diagnostico, falta_evidencia, Detalle) :-
    patron_falla(Diagnostico, SintomasPatron),
    % Justificación de \+: seguro porque Diagnostico y ListaSintomas están ligados.
    % Excluye diagnósticos ya excluidos por Caso A o que hayan concluido con éxito.
    \+ diagnostico_excluido(Diagnostico, ListaSintomas),
    \+ diagnostico_posible(Diagnostico, ListaSintomas, _),
    include(contiene_sintoma(ListaSintomas), SintomasPatron, Presentes),
    Presentes \= [],
    subtract(SintomasPatron, Presentes, Faltantes),
    atomic_list_concat(Faltantes, ', ', FaltantesStr),
    atomic_list_concat(Presentes, ', ', PresentesStr),
    format(atom(Detalle), 'Evidencia insuficiente: presentes [~w], requiere al menos [~w]', [PresentesStr, FaltantesStr]).

%% hipotesis_descartadas/2
%% +ListaSintomas, -Descartadas
%% Recolecta todas las hipótesis alternativas descartadas para la lista de síntomas.
hipotesis_descartadas(ListaSintomas, Descartadas) :-
    findall(
        descarte(Diag, Tipo, Detalle),
        hipotesis_descartada(ListaSintomas, Diag, Tipo, Detalle),
        Brutas
    ),
    list_to_set(Brutas, Descartadas).

%% =============================================================================
%% SECCIÓN 12: MÓDULO DE RECOMENDACIÓN ("¿QUÉ FALTA?" / CONSULTA DE DESEMPATE)
%% =============================================================================
%% % Fuente: S1, S2, T1
%% Evalúa las hipótesis parcialmente activas y determina qué síntoma adicional
%% tiene mayor peso y capacidad de discriminación para desempatar o confirmar.
%% =============================================================================

%% peso_severidad/2: asigna puntuación según severidad para priorizar fallas graves
peso_severidad(critico, 40).
peso_severidad(alto,    30).
peso_severidad(medio,   20).
peso_severidad(bajo,    10).
peso_severidad(_,        0).

%% hipotesis_parcial/5
%% +ListaSintomas, -Diag, -Coincidentes, -Faltantes, -Total
%% Identifica diagnósticos activos parcialmente que aún no concluyen.
%% Requiere que al menos un síntoma observado esté presente en el patrón.
hipotesis_parcial(ListaSintomas, Diag, Coincidentes, Faltantes, Total) :-
    ListaSintomas \= [],
    patron_falla(Diag, Requeridos),
    % Justificación de \+: seguro porque Diag y ListaSintomas están ligados.
    % Excluye diagnósticos ya concluidos o excluidos.
    \+ diagnostico_excluido(Diag, ListaSintomas),
    \+ diagnostico_posible(Diag, ListaSintomas, _),
    include(contiene_sintoma(ListaSintomas), Requeridos, Coincidentes),
    Coincidentes \= [],
    subtract(Requeridos, Coincidentes, Faltantes),
    Faltantes \= [],
    length(Requeridos, Total).

%% hipotesis_parciales/2
%% +ListaSintomas, -ListaParciales
%% Retorna la lista de términos parcial(Diag, Coincidentes, Faltantes, Total).
hipotesis_parciales(ListaSintomas, ListaParciales) :-
    findall(
        parcial(Diag, Coinc, Falt, Tot),
        hipotesis_parcial(ListaSintomas, Diag, Coinc, Falt, Tot),
        Brutas
    ),
    list_to_set(Brutas, ListaParciales).

%% peso_sintoma_candidato/4
%% +Sintoma, +ListaSintomas, +HipotesisParciales, -PesoTotal
%% Calcula el peso de un síntoma candidato no ingresado:
%% - Síntoma crítico (+50 pts)
%% - Severidad de las hipótesis beneficiadas (+10 a +40 pts)
%% - Bono por desempate multi-hipótesis (+20 pts por cada hipótesis que ayuda)
peso_sintoma_candidato(Sintoma, _ListaSintomas, HipotesisParciales, PesoTotal) :-
    ( es_sintoma_critico(Sintoma) -> PtsCrit = 50 ; PtsCrit = 0 ),
    findall(
        PtsHip,
        (
            member(parcial(Diag, _, Faltantes, _), HipotesisParciales),
            member(Sintoma, Faltantes),
            severidad_diagnostico(Diag, Sev),
            peso_severidad(Sev, PtsSev),
            PtsHip is PtsSev + 20
        ),
        PuntosLista
    ),
    sum_list(PuntosLista, PtsHips),
    PtsHips > 0,
    PesoTotal is PtsCrit + PtsHips.

%% sintoma_desempate/4
%% +ListaSintomas, -SintomaSugerido, -HipotesisBeneficiadas, -Motivo
%% Determina qué síntoma no ingresado tiene mayor peso para desempatar o confirmar.
sintoma_desempate(ListaSintomas, SintomaSugerido, HipotesisBeneficiadas, Motivo) :-
    ListaSintomas \= [],
    hipotesis_parciales(ListaSintomas, Parciales),
    Parciales \= [],
    findall(
        S,
        (
            member(parcial(_, _, Faltantes, _), Parciales),
            member(S, Faltantes),
            \+ member(S, ListaSintomas),
            % \+ seguro: S y ListaSintomas ligados; no sugiere un síntoma
            % que contradiga lo ya reportado (Sección 16).
            \+ incompatible_con_lista(S, ListaSintomas)
        ),
        CandidatosBrutos
    ),
    list_to_set(CandidatosBrutos, Candidatos),
    Candidatos \= [],
    findall(
        Peso-Sint,
        (
            member(Sint, Candidatos),
            peso_sintoma_candidato(Sint, ListaSintomas, Parciales, Peso)
        ),
        ParesPesos
    ),
    ParesPesos \= [],
    max_par(ParesPesos, _MaxPeso-SintomaSugerido),
    findall(
        Diag,
        (
            member(parcial(Diag, _, Falt, _), Parciales),
            member(SintomaSugerido, Falt)
        ),
        HipotesisBeneficiadas
    ),
    atomic_list_concat(HipotesisBeneficiadas, ', ', HipsStr),
    ( es_sintoma_critico(SintomaSugerido) ->
        format(atom(Motivo), 'Sintoma critico de alta prioridad; desempata y aproxima: ~w', [HipsStr])
    ;
        format(atom(Motivo), 'Mayor peso diferencial; desempata y aproxima: ~w', [HipsStr])
    ).

%% =============================================================================
%% SECCIÓN 13: PROCESAMIENTO DE LENGUAJE NATURAL MEDIANTE DCG
%% =============================================================================
%% % Fuente: S1, T1
%% Gramática de Cláusulas Definidas (DCG) que analiza una secuencia de átomos
%% léxicos ingresados libremente por el usuario y extrae los síntomas canónicos
%% correspondientes, filtrando palabras de relleno, conectores y verbos.
%% =============================================================================

%% extraer_sintomas_dcg/2
%% +Tokens, -Sintomas
%% Analiza la lista de átomos léxicos mediante la gramática y devuelve la lista
%% unificada y sin duplicados de síntomas reconocidos.
extraer_sintomas_dcg(Tokens, Sintomas) :-
    is_list(Tokens),
    phrase(analisis_texto_dcg(SintomasBrutos), Tokens),
    list_to_set(SintomasBrutos, Sintomas), !.
% CORTE: el primer análisis (que prioriza reconocer frases sobre ignorar palabras) es el válido;
% excluye el fallback que devuelve [].
extraer_sintomas_dcg(_, []).

%% Regla recursiva principal del parser DCG
analisis_texto_dcg([S | Resto]) -->
    frase_sintoma(S), !,
    % CORTE: si una frase se reconoce, no se reinterpreta su primera palabra como ruido.
    conector_opcional,
    analisis_texto_dcg(Resto).
analisis_texto_dcg(Resto) -->
    [_PalabraIgnorada],
    analisis_texto_dcg(Resto).
analisis_texto_dcg([]) --> [].

%% Conectores y palabras de enlace opcionales
%% CORTE (cada cláusula): consumido el conector, no se prueba la alternativa vacía.
conector_opcional --> [y], !.
conector_opcional --> [e], !.
conector_opcional --> [ademas], !.
conector_opcional --> [tambien], !.
conector_opcional --> [o], !.
conector_opcional --> [con], !.
conector_opcional --> [pero], !.
conector_opcional --> [].

%% Lexicón gramatical de síntomas (frases compuestas y sinónimos técnicos)
%% 1. Pantalla Azul (BSOD)
frase_sintoma(pantalla_azul) --> [pantalla, de, la, muerte].
frase_sintoma(pantalla_azul) --> [pantalla, se, pone, azul].
frase_sintoma(pantalla_azul) --> [pantalla, esta, azul].
frase_sintoma(pantalla_azul) --> [pantallazo, azul].
frase_sintoma(pantalla_azul) --> [pantalla, azul].
frase_sintoma(pantalla_azul) --> [bsod].
frase_sintoma(pantalla_azul) --> [volcado, de, memoria].

%% 2. Reinicios Aleatorios
frase_sintoma(reinicios_aleatorios) --> [reinicios, aleatorios].
frase_sintoma(reinicios_aleatorios) --> [reinicios, constantes].
frase_sintoma(reinicios_aleatorios) --> [reinicios, continuos].
frase_sintoma(reinicios_aleatorios) --> [se, apaga, y, prende].
frase_sintoma(reinicios_aleatorios) --> [se, reinicia, sola].
frase_sintoma(reinicios_aleatorios) --> [se, reinicia, solo].
frase_sintoma(reinicios_aleatorios) --> [se, reinicia].
frase_sintoma(reinicios_aleatorios) --> [reinicio, inesperado].
frase_sintoma(reinicios_aleatorios) --> [reinicio, aleatorio].

%% 3. Sobrecalentamiento
frase_sintoma(sobrecalentamiento) --> [calentamiento, excesivo].
frase_sintoma(sobrecalentamiento) --> [temperatura, muy, alta].
frase_sintoma(sobrecalentamiento) --> [se, calienta, mucho].
frase_sintoma(sobrecalentamiento) --> [se, calienta, demasiado].
frase_sintoma(sobrecalentamiento) --> [se, calienta].
frase_sintoma(sobrecalentamiento) --> [muy, caliente].
frase_sintoma(sobrecalentamiento) --> [hirviendo].
frase_sintoma(sobrecalentamiento) --> [sobrecalentamiento].

%% 4. Throttling
frase_sintoma(throttling) --> [thermal, throttling].
frase_sintoma(throttling) --> [bajada, de, reloj].
frase_sintoma(throttling) --> [frecuencia, reducida].
frase_sintoma(throttling) --> [estrangulamiento, termico].
frase_sintoma(throttling) --> [throttling].

%% 5. Errores de Memoria RAM
frase_sintoma(errores_memoria) --> [errores, de, memoria].
frase_sintoma(errores_memoria) --> [errores, en, ram].
frase_sintoma(errores_memoria) --> [falla, en, ram].
frase_sintoma(errores_memoria) --> [fallos, de, memoria].
frase_sintoma(errores_memoria) --> [memoria, defectuosa].
frase_sintoma(errores_memoria) --> [errores_memoria].

%% 6. Artefactos Gráficos
frase_sintoma(artefactos_graficos) --> [artefactos, graficos].
frase_sintoma(artefactos_graficos) --> [artefactos, visuales].
frase_sintoma(artefactos_graficos) --> [glitches, en, pantalla].
frase_sintoma(artefactos_graficos) --> [lineas, en, pantalla].
frase_sintoma(artefactos_graficos) --> [distorsion, visual].
frase_sintoma(artefactos_graficos) --> [glitches].

%% 7. Pantalla Negra
frase_sintoma(pantalla_negra) --> [sin, senal, de, video].
frase_sintoma(pantalla_negra) --> [pantalla, en, negro].
frase_sintoma(pantalla_negra) --> [pantalla, negra].
frase_sintoma(pantalla_negra) --> [no, da, video].
frase_sintoma(pantalla_negra) --> [sin, video].
frase_sintoma(pantalla_negra) --> [monitor, sin, senal].

%% 8. No Arranca
frase_sintoma(no_arranca) --> [no, completa, el, post].
frase_sintoma(no_arranca) --> [no, pasa, del, post].
frase_sintoma(no_arranca) --> [no, arranca].
frase_sintoma(no_arranca) --> [no, prende].
frase_sintoma(no_arranca) --> [no, enciende].
frase_sintoma(no_arranca) --> [no, bootea].

%% 9. Pitidos BIOS
frase_sintoma(pitidos_bios) --> [pitidos, de, la, bios].
frase_sintoma(pitidos_bios) --> [pitidos, de, bios].
frase_sintoma(pitidos_bios) --> [pitidos, al, encender].
frase_sintoma(pitidos_bios) --> [beeps, de, bios].
frase_sintoma(pitidos_bios) --> [pitidos, bios].
frase_sintoma(pitidos_bios) --> [beeps].

%% 10. Rendimiento Lento
frase_sintoma(rendimiento_lento) --> [pc, muy, lenta].
frase_sintoma(rendimiento_lento) --> [computadora, lenta].
frase_sintoma(rendimiento_lento) --> [computador, lento].
frase_sintoma(rendimiento_lento) --> [sistema, lento].
frase_sintoma(rendimiento_lento) --> [lentitud, extrema].
frase_sintoma(rendimiento_lento) --> [rendimiento, lento].
frase_sintoma(rendimiento_lento) --> [se, congela].
frase_sintoma(rendimiento_lento) --> [se, traba].
frase_sintoma(rendimiento_lento) --> [lentitud].

%% 11. Disco No Detectado
frase_sintoma(disco_no_detectado) --> [no, reconoce, el, disco].
frase_sintoma(disco_no_detectado) --> [sin, dispositivo, de, arranque].
frase_sintoma(disco_no_detectado) --> [disco, no, detectado].
frase_sintoma(disco_no_detectado) --> [disco, no, aparece].
frase_sintoma(disco_no_detectado) --> [ssd, no, detectado].
frase_sintoma(disco_no_detectado) --> [disco_no_detectado].

%% 12. Ruidos de Disco
frase_sintoma(ruidos_disco) --> [chasquidos, en, el, disco].
frase_sintoma(ruidos_disco) --> [ruidos, en, el, disco].
frase_sintoma(ruidos_disco) --> [clics, en, el, disco].
frase_sintoma(ruidos_disco) --> [ruidos, de, disco].
frase_sintoma(ruidos_disco) --> [ruidos, mecanicos].
frase_sintoma(ruidos_disco) --> [ruidos, disco].

%% 13. Voltaje Inestable
frase_sintoma(voltaje_inestable) --> [caidas, de, voltaje].
frase_sintoma(voltaje_inestable) --> [variaciones, de, voltaje].
frase_sintoma(voltaje_inestable) --> [fluctuaciones, de, energia].
frase_sintoma(voltaje_inestable) --> [inestabilidad, de, voltaje].
frase_sintoma(voltaje_inestable) --> [voltaje_inestable].

%% 14. Apagado Brusco
frase_sintoma(apagado_brusco) --> [se, apaga, de, golpe].
frase_sintoma(apagado_brusco) --> [se, apaga, de, repente].
frase_sintoma(apagado_brusco) --> [corte, de, energia].
frase_sintoma(apagado_brusco) --> [se, apaga, sola].
frase_sintoma(apagado_brusco) --> [apagados, bruscos].
frase_sintoma(apagado_brusco) --> [apagado, brusco].

%% 15. Puertos USB Fallan
frase_sintoma(puertos_usb_fallan) --> [puertos, usb, sin, energia].
frase_sintoma(puertos_usb_fallan) --> [no, reconoce, usb].
frase_sintoma(puertos_usb_fallan) --> [usb, no, funcionan].
frase_sintoma(puertos_usb_fallan) --> [puertos, usb, fallan].
frase_sintoma(puertos_usb_fallan) --> [usb, fallan].

%% 16. FPS Bajos
frase_sintoma(fps_bajos) --> [cuadros, por, segundo, bajos].
frase_sintoma(fps_bajos) --> [tirones, en, juegos].
frase_sintoma(fps_bajos) --> [caida, de, fps].
frase_sintoma(fps_bajos) --> [bajos, fps].
frase_sintoma(fps_bajos) --> [fps, bajos].

%% 17. Temperatura Alta GPU
frase_sintoma(temperatura_alta_gpu) --> [temperatura, alta, en, tarjeta, grafica].
frase_sintoma(temperatura_alta_gpu) --> [temperatura, alta, gpu].
frase_sintoma(temperatura_alta_gpu) --> [grafica, muy, caliente].
frase_sintoma(temperatura_alta_gpu) --> [gpu, muy, caliente].
frase_sintoma(temperatura_alta_gpu) --> [grafica, hirviendo].

%% 18. Errores de Entrada/Salida (I/O)
frase_sintoma(errores_io) --> [fallos, de, lectura, y, escritura].
frase_sintoma(errores_io) --> [errores, de, entrada, y, salida].
frase_sintoma(errores_io) --> [errores, de, io].
frase_sintoma(errores_io) --> [errores, io].

%% 19. Corrupción de Datos
frase_sintoma(corrupcion_datos) --> [sistema, de, archivos, danado].
frase_sintoma(corrupcion_datos) --> [corrupcion, de, datos].
frase_sintoma(corrupcion_datos) --> [archivos, corruptos].
frase_sintoma(corrupcion_datos) --> [corrupcion, datos].

%% 20. Ventilador No Gira
frase_sintoma(ventilador_no_gira) --> [disipador, no, gira].
frase_sintoma(ventilador_no_gira) --> [ventiladores, no, giran].
frase_sintoma(ventilador_no_gira) --> [ventilador, no, gira].
frase_sintoma(ventilador_no_gira) --> [ventilador, parado].
frase_sintoma(ventilador_no_gira) --> [cooler, detenido].
frase_sintoma(ventilador_no_gira) --> [cooler, no, gira].

%% =============================================================================
%% SECCIÓN 14: ADQUISICIÓN DINÁMICA DE CONOCIMIENTO (MODO EXPERTO)
%% =============================================================================
%% % Fuente: S1, T1
%% Permite inyectar en memoria viva nuevos diagnósticos formulados por un
%% usuario con rol Experto, garantizando consistencia en las relaciones lógicas.
%% =============================================================================

registrar_diagnostico_dinamico(IdDiag, Componente, Severidad, ListaSintomas, Descripcion) :-
    % \+ seguro: ListaSintomas ligada. Un patrón con síntomas incompatibles
    % (Sección 16) nunca podría dispararse; se rechaza antes del assertz.
    \+ entrada_contradictoria(ListaSintomas),
    assertz(patron_falla(IdDiag, ListaSintomas)),
    assertz(severidad_diagnostico(IdDiag, Severidad)),
    assertz(diagnostico_describe(IdDiag, Descripcion)),
    forall(
        member(Sintoma, ListaSintomas),
        (
            ( componente_sintoma(Componente, Sintoma) -> true ; assertz(componente_sintoma(Componente, Sintoma)) ),
            ( sintoma_valido(Sintoma) -> true ; assertz(sintoma_valido(Sintoma)) )
        )
    ).

%% =============================================================================
%% SECCIÓN 16: CONSISTENCIA DE LA ENTRADA (ENTREGABLE 4)
%% =============================================================================
%% Detecta síntomas que no pueden observarse a la vez y bloquea el diagnóstico
%% antes de emitirlo. no_arranca = el equipo no enciende o no pasa del POST
%% (ver frase_sintoma(no_arranca)); los síntomas de abajo exigen el sistema
%% operativo en ejecución, así que no pueden coexistir con él.

%% --- Nivel 1: hechos de incompatibilidad -------------------------------------
%% incompatible(+SintomaA, +SintomaB, -Motivo). Se escribe en un solo sentido;
%% incompatible_con_lista/2 y par_contradictorio/4 la consultan en ambos.
% [PENDIENTE-VALIDAR] Ninguna fuente de adquisicion-conocimiento.md lista estas
% exclusiones; se derivan de la definición de no_arranca. Validar con T1.
incompatible(no_arranca, fps_bajos,
    'Medir FPS exige que el equipo arranque y ejecute una aplicacion grafica').
incompatible(no_arranca, throttling,
    'El throttling solo se observa con el procesador trabajando bajo carga en el sistema operativo').
incompatible(no_arranca, rendimiento_lento,
    'Evaluar el rendimiento exige que el sistema operativo este en ejecucion').

%% par_contradictorio/4  (Nivel 1: solo consulta hechos y la lista)
%% +Lista, -A, -B, -Motivo
par_contradictorio(Lista, A, B, Motivo) :-
    incompatible(A, B, Motivo),
    memberchk(A, Lista),
    memberchk(B, Lista).

%% incompatible_con_lista/2  (Nivel 1)
%% +Sintoma, +Lista: Sintoma choca con algún síntoma ya presente en Lista.
incompatible_con_lista(S, Lista) :-
    ( incompatible(S, Otro, _) ; incompatible(Otro, S, _) ),
    memberchk(Otro, Lista), !.
% CORTE: basta un choque; evita soluciones repetidas. Seguro: S y Lista ligados.

%% --- Nivel 2: conjunto de conflictos y estado --------------------------------
%% contradicciones/2
%% +Lista, -Pares: lista de conflicto(A, B, Motivo) sin duplicados; [] si la
%% entrada no es lista (nunca lanza excepción a Python).
contradicciones(Lista, Pares) :-
    is_list(Lista), !,
    % CORTE: separa la entrada válida del caso no-lista de la cláusula siguiente.
    findall(conflicto(A, B, M), par_contradictorio(Lista, A, B, M), Brutos),
    list_to_set(Brutos, Pares).
contradicciones(_, []).

%% entrada_contradictoria/1
%% +Lista: verdadero si hay al menos un conflicto.
entrada_contradictoria(Lista) :-
    is_list(Lista),
    par_contradictorio(Lista, _, _, _), !.
% CORTE: con un conflicto basta; no se enumeran los demás.

%% estado_consistencia/2
%% +Lista, -Estado: consistente | contradictoria. Lo consulta Python antes de
%% mostrar diagnósticos.
estado_consistencia(Lista, contradictoria) :-
    entrada_contradictoria(Lista), !.
% CORTE: precedencia; si hay conflicto no se evalúa la cláusula por defecto.
estado_consistencia(_, consistente).

%% =============================================================================
%% SECCIÓN 15: REGLAS ADQUIRIDAS EN CALIENTE (PERSISTENCIA MODO EXPERTO)
%% =============================================================================
%% El contenido a continuación de esta línea se añade dinámicamente mediante
%% el panel Experto de la aplicación y persiste entre reinicios.


%% [DINAMICO - ADQUIRIDO EN CALIENTE: falla_vrm_placa]
patron_falla(falla_vrm_placa, [voltaje_inestable,apagado_brusco]).
severidad_diagnostico(falla_vrm_placa, critico).
diagnostico_describe(falla_vrm_placa, 'Falla en modulo regulador de voltaje (VRM) de la placa madre.').
componente_sintoma(placa_madre, voltaje_inestable).
sintoma_valido(voltaje_inestable).
componente_sintoma(placa_madre, apagado_brusco).
sintoma_valido(apagado_brusco).

%% [DINAMICO - ADQUIRIDO EN CALIENTE: falla_vrm_placa]
patron_falla(falla_vrm_placa, [voltaje_inestable,apagado_brusco]).
severidad_diagnostico(falla_vrm_placa, critico).
diagnostico_describe(falla_vrm_placa, 'Falla en modulo regulador de voltaje (VRM) de la placa madre.').
componente_sintoma(placa_madre, voltaje_inestable).
sintoma_valido(voltaje_inestable).
componente_sintoma(placa_madre, apagado_brusco).
sintoma_valido(apagado_brusco).

%% [DINAMICO - ADQUIRIDO EN CALIENTE: falla_vrm_placa]
patron_falla(falla_vrm_placa, [voltaje_inestable,apagado_brusco]).
severidad_diagnostico(falla_vrm_placa, critico).
diagnostico_describe(falla_vrm_placa, 'Falla en modulo regulador de voltaje (VRM) de la placa madre.').
componente_sintoma(placa_madre, voltaje_inestable).
sintoma_valido(voltaje_inestable).
componente_sintoma(placa_madre, apagado_brusco).
sintoma_valido(apagado_brusco).

%% [DINAMICO - ADQUIRIDO EN CALIENTE: falla_pasta_termica]
patron_falla(falla_pasta_termica, [sobrecalentamiento,throttling]).
severidad_diagnostico(falla_pasta_termica, alto).
diagnostico_describe(falla_pasta_termica, 'Degradación del compuesto térmico entre el procesador y el disipador. Se recomienda limpiar con alcohol isopropílico y reaplicar pasta térmica de alta conductividad.').
