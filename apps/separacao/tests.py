from datetime import date, timedelta

from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Separacao


class SeparacaoJsonEndpointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ajax_temp",
            email="ajax_temp@example.com",
            password="SenhaTeste123",
        )
        self.user.user_permissions.set(
            Permission.objects.filter(
                codename__in=["access_separacao", "edit_record"],
            )
        )
        self.separacao = Separacao.objects.create(
            data=date(2026, 7, 2),
            romaneio="ROM-AJAX",
            documento="DOC-AJAX",
            grupo="GRP",
            quantidade=1,
            vencimento=timezone.localdate() + timedelta(days=3),
            tipo=Separacao.Tipo.NORMAL,
            status=Separacao.Status.ABERTA,
            quantidade_pendente=1,
            status_operacional=Separacao.StatusOperacional.PENDENTE,
            status_documento=Separacao.StatusDocumento.VALIDO,
            quantidade_conferida=0,
            status_autorizacao=Separacao.StatusAutorizacao.PENDENTE,
            atribuido=self.user,
            anotacoes="Prioridade operacional",
        )

    def test_indicadores_json_respeita_filtros(self):
        client = Client(HTTP_HOST="127.0.0.1")
        client.login(username="ajax_temp", password="SenhaTeste123")

        response = client.get(
            reverse("separacao:indicadores_json"),
            {"documento": "DOC-AJAX"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["indicadores"]["total"], 1)

    def test_atualizar_status_json_com_csrf(self):
        client = Client(HTTP_HOST="127.0.0.1", enforce_csrf_checks=True)
        client.login(username="ajax_temp", password="SenhaTeste123")
        client.get(reverse("separacao:list"))
        csrf_token = client.cookies["csrftoken"].value

        response = client.post(
            reverse(
                "separacao:atualizar_status_json",
                kwargs={"pk": self.separacao.pk},
            ),
            data='{"field":"status_operacional","value":"em_separacao"}',
            content_type="application/json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.separacao.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertEqual(
            self.separacao.status_operacional,
            Separacao.StatusOperacional.EM_SEPARACAO,
        )

    def test_atualizar_status_json_sem_csrf_e_bloqueado(self):
        client = Client(HTTP_HOST="127.0.0.1", enforce_csrf_checks=True)
        client.login(username="ajax_temp", password="SenhaTeste123")

        response = client.post(
            reverse(
                "separacao:atualizar_status_json",
                kwargs={"pk": self.separacao.pk},
            ),
            data='{"field":"status_operacional","value":"em_separacao"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

    def test_busca_datatable_json_retorna_colunas_operacionais(self):
        client = Client(HTTP_HOST="127.0.0.1")
        client.login(username="ajax_temp", password="SenhaTeste123")

        response = client.get(
            reverse("separacao:busca_datatable_json"),
            {
                "q": "DOC-AJAX",
                "grupo": "GRP",
                "status_operacional": Separacao.StatusOperacional.PENDENTE,
                "atribuido": self.user.pk,
                "vencimento": "proximos",
            },
        )

        payload = response.json()
        registro = payload["results"][0]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["total"], 1)
        self.assertEqual(registro["documento"], "DOC-AJAX")
        self.assertEqual(registro["romaneio"], "ROM-AJAX")
        self.assertEqual(registro["qtd_doc"], 1)
        self.assertEqual(registro["qtde_pen"], 1)
        self.assertIn("detalhe", registro["acoes"])
        self.assertIn("editar", registro["acoes"])
        self.assertIn("excluir", registro["acoes"])
