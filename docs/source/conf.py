# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CL Bot'
copyright = '2025, Mark Davian'
author = 'Mark Davian'
release = '2.0'
html_title = "CL BOT 2.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# Импортируем модуль-заглушку для мокирования импортов
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('.'))

# Импортируем заглушки вместо реальных модулей
import conf_mock
sys.modules['config'] = conf_mock

# Автоматически генерировать документацию для модулей
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
    'special-members': '__init__',
    'show-inheritance': True,
}

# Настройка обработки русской документации
autodoc_docstring_signature = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
