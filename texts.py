class TextsTg:

    m_main_info = ("\U0001F3B0 В данном боте вы можете проверить свою удачу. "
                   "\nДля старта игры необходимо выбрать игру и ставку. "
                    "\n\nЕсли вы выбрали *онлайн *игру, то в зависимости от выбора вы попадаете в комнату, где помимо вас находится еще от 1 до 99 игроков. "
                    "Из всех игроков побеждает лишь один."
                   "\n*Выигравший забирает ставки остальных.*"
                   "\n\nВ *быстрой* игре в зависимости от выбранной игры выпадает случайное число которое соответствует"
                   " коэффициенту от 0 до 10, на которое умножается ваша ставка."
                   "\n"
                    '\nПодробнее про каждую игру вы можете почитать при нажатии на нее в пункте "Игры".')

    m_where10 = '\U0001F4CC Содержание и разработка площадки требует денежных средств, из за чего мы вынуждены брать комиссию с каждой игры. ' \
                    '\n*Комиссия площадки - 5%.*';

    m_why_rand = ("\U0001F3B2 Выбор чисел для *онлайн* игр происходит автоматически при помощи генератора случайных чисел random.org."
                  "\n"
                    "Данный сервис генерирует числа на основе атмосферных шумов."
                  "\n\nДля *быстрых* игр при генерации выпадения числа в смайлике используются сервера Telegram."
                  "\n"
                    "\nБольше информации здесь - \nhttps://ru.wikipedia.org/wiki/Random.org"
                  "\nhttps://core.telegram.org/api/dice")

    m_question_duel = ("\U0001F93A В режиме Дуэль вы соперничаете с 1 противником. Шанс победить - 50%."
                       "\n" 
                       "\n*Побеждаете - забираете его ставку.*")

    m_question_russ = ('\U0001F3B2 В режиме Русская рулетка вы соперничаете с 5 противниками. Шанс победить - 16%.'
                       "\n" 
                       "\n*Побеждаете - забираете ставки 5 участников.*")

    m_question_king = ('\U0001F451 В режиме Королевская битва вы соперничаете с множеством противников, от 6 до 99. '
                       "\n" 
                       "\n*Побеждаете - забираете ставки всех участников.*")

    m_question_bowl = ("\U0001F3B3 Правила просты \n\nВыбиваете *страйк* - делаете *х2*.\nОстается 1 кегля - *х1.5*"
                       "\nОставшиеся 2 кегли дадут *х1.25*\nОсталось 3 кегли - *x1*"
                       "\n\nСбили меньше - увы, ставка не сыграла.")

    m_question_cube = ("\U0001F3B2 Классика всех игр \n\nВ зависимости от выпаших очков ваша ставка умножается на коэффициент:"
                       "\n\n*6* очков - *х2*\n*5* - *x1.5*\n*4* - *x1.25*\n*3* - *x1*\n\nМеньше - увы, ставка не сыграла")

    m_question_slot = ("\U0001F3B0 Старый добрый однорукий бандит"
                       "\n\nВыпало *777* - словили *джекпот*! Ваша ставка делает *х10*!"
                       "\nТри \U0001F347, \U0001F34B или *BAR* - коэффициент *х3*"
                       "\nЛюбые *две 7* - Ставка умножается на *х2!*"
                       "\n*Одна 7* и *два* \U0001F347, \U0001F34B или *BAR* - коэффициент *х1.5*"
                       "\nДаже если все *3 разные* - кэшбек с коэффициентом *x0.4*!"
                       "\n\nВ остальных случаях - увы, ставка не сыграла")

    m_rules = ("\U0001F4CB Использование бота подразумевает согласие с настоящими правилами:"
               "\n"
               "\n1. Админ всегда прав."
               "\n"
               "\n2. Никакой подкрутки нет. Все зависит от рандома."
               "\n"
               "\n3. Ни за что ответственности не несем."
               "\n"
               "\n4. Ничего не возмещаем."
               "\n"
               "\n5. В случае чего сами виноваты.")

    m_enter_requisites_bank = ("*Введите номер карты:*"
                               "\n\nФормат номера карты - 16 цифр без пробелов и других разделяющих знаков"
                               "\nНапример - _4617006599722675_")

    m_enter_requisites_qiwi = ("*Введите номер телефона:*"
                               "\n\nФормат номера телефона - 11 цифр без пробелов и других разделяющих знаков с кодом страны в начале (без + в начале)"
                               "\nНапример - _79999224601_")

    m_topup_create_1 = ("\U0000267B<b>Ваша транзакция зарегистрирована!</b>"
                            '\n'
                            "\n\U0001F4B8 Для ее выполнения совершите перевод ")

    m_topup_create_2 = ('\n'
                            '\n<b>После</b> выполнения перевода нажмите кнопку ниже')

    dct_games_que = {
        "duel": m_question_duel,
        "king": m_question_king,
        "russ": m_question_russ,
        "bowl": m_question_bowl,
        "cube": m_question_cube,
        "slot": m_question_slot
        }

    dct_enter_req = {
        "bank": m_enter_requisites_bank,
        "qiwi": m_enter_requisites_qiwi
    }

    dct_type_way = {
        "topup": "*Выберите способ пополнения*",
        "withd": "*Выберите способ вывода средств*"
    }

    dct_que_answ = {
        "\U0001F4AC Комиссия": m_where10,
        "\U0001F4AC Алгоритмы": m_why_rand,
        "\U0001F4AC Правила": m_rules
    }

