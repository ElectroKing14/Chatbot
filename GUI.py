import tkinter as tk
import threading
import tkinter.ttk as ttk


class App:

    def __init__(self):
        self.response = None
        self.input = ""
        self.input_event = threading.Event()
        self.click_event = threading.Event()

        self.root = tk.Tk()
        self.root.title("Chatbot")
        self.root.geometry("600x800")

        self.bg_color = "#1c1c1c"
        self.fg_color = "#ffffff"
        self.btn_bg_color = "#333333"
        self.input_bg_color = "#252525"

        self.font = ("Calibri", 12)

        self.conversation_box = tk.Text(self.root, bg=self.bg_color, fg=self.fg_color, font=self.font, height=30,
                                        width=60, bd=0, highlightthickness=0)
        self.conversation_box.config(state="disabled")
        self.conversation_box.pack(pady=20, padx=10)

        self.input_label = tk.Label(self.root, text="User Input:", font=self.font, bg=self.bg_color, fg=self.fg_color)
        self.input_label.pack(pady=(0, 10))
        self.input_field = tk.Entry(self.root, bg=self.input_bg_color, fg=self.fg_color, font=self.font, width=50,
                                    bd=0, highlightthickness=0, insertbackground=self.fg_color)
        self.input_field.pack(ipady=5, padx=20)

        self.submit_button = tk.Button(self.root, text="Send", font=self.font, bg=self.btn_bg_color, fg=self.fg_color,
                                       relief="flat", command=self.handle_input)
        self.submit_button.pack(pady=(10, 20))

        self.ja_button = tk.Button(self.root, text="Ja", font=self.font, bg=self.btn_bg_color, fg=self.fg_color,
                                   relief="flat", command=lambda: self.set_response(True), activebackground="#555555")
        style = ttk.Style()
        style.configure("Black.TSeparator", background="black", foreground="black")
        self.seperator = ttk.Separator(self.root, orient='vertical', style="Black.TSeparator")
        self.nein_button = tk.Button(self.root, text="Nein", font=self.font, bg=self.btn_bg_color, fg=self.fg_color,
                                     relief="flat", command=lambda: self.set_response(False))
        self.ja_button.bind("<Return>", lambda event: self.handle_input())
        self.input_field.bind("<Return>", lambda event: self.handle_input())

        self.root.config(bg=self.bg_color)

        self.input_field.focus()

    def handle_input(self):
        self.input = self.input_field.get()
        self.insert_text(f"Sie: {self.input}")
        self.input_field.delete(0, tk.END)
        self.input_field.focus()
        self.input_event.set()

    def get_input(self):
        self.input_event.wait()
        self.input_event.clear()
        return self.input

    def insert_text(self, text):
        self.conversation_box.config(state="normal")
        self.conversation_box.insert(tk.END, f"{text}\n")
        self.conversation_box.see(tk.END)
        self.conversation_box.config(state="disabled")

    def replace_input_with_buttons(self):
        self.input_label.pack_forget()
        self.input_field.pack_forget()
        self.submit_button.pack_forget()

        self.ja_button.pack(side="left", fill="both", expand=True)
        self.seperator.pack(side='left', fill='y')
        self.nein_button.pack(side="left", fill="both", expand=True)

        self.ja_button.bind("<Enter>", lambda event: self.ja_button.config(bg="#555555"))
        self.ja_button.bind("<Leave>", lambda event: self.ja_button.config(bg=self.btn_bg_color))

        self.nein_button.bind("<Enter>", lambda event: self.nein_button.config(bg="#555555"))
        self.nein_button.bind("<Leave>", lambda event: self.nein_button.config(bg=self.btn_bg_color))

    def replace_buttons_with_input(self):
        self.ja_button.pack_forget()
        self.nein_button.pack_forget()
        self.seperator.pack_forget()

        self.input_label.pack(pady=(0, 10))
        self.input_field.pack(ipady=5, padx=20)
        self.submit_button.pack(pady=(10, 20))

        self.input_field.focus()
        self.input_field.delete(0, tk.END)

    def user_consent(self):
        self.replace_input_with_buttons()
        self.click_event.wait()
        self.click_event.clear()
        self.replace_buttons_with_input()
        return self.response

    def set_response(self, response):
        self.response = response
        if response:
            self.insert_text("Sie: Ja")
        else:
            self.insert_text("Sie: Nein")
        self.click_event.set()

    def run(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()
        exit()
