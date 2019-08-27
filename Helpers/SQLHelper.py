import psycopg2

class SQLHelper():
    # тут создавать коннекшен стринг
    def __init__(self):
        self.host = "postgres.cain.loc"
        self.database = "eva"
        self.user = "eva"
        self.password = "eva"
        self.port = "5432"

    def connect_to_database(self):
        """
        Подключается к бд указанной в __init__ (возможно вынесу данные в конфиг)
        :return: cursor объект для взаимодействия с бд, connection объект подключения к бд
        """
        connectionString = ("dbname=%s user=%s password=%s host=%s port=%s" % (self.database, self.user, self.password, self.host, self.port))
        connection = psycopg2.connect(connectionString)
        cursor = connection.cursor()
        return cursor, connection

    def __get_user_from_database(self, email):
        """
        Получает id юзера из бд по email
        :param email: email юзера
        :return: tuple с ID юзера
        """
        cursor, connection = self.connect_to_database()
        cursor.execute("SELECT id FROM public.user WHERE email = (%s)", (email,))  # пример коннекшена (работает и возвращает имя юзера)
        return cursor.fetchone()

    # тут пойдут методы которые будут дергаться в сетапе/тирдауне
    def delete_user_from_database(self, email):
        """
        Удаляет записи из user и user_social по email пользователя
        :param email: email удаляемого юзера
        """
        cursor, connection = self.connect_to_database()
        cursor.execute("DELETE FROM public.user WHERE email = (%s)", (email,))  # удаляем юзера из user
        cursor.execute("DELETE FROM public.user_social WHERE email = (%s)", (email,))  # удаляем юзера из user_social
        connection.commit()  # коммитим изменения в БД, взяв коннекшен из внутреннего метода (постгрес такой постгрес)

    def delete_multisig_emails(self, email):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("DELETE FROM public.user_multisig_pending_emails WHERE user_id = (%s)", (user_id,))
        cursor.execute("DELETE FROM public.user_multisig_emails WHERE user_id = (%s)", (user_id,))
        connection.commit()

    def add_multisig_email(self, email, multisig_email):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("INSERT INTO public.user_multisig_emails (user_id, email) VALUES (%s, %s)", (user_id, multisig_email, ))
        connection.commit()


    def get_limits_by_email_from_database(self, email):
        """
        Получает лимиты по всем кошелькам по email юзера
        :param email: email пользователя
        :return: список tuple с валютами лимитов этого юзера
        """
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("SELECT currency FROM public.user_limits WHERE user_id = (%s)", (user_id,))
        return cursor.fetchall()

    def delete_limits_by_email_from_database(self, email):
        """
        Удаляет лимиты по всем кошелькам по email юзера
        :param email: email пользователя
        """
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("DELETE FROM public.user_limits WHERE user_id = (%s)", (user_id,))
        cursor.execute("DELETE FROM public.user_limits_periods WHERE user_id = (%s)", (user_id,))
        connection.commit()

    def set_local_currency(self, email, currency):
        """
        Меняет local currency у юзера с заданным email
        :param email: Емейл пользователя
        :param currency: local currency, usd/eur
        :return:
        """
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("UPDATE public.user_settings SET local_currency = (%s) WHERE user_id = (%s)", (currency, user_id,))
        connection.commit()