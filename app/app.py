import tkinter as tk
from tkinter import Text, messagebox,Label,Frame,Button,Entry,Scrollbar

class ChatbotAPP:
    def __init__(self, root):
        self.root=root
        self.root.title("Chatbot")
        self.root.geometry("400x600")
        self.root.resizable(width=False, height=False)
        
        self.create_header()
        self.create_message_area()
        self.create_input_area()
        self.load_messages()
        
    def create_header(self):
        header=Frame(self.root,bg="#007bff",height=False)
        header.pack(fill=tk.X)
        
        header_label=Label(header,bg="#007bff",fg="white",text="Chatbot",font=("Arial",20,"bold"))
        header_label.pack(pady=10)   

        #line = Label(header, width=450, bg="#007bff")
        #line.place(relwidth=1, rely=0.07, relheight=0.012)
        
    def create_message_area(self):
        self.messages_frame=Frame(self.root,bg="#f1f1f1")
        self.messages_frame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
        
        self.scrollbar=Scrollbar(self.messages_frame)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.text_widget=Text(self.messages_frame,yscrollcommand=self.scrollbar.set,wrap=tk.WORD,bg="white",fg="black",font=("Arial",12))
        #self.text_widget.place(relwidth=1,relheight=0.974)
        self.text_widget.pack(fill=tk.BOTH,expand=True)
        self.scrollbar.config(command=self.text_widget.yview)
        
        self.text_widget.tag_config("bot",foreground="red", font=("Arial",11,"bold"))
        self.text_widget.tag_config("bot_msg",foreground="gray", font=("Arial",11,"italic"))
        self.text_widget.tag_config("you",foreground="blue", font=("Arial",11,"bold"))
        self.text_widget.tag_config("you_msg",foreground="green", font=("Arial",11))
        self.text_widget.config(state=tk.DISABLED,cursor="arrow")
            
    def create_input_area(self):
        input_frame=Frame(self.root,bg="white")
        input_frame.pack(fill=tk.X,pady=5)
        
        self.entry=Entry(input_frame,font=("Arial",12))
        #self.entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entry.focus()
        self.entry.bind("<Return>",self.send_message)
        self.entry.pack(side=tk.LEFT,padx=10,pady=5,fill=tk.X,expand=True)

        
        
        self.send_button=Button(input_frame,text="Enviar",bg="#007bff",fg="white",font=("Arial",12),command=lambda:self.send_message(None) or self.send_message(None)) 
        self.send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        self.send_button.pack(padx=10,pady=10,side=tk.RIGHT)
        

    
    def load_messages(self):
        messages = [
            ("Bot", "welcome, anything else i can assist you with?"),
            ("You", "do you speak spanish?"),
            ("Bot", "Yes, I enjoy talking"),
            ("You", "que bueno"),
            ("Bot", "¡Qué bueno verte! 😊 ¿Cómo te sientes?"),
            ("You", "bien y tu"),
            ("Bot", "Oh, qué gracioso, pensaste que me importaba. Me haces reír."),
        ]

        for sender, message in messages:
            self.add_message(message, sender)
    
    
    def add_message(self,message,sender):
        self.text_widget.config(state=tk.NORMAL)
        if sender=="Bot":
            self.text_widget.insert(tk.END,f"{sender}: ","bot")
            self.text_widget.insert(tk.END,f"{message}\n\n","bot_msg")
        else:
            self.text_widget.insert(tk.END,f"{sender}: ","you")
            self.text_widget.insert(tk.END,f"{message}\n\n","you_msg")
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)
        
    def send_message(self,event):
        user_mensaje=self.entry.get()
        if user_mensaje.strip():
            self.add_message(user_mensaje,"you")
            self.entry.delete(0,tk.END)
            
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotAPP(root)
    root.mainloop()