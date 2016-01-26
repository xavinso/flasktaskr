import unittest
from test import AllTests


class MainTests(AllTests):

    def test_404_error(self):
        response = self.app.get('/this-route-does-not-exist/')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b'Sorry. There\'s nothing here.', response.data)

    def test_500_error(self):
        bad_user = self.User(
            name='Jeremy',
            email='jeremy@realpython.com',
            password='django'
        )
        self.db.session.add(bad_user)
        self.db.session.commit()
        response = self.login('Jeremy', 'django')
        self.assertEquals(response.status_code, 500)
        self.assertNotIn(b'ValueError: Invalid salt', response.data)
        self.assertIn(b'Something went terribly wrong.', response.data)

if __name__ == "__main__":
    unittest.main()
