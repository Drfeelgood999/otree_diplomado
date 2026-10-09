from otree.api import *
from otree.database import db

from . import *

# Bots del juego del ultimátum.
# Paso 7 de la tarea: copien este archivo a la carpeta ultimatum/ con el nombre tests.py
# (reemplazando el que venía del dictador) y corran:   otree test ultimatum


def refrescar():
    # Los bots leen la base de datos con una conexión propia que guarda en
    # memoria los objetos ya leídos. Antes de verificar valores que cambiaron
    # en el servidor (pagos), se descarta esa memoria.
    db.commit()


class PlayerBot(Bot):
    # Cinco casos: (ECU que A propone para B, ¿B acepta?)
    cases = [
        (0, True),
        (40, True),
        (40, False),
        (100, True),
        (100, False),
    ]

    def play_round(self):
        propuesta, acepta = self.case
        propuesta = cu(propuesta)

        # 1. Las instrucciones deben explicar qué pasa si B rechaza
        expect('Si B rechaza, ninguno de los dos recibe ECU', 'in', self.html)
        yield Instrucciones

        # 2. Comprensión: si B rechaza, B recibe 0. La respuesta 30 debe ser rechazada.
        yield SubmissionMustFail(Comprension, dict(comprension=cu(30)))
        yield Comprension, dict(comprension=cu(0))

        if self.player.role == C.A_ROLE:
            # 3. A propone; una propuesta mayor que la dotación debe ser rechazada
            yield SubmissionMustFail(Decision, dict(enviado=C.DOTACION + 1))
            yield Decision, dict(enviado=propuesta)
        else:
            # 4. B debe ver la propuesta en su pantalla antes de responder
            expect(str(propuesta), 'in', self.html)
            # Sin elegir una opción no se puede avanzar
            yield SubmissionMustFail(Respuesta, dict())
            yield Respuesta, dict(aceptado=acepta)

        # 5. Pagos: se calculan en la espera final; se verifican en Resultados
        yield Resultados
        refrescar()
        a = self.group.get_player_by_role(C.A_ROLE)
        b = self.group.get_player_by_role(C.B_ROLE)
        if acepta:
            expect(b.payoff, propuesta)
            expect(a.payoff, C.DOTACION - propuesta)
        else:
            expect(a.payoff, 0)
            expect(b.payoff, 0)
