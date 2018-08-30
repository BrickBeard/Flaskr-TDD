import unittest
import os
import tempfile
import app
import json

class BasicTestCase(unittest.TestCase):
    
    def test_index(self):
        '''Initial test: Ensure flask was set up correctly'''
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_database(self):
        '''Initial test: Ensure that the database exists.''' 
        tester = os.path.exists('flaskr.db')
        self.assertTrue(tester, True)
   
class FlaskrTestCase(unittest.TestCase):
    
    def setUp(self):
        '''Set up a blank temp database before each test'''
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()
        
    def tearDown(self):
        ''' Destroy blank temp database after each test'''
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
        
    def login(self, username, password):
        '''Login helper function'''
        return self.app.post('/login', data=dict(
            username = username,
            password = password
        ), follow_redirects=True)
    
    def logout(self):
        '''Logout helper function'''
        return self.app.get('/logout', follow_redirects=True)
    
    # Assert functions
    
    def test_empty_db(self):
        '''Ensure the Database is blank'''
        rv = self.app.get('/')
        assert b'No entries yet. Add some!' in rv.data
        
    def test_login_logout(self):
        '''Test login and logout using helper functions'''
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        assert b'You were successfully logged in' in rv.data
        rv = self.logout()
        assert b'You were successfully logged out' in rv.data
        rv = self.login(
            app.app.config['USERNAME'] + 'x',
            app.app.config['PASSWORD']
        )
        assert b'Invalid username' in rv.data
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD'] + 'x'
        )
        assert b'Invalid password' in rv.data
        
    def test_messages(self):
        '''Ensure that a user can post messages'''
        self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        rv = self.app.post('/add', data=dict(
            title = '<Hello>',
            text = '<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries yet. Add some!' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        
    def test_delete_message(self):
        '''Ensure the messages are being deleted'''
        rv = self.app.get('/delete/1')
        data = json.loads((rv.data).decode('utf-8'))
        self.assertEqual(data['status'], 1)

        
if __name__ == '__main__':
    unittest.main()
    