import unittest
from test import AllTests
from datetime import date


class APITests(AllTests):

    def add_tasks(self):
        self.db.session.add(
            self.Task(
                "Run around in circles",
                date(2015, 10, 22),
                10,
                1,
                date(2015, 10, 5),
                1
            )
        )
        self.db.session.commit()

        self.db.session.add(
            self.Task(
                "Purchase Real Python",
                date(2015, 11, 3),
                10,
                1,
                date(2015, 11, 1),
                1
            )
        )
        self.db.session.commit()

    def test_collection_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/v1/tasks/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Run around in circles', response.data)
        self.assertIn(b'Purchase Real Python', response.data)

    def test_resource_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/v1/tasks/2', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Purchase Real Python', response.data)
        self.assertNotIn(b'Run around in circles', response.data)

    def test_invalid_resource_endpoint_returns_error(self):
        self.add_tasks()
        response = self.app.get('api/v1/tasks/209', follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Element does not exist', response.data)

if __name__ == "__main__":
    unittest.main()
