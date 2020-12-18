from unittest import mock
import pytest

from django.test import TestCase

from dominio.tests.testconf import NoJWTTestCase, NoCacheTestCase
from dominio.suamesa.exceptions import APIMissingRequestParameterSuaMesa
from dominio.suamesa.dao_functions import (
    get_vistas,
    get_tutela_investigacoes,
    get_tutela_processos,
    get_pip_inqueritos,
    get_pip_pics,
    get_pip_aisp,
    get_tutela_finalizados,
    get_pip_finalizados,
)


class TestSuaMesaFunctions(NoJWTTestCase, NoCacheTestCase, TestCase):
    @mock.patch('dominio.suamesa.dao_functions.Vista')
    def test_get_vistas(self, _Vista):
        manager_mock = mock.MagicMock()
        manager_mock.count.return_value = 1
        _Vista.vistas.abertas_promotor.return_value = manager_mock

        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {'cpf': '1234'}

        output = get_vistas(orgao_id, mock_request)

        self.assertEqual(output, 1)
        _Vista.vistas.abertas_promotor.assert_called_once_with(
            orgao_id, '1234'
        )
        manager_mock.count.assert_called_once_with()

    def test_get_vistas_no_cpf(self):
        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        with pytest.raises(APIMissingRequestParameterSuaMesa):
            get_vistas(orgao_id, mock_request)

    @mock.patch('dominio.suamesa.dao_functions.Documento')
    def test_get_tutela_investigacoes(self, _Documento):
        _Documento.investigacoes.em_curso.return_value = 1
        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        output = get_tutela_investigacoes(orgao_id, mock_request)

        self.assertEqual(output, 1)
        _Documento.investigacoes.em_curso.assert_called_once_with(
            orgao_id, [51219, 51220, 51221, 51222, 51223, 392, 395],
            remove_out=True
        )

    @mock.patch('dominio.suamesa.dao_functions.Documento')
    def test_get_tutela_processos(self, _Documento):
        _Documento.processos.em_juizo.return_value = 1
        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}
        regras = [
            441, 177, 175, 176, 127, 18, 126, 159,
            320, 582, 323, 319, 51218, 51217, 51205
        ]

        output = get_tutela_processos(orgao_id, mock_request)

        self.assertEqual(output, 1)
        _Documento.processos.em_juizo.assert_called_once_with(
            orgao_id,
            regras
        )

    @mock.patch('dominio.suamesa.dao_functions.Documento')
    def test_get_pip_inqueritos(self, _Documento):
        _Documento.investigacoes.em_curso.return_value = 1
        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        output = get_pip_inqueritos(orgao_id, mock_request)

        self.assertEqual(output, 1)
        _Documento.investigacoes.em_curso.assert_called_once_with(
            orgao_id, [494, 3]
        )

    @mock.patch('dominio.suamesa.dao_functions.Documento')
    def test_get_pip_pics(self, _Documento):
        _Documento.investigacoes.em_curso.return_value = 1
        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        output = get_pip_pics(orgao_id, mock_request)

        self.assertEqual(output, 1)
        _Documento.investigacoes.em_curso.assert_called_once_with(
            orgao_id, [590]
        )

    @mock.patch('dominio.suamesa.dao_functions.get_orgaos_same_aisps')
    @mock.patch('dominio.suamesa.dao_functions.Documento')
    def test_get_pip_aisp(self, _Documento, _get_orgaos_aisp):
        _Documento.investigacoes.em_curso_grupo.return_value = 1
        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        _get_orgaos_aisp.return_value = "", [1, 2]

        output = get_pip_aisp(orgao_id, mock_request)

        self.assertEqual(output, 1)
        _Documento.investigacoes.em_curso_grupo.assert_called_once_with(
            [1, 2], [494, 3, 590]
        )
        _get_orgaos_aisp.assert_called_once_with(orgao_id)

    @mock.patch('dominio.suamesa.dao_functions.SubAndamento')
    def test_get_tutela_finalizados(self, _SubAndamento):
        regras_ajuizamento = (6251, )
        regras_tac = (6655, 6326)
        regras_arquiv = (7912, 6548, 6326, 6681, 6678, 6645, 6682, 6680, 6679,
                         6644, 6668, 6666, 6665, 6669, 6667, 6664, 6655, 6662,
                         6659, 6658, 6663, 6661, 6660, 6657, 6670, 6676, 6674,
                         6673, 6677, 6675, 6672, 6018, 6341, 6338, 6019, 6017,
                         6591, 6339, 6553, 7871, 6343, 6340, 6342, 6021, 6334,
                         6331, 6022, 6020, 6593, 6332, 7872, 6336, 6333, 6335,
                         7745, 6346, 6345, 6015, 6016, 6325, 6327, 6328, 6329,
                         6330, 6337, 6344, 6656, 6671, 7869, 7870, 6324, 7834,
                         7737, 6350)

        regras = regras_ajuizamento + regras_tac + regras_arquiv
        manager_mock = mock.MagicMock()

        _SubAndamento.finalizados.trinta_dias.return_value = manager_mock
        manager_mock.count.return_value = 1

        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        output = get_tutela_finalizados(orgao_id, mock_request)

        self.assertEqual(output, 1)
        _SubAndamento.finalizados.trinta_dias.assert_called_once_with(
            orgao_id, regras
        )
        manager_mock.count.assert_called_once_with()

    @mock.patch('dominio.suamesa.dao_functions.SubAndamento')
    def test_get_pip_finalizados(self, _SubAndamento):
        regras_arquiv = (6682, 6669, 6018, 6341, 6338, 6019, 6017, 6591, 6339,
                         7871, 6343, 6340, 6342, 7745, 6346, 7915, 6272, 6253,
                         6392, 6377, 6378, 6359, 6362, 6361, 6436, 6524, 7737,
                         7811, 6625, 6718, 7834, 6350)

        manager_mock = mock.MagicMock()

        _SubAndamento.finalizados.trinta_dias.return_value = manager_mock
        manager_mock.count.return_value = 1

        orgao_id = 10
        mock_request = mock.MagicMock()
        mock_request.GET = {}

        output = get_pip_finalizados(orgao_id, mock_request)

        self.assertEqual(output, 1)
        _SubAndamento.finalizados.trinta_dias.assert_called_once_with(
            orgao_id, regras_arquiv
        )
        manager_mock.count.assert_called_once_with()
