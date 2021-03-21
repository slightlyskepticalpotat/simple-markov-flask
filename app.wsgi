import logging
import secrets
import sys

logging.basicConfig(stream = sys.stderr)
sys.path.insert(0,"/home/chenanthony365/chenanthony-markov/")
from app import app as application
