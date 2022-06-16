import contexts
# SIMULATION_MODE
SIMULATION_MODE = "REAL_TIME"
TIME_DENSITY = 1

TELEGRAM_API_KEY ="YOUR-TELEGRAM-BOT-KEY-COLLECT"

import os
if os.path.isfile("../instance/config.py"):
	from instance.config import *