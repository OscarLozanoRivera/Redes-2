"""from tkinter import ttk,Tk,PhotoImage,LEFT
from tkinter.ttk import Frame, Label,Button

  
root = Tk() 
ancho_ventana = 785
alto_ventana = 700
x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2  
posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)
Label(root, text = 'GeeksforGeeks', font =( 'Verdana', 15)).grid() 
photo = PhotoImage(file = r"Problema1/persona.png") 
  
photoimage = photo.subsample(3, 3) 
s = ttk.Style()
s.configure("Peligro.TButton",borderwidth=3, relief="raised",text="assdf",image=photoimage,padding=10)
s.map("Peligro.TButton", text=[("active", "#FFA500")])
s.map("Peligro.TButton", text=[("disabled", "#FFA500")])


  
Button(root,style="Peligro.TButton", compound = LEFT).grid() 
Button(root,style="Peligro.TButton",compound = LEFT).grid() 
Button(root,style="Peligro.TButton",compound = LEFT).grid() 
Button(root,style="Peligro.TButton",compound = LEFT).grid() 

  
root.mainloop()"""
"""
import pathlib

directorio = pathlib.Path('Problema1/media/personajes')
ls=[]
for fichero in directorio.iterdir():
    ls.append(fichero.name)
for archivo in ls:
    print(archivo[:-4])

    """

personajes=[
    {'nombre':'Billy',
     'genero':'hombre',
     'estatura':'alto',
     'articuloCabeza':'gorra',
     'ropa':'pantalón',
     'zapatos':'botas'
    },
    {'nombre':'Brad',
     'genero':'hombre',
     'estatura':'alto',
     'ropa':'pantalón',
     'zapatos':'tennis'
    },
    {'nombre':'Briana',
     'genero':'mujer',
     'estatura':'pequeña',
     'articuloCabeza':['tiara','corona'],
     'ropa':'pantalón',
     'zapatos':'botas'
    },
    {'nombre':'Gunther',
     'genero':'hombre',
     'estatura':'pequeño',
     'articuloCabeza':'gorra',
     'ropa':'short',
     'zapatos':'vikingos'
    },
    {'nombre':'Helga',
     'genero':'mujer',
     'estatura':'alta',
     'articuloCabeza':['diadema','banda'],
     'ropa':'falda',
     'zapatos':'botas'
    },
    {'nombre':'Honey',
     'genero':'mujer',
     'estatura':'alto',
     'ropa':'pantalón',
     'zapatos':'zapatos'
    },
    {'nombre':'Jackie',
     'genero':'hombre',
     'estatura':'alto',
     'articuloCabeza':'gorro',
     'ropa':'pantalón',
     'zapatos':'tennis'
    },
    {'nombre':'Kendall',
     'genero':'mujer',
     'estatura':'alta',
     'articuloCabeza':['diadema','banda'],
     'ropa':'falda',
     'zapatos':'zapatos'
    },
    {'nombre':'Kick',
     'genero':'hombre',
     'estatura':'pequeño',
     'articuloCabeza':'casco',
     'ropa':'overol',
     'zapatos':'botas'
    },
    {'nombre':'Magnus',
     'genero':'hombre',
     'estatura':'alto',
     'articuloCabeza':'casco',
     'ropa':'falda',
     'zapatos':'botas'
    },
]
"""for personaje in personajes:
    try:
        print(personaje['articuloCabeza'])
    except:
        print("No lleva nada en la cabeza")
        """
for personaje in personajes:
    print(personaje['nombre'])