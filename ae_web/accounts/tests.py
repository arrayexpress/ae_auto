import json
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from .models import User


class TestLogin(TestCase):

    def setUp(self):
        user = User(username='testuser')
        user.set_password('rightpassword')
        user.save()
        self.user_id = user.id

    def test_login_invalid_password(self):
        response = self.client.post('/accounts/login', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEquals(response.status_code, 400)

    def test_login_invalid_username(self):
        response = self.client.post('/accounts/login', {
            'username': 'nottestuser',
            'password': 'rightpassword'
        })
        self.assertEquals(response.status_code, 400)

    def test_login_valid_username_and_password_status_code(self):
        response = self.client.post('/accounts/login', {
            'username': 'testuser',
            'password': 'rightpassword'
        })
        self.assertEquals(response.status_code, 302)

    def test_login_valid_username_and_password_updates_session(self):
        self.client.post('/accounts/login', {
            'username': 'testuser',
            'password': 'rightpassword'
        })
        self.assertEquals(int(self.client.session['_auth_user_id']), self.user_id)


class TestRegistration(TestCase):

    def setUp(self):
        user = User(username="test")
        user.set_password("testpassword")
        user.is_admin = True
        user.save()
        self.user = user
        self.client.login(username='test', password='testpassword')

    def test_missing_username(self):
        response = self.client.post('/accounts/register', {
            'password': 'validpassword',
            'email': 'valid@email.com',
             
        })
        self.assertEquals(response.status_code, 400)

    def test_missing_password(self):
        response = self.client.post('/accounts/register', {
            'username': 'validuser',
            'email': 'valid@email.com',
             
        })
        self.assertEquals(response.status_code, 400)

    def test_missing_email(self):
        response = self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
             
        })
        self.assertEquals(response.status_code, 400)

    def test_invalid_email(self):
        response = self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'invalidemail',
             
        })
        self.assertEquals(response.status_code, 400)

    def test_unique_username(self):
        user = User(username='validuser')
        user.set_password('rightpassword')
        user.save()
        response = self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
             
        })
        self.assertEquals(response.status_code, 400)

    def test_unique_email(self):
        user = User(username='anothervaliduser', email='valid@email.com')
        user.set_password('rightpassword')
        user.save()
        response = self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
             
        })
        self.assertEquals(response.status_code, 400)

    def test_valid(self):
        response = self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
             
        })
        self.assertEquals(response.status_code, 201)

    def test_valid_creates_user(self):
        self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
             
        })
        user = User.objects.get(username='validuser')
        self.assertIsNotNone(user)

    def test_defaults(self):
        params = {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
             
        }
        self.client.post('/accounts/register', params)
        user = User.objects.get(username='validuser')
        self.assertEquals(user.email, params['email'])
        self.assertEquals(user.first_name, '')
        self.assertEquals(user.last_name, '')
        self.assertEquals(user.is_admin, False)

    def test_fields_set_correctly(self):
        params = {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
        }
        self.client.post('/accounts/register', params)

        user = User.objects.get(username='validuser')
        self.assertEquals(user.email, params['email'])
        self.assertEquals(user.first_name, '')
        self.assertEquals(user.last_name, '')


    def test_user_manager(self):
        self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
             
        })
        user = User.objects.get(username='validuser')

        self.assertEquals(user.manager, self.user)

    def test_adding_admin_not_valid(self):
        response = self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
             
            'is_admin': True,
        })
        self.assertEquals(response.status_code, 400)

    def test_adding_admin_valid(self):
        user = User(username="super_test")
        user.set_password("testpassword")
        user.is_super_admin = True
        user.save()
        self.client.login(username='super_test', password='testpassword')
        self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
             
            'is_admin': True,
        })
        user = User.objects.get(username='validuser')
        self.assertEquals(user.is_admin, True)


class RegistrationPermissionsTest(TestCase):

    def test_create_not_logged_in(self):
        response = self.client.post('/accounts/register', {
            'username': 'validuser',
            'password': 'validpassword',
            'email': 'valid@email.com',
        })
        self.assertEquals(response.status_code, 403)

    def test_user_is_not_admin(self):
        user = User(username='validuser')
        user.set_password('validpassword')
        user.save()
        self.client.login(username='validuser', password='validpassword')
        response = self.client.post('/accounts/register', {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'new@email.com',
        })
        self.assertEquals(response.status_code, 403)


