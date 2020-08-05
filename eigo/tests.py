from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.shortcuts import reverse

from .models import Phrase, Example


class PhraseModelTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='phraseuser',
            email='phraseuser@email.com',
            password='testpass1234')
        self.phrase = Phrase.objects.create(
            phrase='example phrase',
            user=self.user)
        self.example = Example.objects.create(
            phrase=self.phrase,
            user=self.user,
            example='example text')

    def test_phrase_has_created(self):
        self.assertEqual(Phrase.objects.all().count(), 1)

    def test_example_has_created(self):
        self.assertEqual(Example.objects.all().count(), 1)

    def test_phrase_foreignkey(self):
        self.assertEqual(self.phrase.examples.all().count(), 1)

    def test_inactive_phrase(self):
        Phrase.objects.create(
            phrase='inactive phrase',
            user=self.user,
            is_active=False)
        self.assertEqual(Phrase.objects.all().count(), 1)

    def test_inactive_example(self):
        Example.objects.create(
            phrase=self.phrase,
            user=self.user,
            example='inactive example text',
            is_active=False)
        self.assertEqual(Example.objects.all().count(), 1)


class PhraseViewTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='phraseuser',
            email='phraseuser@email.com',
            password='testpass1234')
        self.phrase = Phrase.objects.create(
            phrase='example phrase',
            user=self.user)
        self.example = Example.objects.create(
            phrase=self.phrase,
            user=self.user,
            example='example text')

    def test_phrase_list_view(self):
        self.client.login(email='phraseuser@email.com',
                          password='testpass1234')
        response = self.client.get(reverse('eigo:eigo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'example phrase')
        self.assertTemplateUsed(response, 'eigo/eigo_list.html')

    def test_phrase_list_view_user_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('eigo:eigo_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/' %
                             (reverse('account_login')))
        response = self.client.get('%s?next=/' %
                                   (reverse('account_login')))
        self.assertContains(response, 'Log In')

    def test_phrase_list_view_search(self):
        self.client.login(email='phraseuser@email.com',
                          password='testpass1234')
        response = self.client.get(reverse('eigo:eigo_list') + '?search=test')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'example phrase')
        self.assertTemplateUsed(response, 'eigo/eigo_list.html')

    def test_phrase_detail_view(self):
        self.client.login(email='phraseuser@email.com',
                          password='testpass1234')
        response = self.client.get(self.phrase.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'example phrase')
        self.assertContains(response, 'example text')
        self.assertTemplateUsed(response, 'eigo/eigo_detail.html')
        no_response = self.client.get('/no-response/')
        self.assertEqual(no_response.status_code, 404)

    # def test_phrase_new_view(self):
    #     self.client.login(email='phraseuser@email.com',
    #                       password='testpass1234')
    #     post_data = {
    #         'phrase': 'post phrase',
    #         'user': self.user,
    #         'examples': [],
    #         'snaps': [],
    #     }
    #     response = self.client.post(reverse('eigo:eigo_new'), data=post_data)
    #     self.assertEqual(response.status_code, 201)
    #     self.assertTemplateUsed(response, 'eigo/eigo_form.html')
