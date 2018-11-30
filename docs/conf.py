from sprockets.mixins.sentry import __version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.httpdomain',
]
master_doc = 'index'
project = 'sprockets.mixins.sentry'
copyright = '2016, AWeber Communications'
version = '.'.join(__version__.split('.')[0:1])
release = __version__
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
intersphinx_mapping = {
    'python': ('https://docs.python.org/', None),
    'tornado': ('http://tornadoweb.org/en/stable/', None),
    'raven': ('https://raven.readthedocs.org/en/latest/', None),
}
