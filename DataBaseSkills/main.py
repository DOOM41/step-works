import psycopg2
from my_db_set import Config
from Work_with_DB import WorkDB
from datetime import datetime

try:
    conection = psycopg2.connect(
        host=Config.HOST,
        user=Config.USER,
        password=Config.PASSWORD,
        database=Config.DB
    )
    conection.autocommit = True
    print('Connected')
    my_users: WorkDB = WorkDB(table_name="my_users",
                              data=[
                                  "login VARCHAR(50) NOT NULL UNIQUE",
                                  "password VARCHAR(50) NOT NULL"
                              ])
    my_users.create()

    users_create_time: WorkDB = WorkDB(table_name="users_create_time",
                                       data=[
                                           "date TIMESTAMP",
                                           "user_id int REFERENCES my_users(id)"
                                       ])
    users_create_time.create()
    try:
        with conection.cursor() as cur:
            cur.execute(f"""
                CREATE OR REPLACE FUNCTION after_insert()
                RETURNS TRIGGER
                AS $$
                BEGIN
                    INSERT INTO users_create_time (user_id)
                    VALUES (NEW.id);
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER after_ins
                AFTER INSERT ON my_users
                    FOR EACH ROW EXECUTE PROCEDURE after_insert();
            """)
    except Exception as e:
        print(e)

    choice = input("Если у вас есть аккаунт нажмите 0.\
Если желаете зарегистрироваться нажмите любую другую клавишу: ")

    if choice != "0":
        while True:
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            password_again = input("Повторите введенный пароль: ")
            if (password == password_again):
                try:
                    my_users.insert(values={
                        "login": f"'{login}'",
                        "password": f"'{password[::-1]}'"
                    })
                    id_ = users_create_time.get_info(values=["id"])[-1][-1]
                    users_create_time.update(values={
                        "date": f"{datetime.now()}"
                    }, id=id_)
                    break
                except Exception as e:
                    print(e)
                    print("Данное имя уже занято выберите другое")
                    continue
            else:
                print("Пароли не совпадают повторите попытку")

    else:
        entered = False
        for i in range(5, 0, -1):
            try:
                login = input("Введите логин: ")
                password_check = my_users.get_info(
                    values=["password"], where=f"login='{login}'")[-1][-1][::-1]
            except:
                print(
                    f"Такого логина не существует! У вас осталось {i} попыток")
                continue
            password = input("Введите пароль: ")

            if password == password_check:
                print("Вы вошли!")
                entered = True
                break
            else:
                print(f"Не верный пароль! У вас осталось {i} попыток")
        if entered:
            print("""Какие изменения желаете внести:\
                        \n1)Обновить пароль\
                        \n2)Узнать количество пользователей\
                        \n3)Узнать день создания аккаунта\
                        \n4)Закончить работу""")
            while True:
                work = input("""Выберите действие: """)
                if work == "1":
                    new_pasword = input("Введите новый пароль: ")[::-1]
                    id_ = my_users.get_info(values=["id"])[-1][-1]
                    my_users.update(values={
                        "password": f"{new_pasword}"
                    }, id=id_)
                elif work == "2":
                    with conection.cursor() as cur:
                        cur.execute("""
                            SELECT COUNT(id) FROM my_users
                        """)
                        print(
                            f'Количество зарегестрированных пользователей {list(cur)[-1][-1]}')
                elif work == "3":
                    with conection.cursor() as cur:
                        cur.execute("""
                            SELECT users_create_time.date, my_users.login
                            FROM users_create_time
                            JOIN my_users ON users_create_time.user_id=my_users.id;
                        """)
                        print(f'{list(cur)}')
                elif work == "4":
                    print("Конец работы!")
                    break

        else:
            print("Попробуйте позже!")


except Exception as e:
    print(e)

finally:
    users_create_time.close_connection()
    my_users.close_connection()
    conection.close()
