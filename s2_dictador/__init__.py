from otree.api import *
#En esta sección se importan las herramientas de oTree que se usarán en el juego. 
#Es importanta importar con "*" para que se incluyan todas las funciones y clases disponibles.

doc = """
Sesión 2 · Juego del dictador básico (PLANTILLA).

Instrucciones para el equipo:
  - Hay 9 huecos (COMPLETAR S2.1 a S2.9): ocho en este archivo (S2.4 y S2.5
    tienen dos "___" cada uno) y S2.9 en Decision.html.
  - Trabaje en orden. Active la plantilla con la variable PLANTILLAS:
        PowerShell:  $env:PLANTILLAS="s2"; otree devserver
    Mientras quede un "___" fuera de una función, el servidor NO arranca: el
    NameError aparece en la terminal con el archivo y la línea. Complete el
    hueco, guarde y vuelva a ejecutar el comando. Los huecos que están
    dentro de una función (S2.3, S2.4 y S2.6) solo fallan cuando esa función
    se ejecuta: por eso los bots son indispensables.
  - Cada hueco se resuelve con una o dos líneas. La documentación de oTree
    (Models, Pages, Forms, Templates) tiene todo lo necesario.
  - Al terminar, ejecute los bots en la misma terminal (con PLANTILLAS=s2):
        PowerShell:  $env:PLANTILLAS="s2"; otree test s2_plantilla

Dos participantes por grupo. A recibe una dotación y decide cuánto enviar a B;
B no toma decisiones. Una sola ronda. Pagos en ECU.
Referencias: Kahneman, Knetsch y Thaler (1986); Forsythe et al. (1994).
"""
#Las triples comillas permiten escribir un texto largo en varias líneas.


# ---------------------------------------------------------------- Clases
class C(BaseConstants):
    NAME_IN_URL = 's2_dictador'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    # COMPLETAR S2.1: la dotación de A es de 100 ECU (use cu(...))
    DOTACION = cu(100) #Cu = currency unit
    # oTree asigna el rol según id_in_group (1 = A, 2 = B); los grupos se barajan en creating_session.
    A_ROLE = 'Participante A'
    B_ROLE = 'Participante B'
    # Respuesta correcta de la pregunta de comprensión
    RESPUESTA_COMPRENSION = cu(30) #SI ESTUVIESE ESCRITO EN ORDEN, esto se declararía al final
    #Contiene valores generales del diseño, permanecen igual en todo momento.


class Subsession(BaseSubsession):
    pass

#Crea una clase Subession que hereda características de BaseSubsession.
#Pass significa que no es necesario hacer nada.

"""Una Session es la ejecución completa del ecperimento: todas las personas, aplicaciones y rondas
Una Subsession es una ronda específica de una aplicación para TODOS los participantes.

Por ejemplo: Si participaran cuatro personas en una ronda del juego del dictador, creacriamos
1 session completa
2 Groups de 2 personas cada uno
4 Players, uno por cada persona en esa ronda
Si el experimento tuviera 3 rondas, creariamos 3 Subsessions,"""

class Group(BaseGroup):
    # Representa una pareja formada por un Participante A y un Participante B.
    # Decisión de A: una sola observación por grupo -> se guarda en Group
    # COMPLETAR S2.2: campo de moneda "enviado", con mínimo 0, máximo la dotación
    # y la etiqueta '¿Cuántos ECU desea enviar al Participante B?'
    enviado = models.CurrencyField(
    min = 0,
    max = C.DOTACION,
    label = '¿Cuántos ECU desea enviar al Participante B?'
    )
    


class Player(BasePlayer):
    comprension = models.CurrencyField(
        label='Si A envía 30 ECU, ¿cuántos ECU recibe B?',
        doc='Respuesta a la pregunta de comprensión (debe ser 30).',
    )

    """La compresión si pertenece a Player porque es una pregunta individual, no de grupo. Cada parjea
    deberá tener una sóla cantidad de enviado,
    de comprensión, y de pago. La pregunta de comprensión es individual.""" 


# ---------------------------------------------------------------- funciones
# Una función es como una receta, le estamos enseñando a python que hacer cuando oTree la llame.
def creating_session(subsession: Subsession):
    # Por omisión oTree forma las parejas en orden de participante (de llegada).
    # Para que "al azar" sea verdad, se barajan: el rol lo sigue dando id_in_group.
    subsession.group_randomly() #LE ordena a la ronda randomizar participantes antes de formar parejas.


def comprension_error_message(player: Player, value):
    # oTree llama a <campo>_error_message al enviar el formulario
    # COMPLETAR S2.3: si la respuesta no es la correcta, devuelva un mensaje de error
    if value != C.RESPUESTA_COMPRENSION:
        return 'Respuesta incorrecta. Revise las instrucciones e intente de nuevo.'


def set_payoffs(group: Group):
    a = group.get_player_by_role(C.A_ROLE)
    b = group.get_player_by_role(C.B_ROLE)
    # COMPLETAR S2.4: pagos de A y de B según el protocolo
    a.payoff = C.DOTACION - group.enviado
    b.payoff = group.enviado


# ---------------------------------------------------------------- páginas
def vars_instrucciones(player: Player):
    # Variable que usa texto_instrucciones.html (se incluye en tres páginas)
    return dict(valor_ecu=cu(1).to_real_world_currency(player.session))
#Esta función devuelve un diccionario con la variable valor_ecu, que es el valor de 1 ECU en la moneda real.


class Instrucciones(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_instrucciones(player)
#Un staticmethod indica que la función no necesita trabajar con un objeto especial.


class Comprension(Page):
    form_model = 'player'
    form_fields = ['comprension']

    @staticmethod
    def vars_for_template(player: Player):
        return vars_instrucciones(player)


class Decision(Page):
    # COMPLETAR S2.5: ¿en qué modelo vive "enviado"? ¿qué campos muestra esta página?
    form_model = 'group'
    form_fields = ['enviado']

    @staticmethod
    def is_displayed(player: Player):
        # COMPLETAR S2.6: solo el Participante A ve esta página
        return player.role==C.A_ROLE

    @staticmethod
    def vars_for_template(player: Player):
        return vars_instrucciones(player)


class EsperaResultados(WaitPage):
    # COMPLETAR S2.7: ¿qué función se ejecuta cuando llegan los dos miembros de la pareja?
    after_all_players_arrive = set_payoffs
    body_text = 'Espere a que su pareja termine.'


class Resultados(Page):
    pass


# COMPLETAR S2.8: orden de las páginas (cinco clases definidas arriba)
page_sequence = [Instrucciones, Comprension, Decision, EsperaResultados, Resultados]
