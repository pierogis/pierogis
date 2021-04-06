from setuptools_scm import get_version

# Project --------------------------------------------------------------

project = "pierogis"
copyright = "2021 pierogis"
author = "pierogis-live"
version = get_version(root='..', relative_to=__file__)

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    # "sphinxcontrib.log_cabinet",
    "sphinx_issues",
]
intersphinx_mapping = {
    "rich": ("https://rich.readthedocs.io/en/stable/", None),
    "imageio": ("https://imageio.readthedocs.io/en/stable/", None),
    "Pillow": ("https://pillow.readthedocs.io/en/stable/", None),
}
issues_github_path = "pierogis/pierogis"

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
