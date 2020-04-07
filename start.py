import os
import sys

sys.path.insert(0,   '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')))

#from modules import create_schema
from script.modules.ui_new import application



if __name__ == '__main__':
    application('Welcome')
