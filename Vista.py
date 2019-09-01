from tkinter import *
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Controlador import *


class Vista:

    #Variables de la base de datos
    features = ['Player', 'Position', 'Games', 'MinutesxGame', 'ThreePointers',
    'FreeTrows', 'OffensiveRebounds', 'DefensiveRebounds', 'Rebounds',
    'Assists', 'Turnovers', 'Blocks', 'Steals', 'PersonalFouls',
    'FlagrantFouls', 'TechnicalFouls', 'Ejections', 'year']

    def __init__(self, parent=None, **configs):
        #Main Frame
        self.myParent = parent
        self.myParent.geometry("500x500")
        #Frame
        self.Main_Frame = Frame(self.myParent, bg="#444")
        self.Main_Frame.pack(expand=YES, fill=BOTH)
        #Controles
        self.Control_Frame = Frame(self.Main_Frame, bg="Gray70",
        borderwidth=2, relief=RAISED)
        self.Control_Frame.pack(side=TOP, expand=NO, fill=BOTH, padx=7,
        pady=7)
        control_title = "Commands"
        Label(self.Control_Frame, text=control_title, bg="Gray10",
        fg="Gray70",
        justify=LEFT).pack(side=TOP, expand=NO, fill=X, anchor=W)
        self.controls = Frame(self.Control_Frame, bg="Gray10")
        self.controls.pack(side=TOP, expand=NO, fill=X)
        #Output
        self.output_window = Frame(self.Main_Frame, bg="Gray70",
        borderwidth=2, relief=RAISED)
        self.output_window.pack(side=BOTTOM, expand=YES, fill=BOTH,
        padx=7, pady=7)
        titulo_grafico = "Graphs"
        Label(self.output_window, text=titulo_grafico, bg="#222",
        fg="Gray70", justify=LEFT).pack(side=TOP, expand=NO, fill=X,
        anchor=W)
        self.output = Frame(self.output_window, bg="Gray10")
        self.output.pack(side=TOP, expand=YES, fill=BOTH)

    #Usa SaveSQlite
    def Save_Button(self):
        Save_Button = Button(self.Control_Frame, text='Save',
        command=(lambda: Vista.SaveSQLITE()))
        Save_Button["width"] = 15
        Save_Button.pack()

    #Usa ReadSQlite
    def Read_Button(self):
        Read_Button = Button(self.Control_Frame, text='Id Search',
        command=(lambda: Vista.ReadSQLITE(True)))
        Read_Button["width"] = 15
        Read_Button.pack()

    #Usa Read_player del controlador
    def Read_Player_Button(self):
        Read_Button = Button(self.Control_Frame, text='Player Search',
        command=(lambda: Vista.ReadSQLITE(False)))
        Read_Button["width"] = 15
        Read_Button.pack()

    #Usa ReadSQlite
    def Del_Button(self):
        Read_Button = Button(self.Control_Frame, text='Id Delete',
        command=(lambda: Vista.DelSQLITE()))
        Read_Button["width"] = 15
        Read_Button.pack()

    #Usa popgraph
    def Histogram_Button(self):
        hist_features = ('Position', 'Games', 'MinutesxGame', 'ThreePointers',
        'FreeTrows', 'OffensiveRebounds', 'DefensiveRebounds', 'Rebounds',
        'Assists', 'Turnovers', 'Blocks', 'Steals', 'PersonalFouls',
        'FlagrantFouls', 'TechnicalFouls', 'Ejections', 'year')
        HistButton = Button(self.Control_Frame, text='Histogram',
        command=(lambda: Vista.popgraph(self.output, hist_features)))
        HistButton["width"] = 15
        HistButton.pack()

    #Usa popscatter
    def Scatter_Button(self):
        scatter_features = ('Games', 'MinutesxGame', 'ThreePointers',
        'FreeTrows', 'OffensiveRebounds', 'DefensiveRebounds', 'Rebounds',
        'Assists', 'Turnovers', 'Blocks', 'Steals', 'PersonalFouls',
        'FlagrantFouls', 'TechnicalFouls', 'Ejections', 'year')
        ScatterButton = Button(self.Control_Frame, text='Scatter',
        command=(lambda: Vista.popgraphscatter(self.output, scatter_features)))
        ScatterButton["width"] = 15
        ScatterButton.pack()

    #Usa browsefunc
    def CSV_Button(self):
        browsebutton = Button(self.Control_Frame, text="Load CSV",
        command=(lambda: Vista.browsefunc()))
        browsebutton["width"] = 15
        browsebutton.pack()

    #Usa readCSVdat del modelo
    def browsefunc():
        filename = askopenfilename()
        Controlador.CSV_data(filename)

    def callback(variable):
        return variable

    #Usa callback
    def dropdown(root, options):

        variable = StringVar(root)
        w = OptionMenu(root, variable, *options, command=Vista.callback)
        w.pack()
        variable.set(options[0])
        return variable

    #Usa Histogramplotting y graph_data del controlador
    def popgraph(root, options):
        for widget in root.winfo_children():
            widget.destroy()
        var = Vista.dropdown(root, options)
        hbutton = Button(root, text='Graph histogram',
        command=(lambda: Vista.Histogramplotting(
            Controlador.graph_data(var.get()), root)))
        hbutton["width"] = 15
        hbutton.pack()

    #Usa ScatterPlotting y graph_data del controlador
    def popgraphscatter(root, options):
        for widget in root.winfo_children():
            widget.destroy()
        var = Vista.dropdown(root, options)
        var2 = Vista.dropdown(root, options)
        sbutton = Button(root, text='graph scatter',
        command=(lambda: Vista.ScatterPlotting(
            Controlador.graph_data(var.get()),
            Controlador.graph_data(var2.get()), root)))
        sbutton["width"] = 15
        sbutton.pack()

    def Read_Form(root):
        form = Frame(root)
        div0 = Frame(form)
        form.pack(fill=X)
        div0.pack(side=TOP, expand=YES, fill=X)
        id_read = Entry(div0, width=10)
        id_read.pack(side=TOP)
        idVar = StringVar()
        id_read.config(textvariable=idVar)
        idVar.set("")
        return idVar

    def Read_Player_Form(root):
        form = Frame(root)
        div0 = Frame(form)
        form.pack(fill=X)
        div0.pack(side=TOP, expand=YES, fill=X)
        player = Entry(div0, width=10)
        player.pack(side=TOP)
        playerVar = StringVar()
        player.config(textvariable=playerVar)
        playerVar.set("")
        return playerVar

    #Usa read_data del controlador
    #Se puede aplicar a la salida de texto como un diccionario
    def SQliteRead(idVar, Read_popup, cond):
        for widget in Read_popup.winfo_children():
            widget.destroy()
        lab = Label(Read_popup, width=500, text=idVar.get())
        lab.pack(side=TOP)
        t = idVar.get()
        keys = Vista.features
        keys.insert(0, 'id')
        if cond is True:
            read_value = Controlador.read_data(t)
            flat_list = []
            for sublist in read_value:
                for item in sublist:
                    flat_list.append(item)
            #dictionary = dict(zip(keys, flat_list))
            lista = list(zip(keys, flat_list))
        else:
            read_value = Controlador.read_player(t)
            flat_list = []
            for sublist in read_value:
                for item in sublist:
                    flat_list.append(item)
            #dictionary = dict(zip(keys, flat_list))
            lista = list(zip(keys, flat_list))
        for i in lista:
            lab_leer = Label(Read_popup, width=15, text=i)
            lab_leer.pack(side=TOP)
        #lab_leer = Label(Read_popup, width=500, text=dictionary)
        #lab_leer.pack(side=TOP)

    #usa SQliteRead y Read_Form
    def ReadSQLITE(cond):
        Read_popup = Toplevel()
        Read_popup.geometry("500x500")
        Read_variable = Vista.Read_Form(Read_popup)
        Button(Read_popup, text='Read', command=(lambda:
        Vista.SQliteRead(Read_variable, Read_popup, cond))).pack()
        Read_popup.grab_set()
        Read_popup.focus_set()
        Read_popup.wait_window()

    #Grafica 2 variables y destruye graficos anteriores
    def ScatterPlotting(var, var2, root):

        for widget in root.winfo_children():
            widget.destroy()
        figure = plt.figure(figsize=(5, 5))
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, root)
        chart_type.get_tk_widget().pack()
        ax.scatter(var, var2)
        ax.set_title('Scatter')

    #Grafica un histograma y destruye graficos anteriores
    def Histogramplotting(var, root):

        for widget in root.winfo_children():
            widget.destroy()
        figure = plt.figure(figsize=(5, 5))
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, root)
        chart_type.get_tk_widget().pack()
        ax.hist(var)
        ax.set_title('Histogram')

    #Usa add_data del controlador
    def SQliteDB(form_out, Save_popup):
        Save_popup.destroy()
        form_params = []
        for var in form_out:
            form_params.append(var.get())
        Controlador.add_data(form_params)

    #Genera un formulario para ingresos en base a las variables de la base de
    #datos y devuelve los datos ingresados
    def Make_Form(root, features):
        form = Frame(root)
        div1 = Frame(form, width=100)
        div2 = Frame(form, padx=7, pady=2)
        form.pack(fill=X)
        div1.pack(side=LEFT)
        div2.pack(side=RIGHT, expand=YES, fill=X)

        variables = []
        for field in features:
            lab = Label(div1, width=15, text=field)
            ent = Entry(div2, width=15, relief=SUNKEN)
            lab.pack(side=TOP)
            ent.pack(side=TOP, fill=X, ipady=1)
            var = StringVar()
            ent.config(textvariable=var)
            var.set('')
            variables.append(var)
        return variables

    #usa SQliteDB y Make_Form
    def SaveSQLITE():
        Save_popup = Toplevel()
        form_out = Vista.Make_Form(Save_popup, Vista.features)
        Button(Save_popup, text='Save', command=(lambda:
        Vista.SQliteDB(form_out, Save_popup))).pack()
        Save_popup.grab_set()
        Save_popup.focus_set()
        Save_popup.wait_window()

    #usa SQliteDel y Read_Form
    def DelSQLITE():
        del_popup = Toplevel()
        form_del = Vista.Read_Form(del_popup)
        Button(del_popup, text='Delete', command=(lambda:
        Vista.SQliteDel(form_del, del_popup))).pack()
        del_popup.grab_set()
        del_popup.focus_set()
        del_popup.wait_window()

    #Usa del_data del controlador
    def SQliteDel(form_del, del_popup):
        del_popup.destroy()
        Controlador.del_data(form_del.get())


if __name__ == "__main__":
    Controlador.gen_database()
    root = Tk()
    run = Vista(root)
    run.Save_Button()
    run.Read_Button()
    run.Read_Player_Button()
    run.Del_Button()
    run.CSV_Button()
    run.Histogram_Button()
    run.Scatter_Button()
    root.mainloop()