import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

host = "hd-rds-interviewees-cluster.cluster-cxqp4co8nabg.eu-west-1.rds.amazonaws.com"
port = 5432
database = "external_demos"


class SQLConnect:
    def __init__(self, user, password) -> None:
        engine_url = URL.create(
            drivername="postgresql+psycopg2",
            username=user,
            password=password,
            host=host,
            port=port,
            database=database,
            query=dict(sslmode="require"),
        )

        engine = create_engine(engine_url)
        self.engine, self.engine_url = engine, engine_url

    def connectCheck(self):
        try:
            dbConnection = self.engine.connect()
        except:
            return False
        dbConnection.close()
        return True

    def loadData(self):
        dbConnection = self.engine.connect()
        query = """select message_timestamp, category
        from telegram_crawler_demo_access2.channel
        join telegram_crawler_demo_access2.message on channel.record_id = message.channel_record_id
        """
        df = pd.read_sql(query, dbConnection)
        dbConnection.close()
        return df
