import tkinter as tk
#from tkinter import *
from tkinter import messagebox, Frame, Label, END,TOP,X,Y,BOTH,LEFT,RIGHT,BOTTOM
import pyperclip
import customtkinter as ct
from PIL import Image, ImageTk
from datetime import datetime
import cProfile
from modelo.chatbot import consulta

root = ct.CTk()
root.title("Chatbot G9")
ct.set_appearance_mode("white")
ct.set_default_color_theme("green")
bgColor = "black"
root.configure(fg_color=bgColor)
root.geometry("1000x650+500+100")


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.resizable(True, True)
        self.root.geometry("620x820+500+100")
        self.imagename="images/people.png"

        self.optionFram = Frame(root, bg="#007bff")
        # All imagas for chatfram code

        submitIconSrc = Image.open("images/paper.png")
        submitIconImage = ImageTk.PhotoImage(submitIconSrc.resize((40, 40)))

        # All imagas for chatfram code ends here
        
        header_label=Label(self.optionFram,bg="#007bff",fg="white",text="Chatbot",font=("Arial",20,"bold"))
        header_label.pack(pady=10) 
        self.optionFram.pack(side=TOP, fill=X, anchor="n")

        self.canvas = tk.Canvas(root, bg='#f0f0f0', highlightthickness=1)
    
        self.label_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.label_frame.pack(side="left", fill="both", expand=True)

        self.scrollable_window = self.canvas.create_window((0, 0), window=self.label_frame, anchor="nw")

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label_frame.bind("<Configure>", self.configure_scroll_region)

        self.scrollbar = ct.CTkScrollbar(self.canvas, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.yview_moveto(1.0)

        self.scrollbar.pack(side="right", fill=Y)

        self.canvas.bind("<Configure>", self.resize_frame)
        self.canvas.pack(side=TOP, fill=BOTH,expand=True)

        bgColorChatFram = "#080420"
        self.chatFram = Frame(root, bg=bgColorChatFram)

        self.msgInput = ct.CTkEntry(self.chatFram, placeholder_text="Escribe el mensaje aqui...", height=40, font=("arial", 18))
        self.msgInput.pack(side=LEFT, pady=10, padx=10, fill=X, expand=True)

        self.submitBtn = ct.CTkButton(self.chatFram, text="", image=submitIconImage, bg_color=bgColorChatFram, fg_color=bgColorChatFram, height=40, width=20, hover_color=bgColorChatFram)
        self.submitBtn.pack(side=LEFT, padx=0, pady=8)
        self.submitBtn.configure(command=self.sendMessage)
        

        self.chatFram.pack(side=BOTTOM, fill=X, ipady=5)

        self.root.bind("<Return>", lambda event: self.sendMessage())

    def copy_bot_message(self, event):
        try:
            #message = event.widget._text  # Usar _text en lugar de cget("text")
            pyperclip.copy(self.last_bot_response)
            messagebox.showinfo("Copiado", "Mensaje copiado al portapapeles")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar: {str(e)}")

    
    def sendMessage(self):

        self.message = self.msgInput.get()
        self.msgInput.delete(0, END)
        user_image_src = Image.open(self.imagename)
        user_image = ImageTk.PhotoImage(user_image_src.resize((40, 40)))        
        bot_image_src = Image.open("images/bot2.png")
        bot_image = ImageTk.PhotoImage(bot_image_src.resize((40, 40)))
        if self.message != "":
            
            self.current_time = datetime.now().strftime("%d/%m/%Y  %I:%M %p")
            self.current_time_label = ct.CTkLabel(self.label_frame, 
                                    text=self.current_time, 
                                    font=("arial", 14, "bold"),
                                    text_color="#007bff",# Color del texto (azul)
                                    fg_color="transparent",  # Fondo transparente
                                    corner_radius=8)
            self.current_time_label.pack(side=TOP, anchor="ne", pady=0, padx=5)
            
            self.user_frame = ct.CTkFrame(self.label_frame, fg_color="#f0f0f0")
            self.user_frame.pack(side=TOP, anchor="ne")
            self.user_label = ct.CTkLabel(self.user_frame, text=self.message, font=("Poppins", 15), fg_color="#419f5b", corner_radius=6,
                                    wraplength=250)
            self.user_label.pack(side=LEFT, anchor="nw", pady=10, ipadx=15, ipady=4, padx=10)
            self.user_image_label = ct.CTkLabel(self.user_frame, text="", image=user_image, fg_color="#f0f0f0")
            self.user_image_label.pack(side=TOP, pady=4)
            self.root.update_idletasks()
            self.canvas.update_idletasks()
            self.canvas.yview_moveto(1.0)
            try:
                self.to_respond = consulta(self.message)
                if self.to_respond:

                    
                    self.current_time = datetime.now().strftime("%d/%m/%Y  %I:%M %p")
                    self.current_time_label = ct.CTkLabel(self.label_frame, 
                                    text=self.current_time, 
                                    font=("arial", 14, "bold"),
                                    text_color="#007bff",# Color del texto (azul)
                                    fg_color="transparent",  # Fondo transparente
                                    corner_radius=8)
                    self.current_time_label.pack(side=TOP, anchor="w", pady=0, padx=15)
                    
                    self.bot_frame = ct.CTkFrame(self.label_frame, fg_color="#f0f0f0")
                    self.bot_frame.pack(side=TOP, anchor="w", padx=10)
                    self.bot_response_label = ct.CTkLabel(self.bot_frame, 
                                                          text=self.to_respond, 
                                                          font=("Poppins", 15), 
                                                          fg_color="#007bff", 
                                                          corner_radius=6, 
                                                          wraplength=300,
                                                          justify=LEFT,
                                                          cursor="hand2")
                    self.last_bot_response = self.to_respond
                    self.bot_response_label.pack(side=LEFT, anchor="w", padx=10, pady=1, ipady=8, ipadx=10)
                    self.bot_response_label.bind("<Button-1>", self.copy_bot_message)
                    
                    self.bot_image_label = ct.CTkLabel(self.bot_frame, text="", image=bot_image, fg_color="#f0f0f0")
                    self.bot_image_label.pack(side=TOP, pady=0)
                    self.canvas.update_idletasks()
                    self.canvas.yview_moveto(1.0)

                if self.msgInput.get() : #esto es para que no se cierre la ventana si el usuario no escribe nada
                    print("Working")
                else:
                    pass
            except Exception:
                pass
        else:
            messagebox.showerror("Error", "Por favor ingrese un mensaje")
    
    def configure_scroll_region(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
    def resize_frame(self, e):
        self.canvas.itemconfigure(self.scrollable_window, width=e.width-40)
        
# AvatorPage(root)
ChatApp(root)

cProfile.run("root.mainloop()")