import aiomysql


class MySQLDB:
    def __init__(self, host: str, db: str, port: int, user: str, password: str):
        self.host = host
        self.db = db
        self.port = port
        self.user = user
        self.password = password

        

    async def get_conn(self):
        self.conn = await aiomysql.connect(
            host=self.host,
            db=self.db,
            user=self.user,
            password=self.password,
            port=self.port,
            cursorclass=aiomysql.DictCursor
        )

        return self.conn