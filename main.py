from flask import Flask, request, jsonify
from telebot import TeleBot
from config import TOKEN, WEBHOOK_URL
import database
import user_management
import airdrop
import wallet
import tasks
import leaderboard
import mining

app = Flask(__name__)
bot = TeleBot(TOKEN)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK'

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    ip_address = request.remote_addr
    user_management.register_user(user_id, ip_address)
    bot.reply_to(message, "Welcome to Kingi Bot! Tap the gold coin to start earning points.")

@bot.message_handler(commands=['tap'])
def tap(message):
    user_id = message.from_user.id
    result = airdrop.tap(user_id)
    bot.reply_to(message, result)

@bot.message_handler(commands=['invite'])
def invite(message):
    user_id = message.from_user.id
    invite_link = user_management.generate_invite_link(user_id)
    bot.reply_to(message, f"Share this link to invite friends: {invite_link}")

@bot.message_handler(commands=['wallet'])
def connect_wallet(message):
    user_id = message.from_user.id
    bot.reply_to(message, "Please provide your wallet address.")

@bot.message_handler(commands=['tasks'])
def daily_tasks(message):
    tasks_list = tasks.get_daily_tasks()
    bot.reply_to(message, f"Today's tasks:\n{tasks_list}")

@bot.message_handler(commands=['leaderboard'])
def show_leaderboard(message):
    top_users = leaderboard.get_top_users()
    bot.reply_to(message, f"Top users:\n{top_users}")

@bot.message_handler(commands=['boost'])
def boost(message):
    user_id = message.from_user.id
    result = airdrop.boost(user_id)
    bot.reply_to(message, result)

@bot.message_handler(commands=['mine'])
def mine(message):
    user_id = message.from_user.id
    result = mining.start_mining(user_id)
    bot.reply_to(message, result)

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + TOKEN)
    app.run(host='0.0.0.0', port=8443)