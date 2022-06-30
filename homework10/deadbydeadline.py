import os
import validators as validators
import telebot
import gspread
import json
import pandas as pd
import re
from datetime import datetime, timedelta
import emoji

bot = telebot.TeleBot('5491840084:AAHlXI7KPbwiWol_b_jieSaZAPQAWmlhiL8')
pinkpony = []

def convert_date(date: str = "01/01/00"):
    """ Конвертируем дату из строки в datetime """
    try:
        return datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        return False



def connect_table(message):
    """ Подключаемся к Google-таблице """
    url = message.text
    sheet_id = ('1bWPrv9Yimuhdp5FmhFC51dLdHPvWyYQi8e1dOdS96SQ') # Нужно извлечь id страницы из ссылки на Google-таблицу
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open('tables.json', 'w') as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")

def access_current_sheet():
    """ Обращаемся к Google-таблице """
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    df = pd.DataFrame(worksheet.get_values(""), columns=worksheet.row_values(1))
    df = df.drop(0)
    df.index -= 1
    return worksheet, tables[max(tables)]["url"], df


def choose_action(message):
    """ Обрабатываем действия верхнего уровня """
    if message.text == "Подключить Google-таблицу":
        connect_table(message)
    elif message.text == "Редактировать предметы" or message.text == emoji.emojize("Редактировать предметы :pen:", variant="emoji_type"):
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить")
        start_markup.row("Редактировать")
        start_markup.row("Удалить одно")
        start_markup.row("Удалить все")
        info = bot.send_message(message.chat.id, "Что делать будем?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)
    elif message.text == "Редактировать дедлайн" or message.text == emoji.emojize("Редактировать дедлайны :pencil:", variant="emoji_type"):
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить дату")
        start_markup.row("Изменить дату")
        info = bot.send_message(message.chat.id, "Что делать будем?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_deadline_action)
    elif message.text == "Посмотреть дедлайны на этой неделе" or  message.text == emoji.emojize("Посмотреть дедлайны на этой неделе :calendar:", variant="emoji_type"):
        today = datetime.today()
        week = today + timedelta(days=7)
        a, b, df = access_current_sheet()
        mes = f""
        for i in range(2, len(a.col_values(1)) + 1):
            for ddl in a.row_values(i)[2:]:
                if convert_date(ddl) <= week and convert_date(ddl) >= today:
                    mes += f"{a.cell(i, 1).value}: {ddl}\n"
        bot.send_message(message.chat.id, mes)
        start(message)
        # stop(message)


def choose_subject_action(message):
    """ Выбираем действие в разделе Редактировать предметы """
    if message.text == "Добавить":
        message = bot.send_message(message.chat.id, "Диктуй, я записываю")
        bot.register_next_step_handler(message, add_new_subject)
    elif message.text == "Редактировать":
        a, b, c = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        # for el in c.subject:
            # mrkp.row(f"{el}")
        inf = bot.send_message(message.chat.id, "Какой предмет редактируем?", reply_markup=mrkp)
        bot.register_next_step_handler(inf, update_subject)
    elif message.text == "Удалить одно":
        a, b, c = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        #for el in c.subject:
           # mrkp.row(f"{el}")
        inf = bot.send_message(message.chat.id, "Какой предмет удаляем?", reply_markup=mrkp)
        bot.register_next_step_handler(inf, delete_subject)

    elif message.text == "Удалить все":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Да")
        start_markup.row("Нет")
        start_markup.row("Не знаю")
        info = bot.send_message(message.chat.id, "Я бы на твоем месте подумал еще", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_removal_option)


def choose_deadline_action(message):
    """ Выбираем действие в разделе Редактировать дедлайн """
    if message.text == "Добавить дату":
        a, b, c = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        # for el in c.subject:
            # mrkp.row(f"{el}")
        inf = bot.send_message(message.chat.id, "Какому предмету добавляем?", reply_markup=mrkp)
        bot.register_next_step_handler(inf,choose_subject)
    elif message.text == "Изменить дату":
        a, b, c = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        # for el in c.subject:
            # mrkp.row(f"{el}")
        inf = bot.send_message(message.chat.id, "Для какого предмета изменяем?", reply_markup=mrkp)
        bot.register_next_step_handler(inf, update_subject_deadline)


def choose_removal_option(message):
    """ Уточняем, точно ли надо удалить все """
    if message.text == "Да":
        clear_subject_list(message)
    elif message.text == "Нет":
        # start(message)
        stop(message)
    elif message.text == "Не знаю":
        # start(message)
        stop(message)
        # bot.send_message(message.chat.id, emoji.emojize(":neutral face:", variant="emoji_type"))

def choose_subject(message):
    """ Выбираем предмет, у которого надо отредактировать дедлайн """
    global pinkpony
    pinkpony= []
    pinkpony.append(message.text)
    inf = bot.send_message(message.chat.id, "Введите время в формате 'dd.mm.yyyy'")
    bot.register_next_step_handler(inf, choose_subject2)

def choose_subject2(message):
    global pinkpony
    if not re.match(r"\d\d.\d\d.\d\d\d\d", message.text):
        inf = bot.send_message(message.chat.id, "Неправильный формат!\nВведите время в формате 'dd.mm.yyyy'")
        bot.register_next_step_handler(inf, choose_subject2)
    elif not convert_date(message.text):
        info = bot.send_message(message.chat.id, "Такой даты не существует, но лабу защищать все равно придется, try again",reply_markup=None,)
        bot.register_next_step_handler(info, choose_subject2)
    else:
        if convert_date(message.text) <= datetime.today():
            bot.send_message(message.chat.id, "Too late, bro")
        elif convert_date(message.text) > datetime.today().replace(year=datetime.today().year + 5):
            info = bot.send_message(message.chat.id, "Ты уже закончишь учиться к тому времени, надеюсь. Введи новую дату", reply_markup=None,)
            bot.register_next_step_handler(info, choose_subject2)
            return
        else:
            a, b, c = access_current_sheet()
            row = a.find(f"{pinkpony[0]}").row
            n = len(a.row_values(row))
            a.update_cell(row, n + 1, message.text)
            if not a.cell(1, n + 1).value:
                num = int(a.cell(1, n).value)
                a.update_cell(1, n + 1, num + 1)
            bot.send_message(message.chat.id, "Изменено!")
            start(message)
            # stop(message)


def update_subject_deadline(message):
    """ Обновляем дедлайн """
    global pinkpony
    pinkpony = []
    pinkpony.append(message.text)
    a, b, c = access_current_sheet()
    mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for el in c.columns[2:]:
        mrkp.row(f"{el}")
    inf = bot.send_message(message.chat.id, "Для какой лабы изменяем?", reply_markup=mrkp)
    bot.register_next_step_handler(inf, update_subject_deadline2)

def update_subject_deadline2(message):
    global pinkpony
    pinkpony.append(message.text)
    inf = bot.send_message(message.chat.id, "Введите время в формате 'dd.mm.yyyy'")
    bot.register_next_step_handler(inf, update_subject_deadline3)


def update_subject_deadline3(message):
    global pinkpony
    if not re.match(r"\d\d.\d\d.\d\d\d\d", message.text):
        inf = bot.send_message(message.chat.id, "Неправильный формат!\nВведите время в формате 'dd.mm.yyyy'")
        bot.register_next_step_handler(inf,choose_subject2)
    elif not convert_date(message.text):
        info = bot.send_message(message.chat.id, "Такой даты не существует, но лабу защищать все равно придется, try again",reply_markup=None,)
        bot.register_next_step_handler(info, update_subject_deadline3)
    else:
        if convert_date(message.text) <= datetime.today():
            bot.send_message(message.chat.id, "Too late, bro")
        elif convert_date(message.text) > datetime.today().replace(year=datetime.today().year + 5):
            info = bot.send_message(message.chat.id, "Ты уже закончишь учиться к тому времени, надеюсь. Введи новую дату", reply_markup=None,)
            bot.register_next_step_handler(info, update_subject_deadline3)
            return
        else:
            a, b, c = access_current_sheet()
            row = a.find(f"{pinkpony[0]}").row
            col = a.find(f"{pinkpony[1]}").col
            a.update_cell(row, col, message.text)
            bot.send_message(message.chat.id, "Изменено!")
            start(message)
            # stop(message)


def add_new_subject(message):
    """ Вносим новое название предмета в Google-таблицу """
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        if validators.url(url):
            worksheet, b, c = access_current_sheet()
            worksheet.append_row([name, url])
            bot.send_message(message.chat.id, "Добавлено!")
        if not validators.url(url):
            info = bot.send_message(
                message.chat.id, "Это не ссылка, но попытка засчитана, введи еще раз", reply_markup=None
            )
            bot.register_next_step_handler(info, add_new_subject)
            return
        stop(message)
    except IndexError:
        inf = bot.send_message(message.chat.id,
                               "Название и ссылка должны быть в одном сообщении и разделены пробелом!")
        bot.register_next_step_handler(inf, add_new_subject)


def add_new_subject_url(message):
    """ Вносим новую ссылку на таблицу предмета в Google-таблицу """
    # PUT YOUR CODE HERE
    pass


def update_subject(message):
    """ Обновляем информацию о предмете в Google-таблице """
    global pinkpony
    pinkpony = []
    pinkpony.append(message.text)
    inf = bot.send_message(message.chat.id,
                           "Введите новую информацию в формате '{название} {ссылка}'. Если что-то из этого не должно измениться напишите его без изменений")
    bot.register_next_step_handler(inf, update_subject2)

def update_subject2(message):
    global pinkpony
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        if validators.url(url):
            worksheet, b, df = access_current_sheet()
            ind = df.loc[df.isin(pinkpony).any(axis=1)].index[0] + 2
            cell_list = worksheet.range(f'A{ind}:B{ind}')
            cell_list[0].value = name
            cell_list[1].value = url
            worksheet.update_cells(cell_list)
            bot.send_message(message.chat.id, "Изменено!")
        if not validators.url(url):
            info = bot.send_message(
                message.chat.id, "Это не ссылка, но попытка засчитана, введи еще раз", reply_markup=None
            )
            bot.register_next_step_handler(info, update_subject2)
            return
    except IndexError:
        inf = bot.send_message(message.chat.id, "Название и ссылка должны быть в одном сообщении и разделены пробелом!")
        bot.register_next_step_handler(inf, update_subject2)
    start(message)
    # stop(message)


def delete_subject(message):
    """ Удаляем предмет в Google-таблице """
    worksheet, b, df = access_current_sheet()
    ind = df.loc[df.isin([message.text]).any(axis=1)].index[0] + 2
    worksheet.delete_rows(int(ind), int(ind))
    bot.send_message(message.chat.id, "Удалено!")
    start(message)
    # stop(message)


def clear_subject_list(message):
    """ Удаляем все из Google-таблицы """
    with open("tables.json") as json_file:
        tables = json.load(json_file)
    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    sh.del_worksheet(worksheet)
    start(message)
    # stop(message)

@bot.message_handler(content_types=["text"])
def marhaba(message):
    if message.text == "Мархаба!":
        start(message)

def start(message):
    global pinkpony
    pinkpony.clear()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if not os.path.exists("tables.json"):
        start_markup.row("Подключить Google-таблицу")

    start_markup.row(emoji.emojize("Посмотреть дедлайны на этой неделе :calendar:", variant="emoji_type"))
    start_markup.row(emoji.emojize("Редактировать дедлайны :pencil:", variant="emoji_type"))
    start_markup.row(emoji.emojize("Редактировать предметы :pen:", variant="emoji_type"))

    info = bot.send_message(message.chat.id, "Что прикажете делать, госпожа?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)

def stop(message):
    if message.text == "Вернуться в начало":
        start(message)
    elif message.text == "Шукран!":
        bot.send_message(message.chat.id, emoji.emojize("Хазз саид! :red_heart:", variant="emoji_type"))



if __name__=="__main__":
    bot.infinity_polling()
