/*
 * Símbolos para el sistema operativo con distribución Español (alfabetización internacional).
 *
 * ZMK envía códigos de tecla US (la posición física). Windows los traduce según su
 * distribución, así que cada macro indica qué tecla física hay que pulsar para que
 * salga ese carácter con el teclado español. AltGr = RA(...).
 */
#pragma once

/* Fila de números con Shift */
#define ES_EXCL   LS(N1)          /* ! */
#define ES_DQUO   LS(N2)          /* " */
#define ES_DLLR   LS(N4)          /* $ */
#define ES_PRCT   LS(N5)          /* % */
#define ES_AMPS   LS(N6)          /* & */
#define ES_SLSH   LS(N7)          /* / */
#define ES_LPAR   LS(N8)          /* ( */
#define ES_RPAR   LS(N9)          /* ) */
#define ES_EQL    LS(N0)          /* = */

/* Teclas a la derecha del 0 */
#define ES_APOS   MINUS           /* ' */
#define ES_QUES   LS(MINUS)       /* ? */
#define ES_IEXL   EQUAL           /* ¡ */
#define ES_IQUE   LS(EQUAL)       /* ¿ */

/* Resto de la fila central e inferior */
#define ES_PLUS   RBKT            /* + */
#define ES_STAR   LS(RBKT)        /* * */
#define ES_MINS   FSLH            /* - */
#define ES_UNDS   LS(FSLH)        /* _ */
#define ES_LT     NON_US_BSLH     /* < */
#define ES_GT     LS(NON_US_BSLH) /* > */
#define ES_NTIL   SEMI            /* ñ */
#define ES_ACUT   SQT             /* ´ (tecla muerta: tildes) */

/* AltGr */
#define ES_PIPE   RA(N1)          /* | */
#define ES_AT     RA(N2)          /* @ */
#define ES_HASH   RA(N3)          /* # */
#define ES_EURO   RA(E)           /* € */
#define ES_BSLH   RA(GRAVE)       /* \ */
#define ES_LBKT   RA(LBKT)        /* [ */
#define ES_RBKT   RA(RBKT)        /* ] */
#define ES_LBRC   RA(SQT)         /* { */
#define ES_RBRC   RA(BSLH)        /* } */

/* Teclas muertas (necesitan Espacio detrás para salir solas: ver macros es_grv, es_circ, es_tild) */
#define ES_DGRV   LBKT            /* ` muerta */
#define ES_DCIR   LS(LBKT)        /* ^ muerta */
#define ES_DTIL   RA(N4)          /* ~ muerta */
