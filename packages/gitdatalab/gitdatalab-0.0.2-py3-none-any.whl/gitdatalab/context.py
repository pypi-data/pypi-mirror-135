"""
    gitdata context
"""

import threading


context = threading.local()
context.db = None
