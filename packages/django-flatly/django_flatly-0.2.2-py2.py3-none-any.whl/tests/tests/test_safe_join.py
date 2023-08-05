import pytest
from flatly.helpers import safe_join
from flatly.exceptions import InvalidTemplatePath


class TestSafeJoin:
    def test_empty_base(self):
        path = safe_join('account/user', '')
        assert path == 'account/user'

    def test_root_base(self):
        path = safe_join('account/user', '/')
        assert path == 'account/user'

    def test_root_folder_base(self):
        path = safe_join('account/user', '/tmp/')
        assert path == 'tmp/account/user'

    def test_slash_ending(self):
        path = safe_join('account/user/', '/tmp')
        assert path == 'tmp/account/user'

    def test_root_folder_base_without_slash(self):
        path = safe_join('account/user', '/tmp')
        assert path == 'tmp/account/user'

    def test_relative_base(self):
        path = safe_join('account/user', 'tmp/dir')
        assert path == 'tmp/dir/account/user'

    def test_absolute_path(self):
        with pytest.raises(InvalidTemplatePath):
            safe_join('/account/user', 'base/path')

    def test_parentheses(self):
        with pytest.raises(InvalidTemplatePath):
            safe_join('../account/user', 'base/path')

        with pytest.raises(InvalidTemplatePath):
            safe_join('account/../../user', 'base/path')
