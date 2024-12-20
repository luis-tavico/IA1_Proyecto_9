import tkinter as tk
from tkinter import Text, messagebox

class ChatbotAPP:
    def __init__(self, root):
        self.root=root
        self.root.title("Chatbot")
        self.root.geometry("400x500")
        self.root.resizable(width=False, height=False)
        
        self.create_header()
        #self.create_message_area()
        #self.create_input_area()
        #self.load_messages()
        
    def create_header(self):
        header=tk.Frame(self.root,bg="#007bff",height=50)
        header.pack(fill=tk.X)
        
        header_label=tk.Label(header,bg="#007bff",fg="white",text="Chatbot",font=("Arial",20,"bold"))
        header_label.pack(pady=10)    

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotAPP(root)
    root.mainloop()