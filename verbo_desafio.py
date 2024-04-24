import random
import customtkinter as ctk
import pygame
import verbos as fn
from PIL import Image
import sys

pygame.mixer.init()
musica_fondo = pygame.mixer.Sound("C:/Users/LENOVO/Downloads/PROYECTO/musica_fondo.mp3")
sonido_incorrecto = pygame.mixer.Sound("C:/Users/LENOVO/Downloads/PROYECTO/incorrecto.mp3")
sonido_correcto = pygame.mixer.Sound("C:/Users/LENOVO/Downloads/PROYECTO/correcto.mp3")
sonido_fin = pygame.mixer.Sound("C:/Users/LENOVO/Downloads/PROYECTO/fin.mp3")
musica_fondo.play(-1)
sonidos_silenciados = False
verbos = fn.verbos_facil
verbos2 = fn.verbos_medio
verbos3 = fn.verbos_dificil
NUM_INTENTOS = 3

def salir_juego():
    if pygame.display.get_init():
        pygame.quit()
    sys.exit()
    
def validar(P):
    return len(P) == 0 or (len(P) == 1 and P.isalpha())
def verificar_verbo(verbo):
    return verbo.lower() in verbos.values()
def alternar_sonidos(boton_sonidos):
    global sonidos_silenciados
    sonidos_silenciados = not sonidos_silenciados
    actualizar_texto_boton(boton_sonidos)
def actualizar_texto_boton(boton_sonidos):
    if sonidos_silenciados:
        sonido_incorrecto.set_volume(0)
        sonido_correcto.set_volume(0)
        sonido_fin.set_volume(0)
        boton_sonidos.configure(text="REACTIVAR SONIDOS")
    else:
        sonido_incorrecto.set_volume(1)
        sonido_correcto.set_volume(1)
        sonido_fin.set_volume(1)
        boton_sonidos.configure(text="SILENCIAR SONIDOS") 
def ajustar_volumen_fondo(valor):
    musica_fondo.set_volume(valor / 100)
def mostrarventana1():
    ventana2.withdraw()
    ventana3.withdraw()
    ventana1.deiconify()
def mostrarventana2():
    ventana1.withdraw()
    ventana3.withdraw()
    ventana2.deiconify()
def mostrarventana3():
    ventana1.withdraw()
    ventana2.withdraw()
    ventana3.deiconify()
def mostrarventana4():
    ventana1.withdraw()
    ventana2.withdraw()
    ventana3.withdraw()
    ventana4.deiconify()
def cambiar_tema(nuevo_tema):
    ctk.set_appearance_mode(nuevo_tema)
def crear_boton(ventana, texto, comando, ancho=150, alto=85, radio=200, borde=5, fuente=("Verdana", 20, "bold"), color_texto="white", color_fondo="Midnight Blue", color_hover="DodgerBlue", color_borde="white", relx=0.5, rely=0.5, anchor="center"):
    boton = ctk.CTkButton(ventana,
                          text=texto,
                          command=comando,
                          width=ancho,
                          height=alto,
                          corner_radius=radio,
                          border_width=borde,
                          font=fuente,
                          text_color=color_texto,
                          fg_color=color_fondo,
                          hover_color=color_hover,
                          border_color=color_borde)
    boton.place(relx=relx, rely=rely, anchor=anchor)
    return boton
