import os
import sys

sys.path.insert(0, os.path.abspath('.'))

# Spécifiez le chemin vers votre répertoire source
source_suffix = '.rst'
master_doc = 'index'

# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'doc-conducteur '
copyright = '2024, El_Prof'
author = 'El_Prof'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# The short X,Y version.
version = ''

# The full version, including alphe/beta/rc tags.
release = ''
language = 'en'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'  # Utilisez le thème ReadTheDocs

# Configurez le chemin de sortie pour être compatible avec Read the Docs
if os.environ.get('READTHEDOCS') == 'True':
    output_path = os.environ.get('READTHEDOCS_OUTPUT', '_build')
    html_output = os.path.join(output_path, 'html')
else:
    html_output = '_build/html'

# Utilisez la variable html_output pour définir le chemin de sortie
html_static_path = [os.path.join(html_output, '_static')]
