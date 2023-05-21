import sqlite3


class DataBase:
    def __init__(self, database=None):
        if database is None:
            database = sqlite3.connect("database1.db")
            database.row_factory = sqlite3.Row
        self.__db = database
        self.__cur = database.cursor()

    def create_application(self, creator_id, price, title, description):
        try:
            self.__cur.execute("INSERT INTO applications VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                               (creator_id, price, title, description, "", 1, ""))
            self.__db.commit()
            self.__cur.execute(
                f"""SELECT MAX(id) FROM applications"""
            )
            return self.__cur.fetchone()[0]
        except Exception as e:
            print('Ошибка добавления в БД', e)
            return False

    def delete_application(self, app_id):
        try:
            self.__cur.execute(f"DELETE FROM applications WHERE id = {app_id}")
            self.__db.commit()
        except Exception as e:
            print('Ошибка добавления в БД', e)
            return False
        return True

    def add_responser(self, app_id, responser_id):
        try:
            self.__cur.execute(
                f"""SELECT * FROM applications WHERE id = {app_id}""",
            )
            responses = self.__cur.fetchone()["responses"]
            responses = responses if responses is not None else ""
            responses = responses.split()
            responses.append(str(responser_id))
            responses = " ".join(responses)
            self.__cur.execute(f"UPDATE applications SET responses = '{responses}' WHERE id = {app_id}")
            self.__db.commit()

            self.__cur.execute(
                f"""SELECT * FROM members WHERE id = {responser_id}""",
            )
            apps = self.__cur.fetchone()["apps"]
            apps = apps if apps is not None else ""
            apps = apps.split()
            apps.append(str(app_id))
            apps = " ".join(apps)
            self.__cur.execute(f"UPDATE members SET apps = '{apps}' WHERE id = {responser_id}")
            self.__db.commit()
        except Exception as e:
            print('Ошибка изменения в БД', e)
            return False
        return True

    def update_application(self, id, change):
        try:
            print(f"UPDATE applications SET {change} WHERE id = '{id}'")
            self.__cur.execute(f"UPDATE applications SET {change} WHERE id = '{id}'")
            self.__db.commit()
        except Exception as e:
            print('Ошибка изменения в БД', e)
            return False
        return True

    def end_application(self, app_id, responser_id):
        try:
            self.__cur.execute(
                f"""SELECT * FROM applications WHERE id = {app_id}""",
            )
            self.__cur.execute(f"UPDATE applications SET responses = '{responser_id}' WHERE id = {app_id}")
            self.__cur.execute(f"UPDATE applications SET active = 0 WHERE id = {app_id}")
            self.__db.commit()
        except Exception as e:
            print('Ошибка изменения в БД', e)
            return False
        return True

    def get_application(self, app_id):
        try:
            self.__cur.execute(
                f"""SELECT * FROM applications WHERE id = {app_id}""",
            )
            res = self.__cur.fetchone()
            return res
        except Exception as e:
            print('Ошибка добавления в БД', e)
            return False

    def get_applications(self):
        try:
            self.__cur.execute(
                f"""SELECT MAX(id) FROM applications"""
            )
            cur_id = self.__cur.fetchone()[0]
            res = list()
            while len(res) < 25 and cur_id >= 0:
                try:
                    self.__cur.execute(
                        f"""SELECT * FROM applications WHERE id = {cur_id}""",
                    )
                    res.append(self.__cur.fetchall()[0])
                except:
                    pass
                cur_id -= 1
            return res
        except Exception as e:
            print('Ошибка добавления в БД', e)
            return False

    def create_member(self, name, surname, email, description, telephone_number, login, password):
        try:
            self.__cur.execute("INSERT INTO members VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)",
                               (name, surname, email, description, "", telephone_number, login, password, "", "", "0"))
            self.__db.commit()
        except Exception as e:
            print('Ошибка добавления в БД', e)
            return False
        return True

    def update_member(self, id, change):
        try:
            print(f"UPDATE members SET {change} WHERE id = '{id}'")
            self.__cur.execute(f"UPDATE members SET {change} WHERE id = '{id}'")
            self.__db.commit()
        except Exception as e:
            print('Ошибка изменения в БД', e)
            return False
        return True

    def check_password(self, login, password):
        try:
            self.__cur.execute(f"SELECT password FROM members WHERE login='{login}'")
            return self.__cur.fetchone()["password"] == password
        except Exception as e:
            print('Ошибка получения члена из БД', e)
            return False

    def delete_member(self, id):
        try:
            self.__cur.execute(f"DELETE FROM members WHERE id={id['id']}")
            self.__db.commit()
            print(f'удален пользователь с id = {id}')
        except Exception as e:
            print('Ошибка удаления из БД', e)
            return False
        return True

    def get_member(self, expression):
        try:
            self.__cur.execute(f"SELECT * FROM members WHERE {expression}")
            return self.__cur.fetchone()
        except Exception as e:
            print('Ошибка получения члена из БД', e)
            return False

    def get_app(self, expression):
        try:
            self.__cur.execute(f"SELECT * FROM applications WHERE {expression}")
            return self.__cur.fetchone()
        except Exception as e:
            print('Ошибка получения члена из БД', e)
            return False

    def update_old(self, change, condition):
        try:
            self.__cur.execute(f'UPDATE mainmenu SET {change} WHERE {condition}')
            self.__db.commit()
        except Exception as e:
            print('Ошибка изменения в БД', e)
            return False
        return True

    def update(self, change):
        try:
            self.__cur.execute(change)
            self.__db.commit()
        except Exception as e:
            print('Ошибка изменения в БД', e)
            return False
        return True

    def get(self, expression):
        try:
            self.__cur.execute(expression)
            return self.__cur.fetchall()
        except Exception as e:
            print('Ошибка получения члена из БД', e)
            return False

    def f(self):
        # try:
        self.__cur.execute("UPDATE members SET surname='Петров' WHERE id='3'")
        f"""
            create table applications (
            id integer primary key autoincrement,
            creator_id text not null,
            price text not null,
            title text not null,
            description text,
            reviews text,
            active text,
            responses text
            );
            DROP TABLE applications;
        """
        self.__db.commit()

    def r(self):
        # try:
        self.__cur.execute(f"""ALTER TABLE members
DROP COLUMN responses;""")
        self.__db.commit()


class User:
    def __init__(self, **kwargs):
        key = [i for i in kwargs.keys()][0]
        member = DataBase().get_member(f"{key}='{kwargs[key]}'")
        self.id = member["id"]
        self.name = member["name"]
        self.surname = member["surname"]
        self.email = member["email"]
        self.description = member["description"]
        self.telephone_number = member["telephone_number"]
        self.login = member["login"]
        self.password = member["password"]
        self.apps = [int(i) for i in member["apps"].split()]
        self.responses = [int(i) for i in member["responses"].split()]
        self.balance = member["balance"]
        self.photo = member["photo"] if member["photo"] else "https://media.discordapp.net/attachments/1058754526045282395/1109615969199984650/1614529410_90-p-golova-na-belom-fone-100.png?width=866&height=625"

    def change_password(self, new):
        try:
            DataBase().update(f"UPDATE members SET password='{new}' WHERE id='{self.id}'")
            self.password = new
            return True
        except:
            return False

    def get_password(self):
        return self.password

    def change_balance(self, new):
        try:
            DataBase().update(f"UPDATE members SET balance='{new}' WHERE id='{self.id}'")
            self.balance = new
            return True
        except:
            return False

    def get_balance(self):
        return self.balance

    def change_email(self, new):
        try:
            DataBase().update(f"UPDATE members SET email='{new}' WHERE id='{self.id}'")
            self.email = new
            return True
        except:
            return False

    def get_email(self):
        return self.email

    def change_phone(self, new):
        try:
            DataBase().update(f"UPDATE members SET telephone_number='{new}' WHERE id='{self.id}'")
            self.telephone_number = new
            return True
        except:
            return False

    def get_phone(self):
        return self.telephone_number

    def add_app(self, app_id):
        try:
            self.apps.append(app_id)
            DataBase().update(
                f"UPDATE members SET apps='{' '.join([str(i) for i in self.apps])}' WHERE id={self.id}")
            return True
        except:
            return False

    def delete_app(self, app_id):
        try:
            self.apps.remove(int(app_id))
            DataBase().update(
                f"UPDATE members SET apps='{' '.join([str(i) for i in self.apps])}' WHERE id={self.id}")
            return True
        except:
            return False

    def get_apps(self):
        return self.responses

    def add_response(self, app_id):
        try:
            self.responses.append(app_id)
            DataBase().update(
                f"UPDATE members SET responses='{' '.join([str(i) for i in self.responses])}' WHERE id={self.id}")
            return True
        except:
            return False

    def delete_response(self, app_id):
        try:
            self.responses.remove(app_id)
            DataBase().update(
                f"UPDATE members SET responses='{' '.join([str(i) for i in self.responses])}' WHERE id={self.id}")
            return True
        except:
            return False

    def get_responses(self):
        return self.responses


class Application:
    def __init__(self, **kwargs):
        key = [i for i in kwargs.keys()][0]
        val = kwargs[key]
        if type(val) == sqlite3.Row:
            app = val
        else:
            app = DataBase().get_app(f"{key} = {val}")
        self.id = app["id"]
        self.creator_id = int(app["creator_id"])
        self.creator = User(id=self.creator_id)
        self.price = app["price"]
        self.title = app["title"]
        self.description = app["description"]
        self.short_description = self.description if len(self.description) < 200 else self.description[:27] + "..."
        self.active = True if int(app["active"]) else False
        self.responses = [int(i) for i in app["responses"].split()]

    def change_description(self, new):
        try:
            DataBase().update(f"UPDATE applications SET description='{new}' WHERE id='{self.id}'")
            self.description = new
            return True
        except:
            return False

    def get_description(self):
        return self.description

    def change_active(self, new):
        try:
            DataBase().update(f"UPDATE applications SET active='{int(new)}' WHERE id='{self.id}'")
            self.active = new
            return True
        except:
            return False

    def get_active(self):
        return self.active

    def add_response(self, user_id):
        try:
            self.responses.append(user_id)
            DataBase().update(
                f"UPDATE applications SET responses='{' '.join([str(i) for i in self.responses])}' WHERE id={self.id}")
            return True
        except:
            return False

    def delete_response(self, app_id):
        try:
            self.responses.remove(app_id)
            DataBase().update(
                f"UPDATE applications SET responses='{' '.join([str(i) for i in self.responses])}' WHERE id={self.id}")
            return True
        except:
            return False

    def get_responses(self):
        return self.responses

    def end(self, responser_id):
        try:
            self.change_active(0)
            self.responses = [responser_id]
            DataBase().update(
                f"UPDATE applications SET responses='{responser_id}' WHERE id={self.id}")
            DataBase().update(
                f"UPDATE applications SET price='Выполнено' WHERE id={self.id}")
            return True
        except:
            return False

    def delete(self):
        try:
            DataBase().update(f"DELETE FROM applications WHERE id = {self.id}")
            return True
        except:
            return False


class Message:
    def __init__(self, **kwargs):
        key = [i for i in kwargs.keys()][0]
        val = kwargs[key]
        if type(val) == sqlite3.Row:
            app = val
        else:
            app = DataBase().get_app(f"{key} = {val}")
        self.id = app["id"]
        self.creator_id = app["creator_id"]
        self.creator = User(id=self.creator_id)
        self.price = app["price"]
        self.title = app["title"]
        self.description = app["description"]
        self.short_description = self.description if len(self.description) < 200 else self.description[:27] + "..."
        self.active = True if app["active"] else False
        self.responses = [int(i) for i in app["responses"].split()]


if __name__ == "__main__":
    # DataBase().create_member("Петя", "Петр3ов", "petya@petya.com", "", "", "Petya", "pass")
    # DataBase().create_application("1", "10000", "Самый-самый крутой заказ", "Описание самого-самого крутого заказа")

    # db = DataBase()
    # """for i in range(50): # удаляем профили до 50
    #     try:
    #         db.delete_member({'id': i})
    #     except:
    #         break"""
    # """for app in db.get_applications(): # удаляет все заказы
    #     db.delete_application(app['id'])"""
    # # db.create_application(35, 200, "Первый заказ от Сани", "Надо доделывать сайт...")
    # db.delete_application(46)
    #
    #
    # # a = [16, 15, 14, 13]
    # # for i in a: db.delete_application(i)
    #
    #
    # # db.create_application(568, "1000", "title3", "description")
    # # db.create_member("Daniel", "Bobrov", "Anatolyevich", "description")


    user = User(id=1)
    # user.delete_response(1)
    print(user.responses)


    app = Application(id=1)
    # app.delete_response(1)
    print(app.responses)
