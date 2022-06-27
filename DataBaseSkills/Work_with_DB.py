import psycopg2
from my_db_set import Config


class WorkDB:
    def __init__(self, table_name, data) -> None:
        self.data = data
        self.conection = psycopg2.connect(
            host=Config.HOST,
            user=Config.USER,
            password=Config.PASSWORD,
            database=Config.DB
        )
        self.conection.autocommit = True
        self.table_name = table_name

    def create(self):
        create = f"CREATE TABLE IF NOT EXISTS {self.table_name} ( id SERIAL4 PRIMARY KEY"
        for i in self.data:
            create += ", " + i
        create += ");"
        try:
            with self.conection.cursor() as cur:
                cur.execute(create)
        except Exception as e:
            print(e)

    def insert(self, values: dict):
        fields: list = [i for i in values.keys()]
        with self.conection.cursor() as cur:
            cur.execute(f"""INSERT INTO {self.table_name} ({",".join(fields)})
            VALUES ({",".join(values.values())})""")

    def update(self, values: dict, id: str):
        create = f"UPDATE {self.table_name} \nSET "
        last = 0
        for key, value in values.items():
            if last == len(values.items())-1:
                create += f"{key}='{value}'"
            else:
                create += f"{key}='{value}',"
                last += 1
        create += f"\nWHERE id={id};"
        try:
            with self.conection.cursor() as cur:
                cur.execute(create)
        except Exception as e:
            print(e)

    def get_info(self, values=None, where=None) -> list:
        result = []
        if where is None:
            if values is None:
                with self.conection.cursor() as cur:
                    cur.execute(f"""
                        SELECT * FROM {self.table_name} 
                    """)
                    for i in cur:
                        result.append(i)
                    return result
            with self.conection.cursor() as cur:
                cur.execute(f"""
                    SELECT {",".join(values)} FROM {self.table_name}
                """)
                for i in cur:
                    result.append(i)
                return result
        with self.conection.cursor() as cur:
            cur.execute(f"""
                SELECT {",".join(values)} FROM {self.table_name}
                WHERE {where}
            """)
            for i in cur:
                result.append(i)
            return result

    def create_function(self, function_name, inside):
        try:
            with self.conection.cursor() as cur:
                cur.execute(f"""
                    CREATE OR REPLACE FUNCTION {function_name}() 
                    RETURNS TRIGGER
                    AS $$
                    BEGIN
                        {inside}
                    END;
                    $$ LANGUAGE plpgsql;
                """)
            print("Функция создана")
        except Exception as e:
            print(f"[ERROR] {e}")

    def create_trigger(self, trigger_name, inside, function_name):
        try:
            with self.conection.cursor() as cur:
                cur.execute(f"""
                    CREATE TRIGGER {trigger_name}
                    {inside} ON {self.table_name}
                        FOR EACH ROW EXECUTE PROCEDURE {function_name}();
                """)
            print("Функция создана")
        except Exception as e:
            print(f"[ERROR] {e}")

    def clear_table(self):
        with self.conection.cursor() as cur:
            cur.execute(f"""
                DELETE FROM {self.table_name};
            """)

    def close_connection(self):
        self.conection.close()