def principal():
    ventana1.withdraw()
    ventana2.withdraw()
    ventana3.withdraw()
    ventana4.withdraw()
    def reiniciar_juego():
        ventana.destroy()
        principal()
    def mostrar_boton_reiniciar():
        boton_reiniciar = crear_boton(ventana, "SIGUIENTE VERBO", reiniciar_juego)
        boton_reiniciar.place(relx=0.5, rely=0.5, anchor="center")
    def mensaje_error(mensaje):
        etiqueta.configure(text=mensaje)
    ventana = ctk.CTk()
    ventana.geometry("1522x780+0+5")
    ventana.title("VERBO DESAFÍO")
    palabras = list(verbos.keys())
    secreto_espanol = random.choice(palabras)
    secreto_ingles = verbos[secreto_espanol]["en_ingles"]
    original = verbos[secreto_espanol]["original"]
    longitud_palabra = len(secreto_ingles)
    frame_cuadritos = ctk.CTkFrame(ventana,
                                   border_width=4,
                                   border_color="White",)
    frame_cuadritos.place(relx=0.5, rely=0.5, anchor="center")
    campos_entrada = [[ctk.CTkEntry(frame_cuadritos,
                            width=75,
                            height=75,
                            font=("Helvetica", 50, "bold"),
                            justify="center",
                            validate="key",
                            border_width=2,
                            border_color="White",
                            validatecommand=(ventana.register(validar),"%P")) for _ in range(longitud_palabra)] for _ in range(NUM_INTENTOS)]
    for counter_2 in range(len(campos_entrada)):
        for counter_1 in range(len(campos_entrada[counter_2])):
            campos_entrada[counter_2][counter_1].grid(row=counter_2,
                                                      column=counter_1,
                                                      padx=10,
                                                      pady=20)
    etiqueta = ctk.CTkButton(ventana,
                            text=f"INGRESE EN PASADO SIMPLE EL VERBO \"{secreto_espanol.upper()}\" EN INGLES",
                            width=100,
                            height=55,
                            border_width=5,
                            font=("Verdana", 18, "bold"),
                            text_color="white",
                            fg_color="dark slate gray",
                            hover_color="dark slate gray",
                            border_color="white",
                            corner_radius=200)
    etiqueta.place(relx=0.5, rely=0.1, anchor="center")
    boton_reiniciar = ctk.CTkButton(ventana, text="SIGUIENTE VERBO",font=("Times New Roman", 14,"bold"), command=reiniciar_juego)
    def ocultar_boton_reiniciar():
        boton_reiniciar.grid_forget()
    def manejar_entrada(event, campos_entrada, counter_2):
        char = event.char
        if char.isalpha() or char == " ":
            siguiente_campo = next((campo for campo in campos_entrada[counter_2] if not campo.get()), None)
            if siguiente_campo:
                siguiente_campo.focus()
                siguiente_campo.insert("end",char)
    def verificarIntento(secreto_ingles,secreto_espanol,campos_entrada, etiqueta,counter_2,intentos_fallidos):
        intento = "".join(char.get() for char in campos_entrada[counter_2])
        mensaje_error(f"INGRESE EN PASADO SIMPLE EL VERBO \"{secreto_espanol.upper()}\" EN INGLES")
        if len(intento) != len(secreto_ingles):
            mensaje_error(f"POR FAVOR INGRESA UN VERBO CON {len(secreto_ingles)} LETRAS")
            if intentos_fallidos < NUM_INTENTOS - 1 and not sonidos_silenciados:
                sonido_incorrecto.play()
        else:
            if intento.lower() == secreto_ingles:
                for counter_1 in range(len(secreto_ingles)):
                    campos_entrada[counter_2][counter_1].configure(state="disabled", text_color="green")
                mensaje_exito = f"FELICIDADES, EL VERBO EN PASADO SIMPLE ES {secreto_ingles.upper()} Y EN SU FORMA ORIGINAL ES {original.upper()}"
                etiqueta.configure(text=mensaje_exito)
                if not sonidos_silenciados:
                    sonido_correcto.play()
                mostrar_boton_reiniciar()
            else:
                for counter_1 in range(len(secreto_ingles)):
                    if counter_1 < len(intento):
                        if intento[counter_1] == secreto_ingles[counter_1]:
                            campos_entrada[counter_2][counter_1].configure(state="disabled", text_color="green")
                        elif intento[counter_1] in secreto_ingles:
                            campos_entrada[counter_2][counter_1].configure(state="disabled", text_color="yellow")
                intentos_fallidos += 1
                if intentos_fallidos == NUM_INTENTOS:
                    mensaje_error(f"LO SIENTO, EL VERBO EN PASADO SIMPLE ES {secreto_ingles.upper()} Y EN SU FORMA ORIGINAL ES {original.upper()}")
                    if not sonidos_silenciados:
                        sonido_fin.play()
                    mostrar_boton_reiniciar()
                else:
                    if intentos_fallidos < NUM_INTENTOS and not sonidos_silenciados:
                        sonido_incorrecto.play()
                    esperarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,counter_2 + 1,intentos_fallidos)  
    def esperarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,counter_2,intentos_fallidos=0):
        for counter_1 in range(len(campos_entrada[counter_2])):
            campos_entrada[counter_2][counter_1].bind("<Key>", lambda event: manejar_entrada(event, campos_entrada, counter_2))
            campos_entrada[counter_2][counter_1].configure(state="normal")
        boton_verificar = crear_boton(ventana, "VERIFICAR", lambda: verificarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,counter_2,intentos_fallidos))
        boton_verificar.place(relx=0.90, rely=0.90, anchor="center")
        campos_entrada[counter_2][0].focus()

    def cerrar():
        ventana.withdraw()
        ventana4.deiconify()
    esperarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,0)
    ocultar_boton_reiniciar()
    
    boton_salir = crear_boton(ventana, "VOLVER", cerrar)
    boton_salir.place(relx=0.1, rely=0.9, anchor="center")
    ventana.mainloop()

