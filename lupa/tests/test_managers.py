from django.test import TestCase
from model_mommy.mommy import make

from lupa.models import DadoEntidade


class ManagerTest(TestCase):

    def test_get_authorized(self):
        permissao = 'ROLE_allowed'
        entidade = make('lupa.Entidade')
        grupo_ok = make('lupa.Grupo', role=permissao)
        grupo_fail = make('lupa.Grupo')
        dado_ok = make(
            'lupa.DadoEntidade',
            entity_type=entidade,
            roles_allowed=[grupo_ok]
        )
        make(
            'lupa.DadoEntidade',
            entity_type=entidade,
            roles_allowed=[grupo_fail]
        )

        queryset = DadoEntidade.objects.get_authorized([permissao])

        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0].id, dado_ok.id)
