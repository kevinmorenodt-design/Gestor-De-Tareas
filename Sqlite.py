import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import *
import os
from tkcalendar import DateEntry
import datetime





root=tk.Tk()

#-----------Conexcion Tablas-------------------


miConexion=sqlite3.connect("GestorDeTareas.db")

miCursor=miConexion.cursor()

#----------Tabla Tareas-----------------------

miCursor.execute("CREATE TABLE IF NOT EXISTS Tareas (ID INTEGER PRIMARY KEY AUTOINCREMENT,Nombre VARCHAR(50),Categoria VARCHAR(50))")

#------------Tabla Registros------------------

miCursor.execute("CREATE TABLE IF NOT EXISTS Registros (ID INTEGER PRIMARY KEY AUTOINCREMENT,Tarea_ID VARCHAR(50),Fecha INTEGER(50)" \
",Tiempo_minutos INTEGER(50),Comentarios VARCHAR(300))")

miConexion.commit()

#-----------Funciones Menu--------------------------

def salirAplicacion():
    
    valor=messagebox.askokcancel("Salir","¿Deseas salir de la aplicacion?")

    if valor==True:
        root.destroy()

def BorrarCampos():

    MiID.set("")
    MiNombre.set("")
    MiCategoria.set("")

def Licencia():
    messagebox.showinfo("Licencia", "Software libre - Uso educativo")

def AcercaDe():
    messagebox.showinfo("Acerca de", "Gestor de Tareas v1.0 - Desarrollado por Kevin")


#---------Funcion Create-------------------

def Create():

    miCursor.execute("INSERT INTO Tareas (Nombre,Categoria) VALUES(?,?)",
                 (MiNombre.get(),MiCategoria.get()))
    
    miConexion.commit()

    messagebox.showinfo("Informacion","informacion cargada con exito")


root.title("Gestor de Tareas")

ventanas=ttk.Notebook(root)

#-------------Funcion Read---------------------

def Read():

    
    

    termino = "%" + MiNombre.get() + "%"

    miTabla.delete(*miTabla.get_children())

    miCursor.execute("SELECT * FROM Tareas WHERE Nombre LIKE ?",(termino,))

    BuscarRegistro=miCursor.fetchall()

    if not BuscarRegistro:

        messagebox.showwarning("Error","No es posible encontrar el registro. Registro Inexistente")
    else:
        for i in BuscarRegistro:

            miTabla.insert("", END, values=(i[0], i[1], i[2]))
#----------------Funcion UPLOAD----------------------

def UPLOAD():

    miCursor.execute( "UPDATE Tareas SET Nombre=?,Categoria=? WHERE ID=?"
                     ,(MiNombre.get(),MiCategoria.get(),MiID.get()))
    
    miConexion.commit()
    messagebox.showinfo("Informacion","informacion actualizada con exito")

#-----------------Funcion DELETE-----------------------

def DELETE():

    
    if messagebox.askyesno("Eliminar", "¿Estás seguro?"):
    
        miCursor.execute("DELETE FROM Tareas WHERE ID=(?)",(MiID.get(),))

        miConexion.commit()
        MiID.set("")
        MiNombre.set("")
        MiCategoria.set("")
#--------------------------Funcion CargarTareas-----------------
def CargarTareas():
    miCursor.execute("SELECT Nombre FROM Tareas")
    tareas = miCursor.fetchall()
    tareaCombo['values'] = [t[0] for t in tareas]

#---------------Funcion Guardar---------------------

def Guardar():

    miCursor.execute("SELECT ID FROM Tareas Where Nombre = ?",(tareaCombo.get(),))

    GuardarT = miCursor.fetchone()

    TotalMinutos =int(horasSpinbox.get()) * 60 + int(minutosSpinbox.get())

  

    miCursor.execute("INSERT INTO Registros (Tarea_ID ,Fecha " \
    ",Tiempo_minutos ,Comentarios) VALUES (?,?,?,?)",
    (GuardarT[0],fechaEntry.get_date(),TotalMinutos,textoComentario.get("1.0", END)))
    miConexion.commit()
    messagebox.showinfo("Informacion","informacion de tareas guardada con exito")

#--------------------Funciones Estadisticas---------------------
#-----Funcion VerDia---------------
def VerDia():

    miCursor.execute("SELECT Tareas.Nombre, Registros.Fecha, Registros.Tiempo_minutos, Registros.Comentarios "\
                        "FROM Registros "\
                        "JOIN Tareas ON Registros.Tarea_ID = Tareas.ID "\
                        "WHERE Registros.Fecha = ?",(datetime.date.today(),))
    
    Estadisticas = miCursor.fetchall()

    miTablaStats.delete(*miTablaStats.get_children())
    for i in Estadisticas:
        miTablaStats.insert("", END, values=(i[0], i[1], i[2], i[3]))

