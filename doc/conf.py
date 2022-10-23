# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "solardem"
copyright = "2022, David Stansby"
author = "David Stansby"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "matplotlib.sphinxext.plot_directive",
    "myst_parser",
    "sphinx.ext.mathjax",
    "sphinx_gallery.gen_gallery",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "examples/*"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"


# -- Sphinx gallery configuration
sphinx_gallery_conf = {
    "examples_dirs": "./examples",  # path to your example scripts
    "gallery_dirs": "./_auto_examples",  # path to where to save gallery generated output
    "download_all_examples": False,
}
