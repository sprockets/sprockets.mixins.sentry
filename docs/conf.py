#!/usr/bin/env python
import sphinx_rtd_theme

from sprockets.mixins.sentry import version_info, __version__

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.httpdomain',
]
templates_path = []
source_suffix = '.rst'
master_doc = 'index'
project = 'sprockets.mixins.sentry'
copyright = '2015, AWeber Communications'
version = '.'.join(__version__.split('.')[0:1])
release = __version__
if len(version_info) > 3:
    release += '-{0}'.format(str(v) for v in version_info[3:])
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
intersphinx_mapping = {
    'python': ('https://docs.python.org/', None),
    'tornado': ('http://tornadoweb.org/en/stable/', None),
    'raven': ('https://raven.readthedocs.org/en/latest/', None),
}
