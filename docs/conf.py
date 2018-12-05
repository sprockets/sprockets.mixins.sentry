import pkg_resources

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
]
master_doc = 'index'
project = 'sprockets.mixins.sentry'
copyright = '2016-2018, AWeber Communications'
release = pkg_resources.get_distribution('sprockets.mixins.sentry').version
version = '.'.join(release.split('.')[0:1])
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
intersphinx_mapping = {
    'python': ('https://docs.python.org/', None),
    'tornado': ('http://tornadoweb.org/en/stable/', None),
    'raven': ('https://raven.readthedocs.org/en/latest/', None),
}
