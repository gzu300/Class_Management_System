import os
import sys

sys.path.insert(0,   '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1]))

#from modules import create_schema
from modules.ui import ui



if __name__ == '__main__':
    obj = ui()
    obj.main()