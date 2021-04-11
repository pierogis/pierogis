import os
import sys

from setuptools_scm import get_version

sys.path.insert(0, os.path.abspath('../'))

# Project --------------------------------------------------------------

project = "pierogis"
copyright = "2021 pierogis"
author = "pierogis-live"
version = get_version(root='..', relative_to=__file__)

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.apidoc',
    'sphinx_issues',
    'sphinx.ext.viewcode'
]
intersphinx_mapping = {
    "rich": ("https://rich.readthedocs.io/en/stable/", None),
    "imageio": ("https://imageio.readthedocs.io/en/stable/", None),
    "Pillow": ("https://pillow.readthedocs.io/en/stable/", None),
}
issues_github_path = "pierogis/pierogis"
apidoc_module_dir = '../src/pyrogis'
apidoc_output_dir = 'source'
apidoc_separate_modules = True

# HTML -----------------------------------------------------------------

html_theme = "alabaster"
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ]
}
html_title = f"pierogis docs ({version})"
html_show_sourcelink = True
html_theme_options = {
    "description": "image and animation processing framework",
    "github_user": "pierogis",
    "github_repo": "pierogis",
    "fixed_sidebar": True,
    'github_type': ''
}
