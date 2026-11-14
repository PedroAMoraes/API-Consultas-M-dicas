from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from rest_framework.test import APITestCase
from consultas.models import Consulta
from profissionais.models import Profissional


class ConsultaAPITests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                                        username="api-tester",
                                        password="SenhaTeste@P1"
                                    )
        self.profissional = Profissional.objects.create(
                                        nome_social="João Silva",
                                        profissao="Cardiologista",
                                        endereco="Rua Principal, 123",
                                        contato="js@gmail.com"
                                    )
        self.consulta = Consulta.objects.create(
                                        data= "2026-11-13T14:30:00Z",
                                        profissional= self.profissional
                                    )


        self.urls = {
            'get_all': reverse('get_all_consultas'),
            'get_by_id': reverse('get_consulta', kwargs={'pk':self.consulta.pk}),
            'create': reverse('add_consulta'),
            'update': reverse('update_consulta', kwargs={'pk':self.consulta.pk}),
            'delete': reverse('delete_consulta', kwargs={'pk':self.consulta.pk}),
        }

        self.client.force_authenticate(user=self.user)

    def test_get_all_consultas(self):
        response = self.client.get(self.urls['get_all'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_consulta(self):
        response = self.client.get(self.urls['get_by_id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            parse_datetime(response.data['data']),
            parse_datetime(str(self.consulta.data)),
        )

    def test_create_consulta(self):
        consulta_nova = {
                                'data': "2027-11-13T14:30:00Z",
                                'profissional': self.profissional.pk
                            }
        response = self.client.post(self.urls['create'], consulta_nova, format= 'json')
        self.assertEqual(response.status_code, 201)

    def test_update_consulta(self):
        consulta_nova = {
            'data': "2029-12-22T09:30:00Z",
            'profissional': self.profissional.pk,
        }
        response = self.client.put(self.urls['update'], consulta_nova, format='json') 
        self.assertEqual(response.status_code, 200)

    def test_delete_consulta(self):
        response = self.client.delete(self.urls['delete']) 
        self.assertEqual(response.status_code, 202)
        self.assertFalse(Consulta.objects.filter(pk=self.consulta.pk).exists())

    def test_create_consulta_rejects_missing_data(self):
        qts_consultas_antes = Consulta.objects.count()
        data = {
            'data': "2029-12-22T09:30:00Z",
            'profissional': self.profissional.pk,
        }
        del data['data']

        response = self.client.post(self.urls['create'], data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('data', response.data)
        self.assertEqual(Consulta.objects.count(), qts_consultas_antes)

    def test_create_consulta_missing_profissional(self):
        qts_consultas_antes = Consulta.objects.count()
        data = {
            'data': "2029-12-22T09:30:10Z",
            'profissional': self.profissional.pk,
        }
        del data['profissional']

        response = self.client.post(self.urls['create'], data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('profissional', response.data)
        self.assertEqual(Consulta.objects.count(), qts_consultas_antes)

    def test_create_consulta_rejects_invalid_data(self):
        qts_consultas_antes = Consulta.objects.count()
        data = {
            'data': "texto, não data",
            'profissional': self.profissional.pk,
        }

        response = self.client.post(self.urls['create'], data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('data', response.data)
        self.assertEqual(Consulta.objects.count(), qts_consultas_antes)

    def test_create_consulta_rejects_invalid_profissional(self):
        qts_consultas_antes = Consulta.objects.count()
        data = {
            'data': "2029-12-22T09:30:10Z",
            'profissional': self.profissional.pk + 9000,
        }

        response = self.client.post(self.urls['create'], data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('profissional', response.data)
        self.assertEqual(Consulta.objects.count(), qts_consultas_antes)

    def test_consulta_list_rejects_unknown_filter(self):
        response = self.client.get(reverse('get_all_consultas'), {'password': 'd'})

        self.assertEqual(response.status_code, 400)
        self.assertIn('query_params', response.data)

    def test_consulta_list_filters_by_profissional_name(self):
        Consulta.objects.create(
            data=parse_datetime('2026-11-13T14:30:00-03:00'), 
            profissional=self.profissional
        )

        response = self.client.get(reverse('get_all_consultas'), {'nome_profissional': 'silva'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_consulta_list_filters_by_profissional_id(self):
        outro_profissional = Profissional.objects.create(
            nome_social='Maria Souza',
            profissao='Dermatologista',
            endereco='Rua Secundária, 45',
            contato='maria@example.com',
        )
        Consulta.objects.create(
            data=parse_datetime('2026-11-14T10:00:00Z'),
            profissional=outro_profissional,
        )

        response = self.client.get(
            self.urls['get_all'],
            {'profissional': self.profissional.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['info_profissional']['id'],
            self.profissional.pk,
        )