def principal2():
    ventana1.withdraw()
    ventana2.withdraw()
    ventana3.withdraw()
    ventana4.withdraw()
    def reiniciar_juego():
        ventana5.destroy()
        principal2()
    def mostrar_boton_reiniciar():
        boton_reiniciar = crear_boton(ventana5, "SIGUIENTE VERBO", reiniciar_juego)
        boton_reiniciar.place(relx=0.5, rely=0.5, anchor="center")
    def mensaje_error(mensaje):
        etiqueta.configure(text=mensaje)
    ventana5 = ctk.CTk()
    ventana5.geometry("1522x780+0+5")
    ventana5.title("VERBO DESAFÍO")
    palabras = list(verbos2.keys())
    secreto_espanol = random.choice(palabras)
    secreto_ingles = verbos2[secreto_espanol]["en_ingles"]
    original = verbos2[secreto_espanol]["original"]
    longitud_palabra = len(secreto_ingles)
    frame_cuadritos = ctk.CTkFrame(ventana5,
                                   border_width=4,
                                   border_color="White",)
    frame_cuadritos.place(relx=0.5, rely=0.5, anchor="center")
    campos_entrada = [[ctk.CTkEntry(frame_cuadritos,
                            width=75,
                            height=75,
                            font=("Helvetica", 50, "bold"),
                            justify="center",
                            validate="key",
                            border_width=2,
                            border_color="White",
                            validatecommand=(ventana5.register(validar),"%P")) for _ in range(longitud_palabra)] for _ in range(NUM_INTENTOS)]
    for counter_2 in range(len(campos_entrada)):
        for counter_1 in range(len(campos_entrada[counter_2])):
            campos_entrada[counter_2][counter_1].grid(row=counter_2,
                                                      column=counter_1,
                                                      padx=10,
                                                      pady=20)
    etiqueta = ctk.CTkButton(ventana5,
                            text=f"INGRESE EN PASADO SIMPLE EL VERBO \"{secreto_espanol.upper()}\" EN INGLES",
                            width=100,
                            height=55,
                            border_width=5,
                            font=("Verdana", 18, "bold"),
                            text_color="white",
                            fg_color="dark slate gray",
                            hover_color="dark slate gray",
                            border_color="white",
                            corner_radius=200)
    etiqueta.place(relx=0.5, rely=0.1, anchor="center")
    boton_reiniciar = ctk.CTkButton(ventana5, text="SIGUIENTE VERBO",font=("Times New Roman", 14,"bold"), command=reiniciar_juego)
    def ocultar_boton_reiniciar():
        boton_reiniciar.grid_forget()
    def manejar_entrada(event, campos_entrada, counter_2):
        char = event.char
        if char.isalpha() or char == " ":
            siguiente_campo = next((campo for campo in campos_entrada[counter_2] if not campo.get()), None)
            if siguiente_campo:
                siguiente_campo.focus()
                siguiente_campo.insert("end",char)
    def verificarIntento(secreto_ingles,secreto_espanol,campos_entrada, etiqueta,counter_2,intentos_fallidos):
        intento = "".join(char.get() for char in campos_entrada[counter_2])
        mensaje_error(f"INGRESE EN PASADO SIMPLE EL VERBO \"{secreto_espanol.upper()}\" EN INGLES")
        if len(intento) != len(secreto_ingles):
            mensaje_error(f"POR FAVOR INGRESA UN VERBO CON {len(secreto_ingles)} LETRAS")
            if intentos_fallidos < NUM_INTENTOS - 1 and not sonidos_silenciados:
                sonido_incorrecto.play()
        else:
            if intento.lower() == secreto_ingles:
                for counter_1 in range(len(secreto_ingles)):
                    campos_entrada[counter_2][counter_1].configure(state="disabled", text_color="green")
                mensaje_exito = f"FELICIDADES, EL VERBO EN PASADO SIMPLE ES {secreto_ingles.upper()} Y EN SU FORMA ORIGINAL ES {original.upper()}"
                etiqueta.configure(text=mensaje_exito)
                if not sonidos_silenciados:
                    sonido_correcto.play()
                mostrar_boton_reiniciar()
            else:
                for counter_1 in range(len(secreto_ingles)):
                    if counter_1 < len(intento):
                        if intento[counter_1] == secreto_ingles[counter_1]:
                            campos_entrada[counter_2][counter_1].configure(state="disabled", text_color="green")
                        elif intento[counter_1] in secreto_ingles:
                            campos_entrada[counter_2][counter_1].configure(state="disabled", text_color="yellow")
                intentos_fallidos += 1
                if intentos_fallidos == NUM_INTENTOS:
                    mensaje_error(f"LO SIENTO, EL VERBO EN PASADO SIMPLE ES {secreto_ingles.upper()} Y EN SU FORMA ORIGINAL ES {original.upper()}")
                    if not sonidos_silenciados:
                        sonido_fin.play()
                    mostrar_boton_reiniciar()
                else:
                    if intentos_fallidos < NUM_INTENTOS and not sonidos_silenciados:
                        sonido_incorrecto.play()
                    esperarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,counter_2 + 1,intentos_fallidos)
                
    def esperarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,counter_2,intentos_fallidos=0):
        for counter_1 in range(len(campos_entrada[counter_2])):
            campos_entrada[counter_2][counter_1].bind("<Key>", lambda event: manejar_entrada(event, campos_entrada, counter_2))
            campos_entrada[counter_2][counter_1].configure(state="normal")
        boton_verificar = crear_boton(ventana5, "VERIFICAR", lambda: verificarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,counter_2,intentos_fallidos))
        boton_verificar.place(relx=0.90, rely=0.90, anchor="center")
        campos_entrada[counter_2][0].focus()
    def cerrar():
        ventana5.withdraw()
        ventana4.deiconify()
    esperarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,0)
    ocultar_boton_reiniciar()
    boton_salir = crear_boton(ventana5, "VOLVER", cerrar)
    boton_salir.place(relx=0.1, rely=0.9, anchor="center")
    ventana5.mainloop()  
