from os import environ
from pathlib import Path as _Path

# ==================================================================
# settings.py: la configuración de TODO el proyecto oTree
# Diplomado básico en economía experimental
# BEER Lab / NudgeTEC, Tec de Monterrey. Versión probada: oTree 6.0.15 (Python 3.14)
#
# QUÉ ES ESTE ARCHIVO
#   Un proyecto de oTree = este settings.py + una carpeta por app.
#   Aquí NO está la lógica del juego (esa vive en el __init__.py de cada app).
#   Aquí se decide qué apps existen, en qué orden corren y con qué parámetros.
#   Si cambian este archivo con `otree devserver` corriendo, el servidor se
#   reinicia solo; si hay un error de Python, aparece en la terminal.
#
# Apps de este proyecto (según la copia, algunas pueden no estar):
#   s2_dictador              -> plantilla de la sesión 2 (huecos COMPLETAR)
#   s5_dictador_ext          -> plantilla de la sesión 5 (huecos COMPLETAR)
#   s6_dictador_con_errores  -> aplicación con errores sembrados (sesión 6)
#   pago_final               -> pantalla de pago común (va al final de todas)
#   *_solucion               -> soluciones (solo en la copia docente)
#
# CÓMO LEERLO, DE ARRIBA ABAJO
#   1. SESSION_CONFIGS: el "menú" de sesiones. Es lo que aparece en la página
#      Demo (localhost:8000) y en Sessions > Create. Cada dict(...) es una
#      configuración:
#        name                   identificador; es el que se usa en
#                               `otree test <name>` (por ejemplo, s2_plantilla)
#        display_name           el texto que se ve en la pantalla
#        app_sequence           las apps, en el orden en que corren
#        num_demo_participants  cuántas personas crea el Demo (y los bots)
#      Cualquier otra clave (emparejamiento, semilla, timeout_decision...) es un
#      parámetro propio del experimento: la app lo lee con
#      session.config['emparejamiento']. Así, la misma app corre con distintas
#      condiciones sin tocar su código.
#   2. PLANTILLAS: recurso del curso. La plantilla de cada equipo (con "___")
#      solo entra al menú si se activa en la terminal:
#          PowerShell:  $env:PLANTILLAS="s2"; otree devserver
#      Así una plantilla incompleta no impide arrancar el servidor.
#   3. El filtro que sigue quita del menú las configuraciones cuyas apps no están
#      en la carpeta (el paquete de estudiantes, sin *_solucion, arranca igual).
#   4. SESSION_CONFIG_DEFAULTS: valores que heredan TODAS las configuraciones.
#        real_world_currency_per_point = 0.10  -> 1 ECU = 10 centavos
#        participation_fee = 50.00             -> pago por participar (MXN)
#      Se pueden cambiar al crear una sesión (Sessions > Create > Configure
#      session) sin editar este archivo.
#   5. PARTICIPANT_FIELDS / SESSION_FIELDS: variables que deben sobrevivir entre
#      apps y rondas (participant.tratamiento, .rol, .ronda_pagada; se usan
#      desde la sesión 5). oTree solo acepta participant.<campo> si el campo
#      está en esta lista.
#   6. Moneda: USE_POINTS = True con POINTS_CUSTOM_NAME = 'ECU' hace que cu(100)
#      se muestre como "100 ECU". Al final, pago_final convierte a pesos:
#      ECU x 0.10 + 50 MXN (participant.payoff_plus_participation_fee()).
#   7. ROOMS: salas con un enlace fijo para todas las estaciones del laboratorio.
#   8. ADMIN_USERNAME / ADMIN_PASSWORD: acceso a la interfaz administrativa. La
#      contraseña NUNCA se escribe aquí: se lee de la variable de entorno
#      OTREE_ADMIN_PASSWORD. Con `otree devserver` en su computadora no se pide.
#   9. DEMO_PAGE_INTRO_HTML: el texto de la página Demo. SECRET_KEY: clave interna
#      de oTree (esta es solo para clase; en un servidor real se cambia).
#
# PARA LA CLASE DE LA SESIÓN 2
#   - Busquen 's2_plantilla' y sigan su app_sequence hasta la carpeta
#     s2_dictador: así se conecta el menú del Demo con el código.
#   - PLAYERS_PER_GROUP y NUM_ROUNDS NO están aquí: están en la clase C del
#     __init__.py de cada app.
#   - Error frecuente: "No session config with name 's2_plantilla'" significa
#     que falta $env:PLANTILLAS="s2" en ESA ventana de la terminal.
# ==================================================================

