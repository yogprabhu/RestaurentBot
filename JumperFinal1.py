from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, YesOrNO, Numberofpeople, AcceptDateTime, displayall   = range(6)

#reply_keyboard = [['Age', 'Favourite colour'],
#                  ['Number of siblings', 'Something else...'],
#                  ['Done']]
#markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

reply_keyboard2 = [['Book a Table'],
                  ['Contact Restaurent...']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)

reply_keyboard3 = [['YES', 'NO']]
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def custom_choice(bot, update):
    update.message.reply_text('Presian Darbar, Byculla : +91 9096492696')


def start(bot, update):
    update.message.reply_text(
        "Welcome to Persian Darbar!!!",
        reply_markup=markup2)

    return CHOOSING


def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text(
        'You requested to  {}? Yes, I would love to hear about that! \n ENTER YOUR NAME'.format(text.lower()))

    return TYPING_REPLY

def OldOrNew(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Welcome to"
                              "{}"
                              "You can tell me more, Are you visiting our restaurent for first time??".format(facts_to_str(user_data)), reply_markup=markup3)

    return YesOrNO

def NewUser(bot, update):
    update.message.reply_text('Welcome !!!!! \n Table For??')

    return Numberofpeople

def seats(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text(
        'You requested to  {}? Yes, I would love to hear more about reservation! \n ENTER Date and Time'.format(text.lower()))

    return AcceptDateTime

def confirm(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("CONGRATULATIONS.... \n Confirmed!!!!! Your Booking is confirmed at"
                              "{}".format(facts_to_str(user_data)))
    return displayall


def detailDisplay(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Your Booking Details"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('559395160:AAGMVOmWGMm0vJ4p-zqrl9p_K4T7bbORV7QYOX')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Book a Table)$',
                                    regular_choice,
                                    pass_user_data=True),
                       RegexHandler('^Contact Restaurent...$',
                                    custom_choice),
                       ],

            

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          OldOrNew,
                                          pass_user_data=True),
                           ],
            
            YesOrNO: [RegexHandler('^(Yes)$',
                                    NewUser,
                                    pass_user_data=True),
                       RegexHandler('^(No)$',
                                    NewUser),
                       ],
            Numberofpeople: [RegexHandler('^(One | Two | Three | Four & More)$',
                                    seats,
                                    pass_user_data=True)
                       ],
            AcceptDateTime: [MessageHandler(Filters.text,
                                          confirm,
                                          pass_user_data=True)
                           ],
            displayall: [RegexHandler('^(Done)$',
                                    detailDisplay,
                                    pass_user_data=True)
                           ]
        },
        fallbacks=[RegexHandler('^Done$', detailDisplay, pass_user_data=True)]

        
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
