import unittest
from test import AllTests


class TasksTests(AllTests):

    def test_only_logged_in_users_can_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

        self.register(
            'Fletcher', 'fletcher@realpython.com', 'python101',
            'python101'
        )
        self.login('Fletcher', 'python101')
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)

    """
    assume only logged in users can add, complete, or
    delete tasks since we already know that only
    logged in users can access the tasks/ endpoint
    """

    def test_users_can_add_tasks(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(
            b'New entry was successfully posted. Thanks.',
            response.data
        )

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
                name='Go to the bank',
                due_date='',
                priority='1',
                posted_date='02/05/2014',
                status='1'
            ), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertIn(b'The task is complete. Nice.', response.data)

    def test_users_can_delete_tasks(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertNotIn(b'Mark as Complete', response.data)

        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(b'The task is complete. Nice.', response.data)
        self.assertIn(
            b'You can only update tasks that belong to you.',
            response.data
        )

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        response = self.app.get('tasks/', follow_redirects=True)

        self.assertNotIn(b'Delete', response.data)

        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertNotIn(
            b'The task was deleted. Why not add a new one?',
            response.data
        )
        self.assertIn(
            b'You can only delete tasks that belong to you.',
            response.data
        )

    def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_admin_user('Superman', 'super@super.com', 'allpowerful')
        self.login('Superman', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)

        response = self.create_task()
        self.assertIn(b'complete/1/', response.data)
        self.assertIn(b'complete/2/', response.data)

        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(
            b'You can only update tasks that belong to you.',
            response.data
        )

    def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_admin_user('Superman', 'super@super.com', 'allpowerful')
        self.login('Superman', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)

        response = self.create_task()
        self.assertIn(b'delete/1/', response.data)
        self.assertIn(b'delete/2/', response.data)

        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertNotIn(
            b'You can only delete tasks that belong to you.',
            response.data
        )


if __name__ == "__main__":
    unittest.main()
