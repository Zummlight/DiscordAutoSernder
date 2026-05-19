import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import requests
import time
import random
import threading
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, 'SenderFiles')

os.makedirs(BASE_DIR, exist_ok=True)

MESSAGE_FILE = os.path.join(BASE_DIR, 'trade_message.txt')
TOKEN_FILE = os.path.join(BASE_DIR, 'trade_token.txt')
CHANNELS_FILE = os.path.join(BASE_DIR, 'trade_channels.txt')

BG_MAIN = '#1e1e2e'
BG_LOG = '#181825'
FG_TEXT = '#cdd6f4'
FONT_MAIN = ('Segoe UI', 10)
FONT_BOLD = ('Segoe UI', 10, 'bold')

BTN_SEND_BG = '#89b4fa'
BTN_SEND_HV = '#b4befe'
BTN_AUTO_OFF_BG = '#f38ba8'
BTN_AUTO_OFF_HV = '#f5c2e7'
BTN_AUTO_ON_BG = '#a6e3a1'
BTN_AUTO_ON_HV = '#94e2d5'
BTN_MSG_BG = '#f9e2af'
BTN_MSG_HV = '#fae3b0'
BTN_CHN_BG = '#fab387'
BTN_CHN_HV = '#f5e0dc'
BTN_TOK_BG = '#cba6f7'
BTN_TOK_HV = '#b4befe'
BTN_DISABLED = '#45475a'

class TradeSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Trade Sender")
        self.root.geometry("680x520")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_MAIN)

        self.auto_running = False
        self.auto_thread = None
        self.token = ""
        self.channels = {}
        self.message_content = ""
        
        title_lbl = tk.Label(root, text="✦ DISCORD AUTO SENDER ✦", bg=BG_MAIN, fg=FG_TEXT, font=('Segoe UI', 14, 'bold'))
        title_lbl.pack(pady=(15, 5))

        button_frame = tk.Frame(root, bg=BG_MAIN)
        button_frame.pack(pady=10)

        self.btn_send = self.create_button(button_frame, "SEND", BTN_SEND_BG, BTN_SEND_HV, self.send_once)
        self.btn_send.grid(row=0, column=0, padx=6)

        self.btn_auto = self.create_button(button_frame, "AUTO: OFF", BTN_AUTO_OFF_BG, BTN_AUTO_OFF_HV, self.toggle_auto)
        self.btn_auto.grid(row=0, column=1, padx=6)

        self.btn_msg = self.create_button(button_frame, "MESSAGE", BTN_MSG_BG, BTN_MSG_HV, self.open_msg_editor)
        self.btn_msg.grid(row=0, column=2, padx=6)

        self.btn_chn = self.create_button(button_frame, "CHANNELS", BTN_CHN_BG, BTN_CHN_HV, self.open_chn_editor)
        self.btn_chn.grid(row=0, column=3, padx=6)

        self.btn_token = self.create_button(button_frame, "TOKEN", BTN_TOK_BG, BTN_TOK_HV, self.prompt_for_token)
        self.btn_token.grid(row=0, column=4, padx=6)

        log_frame = tk.Frame(root, bg=BG_MAIN, bd=0)
        log_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, state='disabled', bg=BG_LOG, fg=FG_TEXT, 
                                                  font=("Consolas", 10), bd=0, padx=10, pady=10, 
                                                  insertbackground=FG_TEXT,
                                                  highlightthickness=1, highlightbackground="#313244", highlightcolor="#313244")
        self.log_area.pack(fill=tk.BOTH, expand=True)

        self.load_token()
        self.load_message()
        self.load_channels()
        
        self.log("Program started. Ready to trade. 🚀")

    def create_button(self, parent, text, bg_color, hover_color, command):
        btn = tk.Button(parent, text=text, width=10, command=command, 
                        bg=bg_color, fg='#11111b', font=FONT_BOLD, 
                        relief='flat', bd=0, activebackground=hover_color, cursor="hand2", pady=4)
        
        btn.default_bg = bg_color
        btn.hover_bg = hover_color
        
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=b.hover_bg) if str(b['state']) != 'disabled' else None)
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=b.default_bg) if str(b['state']) != 'disabled' else None)
        
        return btn

    def log(self, text):
        self.log_area.config(state='normal')
        time_str = time.strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{time_str}] {text}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def load_token(self):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                self.token = f.read().strip()
        
        if not self.token:
            self.log("Token not found. Click TOKEN to add it.")
        else:
            self.log("Token successfully loaded from file.")

    def prompt_for_token(self):
        user_token = simpledialog.askstring("Token Settings", "Enter your Discord token:\n(It will be saved to trade_token.txt)", parent=self.root)
        if user_token:
            self.token = user_token.strip()
            with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
                f.write(self.token)
            self.log("Token saved successfully!")

    def load_message(self):
        if not os.path.exists(MESSAGE_FILE):
            with open(MESSAGE_FILE, 'w', encoding='utf-8') as f:
                f.write("")
            self.message_content = ""
            self.log("Message file not found. Created empty trade_message.txt.")
        else:
            with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
                self.message_content = f.read()

    def save_message(self, new_text):
        with open(MESSAGE_FILE, 'w', encoding='utf-8') as f:
            f.write(new_text)
        self.message_content = new_text

    def open_msg_editor(self):
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Message Editor")
        editor_window.geometry("600x550")
        editor_window.resizable(True, True)
        editor_window.configure(bg=BG_MAIN)
        editor_window.transient(self.root)

        def save_text():
            new_text = text_area.get("1.0", tk.END).strip()
            self.save_message(new_text)
            self.log("Message updated and saved.")
            messagebox.showinfo("Success", "Message saved successfully!", parent=editor_window)

        btn_save = tk.Button(editor_window, text="SAVE & APPLY", command=save_text, 
                             bg=BTN_AUTO_ON_BG, fg='#11111b', font=FONT_BOLD, 
                             relief='flat', bd=0, cursor="hand2", pady=6, width=20)
        btn_save.pack(side=tk.BOTTOM, pady=15)
        btn_save.bind("<Enter>", lambda e: btn_save.config(bg=BTN_AUTO_ON_HV))
        btn_save.bind("<Leave>", lambda e: btn_save.config(bg=BTN_AUTO_ON_BG))

        text_area = scrolledtext.ScrolledText(editor_window, bg=BG_LOG, fg=FG_TEXT, font=("Consolas", 11), 
                                              bd=0, padx=10, pady=10, insertbackground=FG_TEXT, highlightthickness=1, highlightbackground="#313244")
        text_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=(20, 5))
        text_area.insert(tk.END, self.message_content)

    def load_channels(self):
        self.channels = {}
        if not os.path.exists(CHANNELS_FILE):
            default_content = "# Format: ChannelID=Custom Name\n921978118523220039=Deepwoken Trade"
            with open(CHANNELS_FILE, 'w', encoding='utf-8') as f:
                f.write(default_content)
            self.log("Channels file not found. Created default trade_channels.txt.")
        
        with open(CHANNELS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            self.parse_channels(content)

    def parse_channels(self, content):
        self.channels = {}
        for line in content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                cid, cname = line.split('=', 1)
                self.channels[cid.strip()] = cname.strip()
            else:
                self.channels[line] = line

    def save_channels(self, content):
        with open(CHANNELS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        self.parse_channels(content)

    def open_chn_editor(self):
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Channels Editor")
        editor_window.geometry("500x450")
        editor_window.resizable(True, True)
        editor_window.configure(bg=BG_MAIN)
        editor_window.transient(self.root)

        def save_chn():
            new_text = text_area.get("1.0", tk.END).strip()
            self.save_channels(new_text)
            self.log("Channels updated and saved.")
            messagebox.showinfo("Success", "Channels saved successfully!", parent=editor_window)

        btn_save = tk.Button(editor_window, text="SAVE CHANNELS", command=save_chn, 
                             bg=BTN_AUTO_ON_BG, fg='#11111b', font=FONT_BOLD, 
                             relief='flat', bd=0, cursor="hand2", pady=6, width=20)
        btn_save.pack(side=tk.BOTTOM, pady=15)
        btn_save.bind("<Enter>", lambda e: btn_save.config(bg=BTN_AUTO_ON_HV))
        btn_save.bind("<Leave>", lambda e: btn_save.config(bg=BTN_AUTO_ON_BG))

        text_area = scrolledtext.ScrolledText(editor_window, bg=BG_LOG, fg=FG_TEXT, font=("Consolas", 11), 
                                              bd=0, padx=10, pady=10, insertbackground=FG_TEXT, highlightthickness=1, highlightbackground="#313244")
        text_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=(15, 5))
        
        with open(CHANNELS_FILE, 'r', encoding='utf-8') as f:
            text_area.insert(tk.END, f.read())

    def send_to_discord(self, channel_id):
        if not self.token:
            self.log("ERROR: Token not provided! Click the TOKEN button.")
            return None

        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        header = {"Authorization": self.token}
        payload = {"content": self.message_content}
        
        try:
            r = requests.post(url, data=payload, headers=header)
            return r.status_code
        except Exception as e:
            self.log(f"Connection error: {e}")
            return None

    def send_routine(self):
        if not self.channels:
            self.log("ERROR: No channels configured! Click CHANNELS to add some.")
            return "no_channels"

        if not self.message_content.strip():
            self.log("ERROR: Message is empty! Click MESSAGE to add text.")
            return "empty_message"

        for channel_id, channel_name in self.channels.items():
            status = self.send_to_discord(channel_id)
            
            if status == 200:
                self.log(f"Sent to '{channel_name}'")
            elif status == 429:
                self.log(f"Rate Limit hit in '{channel_name}'!")
                return "rate_limit"
            elif status == 401:
                self.log("ERROR 401: Unauthorized. Your token might be invalid.")
                return "unauthorized"
            else:
                self.log(f"Error {status} in '{channel_name}'")
                
            time.sleep(random.randint(3, 8))
        return "success"

    def send_once(self):
        if self.auto_running:
            messagebox.showwarning("Warning", "Please turn off AUTO mode first!")
            return
        
        self.btn_send.config(state='disabled', bg=BTN_DISABLED)
        self.log("Sending manually...")
        
        def run():
            self.send_routine()
            self.btn_send.config(state='normal', bg=self.btn_send.default_bg)
            
        threading.Thread(target=run, daemon=True).start()

    def auto_loop(self):
        self.log("AUTO mode enabled.")
        while self.auto_running:
            result = self.send_routine()
            
            if not self.auto_running:
                break
            
            if result in ["no_channels", "empty_message", "unauthorized"]:
                self.log("Critical error. Stopping AUTO mode.")
                self.toggle_auto()
                break

            if result == "rate_limit":
                wait_time = random.randint(10, 30)
                self.log(f"Waiting {wait_time} sec due to rate limit...")
                for _ in range(wait_time):
                    if not self.auto_running: break
                    time.sleep(1)
            else:
                sleep_time = random.randint(120, 180)
                mins, secs = sleep_time // 60, sleep_time % 60
                self.log(f"Waiting {mins}m {secs}s...")
                
                for _ in range(sleep_time):
                    if not self.auto_running: break
                    time.sleep(1)
                    
        self.log("AUTO mode disabled.")

    def toggle_auto(self):
        if not self.auto_running:
            self.auto_running = True
            
            self.btn_auto.config(text="AUTO: ON", bg=BTN_AUTO_ON_BG)
            self.btn_auto.default_bg = BTN_AUTO_ON_BG
            self.btn_auto.hover_bg = BTN_AUTO_ON_HV
            self.btn_send.config(state='disabled', bg=BTN_DISABLED)
            
            self.auto_thread = threading.Thread(target=self.auto_loop, daemon=True)
            self.auto_thread.start()
        else:
            self.auto_running = False
            
            self.btn_auto.config(text="AUTO: OFF", bg=BTN_AUTO_OFF_BG)
            self.btn_auto.default_bg = BTN_AUTO_OFF_BG
            self.btn_auto.hover_bg = BTN_AUTO_OFF_HV
            self.btn_send.config(state='normal', bg=self.btn_send.default_bg)

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeSenderApp(root)
    root.mainloop()
