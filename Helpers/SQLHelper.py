import psycopg2
import uuid

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
        cursor.execute("SELECT user_id FROM public.user_social WHERE email = (%s)", (email,))  # пример коннекшена (работает и возвращает ид юзера)
        return cursor.fetchone()

    # тут пойдут методы которые будут дергаться в сетапе/тирдауне
    def delete_user_from_database(self, email):
        """
        Удаляет записи из user и user_social по email пользователя
        :param email: email удаляемого юзера
        """
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("DELETE FROM public.user WHERE id = (%s)", (user_id,))  # удаляем юзера из user
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

    def set_user_language(self, email, language):
        cursor, connection = self.connect_to_database()
        cursor.execute("UPDATE public.user SET lang = (%s) WHERE email = (%s)", (language, email,))
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

    def set_settings_payouts_limits(self, slug, limit_amount):
        """
        Меняет лимиты в таблице settings_payout_limits
        :param slug: Название параметра лимита бекенда
        :param limit_amount: лимит
        :return:
        """

        cursor, connection = self.connect_to_database()
        cursor.execute("UPDATE public.settings_payout_limits SET \"limit\" = (%s) WHERE slug = (%s)", (limit_amount, slug,))
        connection.commit()

    def get_user_id(self, email):
        cursor, connection = self.connect_to_database()
        cursor.execute("SELECT id FROM public.user WHERE email = (%s)", (email,))
        return cursor.fetchone()


    def get_user_account_id(self, email):
        """
        Получает account_id(номер кошелька) по емейлу юзера
        :param email:
        :return:
        """

        cursor, connection = self.connect_to_database()
        cursor.execute("SELECT wallet FROM public.user WHERE email = (%s)", (email,))
        return cursor.fetchone()

    def set_user_kyc(self, email, kyc):
        userid = self.get_user_id(email)[0]
        cursor, connection = self.connect_to_database()
        cursor.execute("INSERT INTO public.user_kyc (user_id, level) VALUES (%s, %s)", (userid, kyc,))
        connection.commit()

    def delete_user_kyc(self, email):
        userid = self.get_user_id(email)[0]
        cursor, connection = self.connect_to_database()
        cursor.execute("DELETE FROM public.user_kyc WHERE user_id=(%s)", (userid,))
        connection.commit()




    def get_otp_secret_by_email(self, email):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("SELECT secret FROM public.user_otp_secrets WHERE user_id = (%s)", (user_id,))
        return cursor.fetchone()

    def change_2fa_parameters_by_email(self, email, login="true", payout="true", export="true"):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("UPDATE public.user_otp_secrets SET is_login_enabled = (%s), is_payout_enabled = (%s), "
                       "is_export_enabled = (%s) WHERE user_id = (%s)", (login, payout, export, user_id,))
        connection.commit()

    def change_password_by_email(self, email, password):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("UPDATE public.user_social SET password = (%s) WHERE user_id = (%s)", (password, user_id,))
        connection.commit()

    def remove_freeze_by_email(self, email):
        cursor, connection = self.connect_to_database()
        cursor.execute("UPDATE public.user SET freeze_till = (%s), freeze_reason = (%s) WHERE email = (%s)", (None, None, email,))
        connection.commit()

    def verify_user_by_email(self, email, valid="true"):
        cursor, connection = self.connect_to_database()
        cursor.execute("UPDATE public.user SET email_valid = (%s) WHERE email = (%s)", (valid, email,))
        connection.commit()




    def delete_sessions_by_email(self, email):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("DELETE FROM public.user_sessions WHERE user_id = (%s)", (user_id,))
        connection.commit()

    def get_deleted_sessions_by_email(self, email):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("SELECT id, model FROM public.user_sessions WHERE user_id = (%s) and deleted_at is not null", (user_id, ))
        return cursor.fetchall()

    def insert_session(self, email, model):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("INSERT INTO public.user_sessions (user_id, model, platform, session_id, currency, ip) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, model, "Web", str(uuid.uuid1()), "mw", '10.100.201.1',))
        connection.commit()

    def set_email_for_notifications(self, login_email):
        """
        Устанавливает емайл для нотификаций такой же как и емайл для логина у данного юзера
        :param email: Емейл для логина
        """
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(login_email)  # получаем ид по емайл, который используется для логина
        cursor.execute("UPDATE public.user SET  email = (%s) WHERE id = (%s)", (login_email, user_id,)) # прописываем емайл для нотиыикаций такой же как и для логина
        cursor.execute("UPDATE public.user SET  email_valid = true WHERE id = (%s)", (user_id,)) # верифицируем
        connection.commit()

    def set_email_unverified(self, login_email):
        """
        Убрает галочку верификации емайл у данного юзера
        :param email: Емейл для логина
        """
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(login_email)  # получаем ид по емайл, который используется для логина
        cursor.execute("UPDATE public.user SET  email_valid = false WHERE id = (%s)", (user_id,)) # снимаем верификацию
        connection.commit()