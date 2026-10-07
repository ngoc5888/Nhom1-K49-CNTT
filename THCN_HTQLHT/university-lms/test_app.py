import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from app import create_app

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home_redirect(self):
        # Kiểm tra trang chủ chuyển hướng (302) khi chưa đăng nhập
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login_page(self):
        # Kiểm tra trang đăng nhập hiển thị bình thường (200)
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()