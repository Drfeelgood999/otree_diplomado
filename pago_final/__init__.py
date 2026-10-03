from otree.api import *

doc = """
Pantalla final común: muestra el pago total en ECU, su conversión a pesos y
la tarifa de participación. Se coloca al final de cualquier app_sequence.
"""


class C(BaseConstants):
    NAME_IN_URL = 'pago_final'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class PagoFinal(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return dict(
            pago_ecu=participant.payoff,
            pago_pesos=participant.payoff.to_real_world_currency(player.session),
            tarifa=player.session.config['participation_fee'],
            total=participant.payoff_plus_participation_fee(),
        )


page_sequence = [PagoFinal]
