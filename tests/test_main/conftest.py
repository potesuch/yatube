import os
from tests.test_main.fixtures.fixture_user import *
from tests.test_main.fixtures.fixture_data import *

from yatube.settings import INSTALLED_APPS

assert any(app in INSTALLED_APPS for app in ['posts.apps.PostsConfig', 'posts']), (
    'Пожалуйста зарегистрируйте приложение в `settings.INSTALLED_APPS`'
)
