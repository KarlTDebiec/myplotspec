# -*- coding: utf-8 -*-

todo_include_todos = False

needs_sphinx = '1.3'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.todo']
# templates_path = ['_templates']
source_suffix = '.rst'
source_encoding = 'utf-8'
napoleon_use_rtype = False

master_doc = 'index'
project = "MYPlotSpec"
copyright = "2015, Karl T Debiec"
version = "0.1"
release = "0.1"

# language = None
# today = ''
# today_fmt = '%B %d, %Y'
exclude_patterns = ['_build']
# default_role = None
# add_function_parentheses = True
# add_module_names = True
# show_authors = False
pygments_style = "sphinx"
# modindex_common_prefix = []

html_theme = "default"
# html_theme_options = {}
# html_theme_path = []
# html_title = None
# html_short_title = None
# html_logo = None
# html_favicon = None
html_static_path = ['_static']
# html_last_updated_fmt = '%b %d, %Y'
# html_use_smartypants = True
# html_sidebars = {}
# html_additional_pages = {}
# html_domain_indices = True
# html_use_index = True
# html_split_index = False
# html_show_sourcelink = True
# html_show_sphinx = True
# html_show_copyright = True
# html_use_opensearch = ''
# html_file_suffix = None
htmlhelp_basename = "MYPlotSpecdoc"

latex_elements = {
"preamble": "\setcounter{tocdepth}{4}",
}
latex_use_modindex = False
latex_documents = [
  ("index", "MYPlotSpec.tex", "MYPlotSpec Documentation",
   "Karl T Debiec", "manual"),
]
# latex_logo = None
# latex_use_parts = False
# latex_show_pagerefs = False
# latex_show_urls = False
# latex_appendices = []
# latex_domain_indices = True

# man_pages = [
#     ('index', 'MYPlotSpec', u'MYPlotSpec Documentation',
#      [u'Karl Debiec'], 1)
# ]
# man_show_urls = False

# texinfo_documents = [
#   ('index',
#    'MYPlotSpec',
#    'MYPlotSpec Documentation',
#    'Karl Debiec',
#    'MYPlotSpec',
#    'One line description of project.',
#    'Miscellaneous'),
# ]
# texinfo_appendices = []
# texinfo_domain_indices = True
# texinfo_show_urls = 'footnote'

# intersphinx_mapping = {'http://docs.python.org/': None}
