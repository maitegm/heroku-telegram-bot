

import telegram
import requests
import time

bot = telegram.Bot(token='522017250:AAE89zva8udGDpm5U_c7jei_rgiiXYP_7Lg')

print(bot.get_me())





from telegram.ext import Updater, CommandHandler

#TELEGRAM_TOKEN = "527767265:AAE6VWFeq9KjSgusAhHYXLPn4SucYDdcFJc"
updater = Updater(token='522017250:AAE89zva8udGDpm5U_c7jei_rgiiXYP_7Lg')

dispatcher = updater.dispatcher

def start(bot, update):
	print("hola")
	bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def caps(bot, update, args):
	text_caps = ' '.join(args).upper()
	bot.send_message(chat_id=update.message.chat_id, text=text_caps)
caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

def hello(bot, update):
    print("hello")
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


#updater = Updater('527767265:AAE6VWFeq9KjSgusAhHYXLPn4SucYDdcFJc')

dispatcher.add_handler(CommandHandler('hello', hello))



import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


checking = False

def check_status(bot, update):
	checking = True

	while(checking):

		try:

			r = requests.get('http://www.niclabs.cl')
			if(r.status_code==200):
				bot.send_message(chat_id=update.message.chat_id, text="it's all good, man")	
			else:
				bot.send_message(chat_id=update.message.chat_id, text="Something is wrong...")	
		except:
			bot.send_message(chat_id=update.message.chat_id, text="Something is wrong...")	

		time.sleep(3)
		checking = False

chats_subscribed = []

check_status_handler = CommandHandler('check_status', check_status)
dispatcher.add_handler(check_status_handler)


def stop_check_status(bot, update):
	checking = False
	bot.send_message(chat_id=update.message.chat_id, text="No checking the status")	
		
stop_check_status_handler = CommandHandler('stop_check_status', stop_check_status)
dispatcher.add_handler(stop_check_status_handler)



#stop=True
def callback_alarm(bot, job):
	bot.send_message(chat_id=job.context, text='BEEP')
def callback_timer(bot, update, job_queue):
	#stop=False
	bot.send_message(chat_id=update.message.chat_id, text='Setting a timer for 1 minute!')
	#run_repeating(callback, interval, first=None, context=None, name=None)
	job_queue.run_repeating(callback_alarm, 5, first = 0, context=update.message.chat_id, name = "timer")
	#if(stop):
	#	job_queue.stop()
timer_handler = CommandHandler('timer', callback_timer, pass_job_queue=True)
dispatcher.add_handler(timer_handler)


def stop_timer(bot, update, job_queue):
	job_queue.stop()
	#stop = True
	bot.send_message(chat_id=update.message.chat_id, text="Timer stopped.")	
		
stop_timer_handler = CommandHandler('stop_timer', stop_timer, pass_job_queue=True)
dispatcher.add_handler(stop_timer_handler)


updater.start_polling()
print('running')
updater.idle()
