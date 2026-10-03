from otree.api import *
from . import *


class PlayerBot(Bot):
    def play_round(self):
        # La pantalla final no tiene botón "Siguiente": el bot no la envía.
        # Verificación: total = ganancias convertidas a pesos + pago por participar.
        pp = self.participant
        esperado = pp.payoff.to_real_world_currency(self.session) + self.session.config['participation_fee']
        expect(pp.payoff_plus_participation_fee(), esperado)
        expect('Total a recibir', 'in', self.html)
