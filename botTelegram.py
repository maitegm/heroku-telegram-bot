

import telegram
import requests
import time
import dns.resolver
from telegram.ext import Updater, CommandHandler

TOKEN = '522017250:AAE89zva8udGDpm5U_c7jei_rgiiXYP_7Lg'
bot = telegram.Bot(token=TOKEN)
print(bot.get_me())
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def start(bot, update):
	global d
	bot.send_message(chat_id=update.message.chat_id, text='Checking status every 5 seconds:')
	working = check_web_working()
	d[update.message.chat_id] = working
	send_working_message(bot, working, update.message.chat_id)
	job_queue.run_repeating(check_status, 5, first = 5, context=update.message.chat_id)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

import random

def check_web_working():
	rand = random.randint(0,3)
	return rand
	name = 'niclabs.cl'
	my_resolver = dns.resolver.Resolver()
	# 8.8.8.8 is Google's public DNS server
	my_resolver.nameservers = ['8.8.8.8']	
	try:
		answer = my_resolver.query(name)
		return True
	except:
		print("something is wrong")
		return False
	#try:
	#	r = requests.get(name)
	#	if(r.status_code==200):
	#		return True
	#	else:
	#		return False
	#except:
	#	return False


def send_working_message(bot, working_now,chat_id):
	if(working_now):
		bot.send_message(chat_id=chat_id, text='It\'s all good, man.')
	else:
		bot.send_message(chat_id=chat_id, text='Something is wrong...')

global d
d = {} #dictionary that saves last status check for every chat


def check_status(bot, job):
	global d
	working = check_web_working()
	if(d[job.context] & working == True):
		send_working_message(bot, working,job.context)
		d[job.context] = working

def check_status_timer(bot, update, job_queue):
	global d
	bot.send_message(chat_id=update.message.chat_id, text='Checking status every 5 seconds:')
	working = check_web_working()
	send_working_message(bot, working,update.message.chat_id)
	d[update.message.chat_id] = working

	job_queue.run_repeating(check_status, 5, first = 5, context=update.message.chat_id)

check_status_timer_handler = CommandHandler('check_web', check_status_timer, pass_job_queue=True)
dispatcher.add_handler(check_status_timer_handler)


def stop_check_status(bot, update, job_queue):
	bot.send_message(chat_id=update.message.chat_id, text="Stop checking the status")	
	job_queue.stop()
stop_check_status_handler = CommandHandler('stop_check_status', stop_check_status, pass_job_queue=True)
dispatcher.add_handler(stop_check_status_handler)



updater.start_polling()
print('running')
updater.idle()


exit()


#import logging
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



#def caps(bot, update, args):
#	if(args):
#		stop=False
#	else:
#		stop=True

	#text_caps = ' '.join(args).upper()
#	bot.send_message(chat_id=update.message.chat_id, text=args)
#caps_handler = CommandHandler('caps', caps, pass_args=True)
#dispatcher.add_handler(caps_handler)


#def hello(bot, update):
#	print('hello')
	#print(stop)
	#stop = True
	#print(stop)
#	d[update.message.chat_id]=True
#	update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
#dispatcher.add_handler(CommandHandler('hello', hello))

#def bye(bot, update):
	#print('bye')
	#print(stop)
	#stop = False
	#d[update.message.chat_id]=False
	#print(stop)
#	update.message.reply_text('Bye {}'.format(update.message.from_user.first_name))
#dispatcher.add_handler(CommandHandler('bye', bye))







#stop=True
#def callback_alarm(bot, job):
#	bot.send_message(chat_id=job.context, text='BEEP')
#def callback_timer(bot, update, job_queue):
	#stop=False
#	bot.send_message(chat_id=update.message.chat_id, text='Setting a timer for 1 minute!')
	#run_repeating(callback, interval, first=None, context=None, name=None)
#	job_queue.run_repeating(callback_alarm, 5, first = 0, context=update.message.chat_id, name = "timer")
	#if(stop):
	#	job_queue.stop()
#timer_handler = CommandHandler('timer', callback_timer, pass_job_queue=True)
#dispatcher.add_handler(timer_handler)


#def stop_timer(bot, update, job_queue):
#	job_queue.stop()
	#stop = True
#	bot.send_message(chat_id=update.message.chat_id, text="Timer stopped.")	
		
#stop_timer_handler = CommandHandler('stop_timer', stop_timer, pass_job_queue=True)
#dispatcher.add_handler(stop_timer_handler)
