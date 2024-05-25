import os
import sys
sys.path.insert(0, os.path.abspath('../../'))  # To find your module's docstrings

html_theme = 'press'

project = 'Hyprpy'
copyright = '2023, Julian Lobbes'
author = 'Julian Lobbes'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

add_module_names = False
extensions = [
    'sphinx.ext.autodoc',
    'sphinxemoji.sphinxemoji',
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_member_order = 'bysource'
autodoc_preserve_defaults = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'press'
html_static_path = ['_static']
html_sidebars = {'**': ['util/searchbox.html', 'util/sidetoc.html']}
html_theme_options = {
  "external_links": [
      ("Github", "https://github.com/ulinja/hyprpy"),
      ("Contact", "https://lobbes.dev/contact")
  ]
}
html_css_files = ["css/custom.css"]
html_logo = '_static/hyprpy-logo.png'
