"""This is a docstring which describes the module"""
from django.test import RequestFactory, TestCase
from . import models
from . import views
from . import forms


class TestViews(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = models.CustomUser.objects.create_user(
            email='test@test.com', password='Testing2022', username='Test', subscription=True)

    def test_delete_member_post(self):
        self.client.login(email='test@test.com', password='Testing2022')
        response = self.client.post(f'/members/delete_member/{self.user.id}')
        self.assertRedirects(response, '/accounts/login/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_delete_member_get(self):
        self.client.login(email='test@test.com', password='Testing2022')
        response = self.client.get(f'/members/delete_member/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'member/delete.html')

    def test_my_profile_post(self):
        self.client.login(email='test@test.com', password='Testing2022')
        form_data = {'phone': '0899895543', 'first_name': 'Test',
                     'last_name': 'Test', 'dob': '01/01/1999'}
        form = forms.MyCustomUserForm(data=form_data)
        request = self.factory.post('/members/my_profile', form_data)
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.my_profile(request)
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 302)

    def test_my_profile_post_warning(self):
        self.client.login(email='test@test.com', password='Testing2022')
        request = self.factory.post('/members/my_profile', )
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.my_profile(request)
        self.assertEqual(response.status_code, 200)

    def test_my_profile_get(self):
        self.client.login(email='test@test.com', password='Testing2022')
        request = self.factory.get('/members/my_profile')
        request.user = self.user
        response = views.my_profile(request)
        self.assertEqual(response.status_code, 200)

    def test_tree_get(self):
        self.client.login(email='test@test.com', password='Testing2022')
        request = self.factory.get('/members/tree')
        request.user = self.user
        response = views.tree(request)
        self.assertEqual(response.status_code, 200)

    def test_tree_get_familio_brother(self):
        self.client.login(email='test@test.com', password='Testing2022')
        models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Brother', name='Test')
        request = self.factory.get('/members/tree')
        request.user = self.user
        response = views.tree(request)
        self.assertEqual(response.status_code, 200)

    def test_tree_get_familio_wife(self):
        self.client.login(email='test@test.com', password='Testing2022')
        models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Wife', name='Test')
        request = self.factory.get('/members/tree')
        request.user = self.user
        response = views.tree(request)
        self.assertEqual(response.status_code, 200)

    def test_tree_get_familio_son(self):
        self.client.login(email='test@test.com', password='Testing2022')
        models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Son', name='Test')
        request = self.factory.get('/members/tree')
        request.user = self.user
        response = views.tree(request)
        self.assertEqual(response.status_code, 200)

    def test_tree_get_familio_mother(self):
        self.client.login(email='test@test.com', password='Testing2022')
        models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Mother', name='Test')
        request = self.factory.get('/members/tree')
        request.user = self.user
        response = views.tree(request)
        self.assertEqual(response.status_code, 200)

    def test_tree_get_familio_father(self):
        self.client.login(email='test@test.com', password='Testing2022')
        models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Father', name='Test')
        request = self.factory.get('/members/tree')
        request.user = self.user
        response = views.tree(request)
        self.assertEqual(response.status_code, 200)

    def test_tree_get_familio_father(self):
        self.client.login(email='test@test.com', password='Testing2022')
        models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Father', name='Test', email='test@test.com', approved=True)
        request = self.factory.get('/members/tree')
        request.user = self.user
        response = views.tree(request)
        self.assertEqual(response.status_code, 200)

    def test_group_get(self):
        self.client.login(email='test@test.com', password='Testing2022')
        request = self.factory.get('/members/group')
        request.user = self.user
        response = views.group(request)
        self.assertEqual(response.status_code, 200)

    def test_group_post(self):
        self.client.login(email='test@test.com', password='Testing2022')
        form_data = {'grp_name': 'Test_Group', 'member': self.user}
        request = self.factory.post(
            '/members/group', form_data)
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.group(request)
        self.assertEqual(response.status_code, 200)

    def test_edit_group_get(self):
        self.client.login(email='test@test.com', password='Testing2022')
        group = models.Group.objects.create(
            grp_name='Test_Group', member=self.user)
        request = self.factory.get(
            f'/members/edit_group/{group.id}')
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.edit_group(request, group.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_group(self):
        self.client.login(email='test@test.com', password='Testing2022')
        group = models.Group.objects.create(
            grp_name='Test_Group', member=self.user)
        request = self.factory.get(
            f'/members/delete_group/{group.id}')
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.delete_group(request, group.id)
        self.assertEqual(response.status_code, 302)

    def test_delete_invite(self):
        self.client.login(email='test@test.com', password='Testing2022')
        invite = models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Father', name='Test', email='test@test.com', approved=True)
        request = self.factory.get(
            f'/members/delete_invite/{invite.id}')
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.delete_invite(request, invite.id)
        self.assertEqual(response.status_code, 302)

    def test_edit_invite_post(self):
        self.client.login(email='test@test.com', password='Testing2022')
        invite = models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Father', name='Test', email='test@test.com', approved=True)
        form_data = {'level': 'Close Family', 'member': self.user, 'kinship': 'Mother',
                     'name': 'Test', 'email': 'test@test.com', 'approved': False}

        request = self.factory.post(
            f'/members/edit_invite/{invite.id}', form_data)
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.edit_invite(request, invite.id)
        self.assertEqual(response.status_code, 302)

    def test_edit_invite_get(self):
        self.client.login(email='test@test.com', password='Testing2022')
        invite = models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Father', name='Test', email='test@test.com', approved=True)
        request = self.factory.get(
            f'/members/edit_invite/{invite.id}')
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.edit_invite(request, invite.id)
        self.assertEqual(response.status_code, 200)

    def test_menu(self):
        self.client.login(email='test@test.com', password='Testing2022')
        response = self.client.get(f'/members/menu')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'member/menu.html')

    def test_familio_post(self):
        self.client.login(email='test@test.com', password='Testing2022')
        form_data = {'level': 'Close Family', 'member': self.user, 'kinship': 'Mother',
                     'name': 'Test', 'email': 'test@test.com', 'approved': False}

        request = self.factory.post(
            f'/members/familio', form_data)
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        request.META['HTTP_HOST'] = 'localhost'
        response = views.familio(request)
        self.assertEqual(response.status_code, 302)

    def test_familio_get(self):
        self.client.login(email='test@test.com', password='Testing2022')
        request = self.factory.get(
            f'/members/familio')
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        request.META['HTTP_HOST'] = 'localhost'
        response = views.familio(request)
        self.assertEqual(response.status_code, 200)

    def test_approved_get(self):
        self.client.login(email='test@test.com', password='Testing2022')
        familio = models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Father', name='Test', email='test@test.com', approved=True)
        request = self.factory.get(
            f'/members/approved/{familio.id}')
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.approved(request, familio.id)
        self.assertEqual(response.status_code, 302)

    def test_approved_get_another_email(self):
        self.client.login(email='test@test.com', password='Testing2022')
        familio = models.Familio.objects.create(
            level='Close Family', member=self.user, kinship='Father', name='Test', email='Jose@test.com', approved=False)
        request = self.factory.get(
            f'/members/approved/{familio.id}')
        # why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # ----- #
        request.user = self.user
        response = views.approved(request, familio.id)
        self.assertEqual(response.status_code, 302)
