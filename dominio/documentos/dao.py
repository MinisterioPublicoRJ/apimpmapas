from datetime import datetime


class MinutaPrescricaoDAO:
    @classmethod
    def get(cls, docu_dk, matricula):
        today = datetime.now()

        context = {
            "matricula_promotor": matricula,
            "data_hoje": today,
            "num_procedimento": docu_dk
        }

        return context

