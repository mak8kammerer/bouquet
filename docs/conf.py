# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

os.environ["KIVY_NO_ARGS"] = "true"
os.environ["READTHEDOCS"] = "true"

sys.path.insert(0, os.path.dirname(os.getcwd()))

import bouquet

project = bouquet.__name__
copyright = f'2024, {bouquet.__author__}'
author = bouquet.__author__
release = bouquet.__version__


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton'
]

# InterSphinx configuration.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "kivy": ("https://kivy.org/doc/stable/", None),
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
