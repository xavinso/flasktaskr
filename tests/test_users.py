import unittest
from test import AllTests


class UsersTests(AllTests):

    def test_user_setup(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        test = self.db.session.query(self.User).all()
        for t in test:
            t.name
        assert t.name == "Michael"

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Please sign in to access your task list',
            response.data
        )

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password', response.data)

    def test_users_can_login(self):
        self.register("Michael", "michael@realpython.org", "python", "python")
        response = self.login('Michael', 'python')
        self.assertIn(b'Welcome!', response.data)

    def test_invalid_form_data(self):
        self.register("Michael", "michael@realpython.org", "python", "python")
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Please register to access the task list.',
            response.data
        )

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        # duplicate register
        self.app.get('register/', follow_redirects=True)
        response = self.register(
            'Michael', 'michael@realpython.com', 'python', 'python'
        )
        self.assertIn(
            b'That username and/or email already exist.',
            response.data
        )

    def test_logged_in_users_can_logout(self):
        self.register(
            'Fletcher', 'fletcher@realpython.com',
            'python101', 'python101'
        )
        self.login('Fletcher', 'python101')
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)

    def test_default_user_role(self):
        self.db.session.add(
            self.User(
                "Johnny",
                "john@doe.com",
                "johnny"
            )
        )
        self.db.session.commit()
        users = self.db.session.query(self.User).all()
        print users
        for user in users:
            self.assertEquals(user.role, 'user')

if __name__ == "__main__":
    unittest.main()
