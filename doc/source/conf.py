import sys
import os
sys.path.insert(0, os.path.abspath('../../'))

# -- Path setup --------------------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints'
]
# -- Project information -----------------------------------------------------
project = 'Miblo Bank API Documentation'
copyright = '2025, Miblo Bank'
author = 'Miblo Bank Dev Team'
# spécifiquation des modules à simuler afin d'éviter les erreurs d'imports
autodoc_mock_imports = [
    "sqlalchemy",
    "fastapi",
    "database"
]