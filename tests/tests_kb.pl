%% Pruebas unitarias (plunit) de base_conocimiento.pl
%% Ejecutar: swipl -q -g run_tests -t halt tests/tests_kb.pl

:- use_module(library(plunit)).
:- prolog_load_context(directory, Dir),
   atom_concat(Dir, '/../base_conocimiento.pl', Kb),
   consult(Kb).

:- begin_tests(contradicciones).

test(par_directo_detectado) :-
    contradicciones([no_arranca, fps_bajos], Pares),
    Pares = [conflicto(no_arranca, fps_bajos, _)].

test(orden_inverso_detectado) :-
    contradicciones([fps_bajos, pantalla_azul, no_arranca], [conflicto(no_arranca, fps_bajos, _)]).

test(varios_conflictos) :-
    contradicciones([no_arranca, fps_bajos, throttling, rendimiento_lento], Pares),
    length(Pares, 3).

test(entrada_consistente_sin_conflictos) :-
    contradicciones([pantalla_azul, errores_memoria, reinicios_aleatorios], []).

test(lista_vacia_consistente) :-
    contradicciones([], []),
    \+ entrada_contradictoria([]).

test(no_lista_no_revienta) :-
    contradicciones(no_es_lista, []).

test(estado_consistencia) :-
    estado_consistencia([no_arranca, throttling], contradictoria),
    estado_consistencia([pantalla_azul, errores_memoria], consistente).

test(bloquea_diagnostico) :-
    diagnosticar_todos([no_arranca, pitidos_bios, puertos_usb_fallan, fps_bajos], cualquiera, []).

% nondet: diagnosticar_todos/3 deja un punto de elección previo (cláusula de
% datos insuficientes); Python solo toma la primera solución.
test(no_afecta_entrada_valida, [nondet]) :-
    diagnosticar_todos([pantalla_azul, errores_memoria, reinicios_aleatorios], cualquiera, D),
    memberchk(falla_ram-_, D).

test(desempate_no_sugiere_sintoma_incompatible) :-
    forall(sintoma_desempate([no_arranca, pitidos_bios], S, _, _),
           \+ incompatible_con_lista(S, [no_arranca, pitidos_bios])).

test(experto_rechaza_patron_contradictorio, [fail]) :-
    registrar_diagnostico_dinamico(dx_test_contradictorio, cpu, alto,
                                   [no_arranca, fps_bajos], 'prueba').

:- end_tests(contradicciones).
