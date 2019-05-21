from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import logging
from datetime import timedelta

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Команды:\n"/yxa" - случайный анекдот из контакта\nДля вызова этого сообщения используй /start')


def call(bot, job):
    bot.send_message(job.context, text='event!!!')


def event(bot, update, args, job_queue, chat_data):
    try:
        m = int(args[0])
        tim = timedelta(seconds=m)

        job = job_queue.run_repeating(call, m, context=update.message.chat_id)
        chat_data['event'] = job
        update.message.reply_text('Timer successfully set!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /event <minute>')


def unset(bot, update, args, chat_data):
    """Removes the job if the user changed their mind"""

    if args[0] not in chat_data:
        for d in chat_data:
            update.message.reply_text(d)
        return

    job = chat_data[args[0]]
    job.schedule_removal()
    del chat_data[args[0]]

    update.message.reply_text('Timer successfully unset!')


def main():
    updater = Updater("404672999:AAF2nOfQWL0YL8sbTwuyDsio8B9TEFuV8ZU")
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('event', event,
                                                  pass_args=True,
                                                  pass_job_queue=True,
                                                  pass_chat_data=True))
    updater.dispatcher.add_handler(CommandHandler("unset", unset,
                                                  pass_args=True,
                                                  pass_chat_data=True))
    updater.dispatcher.add_error_handler(error)

    updater.start_polling(poll_interval=3, timeout=20, read_latency=5)
    updater.idle()

if __name__ == '__main__':
    main()