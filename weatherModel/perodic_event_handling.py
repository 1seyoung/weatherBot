from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime

class PeriodicModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, domain):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.insert_input_port("start")
        self.insert_input_port("stop")

        self.bot = domain

    def update_domain(self, domain):
        self.bot = domain

    def ext_trans(self,port, msg):
        if port == "start":
            print(f"[{self.get_name()}][IN]: {datetime.datetime.now()}")
            self._cur_state = "MOVE"
        elif port == "stop":
            print(f"[{self.get_name()}][IN]: {datetime.datetime.now()}")
            self._cur_state = "IDLE"

    def output(self):
        msg = None
        #msg = SysMessage(self.get_name(), "out")
        print(f"[{self.get_name()}][OUT]: {datetime.datetime.now()}")
        self.bot.send_message(1955979869, f"[{self.get_name()}][OUT]: {datetime.datetime.now()}")
        return msg
        
    def int_trans(self):
        #if self._cur_state == "MOVE":
        #    self._cur_state = "IDLE"
        #else:
        self._cur_state = "MOVE"