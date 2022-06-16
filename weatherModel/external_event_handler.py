import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from definition import Infinite


from model_periodic import PeriodicModel
from model_telegram_handler import TelegramHandler

import dill

from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

class TelegramExternalHandler():
    def __init__(self, sys_simulator):
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        #updater = Updater("5010687528:AAEKtgIMrmvIOiF9XwkLPzCj29E7Cjt8F-I")
        self.updater = Updater("5383202051:AAFzfoMp-cyLcgYRPZ7dbIh3ofzeE8cbZUY")

        # Get the dispatcher to register handlers
        dispatcher = self.updater.dispatcher

        #updater.bot.send_message(1955979869, "hello")

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("stop", self.stop))

        dispatcher.add_handler(CommandHandler("help", self.help_command))

        # on non command i.e message - echo the message on Telegram
        #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo))
        dispatcher.add_handler(CommandHandler("start_polling", self.start_polling))

        ##########
        # jaiyun
        dispatcher.add_handler(CommandHandler("dump", self.dump))
        dispatcher.add_handler(CommandHandler("new_sim", self.new_sim))
        dispatcher.add_handler(CommandHandler("add_model", self.add_model))
        dispatcher.add_handler(CommandHandler("start_sim", self.start_sim))
        ##########

        # Start the Bot
        self.updater.start_polling()

        self.simulator = sys_simulator

        self.reconstruct_simulator = None

        #########
        ## jaiyun
        self.simulator.get_engine("sname").insert_input_port("start_polling")
        th = TelegramHandler(0, Infinite, "TelegramHandler", "sname", self.simulator)
        self.simulator.get_engine("sname").register_entity(th)
        self.simulator.get_engine("sname").coupling_relation(None, "start_polling", th, "start_polling")

        self.simulator.get_engine("sname").insert_input_port("start")
        gen = PeriodicModel(0, Infinite, "Periodic", "sname", th.get_updater().bot)
        self.simulator.get_engine("sname").register_entity(gen)
        self.simulator.get_engine("sname").coupling_relation(None, "start", gen, "start")
                
        self.simulator.get_engine("sname").insert_input_port("stop")
        self.simulator.get_engine("sname").coupling_relation(None, "stop", gen, "stop")

        ## jaiyun
        #########
        self.simulator.exec_non_block_simulate(["sname"])
        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        print(update)
        self.simulator.get_engine("sname").insert_external_event("start", None)

    def stop(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        self.simulator.get_engine("sname").insert_external_event("stop", None)

    def help_command(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def echo(self, update: Update, context: CallbackContext) -> None:
        """Echo the user message."""        
        update.message.reply_text(update.message.text)

    def start_polling(self, update: Update, context: CallbackContext) -> None:
        """Echo the user message."""        
        self.simulator.get_engine("sname").insert_external_event("start_polling", None)

    def dump(self, update: Update, context: CallbackContext) -> None:
        gen = update['message']['text'].split()[1]
        model = self.simulator.get_engine("sname").get_model(gen)
        with open(f"{gen}.simx", 'wb') as f:
            dill.dump(model, f)
            print("done")

    def new_sim(self, update: Update, context: CallbackContext) -> None:
        self.reconstruct_simulator = SystemSimulator()
        self.reconstruct_simulator.register_engine("sname", "REAL_TIME", 1)
        self.reconstruct_simulator.get_engine("sname").insert_input_port("start")
        self.reconstruct_simulator.get_engine("sname").insert_input_port("stop")
        print("new_sim")

    def start_sim(self, update: Update, context: CallbackContext) -> None:
        print(update)
        self.reconstruct_simulator.get_engine("sname").insert_external_event("start", None)
        self.reconstruct_simulator.get_engine("sname").simulate()

    def add_model(self, update: Update, context: CallbackContext) -> None:
        _, gen, token = update['message']['text'].split()
        with open(f"{gen}.simx", 'rb') as f:
            model = dill.load(f)
            #reconstruct_updater = Updater("5190485547:AAGdmxLqY9Q1SyQ5ZS6BrwVM3jgKykS6n-g")
            reconstruct_updater = Updater(token)
            reconstruct_updater.start_polling() 

            model.update_domain(reconstruct_updater.bot)
            self.reconstruct_simulator.get_engine("sname").register_entity(model)
            self.reconstruct_simulator.get_engine("sname").coupling_relation(None, "start", model, "start")
            self.reconstruct_simulator.get_engine("sname").coupling_relation(None, "stop", model, "stop")
            print(f"{gen}.simx")