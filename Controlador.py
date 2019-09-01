from Modelo import *


class Controlador:

    #usa insertdata del modelo
    def add_data(data):
        cond1 = Controlador.verify_entry(data)
        if cond1 is True:
            res = Modelo.insertdata(data)
            return res

    #usa readdata del modelo
    def read_data(data):
        res = Modelo.readdata(data)
        return res

    #usa readplayer del modelo
    def read_player(data):
        res = Modelo.readPlayer(data)
        return res

    #usa deldata del modelo
    def del_data(data):
        Modelo.deldata(data)

    #usa readselecteddata del modelo
    def graph_data(data):
        res = Modelo.readselecteddata(data)
        return res

    #usa readCSVdata del modelo
    def CSV_data(path):
        res = Modelo.readCSVdata(path)
        return res

    #Verifica el numero de columnas
    def verify_entry(data):
        if len(data) == 18:
            return True
        else:
            return False

    #genea base de datos inicial
    def gen_database():
        Modelo.connect_db()