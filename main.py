from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import gdax
import requests
from random import *
from bitfinex.client import Client
from bittrex.bittrex import Bittrex

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

gdax_client = gdax.PublicClient()
bitf_client = Client()
bittrex_client = Bittrex(None, None)

def help(bot, update):
    result = "Supported Commands\n"
    result = result + "(GDAX Price Lookup) /gdax <FIRST-H-PAIR> <SECOND-H-PAIR>\n"
    result = result + "(Bittrex Price Lookup) /btrx <FIRST-H-PAIR> <SECOND-H-PAIR>\n"
    result = result + "(Bitfinex Price Lookup) /bitf <FIRST-H-PAIR> <SECOND-H-PAIR>\n"
    result = result + "(Kraken Price Lookup) /krkn <FIRST-H-PAIR> <Second-H-PAIR>\n"
    result = result + "(Random Coin BTRX) /rcoin\n"
    result = result + "Example: /gdax ETH USD\n"
    update.message.reply_text(result)



def gdax(bot, update):
    split_command = update.message.text.split(' ')
    if len(split_command) == 3:
        pair_combined = split_command[1].upper()+"-"+split_command[2].upper()
        current_ticker = gdax_client.get_product_ticker(product_id=pair_combined)
        if not 'message' in current_ticker:
            result = ""
            result = result + "Bid: " + str(current_ticker['bid']) + "\n"
            result = result + "Ask: " + str(current_ticker['ask']) + "\n"
            result = result + "Last: " + str(current_ticker['price'])
            update.message.reply_text(result)
        else:
            update.message.reply_text("Unkown GDAX Pair")

def bitf(bot, update):
    split_command = update.message.text.split(' ')
    if len(split_command) == 3:
        pair_combined = split_command[1]+split_command[2]
        current_ticker = bitf_client.ticker(pair_combined)
        if not 'message' in current_ticker:
            result = ""
            result = result + "Bid: " + str(current_ticker['bid']) + "\n"
            result = result + "Ask: " + str(current_ticker['mid']) + "\n"
            result = result + "Last: " + str(current_ticker['last_price'])
            update.message.reply_text(result)
        else:
            update.message.reply_text("Unkown Bitfinex Pair")

def btrx(bot, update):
    split_command = update.message.text.split(' ')
    if len(split_command) == 3:
        pair_combined = split_command[1].upper()+"-"+split_command[2].upper()
        current_ticker = bittrex_client.get_ticker(pair_combined)
        if str(current_ticker['message']) == '':
            result = ""
            result = result + "Bid: " + str(current_ticker['result']['Bid']) + "\n"
            result = result + "Ask: " + str(current_ticker['result']['Ask']) + "\n"
            result = result + "Last: " + str(current_ticker['result']['Last'])
            update.message.reply_text(result)
        else:
            update.message.reply_text("Unkown Bittrex Pair")

def krkn(bot,update):
    split_command = update.message.text.split(' ')
    if len(split_command) == 3:
        pair_combined = split_command[1].upper()+split_command[2].upper()

        r = requests.post('https://api.kraken.com/0/public/Ticker', data={'pair':pair_combined})
        current_ticker = r.json()

        if len(current_ticker['error']) == 0:
            result = ""
            result = result + "Bid: " + str(current_ticker['result'].items()[0][1]['b'][0]) + "\n"
            result = result + "Ask: " + str(current_ticker['result'].items()[0][1]['a'][0]) + "\n"
            result = result + "Last: " + str(current_ticker['result'].items()[0][1]['c'][0])
            update.message.reply_text(result)
        else:
            update.message.reply_text("Unkown Kraken Pair")

 
def rcoin(bot,update):

    pair_combined = bittrex_client.get_markets()['result'][randint(0, 261)]['MarketName']
    current_ticker = bittrex_client.get_ticker(pair_combined)
    if str(current_ticker['message']) == '':
        result = "Coin: " + pair_combined + "\n"
        result = result + "Bid: " + str(current_ticker['result']['Bid']) + "\n"
        result = result + "Ask: " + str(current_ticker['result']['Ask']) + "\n"
        result = result + "Last: " + str(current_ticker['result']['Last'])
        update.message.reply_text(result)
    else:
        update.message.reply_text("Unkown Bittrex Pair")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    print "Starting Crypto Notification Bot"

    updater = Updater("<BOT FATHER API KEY HERE>")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("gdax", gdax))
    dp.add_handler(CommandHandler("bitf", bitf))
    dp.add_handler(CommandHandler("btrx", btrx))
    dp.add_handler(CommandHandler("krkn", krkn))
    dp.add_handler(CommandHandler("rcoin", rcoin))
    
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()