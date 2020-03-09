import os
import sys

sys.path.insert(0,   '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')))

#from modules import create_schema
from script.modules.ui import ui



if __name__ == '__main__':
    obj = ui()
    obj.main()