#-----Funcion VerMes---------------

def VerMes():

    mes_actual= datetime.date.today().strftime("%Y-%m")

    miCursor.execute("SELECT Tareas.Nombre, Registros.Fecha, Registros.Tiempo_minutos, Registros.Comentarios "\
                        "FROM Registros "\
                        "JOIN Tareas ON Registros.Tarea_ID = Tareas.ID "\
                        "WHERE Registros.Fecha LIKE ?",(mes_actual + "%",))
    
    Estadisticas = miCursor.fetchall()

    miTablaStats.delete(*miTablaStats.get_children())
    for i in Estadisticas:
        miTablaStats.insert("", END, values=(i[0], i[1], i[2], i[3]))

#-----Funcion VerAño---------------


def VerAño():

    Año_actual= datetime.date.today().strftime("%Y")

    miCursor.execute("SELECT Tareas.Nombre, Registros.Fecha, Registros.Tiempo_minutos, Registros.Comentarios "\
                        "FROM Registros "\
                        "JOIN Tareas ON Registros.Tarea_ID = Tareas.ID "\
                        "WHERE Registros.Fecha LIKE ?",(Año_actual + "%",))
    
    Estadisticas = miCursor.fetchall()

    miTablaStats.delete(*miTablaStats.get_children())
    for i in Estadisticas:
        miTablaStats.insert("", END, values=(i[0], i[1], i[2], i[3]))


    

#---------------Frames---------------------

miFrame_CRUD=ttk.Frame(ventanas, width=1200,height=600)
miFrame_CheckList=ttk.Frame(ventanas, width=1200,height=600)
miFrame_Estadisticas=ttk.Frame(ventanas, width=1200,height=600)

ventanas.pack()

ventanas.add(miFrame_CRUD,text="CRUD")


ventanas.add(miFrame_CheckList,text="CheckList")


ventanas.add(miFrame_Estadisticas,text="Estadisticas")

#--------------Entry CRUD----------------------

MiNombre=StringVar()
MiCategoria=StringVar()
MiID = StringVar()

cuadroID=Entry(miFrame_CRUD,textvariable=MiID)
cuadroID.grid(row=0, column=1,padx=10,pady=10)


cuadroNombre=Entry(miFrame_CRUD,textvariable=MiNombre)
cuadroNombre.grid(row=1, column=1,padx=10,pady=10)


cuadroCategoria=Entry(miFrame_CRUD,textvariable=MiCategoria)
cuadroCategoria.grid(row=2, column=1,padx=10,pady=10)
#-------------------Label CRUD-----------------------

IDLabel=Label(miFrame_CRUD, text="ID: ")
IDLabel.grid(row=0,column=0,sticky="e",padx=10,pady=10)

NombreLabel=Label(miFrame_CRUD, text="Nombre: ")
NombreLabel.grid(row=1,column=0,sticky="e",padx=10,pady=10)

CategoriaLabel=Label(miFrame_CRUD, text="Categoria: ")
CategoriaLabel.grid(row=2,column=0,sticky="e",padx=10,pady=10)

#--------------Entry CheckList----------------------



fechaEntry=DateEntry(miFrame_CheckList,selectmode='day')
fechaEntry.grid(row=0, column=1,padx=10,pady=10)

horasSpinbox = Spinbox(miFrame_CheckList, from_=0, to=23, width=3)
horasSpinbox.grid(row=1,column=1, padx=0, sticky="e")

minutosSpinbox = Spinbox(miFrame_CheckList, from_=0, to=59, width=3)
minutosSpinbox.grid(row=1,column=3)



tareaCombo = ttk.Combobox(miFrame_CheckList,)
tareaCombo.grid(row=2, column=1, padx=10, pady=10)

textoComentario=Text(miFrame_CheckList,width=16,height=5)
textoComentario.grid(row=5,column=1,padx=10,pady=10)

scrollVert=Scrollbar(miFrame_CheckList, command=textoComentario.yview)
scrollVert.grid(row=5,column=2,sticky="nsew")

textoComentario.config(yscrollcommand=scrollVert.set)



#--------------Label CheckList-------------------


fechaLabel=Label(miFrame_CheckList,text="Fecha: ")

fechaLabel.grid(row=0, column=0,padx=10,pady=10)

MiTiempoLabel = Label(miFrame_CheckList, text="Tiempo: ")
MiTiempoLabel.grid(row=1, column=0, padx=10, pady=10,sticky="e")

