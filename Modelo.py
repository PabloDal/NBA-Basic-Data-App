import sqlite3
from sqlite3 import Error
import os
import atexit
import pandas as pd
from tkinter import *


class Modelo:

    features = ['id', 'Player', 'Position', 'Games', 'MinutesxGame',
    'ThreePointers', 'FreeTrows', 'OffensiveRebounds', 'DefensiveRebounds',
    'Rebounds', 'Assists', 'Turnovers', 'Blocks', 'Steals', 'PersonalFouls',
    'FlagrantFouls', 'TechnicalFouls', 'Ejections', 'year']
    dirname = os.path.dirname(os.path.abspath(__file__)).replace('\'', "\\")
    database = dirname + "\\playersSQlite.db"

    def create_connection(db_file):
        #Crea una base de datos si no la hay
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

    def create_table(conn, create_table_sql):
        #crea una tabla
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    #genera una conexion a la base de datos, si no la hay crea una con una
    #tabla 'players'
    #usa create_connection y create_table
    def connect_db():

        #datos de la tabla
        sql_create_table = """ CREATE TABLE IF NOT EXISTS players (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        Player VARCHAR(40),
                                        Position VARCHAR(20),
                                        Games integer,
                                        MinutesxGame integer,
                                        ThreePointers integer,
                                        FreeTrows integer,
                                        OffensiveRebounds integer,
                                        DefensiveRebounds integer,
                                        Rebounds integer,
                                        Assists integer,
                                        Turnovers integer,
                                        Blocks integer,
                                        Steals integer,
                                        PersonalFouls integer,
                                        FlagrantFouls integer,
                                        TechnicalFouls integer,
                                        Ejections integer,
                                        year integer
                                    ); """

        #crea la conexion a la base de datos
        conn = Modelo.create_connection(Modelo.database)
        if conn is not None:
            #crea una tabla
            Modelo.create_table(conn, sql_create_table)
            return conn
        else:
            print("Error! cannot create the database connection.")

    #agrega a la base de datos
    def insertdata(data_list):

        conn = Modelo.connect_db()
        sql_insert = """ INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        c = conn.cursor()
        c.execute(sql_insert, (
            None, data_list[0], data_list[1], data_list[2], data_list[3],
            data_list[4], data_list[5], data_list[6], data_list[7],
            data_list[8], data_list[9], data_list[10], data_list[11],
            data_list[12], data_list[13], data_list[14], data_list[15],
            data_list[16], data_list[17],))

        conn.commit()
        atexit.register(conn.close)

    #lee de la base de datos por id
    def readdata(idq):

        conn = Modelo.create_connection(Modelo.database)
        sql_read = """ SELECT * FROM players WHERE id = ?"""

        c = conn.cursor()
        c.execute(sql_read, (idq,))
        selected = c.fetchall()
        #table = pd.DataFrame(selected, columns=Modelo.features)
        return selected

    #borra de la base de datos por id
    def deldata(idq):

        conn = Modelo.create_connection(Modelo.database)
        sql_del = """ DELETE FROM players WHERE id = ?"""

        c = conn.cursor()
        c.execute(sql_del, (idq,))
        conn.commit()

    #lee de la base de datos por columna
    def readselecteddata(colname):

        conn = Modelo.create_connection(Modelo.database)
        sql_read = " SELECT " + colname + " FROM players"

        c = conn.cursor()
        c.execute(sql_read)
        selected = c.fetchall()
        return selected

    #lee de la base de datos por jugador
    def readPlayer(player):

        conn = Modelo.create_connection(Modelo.database)
        sql_read = """ SELECT * FROM players WHERE Player = ?"""

        c = conn.cursor()
        c.execute(sql_read, (player,))
        selected = c.fetchall()
        return selected

    #agrega datos desde un CSV
    #los errores solo se devuelven en la consola de python y no dentro del
    #programa, se puede modificar para que lo haga.
    def readCSVdata(csvpath):
        try:
            data = pd.read_csv(csvpath)
        except Exception:
            print('Wrong csv file path')
        else:
            if len(data.columns) == 18:
                print('Loading ' + str(data.shape[0]) + 'entries...')
                for n in range(0, data.shape[0]):
                    Modelo.insertdata(data[n:n + 1].values.flatten())
                print('Data loaded')
            else:
                data = pd.read_csv(csvpath)
                if len(data.columns) == 18:
                    print('Loading ' + str(data.shape[0]) + 'entries...')
                    for n in range(0, data.shape[0]):
                        Modelo.insertdata(data[n:n + 1].values.flatten())
                    print('Data loaded')
                else:
                    print('Incorrent column number')
