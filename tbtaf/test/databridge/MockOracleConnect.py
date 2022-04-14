from unittest import mock
import cx_Oracle

class MockCursor:
    def __init__(self, *args, **kwargs):
        self.fetched = False
        self.rows = None
        self.description = [("SUITE_TYPE",), ("SUITE_ID",)]

    def callfunc(self, *args):
        return self

    @staticmethod
    def var(*args):
        pass

    @staticmethod
    def execute(query, id=dict):
        pass

    @staticmethod
    def var(query):
        return returned_id

    @staticmethod
    def close():
        pass

    def fetchmany(self, *args):
        if not self.fetched:
            self.rows = self.fetch_rows()
            self.fetched = True

        return next(self.rows)

    @staticmethod
    def fetchall():
        return [
            ('Smart', "TEST A")
        ]


    def fetch_rows(self):
        yield self.fetchall()
        yield None


class MockConnect:
    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @staticmethod
    def cursor():
        return MockCursor()

    @staticmethod
    def close():
        pass

    @staticmethod
    def commit():
        pass

class returned_id:
    def getvalue():
        return [1]