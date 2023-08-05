from urllib.parse import urlsplit

from django.test.client import Client


class TestAppendSlash:
    def setup(self):
        self.client = Client()

    def test_admin_page_without_slash(self):
        response = self.client.get('/admin/login')
        assert response.status_code in {301, 302}

        parsed = urlsplit(response['location'])
        assert parsed.path == '/admin/login/'

    def test_admin_page_with_slash(self):
        response = self.client.get('/admin/login/')
        assert response.status_code == 200

    def test_home_page(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_app_page_without_slash(self):
        response = self.client.get('/app')
        assert response.status_code == 301
        assert response['location'] == '/app/'

    def test_app_page_with_slash(self):
        response = self.client.get('/app/')
        assert response.status_code == 200

    def test_flatly_page_without_slash(self):
        response = self.client.get('/blog')
        assert response.status_code == 301
        assert response['location'] == '/blog/'

    def test_flatly_page_with_slash(self):
        response = self.client.get('/blog/')
        assert response.status_code == 200

    def test_missing_page_without_slash(self):
        response = self.client.get('/missing')
        assert response.status_code == 404

    def test_missing_page_with_slash(self):
        response = self.client.get('/missing/')
        assert response.status_code == 404
