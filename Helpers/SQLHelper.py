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
        connectionString = ("dbname=%s user=%s password=%s host=%s port=%s" % (self.database, self.user, self.password, self.host, self.port))
        connection = psycopg2.connect(connectionString)
        cursor = connection.cursor()
        return cursor, connection

    def __get_user_from_database(self, email):
        cursor, connection = self.connect_to_database()
        cursor.execute("SELECT id FROM public.user WHERE email = (%s)", (email,))  # пример коннекшена (работает и возвращает имя юзера)
        return cursor.fetchone()


    # тут пойдут методы которые будут дергаться в сетапе/тирдауне
    def delete_user_from_database(self, email):
        cursor, connection = self.connect_to_database()
        cursor.execute("DELETE FROM public.user WHERE email = (%s)", (email,))  # удаляем юзера из user
        cursor.execute("DELETE FROM public.user_social WHERE email = (%s)", (email,))  # удаляем юзера из user_social
        connection.commit()  # коммитим изменения в БД, взяв коннекшен из внутреннего метода (постгрес такой постгрес)


    def get_limits_by_email_from_database(self, email):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("SELECT currency FROM public.user_limits WHERE user_id = (%s)", (user_id,))
        return cursor.fetchall()

    def delete_limits_by_email_from_database(self, email):
        cursor, connection = self.connect_to_database()
        user_id = self.__get_user_from_database(email)
        cursor.execute("DELETE FROM public.user_limits WHERE user_id = (%s)", (user_id,))
        cursor.execute("DELETE FROM public.user_limits_periods WHERE user_id = (%s)", (user_id,))
        connection.commit()
