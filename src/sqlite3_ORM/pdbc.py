#! /usr/bin/env python3

from json import dumps
from sqlite3 import connect, Row
from configparser import ConfigParser
from itertools import product


def print_exceptions(method):
    def wrap(self, *args, **kwargs):
        try:
            result = method(self, *args, **kwargs)
            self._con.commit()
            return result
        except Exception as e:
            self._con.close()
            print(str(e))
            raise Exception
    return wrap


class PDBC(object):

    def __init__(self):
        with connect(self._db_path()) as c:
            self._con = c

    @staticmethod
    def _db_path():
        conf = ConfigParser()
        conf.read('conf.ini')
        return conf.get('db_settings', 'db_path')

    @print_exceptions
    def query_for_dict(self, command, params=None, return_id=False):
        self._con.row_factory = Row
        cur = self._con.cursor()
        if params:
            cur.execute(command, params)
        else:
            cur.execute(command)
        data = cur.fetchall()
        return [dict(item) for item in data if item]

    @print_exceptions
    def query_for_list(self, command, params=None, return_id=False):
        cur = self._con.cursor()
        if params:
            cur.execute(command, params)
        else:
            cur.execute(command)
        return cur.fetchall()

    @print_exceptions
    def query_for_singles(self, command, params=None, return_id=False):
        cur = self._con.cursor()
        if params:
            cur.execute(command, params)
        else:
            cur.execute(command)
        data = cur.fetchall()
        return [x[0] for x in data if x[0]]

    @print_exceptions
    def scalar(self, command, params=None, return_id=False):
        cur = self._con.cursor()
        if params:
            cur.execute(command, params)
        else:
            cur.execute(command)
        data = cur.fetchall()
        return data[0][0] if data and data[0] else ""

    @print_exceptions
    def sql_update(self, command, params=None, return_id=False):
        cur = self._con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        if params:
            cur.execute(command, params)
        else:
            cur.execute(command)
        last_id = cur.lastrowid if return_id else None
        return last_id

    @print_exceptions
    def sql_update_many(self, command, params, return_id=False):
        cur = self._con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.executemany(command, params)
        last_id = cur.lastrowid if return_id else None
        return last_id

    @print_exceptions
    def sql_update_script(self, command, params=None, return_id=False):
        cur = self._con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.executescript(command)
        last_id = cur.lastrowid if return_id else None
        return last_id


