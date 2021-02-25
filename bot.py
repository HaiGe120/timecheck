#! /usr/bin/env python3
from baiduspider import BaiduSpider
from pprint import pprint
import datetime
import telebot
import sys
import io

spider = BaiduSpider()
bot = telebot.TeleBot("TOKEN") #replace the TOKEN!!
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    cid = message.chat.id
    mid = message.message_id
    searx = message.text
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    result=spider.search_web(query=searx)
    result1 = result['results']
    del result1[1:2]
    del result1[-1]

    def get_recursively(search_dict, field):
        """
        Takes a dict with nested lists and dicts,
        and searches all dicts for a key of the field
        provided.
        """
        fields_found = []

        for key, value in search_dict.items():

            if key == field:
                fields_found.append(value)
            if key == 'time':
                fields_found.append(value)

            elif isinstance(value, dict):
                results = get_recursively(value, field)
                for result in results:
                    fields_found.append(result)
                    if key == 'time':
                        fields_found.append(result)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        more_results = get_recursively(item, field)
                        for another_result in more_results:
                            fields_found.append(another_result)
                            if key == 'time':
                                fields_found.append(result)

        return fields_found

    des = get_recursively(result, 'des')
    des1 = des
    j = 1
    for i in enumerate(des):
        des[j] = str(des[j])
        j += 1
        if j == len(des1):
            break

    matching = [n for n, x in enumerate(des) if searx in x]

    final = []

    for n in matching:
        final.append(des[n+1])
        final.append(des[n])

    c = 0
    now = datetime.datetime.now()
    for n in matching:
        if des[n+1][0:4].isdecimal():
            date = int(des[n+1][0:4])
            if date < now.year:
                c += 1
    end = telebot.types.Message(from_user = 0,
                        date = '',
                        options = [],
                        json_string = '',
                        content_type='text',
                        chat = 0,
                        message_id = 0)

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    print('There are',c,'suspected rumors counted\n\n', final)
    output = new_stdout.getvalue()
    sys.stdout = old_stdout
    end.text = output
    bot.reply_to(message, end.text)

bot.polling()