def principal3():
    ventana1.withdraw()
    ventana2.withdraw()
    ventana3.withdraw()
    ventana4.withdraw()
    def reiniciar_juego():
        ventana6.destroy()
        principal3()
    def mostrar_boton_reiniciar():
        boton_reiniciar = crear_boton(ventana6, "SIGUIENTE VERBO", reiniciar_juego)
        boton_reiniciar.place(relx=0.5, rely=0.5, anchor="center")
    def mensaje_error(mensaje):
        etiqueta.configure(text=mensaje)
    ventana6 = ctk.CTk()
    ventana6.geometry("1522x780+0+5")
    ventana6.title("VERBO DESAFÍO")
    palabras = list(verbos3.keys())
    secreto_espanol = random.choice(palabras)
    secreto_ingles = verbos3[secreto_espanol]["en_ingles"]
    original = verbos3[secreto_espanol]["original"]
    longitud_palabra = len(secreto_ingles)
    frame_cuadritos = ctk.CTkFrame(ventana6,
                                   border_width=4,
                                   border_color="White",)
    frame_cuadritos.place(relx=0.5, rely=0.5, anchor="center")
    campos_entrada = [[ctk.CTkEntry(frame_cuadritos,
                            width=75,
                            height=75,
                            font=("Helvetica", 50, "bold"),
                            justify="center",
                            validate="key",
                            border_width=2,
                            border_color="White",
                            validatecommand=(ventana6.register(validar),"%P")) for _ in range(longitud_palabra)] for _ in range(NUM_INTENTOS)]
    for counter_2 in range(len(campos_entrada)):
        for counter_1 in range(len(campos_entrada[counter_2])):
            campos_entrada[counter_2][counter_1].grid(row=counter_2,
                                                      column=counter_1,
                                                      padx=10,
                                                      pady=20)
    etiqueta = ctk.CTkButton(ventana6,
                            text=f"INGRESE EN PASADO SIMPLE EL VERBO \"{secreto_espanol.upper()}\" EN INGLES",
                            width=100,
                            height=55,
                            border_width=5,
                            font=("Verdana", 18, "bold"),
                            text_color="white",
                            fg_color="dark slate gray",
                            hover_color="dark slate gray",
                            border_color="white",
                            corner_radius=200)
    etiqueta.place(relx=0.5, rely=0.1, anchor="center")
    boton_reiniciar = ctk.CTkButton(ventana6, text="SIGUIENTE VERBO",font=("Times New Roman", 14,"bold"), command=reiniciar_juego)
    def ocultar_boton_reiniciar():
        boton_reiniciar.grid_forget()
    def manejar_entrada(event, campos_entrada, counter_2):
        char = event.char
        if char.isalpha() or char == " ":
            siguiente_campo = next((campo for campo in campos_entrada[counter_2] if not campo.get()), None)
            if siguiente_campo:
                siguiente_campo.focus()
                siguiente_campo.insert("end",char)
    def verificarIntento(secreto_ingles,secreto_espanol,campos_entrada, etiqueta,counter_2,intentos_fallidos):
        intento = "".join(char.get() for char in campos_entrada[counter_2])
        mensaje_error(f"INGRESE EN PASADO SIMPLE EL VERBO \"{secreto_espanol.upper()}\" EN INGLES")
        if len(intento) != len(secreto_ingles):
            mensaje_error(f"POR FAVOR INGRESA UN VERBO CON {len(secreto_ingles)} LETRAS")
            if intentos_fallidos < NUM_INTENTOS - 1 and not sonidos_silenciados:
                sonido_incorrecto.play()
        else:
            if intento.lower() == secreto_ingles:
                for counter_1 in range(len(secreto_ingles)):
                    campos_entrada[counter_2][counter_1].configure(state="disabled", text_color="green")
                mensaje_exito = f"FELICIDADES, EL VERBO EN PASADO SIMPLE ES {secreto_ingles.upper()} Y EN SU FORMA ORIGINAL ES {original.upper()}"
                etiqueta.configure(text=mensaje_exito)
                if not sonidos_silenciados:
                    sonido_correcto.play()
                mostrar_boton_reiniciar()
            else:
                for counter_1 in range(len(secreto_ingles)):
                    if counter_1 < len(intento):
                        if intento[counter_1] == secreto_ingles[counter_1]:
                            campos_entrada[counter_2][counter_1].configure(state="disabled", text_color="green")
                        elif intento[counter_1] in secreto_ingles:
                            campos_entrada[counter_2][counter_1].configure(state="disabled", text_color="yellow")
                intentos_fallidos += 1
                if intentos_fallidos == NUM_INTENTOS:
                    mensaje_error(f"LO SIENTO, EL VERBO EN PASADO SIMPLE ES {secreto_ingles.upper()} Y EN SU FORMA ORIGINAL ES {original.upper()}")
                    if not sonidos_silenciados:
                        sonido_fin.play()
                    mostrar_boton_reiniciar()
                else:
                    if intentos_fallidos < NUM_INTENTOS and not sonidos_silenciados:
                        sonido_incorrecto.play()
                    esperarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,counter_2 + 1,intentos_fallidos)
    def esperarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,counter_2,intentos_fallidos=0):
        for counter_1 in range(len(campos_entrada[counter_2])):
            campos_entrada[counter_2][counter_1].bind("<Key>", lambda event: manejar_entrada(event, campos_entrada, counter_2))
            campos_entrada[counter_2][counter_1].configure(state="normal")
        
        boton_verificar = crear_boton(ventana6, "VERIFICAR", lambda: verificarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,counter_2,intentos_fallidos))
        boton_verificar.place(relx=0.90, rely=0.90, anchor="center")
        campos_entrada[counter_2][0].focus()
    def cerrar():
        ventana6.withdraw()
        ventana4.deiconify()
    esperarIntento(secreto_ingles,secreto_espanol,campos_entrada,etiqueta,0)
    ocultar_boton_reiniciar()
    boton_salir = crear_boton(ventana6, "VOLVER", cerrar)
    boton_salir.place(relx=0.1, rely=0.9, anchor="center")
    ventana6.mainloop()   
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("Dark")
ventana1 = ctk.CTk()
ventana1.geometry("1522x780+0+5")
ventana1.title("VERBODESAFÍO")
isologo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/isologoazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/isologoblanco.png"),size=(250,250))
image_label = ctk.CTkLabel(ventana1, image=isologo, text="")
image_label.pack(pady = 10)
image_label.place(x=150, y=250)
logo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/logotipoazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/logotipoblanco.png"),size=(180,50))
image_label = ctk.CTkLabel(ventana1, image=logo, text="")
image_label.pack(pady = 10)
image_label.place(x=1150, y=370)
logo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/sloganazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/sloganblanco.png"),size=(270,47))
image_label = ctk.CTkLabel(ventana1, image=logo, text="")
image_label.pack(pady = 10)
image_label.place(x=627, y=20)
boton_jugar = crear_boton(ventana1, "JUGAR", mostrarventana4)
boton_jugar.place(relx=0.5, rely=0.3, anchor="center")
boton_instrucciones = crear_boton(ventana1, "INSTRUCCIONES", mostrarventana2)
boton_instrucciones.place(relx=0.5, rely=0.5, anchor="center")
boton_configurar = crear_boton(ventana1, "CONFIGURACIÓN", mostrarventana3)
boton_configurar.place(relx=0.5, rely=0.7, anchor="center")
boton_salir = crear_boton(ventana1, "SALIR", salir_juego)
boton_salir.place(relx=0.5, rely=0.9, anchor="center")


