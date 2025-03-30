# This directory will contain the application log files
import os
if not os.path.exists(os.path.dirname(__file__)):
    os.makedirs(os.path.dirname(__file__))