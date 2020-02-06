from unittest import mock

from django.test import TestCase

from mprj_api.db_routers import DominioRouter


class DominioDbTest(TestCase):

    def test_db_router(self):
        router = DominioRouter()
        model = mock.MagicMock()
        model._meta.app_label = 'dominio'

        result = router.db_for_read(model)
        self.assertEqual(result, 'dominio_db')
