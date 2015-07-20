"""Adapters to support different input devices

All adapters must be imported in this file and added
to the adapters list below in order to be available to the app
"""

from KeyboardAdapter import KeyboardAdapter

# list of adapters
adapters = [KeyboardAdapter]