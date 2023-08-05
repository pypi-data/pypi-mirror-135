from django.test.client import Client


class TestTemplateRoot:
    def setup(self):
        self.client = Client()

    def test_page_with_empty_setting(self, flatly_conf):
        flatly_conf.TEMPLATE_ROOT = ""

        response = self.client.get('/about/')
        assert response.status_code == 200
        assert response.templates[0].name == 'about/index.html'

    def test_page_from_flatly_root(self, flatly_conf):
        flatly_conf.TEMPLATE_ROOT = "flatly_root"

        response = self.client.get('/about/')
        assert response.status_code == 200
        assert response.templates[0].name == 'flatly_root/about.html'

    def test_parentheses(self, flatly_conf):
        flatly_conf.TEMPLATE_ROOT = "flatly_root"

        response = self.client.get('/about/../blog/')
        assert response.status_code == 404


class TestExtensions:
    def setup(self):
        self.client = Client()

    def test_extension_not_found(self, flatly_conf):
        flatly_conf.TEMPLATE_ROOT = "flatly_root"
        flatly_conf.EXTENSIONS = ["html"]

        response = self.client.get('/blog/')
        assert response.status_code == 404

    def test_with_correct_extension(self, flatly_conf):
        flatly_conf.TEMPLATE_ROOT = "flatly_root"
        flatly_conf.EXTENSIONS = ["html", "htm"]

        response = self.client.get('/blog/')
        assert response.status_code == 200
        assert response.templates[0].name == 'flatly_root/blog.htm'
