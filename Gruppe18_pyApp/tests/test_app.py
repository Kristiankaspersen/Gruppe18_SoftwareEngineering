import pytest
from app_flask import app


def test_if_app_name_is_app_flask():
    assert app.name == "app_flask"


def test_if_app_secret_key_is_correct():
    assert app.secret_key == "5f4b0959c458e6b06c51097e"


def test_if_app_import_name_is_app_flask():
    assert app.import_name == "app_flask"


def test_if_app_template_folder_is_named_templates():
    assert app.template_folder == "templates"
