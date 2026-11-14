from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from consultas.models import Consulta
from profissionais.models import Profissional


class ProfissionalAPITests(APITestCase):
    def setUp(self):
            self.user = get_user_model().objects.create_user(
                                            username="api-tester",
                                            password="SenhaTeste@P1"
                                        )
            self.profissional = Profissional.objects.create(
                                            nome="João Silva",
                                            profissao="Cardiologista",
                                            endereco="Rua Principal, 123",
                                            contato="js@gmail.com"
                                        )
    
            self.urls = {
                'get_all': reverse('get_all_profissionais'),
                'get_by_id': reverse('get_profissional', kwargs={'pk':self.profissional.pk}),
                'create': reverse('add_profissional'),
                'update': reverse('update_profissional', kwargs={'pk':self.profissional.pk}),
                'delete': reverse('delete_profissional', kwargs={'pk':self.profissional.pk}),
            }
    
            self.client.force_authenticate(user=self.user)

    def teste_get_all(self):
        response = self.client.get(self.urls['get_all'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def teste_get_by_id(self):
        response = self.client.get(self.urls['get_by_id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nome'], self.profissional.nome)

    def teste_create(self):
        novo_profissional = {
            'nome': "Caio Gomes",
            'profissao': "Terapeuta",
            'endereco': "Avenida Tiradentes, 230",
            'contato': "drgomes@email.com"
        }
        
        response = self.client.post(self.urls['create'], novo_profissional, format='json')
        self.assertEqual(response.status_code, 200)

    def teste_update(self):
        novo_profissional = {
            'nome': "João Silva",
            'profissao': "Cardiologista",
            'endereco': "Rua Principal, 123",
            'contato': "drjoao@gmail.com"  
            }
        
        response = self.client.put(self.urls['update'], novo_profissional, format='json') 
        self.assertEqual(response.status_code, 200)

    def teste_delete(self):
        response = self.client.delete(self.urls['delete']) 
        self.assertEqual(response.status_code, 202)
        self.assertFalse(Consulta.objects.filter(pk=self.profissional.pk).exists())
 
    def testt_create_rejects_missing_required_field(self):
        novo_profissional = {
                    'nome': "Pedro Silva",
                    'profissao': "Radiologista",
                    'endereco': "Rua Nova, 123",
                    'contato': "pds@gmail.com"  
                    }
        del novo_profissional['nome']

        response = self.client.post(self.urls['create'], novo_profissional, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('nome', response.data)
        self.assertEqual(Profissional.objects.count(), 1)

    def test_list_rejects_unknown_filter(self):
        response = self.client.get(self.urls['get_all'], {'password': 'd'})

        self.assertEqual(response.status_code, 400)
        self.assertIn('query_params', response.data)

    def test_profissional_list_filters_by_name(self):
        Profissional.objects.create(
            nome="Paulo Gustavo",
            profissao="Dentista",
            endereco="Rua Principal, 123",
            contato="paulogu@gmail.com"
        )

        response = self.client.get(self.urls['get_all'], {'nome': 'silva'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item['nome'] for item in response.data], ['João Silva'])