class UserListView(TestCase):

    def setUp(self):
        users = []
        users.append(User(username='superadmin', is_super_admin=True))
        users.append(User(username='admin1', is_admin=True))
        users.append(User(username='admin2', is_admin=True))
        for user in users:
            user.set_password('password')
            user.save()
        users.append(User(username='user1', manager=users[1]))
        users.append(User(username='user2', manager=users[1]))
        for user in users:
            user.set_password('password')
            user.save()

    def test_super_admin(self):
        self.client.login(username='superadmin', password='password')
        response = self.client.get('/api/users/')
        self.assertEquals(response.status_code, 200)
        users = json.loads(response.content)
        self.assertEquals(len(users), 5)

    def test_admin(self):
        self.client.login(username='admin1', password='password')
        response = self.client.get('/api/users/')
        self.assertEquals(response.status_code, 200)
        users = json.loads(response.content)
        self.assertEquals(len(users), 3)


class UserDetailView(TestCase):

    def setUp(self):
        users = []
        users.append(User(username='superadmin', is_super_admin=True))
        users.append(User(username='admin1', is_admin=True))
        users.append(User(username='admin2', is_admin=True))
        for user in users:
            user.set_password('password')
            user.save()
        users.append(User(username='user1', manager=users[1]))
        users.append(User(username='user2', manager=users[1]))
        for user in users:
            user.set_password('password')
            user.save()
        self.super_admin = users[0]
        self.admin1 = users[1]
        self.user1 = users[3]

    def test_get_account(self):
        self.client.login(username='superadmin', password='password')
        response = self.client.get('/api/users/%s' % self.super_admin.id)
        self.assertEquals(response.status_code, 200)
        user = json.loads(response.content)
        self.assertEquals(user['username'], self.super_admin.username)

    def test_get_account_superadmin_logged_in_as_admin(self):
        self.client.login(username='user1', password='password')
        response = self.client.get('/api/users/%s' % self.super_admin.id)
        self.assertEquals(response.status_code, 403)

    def test_get_account_superadmin_direct_manager(self):
        self.client.login(username='admin1', password='password')
        response = self.client.get('/api/users/%s' % self.user1.id)
        self.assertEquals(response.status_code, 200)

    def test_cant_delete_myself(self):
        self.client.login(username='admin1', password='password')
        response = self.client.delete('/api/users/%s' % self.admin1.id)
        self.assertEquals(response.status_code, 400)

    def test_cant_delete_admin_with_children(self):
        self.client.login(username='superadmin', password='password')
        response = self.client.delete('/api/users/%s' % self.admin1.id)
        self.assertEquals(response.status_code, 400)


class UserEditPassword(TestCase):

    def setUp(self):
        self.user = User(username='test')
        self.user.set_password('test_password')
        self.user.save()
        self.client.login(username='test', password='test_password')

    def test_user_can_change_his_password(self):
        old_password = self.user.password
        response = self.client.post('/accounts/edit', {
            'id': self.user.id,
            'password': 'new_test_password'
        })
        self.assertEquals(response.status_code, 200)
        self.user = User.objects.get(id=self.user.id)
        self.assertNotEqual(self.user.password, old_password)


class UserAuthToken(TestCase):

    def test_user_has_token(self):
        user = User(username="super_test")
        user.set_password("testpassword")
        user.is_super_admin = True
        user.save()
        try:
            token = user.auth_token
            self.assertIsNotNone(token.key)
        except ObjectDoesNotExist, e:
            self.fail(str(e))

    def test_user_with_token(self):
        # response = self.client.get('/api/users/')
        # self.assertEquals(response.status_code, 403)

        user = User(username="super_test")
        user.set_password("testpassword")
        user.is_super_admin = True
        user.save()
        token = user.auth_token.key
        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token
        }
        response = self.client.get('/api/accounts/', {}, **header)
        self.assertEquals(response.status_code, 200)