SESSION_CONFIGS = [
    # ---------------- Sesión 2 ----------------
    dict(
        name='s2_solucion',
        display_name='S2 · Dictador básico (solución)',
        app_sequence=['s2_dictador_solucion', 'pago_final'],
        num_demo_participants=2,
    ),
    # ---------------- Sesión 5 ----------------
    # Con emparejamiento aleatorio se necesitan al menos 8 personas
    # (dos parejas por tratamiento); con 4, el "aleatorio" sería fijo.
    dict(
        name='s5_solucion_fijo',
        display_name='S5 · Dictador extendido, pareja fija (solución)',
        app_sequence=['s5_dictador_ext_solucion', 'pago_final'],
        num_demo_participants=8,
        emparejamiento='fijo',
    ),
    dict(
        name='s5_solucion_aleatorio',
        display_name='S5 · Dictador extendido, parejas aleatorias (solución)',
        app_sequence=['s5_dictador_ext_solucion', 'pago_final'],
        num_demo_participants=8,
        emparejamiento='aleatorio',
    ),
    # ---------------- Sesión 6 ----------------
    dict(
        name='s6_con_errores',
        display_name='S6 · Dictador extendido con errores sembrados',
        app_sequence=['s6_dictador_con_errores', 'pago_final'],
        num_demo_participants=8,
        emparejamiento='aleatorio',
        timeout_decision=90,
    ),
    # ---------------- Datos simulados de la sesión 7 ----------------
    # Configuraciones docentes: regeneran analisis/datos_simulados/ (solo se
    # muestran en la copia docente, donde está la app de solución).
    dict(
        name='sim_fijo',
        display_name='Docente · datos simulados, sesión 1 (fija)',
        app_sequence=['s5_dictador_ext_solucion', 'pago_final'],
        num_demo_participants=16,
        emparejamiento='fijo',
        semilla=2026,
        timeout_decision=90,
        etiqueta_sim='s5_solucion_fijo',
    ),
    dict(
        name='sim_aleatorio',
        display_name='Docente · datos simulados, sesión 2 (aleatoria)',
        app_sequence=['s5_dictador_ext_solucion', 'pago_final'],
        num_demo_participants=20,
        emparejamiento='aleatorio',
        semilla=2027,
        timeout_decision=90,
        etiqueta_sim='s5_solucion_aleatorio',
    ),
]

# Las plantillas del equipo se activan con la variable de entorno PLANTILLAS,
# una por una, para que una plantilla incompleta no impida usar la otra:
#   PowerShell:  $env:PLANTILLAS="s2"; otree devserver
#                $env:PLANTILLAS="s5"; otree devserver
#   Git Bash:    PLANTILLAS=s2 otree devserver
# La variable vale para esa ventana de la terminal: los bots se corren en la
# misma ventana (o se vuelve a definir en otra).
# Mientras quede un "___" fuera de una función, el servidor no arranca: el
# NameError aparece en la terminal con el archivo y la línea pendiente.
PLANTILLAS = [x.strip() for x in environ.get('PLANTILLAS', '').split(',') if x.strip()]

if 's2' in PLANTILLAS:
    SESSION_CONFIGS.append(
        dict(
            name='s2_plantilla',
            display_name='S2 · Dictador básico (PLANTILLA del equipo)',
            app_sequence=['s2_dictador', 'pago_final'],
            num_demo_participants=2,
        )
    )
if 's5' in PLANTILLAS:
    SESSION_CONFIGS += [
        dict(
            name='s5_plantilla',
            display_name='S5 · Dictador extendido, parejas aleatorias (PLANTILLA del equipo)',
            app_sequence=['s5_dictador_ext', 'pago_final'],
            num_demo_participants=8,
            emparejamiento='aleatorio',
        ),
        dict(
            name='s5_plantilla_fijo',
            display_name='S5 · Dictador extendido, pareja fija (PLANTILLA del equipo)',
            app_sequence=['s5_dictador_ext', 'pago_final'],
            num_demo_participants=8,
            emparejamiento='fijo',
        ),
    ]

# Solo se muestran las configuraciones cuyas apps existen en esta carpeta.
# Así, el paquete de estudiantes (sin carpetas *_solucion) arranca igual.
SESSION_CONFIGS = [
    c for c in SESSION_CONFIGS
    if all((_Path(__file__).parent / app / '__init__.py').is_file() for app in c['app_sequence'])
]

SESSION_CONFIG_DEFAULTS = dict(
    # 1 ECU = 0.10 MXN; con 100 ECU de dotación, una ronda paga como máximo 10 MXN
    real_world_currency_per_point=0.10,
    participation_fee=50.00,
    # 'fijo' o 'aleatorio' (cualquier otro valor detiene la creación de la sesión)
    emparejamiento='aleatorio',
    # Semilla de la asignación aleatoria: un entero la hace reproducible; 0 = sin semilla.
    # Se puede cambiar al crear la sesión (Sessions > Create > Configure session).
    semilla=0,
    # Segundos que tiene A para decidir; 0 = sin límite (en una sesión real conviene 90).
    timeout_decision=0,
    doc='',
)

PARTICIPANT_FIELDS = ['tratamiento', 'rol', 'ronda_pagada']
SESSION_FIELDS = []

LANGUAGE_CODE = 'es'
REAL_WORLD_CURRENCY_CODE = 'MXN'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECU'

ROOMS = [
    dict(name='diplomado', display_name='Diplomado · sala de prueba'),
]

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
<p><strong>Diplomado básico en economía experimental</strong> · BEER Lab.</p>
<p>Para ver la plantilla de su equipo, arranque el servidor en PowerShell con
<code>$env:PLANTILLAS="s2"; otree devserver</code> (o <code>"s5"</code>).
Sin esa variable solo aparece la app de la sesión 6.</p>
"""

SECRET_KEY = 'diplomado-beer-lab-solo-para-clase'

INSTALLED_APPS = ['otree']
