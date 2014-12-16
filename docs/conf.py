# -*- coding: utf-8 -*-
#
# PyVDF documentation build configuration file

import sys
import os

# sys.path.insert(0, '/home/wolf/Projects/Python/PyVDF/')

import PyVDF

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))

# -- General configuration ------------------------------------------------

needs_sphinx = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    '_ext.autosummary_fork',
    '_ext.toctree',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'PyVDF Documentation'
copyright = u'2014, Austin Reuland'

version = PyVDF.__version__
release = PyVDF.__release__

exclude_patterns = ['_build']

add_module_names = False
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

html_theme = "amr"
html_theme_options = {}
html_theme_path = ['_themes/',]
html_title = None
html_short_title = "PyVDF {} Documentation".format(version)
html_logo = None
html_favicon = None
html_static_path = ['_static']
html_extra_path = []
html_last_updated_fmt = '%b %d, %Y'
html_use_smartypants = True
html_sidebars = {}
html_additional_pages = {}
html_domain_indices = False
html_use_index = False
html_split_index = False
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True
html_use_opensearch = ''
html_file_suffix = None
htmlhelp_basename = 'PyVDFdoc'


latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

latex_documents = [
  ('index', 'PyVDF.tex', u'PyVDF Documentation',
   u'Austin Reuland', 'manual'),
]

latex_logo = None
latex_use_parts = False
latex_show_pagerefs = False
latex_show_urls = False
latex_appendices = []
latex_domain_indices = False


# -- Options for manual page output ---------------------------------------

man_pages = [
    ('index', 'pyvdf', u'PyVDF Documentation',
     [u'Austin Reuland'], 1)
]

man_show_urls = False

# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
  ('index', 'PyVDF', u'PyVDF Documentation',
   u'Austin Reuland', 'PyVDF', 'One line description of project.',
   'Miscellaneous'),
]

texinfo_appendices = []
texinfo_domain_indices = True
texinfo_show_urls = 'footnote'
texinfo_no_detailmenu = False
