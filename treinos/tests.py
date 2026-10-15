from unittest.mock import Mock, patch

import requests
from django.test import SimpleTestCase

from .views import _gerar_e_salvar_plano


class GeminiErrorTests(SimpleTestCase):
    @patch('treinos.views.gerar_plano_treino')
    def test_erro_403_mostra_detalhe_e_orientacao_de_permissoes(self, gerar_plano):
        response = Mock(status_code=403)
        response.json.return_value = {
            'error': {'message': 'This API key does not have permission to use this API.'}
        }
        gerar_plano.side_effect = requests.HTTPError(response=response)

        plano, erro = _gerar_e_salvar_plano(object())

        self.assertIsNone(plano)
        self.assertIn('permissões do projeto', erro)
        self.assertIn('This API key does not have permission', erro)

    @patch('treinos.views.gerar_plano_treino')
    def test_erro_http_sem_corpo_json_tem_fallback(self, gerar_plano):
        response = Mock(status_code=403)
        response.json.side_effect = ValueError('invalid JSON')
        gerar_plano.side_effect = requests.HTTPError(response=response)

        plano, erro = _gerar_e_salvar_plano(object())

        self.assertIsNone(plano)
        self.assertIn('confira a chave', erro)
        self.assertNotIn('Detalhe:', erro)