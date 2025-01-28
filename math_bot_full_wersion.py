import telebot
import time

bot = telebot.TeleBot("7590412045:AAFYSqWWtqxq_xPqcB_GsFATozVgA4crjH4")
ADMIN_ID = "5175228298"
TEACHER_ID = ""

user_data = {}
equations = [
    {"example": "x² − 4x − 5 = 0", "roots": "5;-1"},
    {"example": "x² − 5x + 6 = 0", "roots": "2;3"},
    {"example": "2x² + 5x + 3 = 0", "roots": "-1;-1,5"},
    {"example": "4x² − 11x + 6 = 0", "roots": "3;1,5"},
    {"example": "x² − 6x + 8 = 0", "roots": "2;4"},]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Здравствуй, @{message.chat.username}, это закрытый алгебра-бот. Введи имя и фамилию для корректного отображения вашего результата.")
    bot.register_next_step_handler(message, ask_how_are_you)

def ask_how_are_you(message):
    user_data[message.chat.id] = {"name": message.text, "score": 0, "start_time": time.time()}
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_message(message.chat.id, f"Привет, это мини-бот созданный для тех кто хочет получить почти бесплатную оценку по алгебре (правда же? ;-) ). Собери все свои знания о дискриминанте и реши <b>5</b> сложнейших уравнений и получи оценку! Не забудь приготовить <b>листочек</b> и <b>ручку</b> что-бы решать!", reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton("Продолжить", callback_data="continue")),  parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "continue")
def continue_test(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Как уже было сказано уравнений всего 5, каждое выдаётся в случайном порядке и решается отдельно.\n <b>У вас будет всего одна попытка!</b>\n\n Ответ из 2-х корней обязательно нужно записывать так: (первый корень);(второй корень). \n <i>Пример:</i> <b>2;-8</b> \n\nПосле нажатия кнопки <i>'Начать решать'</i> будет запущен секундомер который будет считать потраченное время на все 5 уравнений.\n\nВ конце работы вы и учитель увидите результаты и ПРИБЛИЗИТЕЛЬНУЮ оценку за работу", reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton("Начать решать", callback_data="start_solving")), parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "start_solving")
def start_solving(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_equation(call.message.chat.id, 0)

def send_equation(chat_id, index):
    if index < len(equations):
        bot.send_message(chat_id, f"Уравнение №{index + 1} : {equations[index]['example']}, \n\n")
        bot.register_next_step_handler_by_chat_id(chat_id, lambda message: check_answer(message, index))
    else:
        end_test(chat_id)

def check_answer(message, index):
    if message.text == equations[index]['roots']:
        user_data[message.chat.id]['score'] += 1
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    send_equation(message.chat.id, index + 1)

def end_test(chat_id):
    elapsed_time = time.time() - user_data[chat_id]['start_time']
    score = user_data[chat_id]['score']
    grade = "5" if score == 5 else "4" if score == 4 else "3" if score == 3 else "2"
    name = user_data[chat_id]["name"]
    bot.send_message(chat_id, f"Поздравляем! Вы выполнили <b>все задания</b>! !\n<b> Правильно сделано заданий</b>: <i>{score}/5</i>\n <b>Общее время выполнения</b>: {elapsed_time:.0f} сек\n <b>Ваша примерная оценка</b>: <b>{grade}</b> \n(Учитель может поставить другую оценку)", reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton("Разработчики / вопросы / помощь", callback_data="help")), parse_mode="HTML")
    bot.send_message(ADMIN_ID, f"Задание выполнил(а): {name}\n<b> Правильно сделано заданий</b>: <i>{score}/5</i>\n <b>Время выполнения</b>: {elapsed_time:.0f} сек.\n <b>Примерная оценка</b>: {grade} <i>(Вы можете поставить свою)</i>", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_message(call):
    bot.send_message(call.message.chat.id, "По вопросам и помощью обращаться: @midomi047_support\n\n\n<b>Разработчики</b>:\n\n <b>Автор идеи</b>: <i>@NataGrigorevaV</i>\n\n <b>Безсонный кодер (программист)</b>: <i>@midomi047</i>\n\n <b>Копирайтер</b>: <i>@midomi047</i> \n\n <b>Подопытный кролик (тестировщик)</b>: Даниил \n\n\n\n<tg-spoiler>Не бейте шваброй если что-то не правильно...     Делалось всё под 3 кружками кофе...  :)</tg-spoiler>\n\n <i>MIDOMI TEAM© 2025</i>", parse_mode="HTML")


@bot.message_handler(commands=['what'])
def what(message):
    bot.send_message(message.chat.id, "<i>Ты нашёл секретку!</i>\n\n  Раз ты такой опытный пользователь телеграмма держи подсказку. Ответ на 2-ое уравнение <tg-spoiler>2,3</tg-spoiler>!", parse_mode="HTML")

bot.polling()