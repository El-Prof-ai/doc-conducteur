import os
import sys

sys.path.insert(0, os.path.abspath('.'))

# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'presentationConducteur'
copyright = '2024, El_Prof'
author = 'El_Prof'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

source_suffix = '.rst '

# The master toctree document.
master_doc = 'index'

# The short X,Y version.
version = ''

# The full version, including alphe/beta/rc tags.
release = ''
language = None

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'  # Utilisez le thème ReadTheDocs
html_static_path = ['_static']  # Ne pas inclure le répertoire de sortie ici