ventana2 = ctk.CTkToplevel(ventana1)
ventana2.geometry("1522x780+0+5")
ventana2.title("INSTRUCCIONES")

isologo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/isologoazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/isologoblanco.png"),size=(750,750))
image_label = ctk.CTkLabel(ventana2, image=isologo, text="")
image_label.pack(pady = 10)
image_label.place(x=350, y=10)
boton_volver = crear_boton(ventana2, "VOLVER", mostrarventana1)
boton_volver.place(relx=0.1, rely=0.9, anchor="center")
instrucciones = ctk.CTkButton(ventana2,
                            text=fn.instrucciones,   
                            width=150,
                            height=85,
                            corner_radius=0,
                            border_width=5,
                            font=("Verdana", 20, "bold"),
                            text_color="white",
                            fg_color="Midnight Blue",
                            hover_color="Midnight Blue",
                            border_color="DodgerBlue")
instrucciones.place(relx=0.5, rely=0.5, anchor="center")

ventana2.withdraw()
ventana3 = ctk.CTkToplevel(ventana1)
ventana3.geometry("1522x780+0+5")
ventana3.title("CONFIGURACIÓN")
isologo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/isologoazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/isologoblanco.png"),size=(250,250))
image_label = ctk.CTkLabel(ventana3, image=isologo, text="")
image_label.pack(pady = 10)
image_label.place(x=150, y=250)
logo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/logotipoazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/logotipoblanco.png"),size=(180,50))
image_label = ctk.CTkLabel(ventana3, image=logo, text="")
image_label.pack(pady = 10)
image_label.place(x=1150, y=370)
logo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/sloganazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/sloganblanco.png"),size=(270,47))
image_label = ctk.CTkLabel(ventana3, image=logo, text="")
image_label.pack(pady = 10)
image_label.place(x=627, y=50)
boton_oscuro = crear_boton(ventana3, "TEMA OSCURO",lambda: cambiar_tema("Dark"))
boton_oscuro.place(relx=0.5, rely=0.3, anchor="center")
boton_claro = crear_boton(ventana3, "TEMA CLARO",lambda: cambiar_tema("Light"))
boton_claro.place(relx=0.5, rely=0.5, anchor="center")
boton_sonidos = crear_boton(ventana3, "SILENCIAR SONIDOS",lambda: alternar_sonidos(boton_sonidos))
boton_sonidos.place(relx=0.5, rely=0.7, anchor="center")
boton_volver2 = crear_boton(ventana3, "VOLVER",mostrarventana1)
boton_volver2.place(relx=0.1, rely=0.9, anchor="center")
label_volumen = ctk.CTkLabel(ventana3, text="VOLUMEN:",font=("Verdana", 15, "bold"))
label_volumen.place(relx=0.5, rely=0.85, anchor="center")
barra_volumen_ventana3 = ctk.CTkSlider(ventana3,from_=0,to=100,command=ajustar_volumen_fondo)
barra_volumen_ventana3.set(100)
barra_volumen_ventana3.place(relx=0.5, rely=0.9, anchor="center")
ventana3.withdraw()
ventana4 = ctk.CTkToplevel(ventana1)
ventana4.geometry("1522x780+0+5")
ventana4.title("NIVELES")
isologo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/isologoazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/isologoblanco.png"),size=(250,250))
image_label = ctk.CTkLabel(ventana4, image=isologo, text="")
image_label.pack(pady = 10)
image_label.place(x=150, y=250)
logo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/logotipoazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/logotipoblanco.png"),size=(180,50))
image_label = ctk.CTkLabel(ventana4, image=logo, text="")
image_label.pack(pady = 10)
image_label.place(x=1150, y=370)
logo = ctk.CTkImage(light_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/sloganazul.png"),dark_image=Image.open("C:/Users/LENOVO/Downloads/PROYECTO/sloganblanco.png"),size=(270,47))
image_label = ctk.CTkLabel(ventana4, image=logo, text="")
image_label.pack(pady = 10)
image_label.place(x=627, y=50)
boton_facil= crear_boton(ventana4, "NIVEL FACIL",principal)
boton_facil.place(relx=0.5, rely=0.3, anchor="center")
boton_medio = crear_boton(ventana4, "NIVEL MEDIO",principal2)
boton_medio.place(relx=0.5, rely=0.5, anchor="center")
boton_sonidos = crear_boton(ventana4, "NIVEL DIFICIL",principal3)
boton_sonidos.place(relx=0.5, rely=0.7, anchor="center")
boton_volver2 = crear_boton(ventana4, "VOLVER",mostrarventana1)
boton_volver2.place(relx=0.1, rely=0.9, anchor="center")
ventana4.withdraw()
ventana1.mainloop()
principal()