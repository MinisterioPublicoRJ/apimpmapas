import cx_Oracle


class Oracle_DB:
    @classmethod
    def connect(cls, db_username, db_pwd, db_host):
        orcl = cx_Oracle.connect(
            db_username,
            db_pwd,
            db_host,
            encoding="UTF-8"
        )
        cursor = orcl.cursor()
        return cursor

    @classmethod
    def execute(cls, cursor, query, bindings=None):
        if bindings:
            cursor.execute(query, bindings)
        else:
            cursor.execute(query)
        return cursor.fetchall()
