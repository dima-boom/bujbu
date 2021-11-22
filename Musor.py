try:
    import telebot, vk_api, time, threading, requests, os, psycopg2, random, vk_captchasolver as vc
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
        clava INT,
        pos_gr INT,
        vobs INT);''')
    con.commit()  

    def extract_arg(arg):
        return arg.split()[1]


    def extract_arg2(arg2):
        return arg2.split()[2]

    bot = telebot.TeleBot('1639945945:AAFCziHtYMHdGdQAkM07CKCmDLd1QNVT-xw')

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
    clava4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    c15 = types.KeyboardButton('Ввод')
    c16 = types.KeyboardButton('Последняя')
    clava4.add(c15, c16)
    def clava(send):
        global i
        cur.execute(f"SELECT clava FROM tab WHERE id = '{send}'")
        i = cur.fetchall()[0][0]
    def clava_n(send, zn):
        global i
        cur.execute(f"""UPDATE tab SET clava = {int(zn)} WHERE id = {send}""")
        con.commit()
    def poc_gr(send, zn):
        cur.execute(f"""UPDATE tab SET pos_gr = {int(zn)} WHERE id = {send}""")
        con.commit()
    def voob(send, zn):
        cur.execute(f"""UPDATE tab SET vobs = {int(zn)} WHERE id = {send}""")
        con.commit()
    def polz(send):
        # Добавление записи
        cur.execute(f"SELECT id FROM tab WHERE id = '{send}'")
        if str(cur.fetchall()) == '[]':
            cur.execute(f"""INSERT INTO tab (id, txt, tok, clava, pos_gr, vobs) VALUES ({send}, 'Текст', 'Токен', 0, 0, 0);""")
            con.commit()
        else:
            pass

    def rass(user_id, group_col):
        cur.execute(f"SELECT * FROM tab WHERE id = '{user_id}'")
        vvvb = cur.fetchall()
        text = vvvb[0][1]
        token = vvvb[0][2]
        poc_g = vvvb[0][4]
        vob = vvvb[0][5]
        try:
            vk_session = vk_api.VkApi(token=token)
            vk = vk_session.get_api()
            vk.users.get()
        except:
            clava_n(user_id, 0)
            bot.send_message(user_id, f"Аккаунт заблокирован!")
            return
        vob = int(vob)
        while True:
            try:
                if vob == 0:
                    try:
                        first_group = vk.groups.create(title="Ремонт авто "+str(random.randint(1000, 9999)))["id"]-int(group_col)
                        break

                    except vk_api.Captcha as group_captch:
                        result_solve_captcha = vc.solve(sid=int(group_captch.sid), s=1)
                        try:
                            group_captch.try_again(result_solve_captcha)
                        except vk_api.Captcha as cptch2:
                            pass

                    except:
                        clava_n(user_id, 0)
                        bot.send_message(user_id, f"Аккаунт заблокирован!")
                        return
                else:
                    try:
                        first_group = vk.groups.create(title="Ремонт авто "+str(random.randint(1000, 9999)))["id"]
                        first_group1 = first_group-int(poc_g)
                        first_group = int(first_group-first_group1)
                        break

                    except vk_api.Captcha as group_captch:
                        result_solve_captcha = vc.solve(sid=int(group_captch.sid), s=1)
                        try:
                            group_captch.try_again(result_solve_captcha)
                        except vk_api.Captcha as cptch2:
                            pass

                    except:
                        clava_n(user_id, 0)
                        bot.send_message(user_id, f"Аккаунт заблокирован!")
                        return
            except:
                pass



        sp_group = []
        itog = []
        grp = first_group
        na_a = time.time()
        for i in range(int(group_col)//500):
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
        na_b = time.time()
        vr = int(na_b-na_a)
        bot.send_message(user_id, f"Время сбора информации \nсоставило - "+str(vr)+" сек.\nДоступно для рассылки - "+str(len(itog))+" групп")
        col = 0
        success = 0
        fail = 0
        cost = 0
        vr_r = time.time()
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
            except vk_api.ApiError:
                try:
                    vk_session = vk_api.VkApi(token=token)
                    vk = vk_session.get_api()
                    vk.status.get()
                except vk_api.ApiError:
                    cost = 1
                    break
            except:
                fail += 1
                col += 1
            first_group += 1
        ohib = int(col - success)
        vr_r1 = time.time()
        vr_r2 = int(vr_r1-vr_r)
        poc_gr(user_id, int(D))
        clava_n(user_id, 0)
        if cost == 0:
            bot.send_message(user_id, f"Отчёт. \n\nЗакончились группы! \nВремя - {str(vr_r2)} сек. \n\nУспешно - {str(success)} \nОшибок - {str(ohib)} \nВсего отправлено - {str(col)}", reply_markup=markup)
        else:
            bot.send_message(user_id, f"Отчёт. \n\nАккаунт заблокирован! \nВремя - {str(vr_r2)} сек. \nУспешно - {str(success)} \nОшибок - {str(ohib)} \nВсего отправлено - {str(col)}", reply_markup=markup)


    @bot.message_handler()
    def get_text_messages(message):
        messages = message.from_user.id
        mess = message.text.lower()
        polz(messages)
        clava(messages)
        if mess == "/start":
            bot.send_message(messages, f"Привет, {message.from_user.first_name}! \nРады видеть тебя в нашей группе 😊", reply_markup=markup)
        elif mess[0:11] == 'новый текст':
            clava_n(messages, 2)
            bot.send_message(messages, f"Введите текст.", reply_markup=clava2)
        elif i == 2:
            cur.execute(f"""UPDATE tab SET txt = '{message.text}' WHERE id = {messages}""")
            con.commit()
            clava_n(messages, 0)
            bot.send_message(messages, f"Текст записан.", reply_markup=markup)
        elif mess[0:11] == 'новый токен':
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
        elif mess[0:6] == 'запуск':
            if i == 0:
                clava_n(messages, 7)
                bot.send_message(messages, f"Выбор:", reply_markup=clava4)
            else:
                bot.send_message(messages, f"Уже запущено.", reply_markup=markup)
        elif mess[0:4] == 'ввод' and i == 7:
            clava_n(messages, 10)
            bot.send_message(messages, f"Введите Количество грпупп:", reply_markup=clava2)
        elif mess[0:9] == 'последняя' and i == 7:
            voob(messages, 1)
            clava_n(messages, 11)
            rass(messages, 1)
            bot.send_message(messages, f"Успешно.", reply_markup=markup)
        elif mess == '/new':
            clava_n(messages, 0)
            bot.send_message(messages, f"Перезапуск.", reply_markup=markup)
        elif mess == 'отмена' and i != 0:
            clava_n(messages, 0)
            bot.send_message(messages, f"Главное меню.", reply_markup=markup)
        elif i == 10:
            voob(messages, 0)
            try:
                if int(mess) > 499:  
                    bot.send_message(messages, f"Успешно.", reply_markup=markup)
                    clava_n(messages, 11)
                    rass(messages, mess)
                else:
                    bot.send_message(messages, f"Введите больше 500.", reply_markup=clava2)
            except:
                bot.send_message(messages, f"Количество грпупп?", reply_markup=clava2)
        else:
            bot.send_message(messages, f"Не верно!", reply_markup=markup)
    bot.polling(none_stop=True, interval=0)
except:
    os.system('python Musor.py')
