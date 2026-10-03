from otree.api import *
from otree.database import db

from . import *


def refrescar():
    # Los bots leen la base de datos con una conexión propia que guarda en
    # memoria los objetos ya leídos. Antes de verificar valores que cambiaron
    # en el servidor (pagos), se descarta esa memoria.
    db.commit()


class PlayerBot(Bot):
    # Tres casos: envío mínimo, intermedio y máximo
    cases = [0, 40, 100]

    def play_round(self):
        enviado = cu(self.case)
        # Los bots también leen la pantalla: las instrucciones deben estar visibles
        expect('El Participante B no toma ninguna decisión', 'in', self.html)
        yield Instrucciones
        # La respuesta incorrecta debe ser rechazada
        yield SubmissionMustFail(Comprension, dict(comprension=cu(70)))
        yield Comprension, dict(comprension=cu(30))  # respuesta tomada del protocolo, no de C
        if self.player.role == C.A_ROLE:
            # Fuera de rango: debe fallar
            yield SubmissionMustFail(Decision, dict(enviado=C.DOTACION + 1))
            yield Decision, dict(enviado=enviado)
        # Los pagos se calculan en la página de espera. El bot verifica después de
        # pasarla; refrescar() descarta la copia en memoria de la base.
        yield Resultados
        refrescar()
        a = self.group.get_player_by_role(C.A_ROLE)
        b = self.group.get_player_by_role(C.B_ROLE)
        expect(a.payoff + b.payoff, C.DOTACION)
        expect(b.payoff, enviado)
