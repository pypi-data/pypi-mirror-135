#!/usr/bin/env python

"""Tests for `package_helper_test_2022_01_18_17h12` package."""

import pytest


from package_helper_test_2022_01_18_17h12 import package_helper_test_2022_01_18_17h12


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
