import os
import sys

sys.path.insert(0, '/home/KULLANICI_ADI/melo/backend')
os.environ['FLASK_ENV'] = 'production'
from app import create_app

application = create_app('production')
