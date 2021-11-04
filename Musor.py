try:
	import telebot, os, time, vk_api, vk_captchasolver as vc, random, requests as r
	#os.system("cls")


	bot = telebot.TeleBot("2013056935:AAHLlHvu4qHXn5hTArJw-hGHTdeA3em71r8")

	def msg(id, text, kb, pm=None):
		send = bot.send_message(id, str(text), reply_markup=kb, parse_mode=pm)
		return send
	def msg_edit(chat_id, message_id, text, kb, pm=None):
		bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=kb, parse_mode=pm)
	def msg_new(message, func):
		return bot.register_next_step_handler(message, func)
	def msg_delete(chat_id, message_id):
		bot.delete_message(chat_id, message_id)
	def reply(message, text):
		bot.reply_to(message, text)

	def reply_keyboard():
		reply_kb = telebot.types.ReplyKeyboardMarkup(True)
		return reply_kb
	def inline_keyboard(rw=2):
		inline_kb = telebot.types.InlineKeyboardMarkup(row_width=rw)
		return inline_kb
	def ik_button(name, callback):
		button = telebot.types.InlineKeyboardButton(name, callback_data=callback)
		return button
	def ik_button_url(name, url):
		button = telebot.types.InlineKeyboardButton(name, url=url)
		return button

	kb = reply_keyboard()
	kb.row("⚡Рассылка", "Конфиг📂")
	kb.row("🔙Последняя рассылка⚡")

	kb_info = inline_keyboard()
	kb_info.add(ik_button("Показать информацию", "openinfo"))

	kb_close = inline_keyboard()
	kb_close.add(ik_button("❌Закрыть❌", "close"))

	kb_back = reply_keyboard()
	kb_back.row("Отмена")

	configs = {"1105536555": ["token", "text"],
			   "770430694": ["token", "text"]}
	mailing_sbor = {"1105536555": {"token": None,
								  "text": None},
					"770430694": {"token": None,
								  "text": None}}
	last_mailing = {"success": 0,
					"fail": 0,
					"all": 0,
					"total_time": 0,
					"one_time": 0,
					"search_group": 0,
					}
	last_group = 0
	mailing = False

	@bot.message_handler(content_types=["text"])
	def send_text(message):
		global mailing
		nickname = message.chat.username # Ник юзера
		name = message.chat.first_name # Имя
		id = message.chat.id # Айди
		text = message.text # Текст сообщения
		if str(id) in ["1105536555", "770430694"]:
			if text == "/start":
				msg(id, "Воспользуйся клавиатурой:", kb)
			elif text == "Конфиг📂":
				kb_config = inline_keyboard()
				kb_config.add(ik_button("Токен", str(id)+" 0"), ik_button("Текст", str(id)+" 1"))
				kb_config.add(ik_button("Ред. Токен", str(id)+" new 0"), ik_button("Ред. Текст", str(id)+" new 1"))
				msg(id, "Воспользуйся кнопками:", kb_config)
			elif text == "🔙Последняя рассылка⚡":
				if mailing == True:
					msg(id, "Рассылка кем-то запущена и пока нельзя смотреть статистику", kb)
				else:
					txt = "✅Успешно отправлено - "+str(last_mailing["success"])+"\n---------------------------\n❌Не удачно отправлено - "+str(last_mailing["fail"])+"\n---------------------------\n♾️Всего отправлено - "+str(last_mailing["all"])+"\n---------------------------\n🕒Время отправки - "+str(last_mailing["total_time"])+" с.\n---------------------------\n🕘Время отправки 1 смс - "+str(last_mailing["one_time"])+" с.\n---------------------------\n🔎Найдено групп - "+str(last_mailing["search_group"])
					msg(id, txt, kb_close)
			elif text == "⚡Рассылка":
				if mailing == True:
					msg(id, "Рассылка уже кем-то запущена", kb)
				else:
					kb_new_rass = inline_keyboard()
					kb_new_rass.add(ik_button("Записанный Токен", "readytoken"), ik_button("Записанный Текст", "readytext"))
					kb_new_rass.add(ik_button("Другой Токен", "newtoken"), ik_button("Другой Текст", "newtext"))
					kb_new_rass.add(ik_button("Сброс", "newnew"), ik_button("Обновить", "update"))
					kb_new_rass.add(ik_button("🏁 Запуск 🛎️", "mailing_start"))
					if mailing_sbor[str(id)]["token"] == None:
						tkn = "❌"
					if mailing_sbor[str(id)]["token"] != None:
						tkn = "✅"
					if mailing_sbor[str(id)]["text"] == None:
						txts = "❌"
					if mailing_sbor[str(id)]["text"] != None:
						txts = "✅"
					msg(id, "token - "+tkn+"\ntext - "+txts+"\n\nСобери инфо:", kb_new_rass)
			elif text == "/new":
				mailing = False


	@bot.callback_query_handler(func=lambda call: True)
	def callback(call):
		text = call.data
		id = call.message.chat.id
		message_id = call.message.message_id
		nickname = call.message.chat.username
		name = call.message.chat.first_name
		global last_group

		if text == "close":
			msg_delete(id, message_id)
		elif text in ["readytoken", "readytext"]:
			if text == "readytoken":
				if mailing_sbor[str(id)]["token"] != None and mailing_sbor[str(id)]["token"] == configs[str(id)][0]:
					msg(id, "🕒*Вы уже используйте записанный токен*", kb, pm="Markdown")
				else:
					token = configs[str(id)][0]
					for i in range(2, 4):
						try:
							vk_session = vk_api.VkApi(token=token)
							vk = vk_session.get_api()
							aaaaa = vk.status.get(user_id=554311036)["text"]
							mailing_sbor[str(id)]["token"] = token
							msg(id, "✅*В рассылки будет использоваться записанный токен*", kb, pm="Markdown")
							break
						except vk_api.ApiError:
							if i == 3:
								msg(id, "❌*Аккаунт по записанному токену был удален или заблокирован*", kb, pm="Markdown")
							else:
								continue
						except:
							msg(id, "❌*Не удалось авторизоваться по записанному токену*", kb, pm="Markdown")
							break
			elif text == "readytext":
				if configs[str(id)][1] == "text":
					msg(id, "❌*В конфиге не найден записанный текст*", kb, pm="Markdown")
				elif mailing_sbor[str(id)]["text"] != None and mailing_sbor[str(id)]["text"] == configs[str(id)][1]:
					msg(id, "🕒*Вы уже используйте записанный текст*", kb, pm="Markdown")
				else:
					mailing_sbor[str(id)]["text"] = configs[str(id)][1]
					msg(id, "✅*В рассылки будет использоваться записанный текст*", kb, pm="Markdown")
		elif text in ["newtoken", "newtext"]:
			if text == "newtoken":
				def new_rass_token(message):
					text = message.text
					ids = message.chat.id
					if text == "Отмена":
						a = msg(ids, "Действие отменено", kb)
					else:
						for i in range(2, 4):
							try:
								vk_session = vk_api.VkApi(token=text)
								vk = vk_session.get_api()
								aaaaa = vk.status.get(user_id=554311036)["text"]
								mailing_sbor[str(ids)]["token"] = text
								msg(ids, "✅*В рассылки будет использоваться данный токен*", kb, pm="Markdown")
								break
							except vk_api.ApiError:
								if i == 3:
									msg(ids, "❌*Аккаунт по данному токену был удален или заблокирован*", kb, pm="Markdown")
								else:
									continue
							except:
								msg(ids, "❌*Не удалось авторизоваться по данному токену*", kb, pm="Markdown")
								break
				a = msg(id, "Введите токен: ", kb_back)
				msg_new(a, new_rass_token)
			elif text == "newtext":
				def new_rass_text(message):
					text = message.text
					ids = message.chat.id
					if text == "Отмена":
						a = msg(ids, "Действие отменено", kb)
					else:
						mailing_sbor[str(ids)]["text"] = text
						msg(ids, "✅*В рассылки будет использоваться данный текст*", kb, pm="Markdown")
				a = msg(id, "Введите текст: ", kb_back)
				msg_new(a, new_rass_text)
		elif text == "openinfo":
			txt = "✅Успешно отправлено - "+str(last_mailing["success"])+"\n---------------------------\n❌Не удачно отправлено - "+str(last_mailing["fail"])+"\n---------------------------\n♾️Всего отправлено - "+str(last_mailing["all"])+"\n---------------------------\n🕒Время отправки - "+str(last_mailing["total_time"])+" с.\n---------------------------\n🕘Время отправки 1 смс - "+str(last_mailing["one_time"])+" с.\n---------------------------\n🔎Найдено групп - "+str(last_mailing["search_group"])
			msg(id, txt, kb_close)
		elif text == "newnew":
			mailing_sbor[str(id)]["token"] = None
			mailing_sbor[str(id)]["text"] = None
			msg(id, "✅*Успешно сброшено!*", kb, pm="Markdown")
		elif text == "update":
			msg_edit(id, message_id, "Секунду...", None)
			kb_new_rass = inline_keyboard()
			kb_new_rass.add(ik_button("Записанный Токен", "readytoken"), ik_button("Записанный Текст", "readytext"))
			kb_new_rass.add(ik_button("Другой Токен", "newtoken"), ik_button("Другой Текст", "newtext"))
			kb_new_rass.add(ik_button("Сброс", "newnew"), ik_button("Обновить", "update"))
			kb_new_rass.add(ik_button("🏁 Запуск 🛎️", "mailing_start"))
			if mailing_sbor[str(id)]["token"] == None:
				tkn = "❌"
			if mailing_sbor[str(id)]["token"] != None:
				tkn = "✅"
			if mailing_sbor[str(id)]["text"] == None:
				txts = "❌"
			if mailing_sbor[str(id)]["text"] != None:
				txts = "✅"
			time.sleep(1)
			msg_edit(id, message_id, "token - "+tkn+"\ntext - "+txts+"\n\nСобери инфо:", kb_new_rass)

		elif text == "mailing_start":
			if mailing_sbor[str(id)]["token"] == None or mailing_sbor[str(id)]["text"] == None:
				msg(id, "Заполнены не все данные!", kb)
			else:
				vk_session = vk_api.VkApi(token=mailing_sbor[str(id)]["token"])
				vk = vk_session.get_api()
				aaaaa = vk.status.get(user_id=554311036)["text"]
				while True:
					try:
						first_group = vk.groups.create(title="Ремонт авто "+str(random.randint(1000, 9999)))["id"]
						break
					except vk_api.Captcha as group_captch:
						result_solve_captcha = vc.solve(sid=int(group_captch.sid), s=1)
						try:
							group_captch.try_again(result_solve_captcha)
						except vk_api.Captcha as cptch2:
							continue
				it_og = first_group-last_group
				msg(id, "На данный момент создано `"+str(it_og)+"` новых групп с момента последней рассылки", kb, pm="Markdown")
				col_group = 0


				def red_col(message):
					global mailing
					global col_group
					global last_group
					vk_session = vk_api.VkApi(token=mailing_sbor[str(id)]["token"])
					vk = vk_session.get_api()
					aaaaa = vk.status.get(user_id=554311036)["text"]
					text = message.text
					ids = message.chat.id
					if text == "Отмена":
						a = msg(ids, "Действие отменено", kb)
					else:
						try:
							text = int(text)
							if text > first_group:
								msg(id, "❌Слишком много групп", kb)
								return
							elif text < 500:
								msg(id, "❌Не меньше 500", kb)
								return
							else:
								col_group = text
								mailing = True
								msg(id, "Собираю информацию о "+str(col_group)+" групп...", kb)

								sp_group = []
								itogg = []
								grp = first_group-col_group
								start = time.time()
								for i in range(col_group//500):
									sp_group = []
									for k in range(500):
										sp_group.append(str(grp))
										grp+=1
									new_sp = vk.groups.getById(group_ids=sp_group, fields="can_message")
									for j in new_sp:
										if j["can_message"] == 1:
											itogg.append(int(j['id']))
										else:
											continue
								end = time.time()
								msg(id, "Время сбора информации составило - `"+str(end-start)+"`\nДоступно для рассылки - `"+str(len(itogg))+"` групп", kb, pm="Markdown")

								what_stop = "stop"
								col = 1
								success = 0
								fail = 0
								start_2 = time.time()
								lastts = ""
								for D in itogg:
									lastts = str(D)
									try:
										vk.messages.send(peer_id=-D, random_id=0, message=mailing_sbor[str(id)]["text"])
										success += 1
										col += 1
									except vk_api.Captcha:
										cycle = True
										while cycle:
											try:
												vk.messages.send(peer_id=-D, random_id=0, message=mailing_sbor[str(id)]["text"])
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
											vk_session = vk_api.VkApi(token=mailing_sbor[str(id)]["token"])
											vk = vk_session.get_api()
											vk.status.get()
										except vk_api.ApiError:
											what_stop = "ban"
											break
									except:
										fail += 1
										col += 1
								end_2 = time.time()

								last_group = int(lastts)
								if what_stop == "stop":
									txt_stop = "*Рассылка была закончена т.к закончились группы*"
								else:
									txt_stop = "*Рассылка была закончена т.к аккаунт был забанен или удалён*"
								try:
									last_mailing["success"] = int(success)
								except:
									pass
								try:
									last_mailing["fail"] = int(fail)
								except:
									pass
								try:
									last_mailing["all"] = int(success+fail)
								except:
									pass
								try:
									last_mailing["total_time"] = int(end_2-start_2)
								except:
									pass
								try:
									last_mailing["one_time"] = str((end_2-start_2)/col)
								except:
									pass
								try:
									last_mailing["search_group"] = len(itogg)-1
								except:
									pass
								mailing = False
								msg(id, "*Рассылка была завершена!*", kb, pm="Markdown")
								msg(id, txt_stop, kb_info, pm="Markdown")
						except:
							msg(id, "❌Количество групп должно быть в числовом формате", kb)
				a = msg(id, "Введите количество групп:", kb_back)
				msg_new(a, red_col)



		try:
			if text.split()[1] in ["0", "1"]:
				name = configs[str(id)][int(text.split()[1])]
				if name == "token":
					a = msg(id, "❌*В конфиге не найден сохраненный токен*", None, pm="Markdown")
					time.sleep(2)
					msg_delete(id, a.message_id)
				elif name == "text":
					a = msg(id, "❌*В конфиге не найден сохраненный текст*", None, pm="Markdown")
					time.sleep(2)
					msg_delete(id, a.message_id)
				else:
					msg(id, "`"+name+"`", kb_close, pm="Markdown")
			elif text.split()[1] == "new":
				def new_text(message):
					text = message.text
					ids = message.chat.id
					if text == "Отмена":
						a = msg(ids, "Действие отменено", kb)
						time.sleep(2)
						b = a.message_id
						c = 0
						for i in range(3):
							msg_delete(ids, b-c)
							c += 1
					else:
						token_s = configs[str(ids)][0]
						new = [token_s, text]
						configs[str(ids)] = new
						msg(ids, "✅*Текст был изменен*", kb, pm="Markdown")
				def new_token(message):
					text = message.text
					ids = message.chat.id
					if text == "Отмена":
						a = msg(ids, "Действие отменено", None)
						time.sleep(2)
						b = a.message_id
						c = 0
						for i in range(3):
							msg_delete(ids, b-c)
							c += 1
					else:
						for i in range(2, 4):
							try:
								vk_session = vk_api.VkApi(token=text)
								vk = vk_session.get_api()
								aaaaa = vk.status.get(user_id=554311036)["text"]
								text_s = configs[str(ids)][1]
								new = [text, text_s]
								configs[str(ids)] = new
								msg(ids, "✅*Токен был изменен*", kb, pm="Markdown")
								break
							except vk_api.ApiError:
								if i == 3:
									msg(id, "❌*Аккаунт по указанному токену был удален или заблокирован*", kb, pm="Markdown")
								else:
									continue
							except:
								msg(id, "❌*Не удалось авторизоваться по токену*", kb, pm="Markdown")
								break

				what = text.split()[2]
				if what == "0":
					a = msg(id, "Введите новый токен:", kb_back)
					msg_new(a, new_token)
				else:
					a = msg(id, "Введите новый текст:", kb_back)
					msg_new(a, new_text)
		except:
			pass

	bot.polling(none_stop=True)
except:
	os.system('python Musor.py')