class Base(PDBC):

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__()
        self.__dict__.update(kwargs)

    def create(self, echo=False):
        fields = [str(k) + " " + " ".join([x.upper() for x in v if 'pk' not in x]) for k, v in self.__class__.__dict__.items() if not k.startswith('__') and k != 'FK']
        pk = [x for x, y in self.__class__.__dict__.items() if not x.startswith('__') and 'pk' in y]
        if pk and len(pk) == 1:
            fields.append('PRIMARY KEY ({})'.format(pk[0]))
        elif pk and len(pk) > 1:
            print('Ошибка PRIMARY KEY может быть назначен только на 1 поле.')
            raise Exception

        fkeys = next((y for x, y in self.__class__.__dict__.items() if not x.startswith('__') and 'FK' in x), None)
        if fkeys:
            for fk in fkeys:
                fields.append("FOREIGN KEY('{}') REFERENCES '{}' ('{}') ON DELETE CASCADE".format(fk[0], fk[1].split(".")[0], fk[1].split(".")[1]))

        query = "CREATE TABLE {} ({})".format(self.__class__.__tablename__, ", ".join(fields))
        if echo:
            print(query)
        self.sql_update(query)

    def save(self, echo=False, return_id=False):
        fields_with_values = [(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]
        names = [x[0] for x in fields_with_values]
        values = [str(x[1]) for x in fields_with_values]
        query = "INSERT INTO '{}' ({}) VALUES ('{}')".format(self.__class__.__tablename__, ", ".join(names), "\', \'".join(values))
        if echo:
            print(query)
        return self.sql_update(query, None, return_id)

    def update(self, *args, echo=False, **kwargs):
        to_update = [k + "=\'" + str(v) + "\'" for k, v in kwargs.items()]
        query = "UPDATE '{}' SET {}".format(self.__class__.__tablename__, ", ".join(to_update))
        pk = next((x for x, y in self.__class__.__dict__.items() if not x.startswith('_') and 'pk' in y), None)
        if pk:
            query += " WHERE {}".format(next(k + "=" + str(v) for k, v in self.__dict__.items() if k == pk))
        if echo:
            print(query)
        return self.sql_update(query)

    def filter(self, *args, echo=False, **kwargs):
        filter_values = [k + "=\'" + str(v) + "\'" for k, v in kwargs.items()]
        query = "SELECT * FROM {} WHERE {}".format(self.__class__.__tablename__, " AND ".join(filter_values))
        if echo:
            print(query)
        result = [self.__class__(**x) for x in self.query_for_dict(query)]
        if not result:
            print("Поиск не дал результатов.")
            raise Exception
        return result[0]

    def delete(self, *args, echo=False, **kwargs):
        pk = next((x for x, y in self.__class__.__dict__.items() if not x.startswith('_') and 'pk' in y), None)
        if pk:
            arguments = next(k + "=" + str(v) for k, v in self.__dict__.items() if k == pk)
        else:
            fields_with_values = [k + "=\'" + str(v) + "\'" for k, v in self.__dict__.items() if not k.startswith('_')]
            arguments = " AND ".join(fields_with_values)
        query = "DELETE FROM {} WHERE {}".format(self.__class__.__tablename__, arguments)
        if echo:
            print(query)
        self.sql_update(query)

    def select_with(self, other, condition=None, join=False, echo=False):
        own_fields = [self.__class__.__tablename__ + "." + k + " AS " + self.__class__.__tablename__ + "_" + k for k, v in self.__class__.__dict__.items() if not k.startswith('_') and k != 'FK']
        other_fields = [other.__tablename__ + "." + k + " AS " + other.__tablename__ + "_" + k for k, v in other.__dict__.items() if not k.startswith('_') and k != 'FK']

        if any(('FK' == x for x in self.__class__.__dict__.keys())) or any(('FK' == x for x in other.__dict__.keys())) or join:
            query = "SELECT {} FROM {} JOIN {}".format(", ".join(own_fields + other_fields), self.__class__.__tablename__, other.__tablename__)
            if condition:
                query += " ON {}".format(condition)
            if echo:
                print(query)
            return [
                (self.__class__({k: v for k, v in x.items() if k.startswith(self.__class__.__tablename__)}),
                 other({k: v for k, v in x.items() if k.startswith(other.__tablename__)}))
                for x in self.query_for_dict(query)
            ]
        else:
            query1 = "SELECT * FROM {}".format(self.__class__.__tablename__)
            owns = [self.__class__(**x) for x in self.query_for_dict(query1)]
            query2 = "SELECT * FROM {}".format(other.__tablename__)
            others = [other(**x) for x in self.query_for_dict(query2)]
            if echo:
                print(query1)
                print(query2)
            result = list(product(owns, others))
            if condition:
                result = [x for x in result if eval(condition, {self.__class__.__tablename__: x[0], other.__tablename__: x[1]})]
            return result

    def select_all(self, echo=False):
        query = "SELECT * FROM {}".format(self.__class__.__tablename__)
        if echo:
            print(query)
        return [self.__class__(**x) for x in self.query_for_dict(query)]

    def delete_all(self, echo=False):
        query = "DELETE FROM {}".format(self.__class__.__tablename__)
        if echo:
            print(query)
        self.sql_update(query)

    def __str__(self):
        return dumps({k: v for k, v in self.__dict__.items() if not k.startswith('_')})

