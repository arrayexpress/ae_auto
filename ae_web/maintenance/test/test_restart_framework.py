import time
from django.contrib.auth import authenticate

from accounts.models import User

__author__ = 'Ahmed G. Ali'
from django.test import TestCase

class TestCalls(TestCase):
    def setUp(self):
        print User.objects.all()
        print 'after'
        self.user = User(username="super_test", password="testpassword", first_name='Ahmed', last_name='Ali', email='ahmedgali.86@gmail.com')
        # self.user.set_password("testpassword")
        # self.user.first_name = 'Ahmed'
        # self.user.email = 'ahmed@ebi.ac.uk'
        self.user.save()
        print User.objects.all()
        time.sleep(60)
        # print self.user
        # print type(self.user)
        user = authenticate(username=self.user.username, password=self.user.password)
        # print user
        self.client.post('/accounts/login', {'username':self.user.username, 'password':self.user.password})




    def test_restart_framework(self):
        # self.client.login(username='ahmed', password='enggemmy')

        response = self.client.post('/api/maintenance/framework/restart', )
        self.assertEqual(response.status_code, 200)
