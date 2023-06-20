import os
import sys

# internal_service - это путь к директории приложения
APP_DIR = os.path.join(os.path.dirname(os.path.abspath(__name__)), "internal_service")
sys.path.append(APP_DIR)