LabelHoras=Label(miFrame_CheckList,text="Horas")
LabelHoras.grid(row=1, column=2, padx=0, sticky="w")

LabelMinutos=Label(miFrame_CheckList,text="Minutos")
LabelMinutos.grid(row=1, column=4)

tareaLabel=Label(miFrame_CheckList,text="Tarea: ")
tareaLabel.grid(row=2, column=0, padx=10, pady=10)

comentariosLabel=Label(miFrame_CheckList, text="Comentarios: ")
comentariosLabel.grid(row=5,column=0,sticky="e",padx=10,pady=10)




#-------------------Menu------------------

barraMenu=Menu(root)

root.config(menu=barraMenu,width=300,height=300)


menuBBDD=Menu(barraMenu,tearoff=0)

menuBBDD.add_command(label="Salir",command=salirAplicacion)

menuBorrar=Menu(barraMenu,tearoff=0)
menuBorrar.add_command(label="Borrar campos",command=BorrarCampos)


menuAyuda=Menu(barraMenu,tearoff=0)
menuAyuda.add_command(label="Licencia",command=Licencia)
menuAyuda.add_command(label="Acerca de....",command=AcercaDe)


barraMenu.add_cascade(label="BBDD",menu=menuBBDD)
barraMenu.add_cascade(label="Borrar",menu=menuBorrar)
barraMenu.add_cascade(label="Ayuda",menu=menuAyuda)

#----------------------Botones CRUD-----------------------

frameBotons=Frame(miFrame_CRUD)
frameBotons.grid(row=6, column=0, columnspan=2, pady=10)

botonCreate=Button(frameBotons, text="Create", width=6,command=Create)
botonCreate.pack(side="left", padx=5)
botonRead=Button(frameBotons, text="Read", width=6,command=Read)
botonRead.pack(side="left", padx=5)
botonUpdate=Button(frameBotons, text="Update", width=6,command=UPLOAD)
botonUpdate.pack(side="left", padx=5)
botonDelete=Button(frameBotons, text="Delete", width=6,command=DELETE)
botonDelete.pack(side="left", padx=5)
#-------------------Boton CheckList-------------------------

frameBotons2=Frame(miFrame_CheckList)
frameBotons2.grid(row=9, column=0, columnspan=2, pady=10)

BotonGuardar=Button(frameBotons2,text="Guardar",width=6,command=Guardar)
BotonGuardar.pack( padx=7)

#-----------------Botones Estadisticas--------------------
frameBotons3=Frame(miFrame_Estadisticas)
frameBotons3.grid(row=6, column=0, columnspan=2, pady=10)

botonDia=Button(frameBotons3, text="1 Dia", width=6,command=VerDia)
botonDia.pack(side="left", padx=5)
botonMes=Button(frameBotons3, text="1 Mes", width=6,command=VerMes)
botonMes.pack(side="left", padx=5)
botonAnual=Button(frameBotons3, text="1 Año", width=6,command=VerAño)
botonAnual.pack(side="left", padx=5)


#------------Treeview CRUD-------------------------

miTabla = ttk.Treeview(miFrame_CRUD, columns=("ID","Nombre","CATEGORIA"), show="headings")
miTabla.heading("ID", text="ID")
miTabla.heading("Nombre", text="Nombre")
miTabla.heading("CATEGORIA", text="CATEGORIA")

miTabla.grid(row=9, column=0,columnspan=2)

#---------------TreeView Estadisticas----------------

miTablaStats = ttk.Treeview(miFrame_Estadisticas, columns=("Tarea","Fecha","Tiempo","Comentario"), show="headings")
miTablaStats.heading("Tarea", text="Tarea")
miTablaStats.heading("Fecha", text="Fecha")
miTablaStats.heading("Tiempo", text="Tiempo")
miTablaStats.heading("Comentario", text="Comentario")

miTablaStats.grid(row=9, column=0,columnspan=2)


#-------------------BIND------------------

def CargarRegistro(event):

    

    

    seleccion = miTabla.focus()

    fila = miTabla.item(seleccion)

    print(fila)
    
    try:
        fila["values"][0]
        miCursor.execute("SELECT * FROM Tareas WHERE ID=(?)",(fila["values"][0],))
        values=miCursor.fetchone()

        MiID.set(values[0])
        MiNombre.set(values[1])
        MiCategoria.set(values[2])
       


    except IndexError:
        pass






miTabla.bind("<ButtonRelease-1>", CargarRegistro)



CargarTareas()
root.mainloop()



