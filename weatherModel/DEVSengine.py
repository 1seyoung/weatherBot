from model_external_handler import TelegramExternalHandler

from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *

# System Simulator Initialization
ss = SystemSimulator()
ss.register_engine("sname", "REAL_TIME", 1)

#se.get_engine("sname").insert_external_event("start", None)
#se.get_engine("sname").simulate()

a = TelegramExternalHandler(ss)