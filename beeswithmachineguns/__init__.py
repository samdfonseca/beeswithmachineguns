import os
import logging
import logging.config

logging.config.fileConfig('logging.conf')
if os.environ.has_key('log'):
    logging.root.setLevel(getattr(logging, os.environ['log'].upper()))
