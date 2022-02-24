from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):

    def test_create_admin_user(self):
        user = User.objects.create_superuser(
            email='admin@email.net', password='admin123')
        user.full_clean()
        user.save()
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)

    def test_create_commom_user(self):
        user = User(email='teste@email.net', password='123ABCxyz@')
        user.full_clean()
        user.save()
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, False)
