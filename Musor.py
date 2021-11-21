try:
    import telebot, vk_api, time, threading, requests, os, psycopg2, random
    from telebot import types

    con = psycopg2.connect(
      database="d3ukp3qemhnre7", 
      user="jhgqkfekdycrkg", 
      password="fd1052e16657244d53740728bbb8c0d40893ebef71e467161344a62957094fc8", 
      host="ec2-54-72-136-69.eu-west-1.compute.amazonaws.com", 
      port="5432"
    )
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tab(
        id INT,
        txt TEXT,
        tok TEXT,
        clava INT);''')
    con.commit()  

    def extract_arg(arg):
        return arg.split()[1]


    def extract_arg2(arg2):
        return arg2.split()[2]

    bot = telebot.TeleBot('1736495852:AAFrs4OON5l06joK25FE5wh8-LBbHI7GdiA')

    print('Работает!')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Запуск')
    item14 = types.KeyboardButton('Новый текст')
    item15 = types.KeyboardButton('Новый токен')
    item16 = types.KeyboardButton('Текст')
    item17 = types.KeyboardButton('Токен')
    markup.add(item1)
    markup.add(item14, item15)
    markup.add(item16, item17)
    clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    c13 = types.KeyboardButton('Отмена')
    clava2.add(c13)

    def clava(send):
        global i
        cur.execute(f"SELECT clava FROM tab WHERE id = '{send}'")
        i = cur.fetchall()[0][0]
    def clava_n(send, zn):
        global i
        cur.execute(f"""UPDATE tab SET clava = {int(zn)} WHERE id = {send}""")
        con.commit()
    def polz(send):
        # Добавление записи
        cur.execute(f"SELECT id FROM tab WHERE id = '{send}'")
        if str(cur.fetchall()) == '[]':
            cur.execute(f"""INSERT INTO tab (id, txt, tok, clava) VALUES ({send}, 'Текст', 'Токен', 0);""")
            con.commit()
        else:
            pass

    def rass(user_id, group_col):
        bot.send_message(user_id, f"buvv", reply_markup=markup)
        cur.execute(f"SELECT * FROM tab WHERE id = '{user_id}'")
        bot.send_message(user_id, f"1. J", reply_markup=markup)
        text = str(cur.fetchall()[0][1])
        bot.send_message(user_id, f"hhb", reply_markup=markup)
        cur.execute(f"SELECT * FROM tab WHERE id = '{user_id}'")
        tokennn = str(cur.fetchall()[0][2])
        bot.send_message(user_id, f"Глав", reply_markup=markup)
        vk_session = vk_api.VkApi(token=tokennn)
        vk = vk_session.get_api()
        while True:
            try:
                first_group = vk.groups.create(title="Ремонт авто "+str(random.randint(1000, 9999)))["id"]-group_col
                break
            except vk_api.Captcha as group_captch:
                result_solve_captcha = vc.solve(sid=int(group_captch.sid), s=1)
                try:
                    group_captch.try_again(result_solve_captcha)
                except vk_api.Captcha as cptch2:
                    pass
        sp_group = []
        itog = []
        grp = first_group
        for i in range(group_col//500):
            sp_group = []
            for k in range(500):
                sp_group.append(str(grp))
                grp+=1
            new_sp = vk.groups.getById(group_ids=sp_group, fields="can_message")
            for j in new_sp:
                if j["can_message"] == 1:
                    itog.append(int(j['id']))
                else:
                    continue
        col = 0
        success = 0
        fail = 0
        for D in itog:
            try:
                vk.messages.send(peer_id=-D, random_id=0, message=text)
                success += 1
                col += 1
            except vk_api.Captcha:
                cycle = True
                while cycle:
                    try:
                        vk.messages.send(peer_id=-D, random_id=0, message=text)
                    except vk_api.Captcha as cptch:
                        result_solve_captcha = vc.solve(sid=int(cptch.sid), s=1)
                        try:
                            cptch.try_again(result_solve_captcha)
                            cycle = False
                        except vk_api.Captcha as cptch2:
                            pass
                    except:
                        pass
        clava_n(user_id, 0)
        bot.send_message(messages, f"Отчёт. \n\nУспешно - {str(success)} \nВсего отправлено - {str(col-1)}", reply_markup=markup)


    @bot.message_handler()
    def get_text_messages(message):
        messages = message.from_user.id
        mess = message.text.lower()
        polz(messages)
        clava(messages)
        if mess == "/start":
            bot.send_message(messages, f"Привет, {message.from_user.first_name}! \nРады видеть тебя в нашей группе 😊", reply_markup=markup)
        elif mess[0:11] == 'новый текст' and i == 0:
            clava_n(messages, 2)
            bot.send_message(messages, f"Введите текст.", reply_markup=clava2)
        elif i == 2:
            cur.execute(f"""UPDATE tab SET txt = '{message.text}' WHERE id = {messages}""")
            con.commit()
            clava_n(messages, 0)
            bot.send_message(messages, f"Текст записан.", reply_markup=markup)
        elif mess[0:11] == 'новый токен' and i == 0:
            clava_n(messages, 3)
            bot.send_message(messages, f"Введите токен.", reply_markup=clava2)
        elif i == 3:
            try:
                vk_session = vk_api.VkApi(token=mess)
                vk = vk_session.get_api()
                asd = vk.users.get()
                cur.execute(f"""UPDATE tab SET tok = '{message.text}' WHERE id = {messages}""")
                con.commit()
                clava_n(messages, 0)
                bot.send_message(messages, f"Токен записан.", reply_markup=markup)
            except:
                bot.send_message(messages, f"Тoken ban!!!", reply_markup=clava2)

        elif mess == 'текст':
            cur.execute(f"SELECT * FROM tab WHERE id = '{messages}'")
            j = cur.fetchall()[0][1]
            bot.send_message(messages, str(j), reply_markup=markup)
        elif mess == 'токен':
            cur.execute(f"SELECT * FROM tab WHERE id = '{messages}'")
            took = cur.fetchall()[0][2]
            bot.send_message(messages, str(took), reply_markup=markup)
        elif mess[0:6] == 'запуск' and i == 0:
            if i == 0:
                clava_n(messages, 10)
                bot.send_message(messages, f"Количество грпупп:", reply_markup=clava2)
            else:
                bot.send_message(messages, f"Уже запущено.", reply_markup=markup)
        elif mess == '/new':
            clava_n(messages, 0)
            bot.send_message(messages, f"Перезапуск.", reply_markup=markup)
        elif mess == 'отмена' and i != 0:
            clava_n(messages, 0)
            bot.send_message(messages, f"Главное меню.", reply_markup=markup)
        elif i == 10:
            bot.send_message(messages, f"Запущено.", reply_markup=markup)
            rass(messages, mess)
        else:
            bot.send_message(messages, f"Не верно!", reply_markup=markup)
    bot.polling(none_stop=True, interval=0)
except:
    os.system('python Musor.py')
