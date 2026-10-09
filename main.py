import os
import sys
import ctypes
import math
import webbrowser
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

def enable_native_rounded_corners(window):
    """ Applica gli angoli arrotondati nativi su Windows 11 """
    try:
        if sys.platform.startswith("win"):
            window.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
            if not hwnd:
                hwnd = window.winfo_id()
            
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_ROUND = 2
            value = ctypes.c_int(DWMWCP_ROUND)
            
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 
                DWMWA_WINDOW_CORNER_PREFERENCE, 
                ctypes.byref(value), 
                ctypes.sizeof(value)
            )
    except Exception:
        pass

class KirbyBomberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KIRBY BOMBER")
        
        # Finestra verticale (440x600px)
        self.width = 440
        self.height = 600
        self.root.geometry(f"{self.width}x{self.height}")

        # Rimuove la barra di sistema mantenendo la finestra nativa
        self.root.overrideredirect(True)

        # Palette Minimal Gray
        self.BG_COLOR = "#1A1A1A"
        self.TEXT_COLOR = "#888888"

        self.root.config(bg=self.BG_COLOR)

        # Variabili per trascinamento finestra
        self._offset_x = 0
        self._offset_y = 0

        # Riferimenti immagini per evitare garbage collection
        self.keep_images = []

        self.setup_ui()
        self.center_window()
        
        # Gestione chiusura pulita del processo
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        # Applica gli angoli arrotondati nativi (Windows 11)
        enable_native_rounded_corners(self.root)

        # Evento per gestire il ripristino dalla barra delle applicazioni
        self.root.bind("<Map>", self.on_restore)

    def quit_app(self):
        """ Termina istantaneamente il processo Python senza lasciarlo in background """
        try:
            self.root.destroy()
        except Exception:
            pass
        sys.exit(0)

    def center_window(self):
        self.root.update_idletasks()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (self.width / 2)
        y = (hs / 2) - (self.height / 2)
        self.root.geometry(f'{self.width}x{self.height}+{int(x)}+{int(y)}')

    def generate_fade_line(self, width, height=2, color=(136, 136, 136)):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        r, g, b = color
        for x in range(width):
            dist_from_center = abs(x - (width / 2)) / (width / 2)
            alpha = int(255 * (1 - dist_from_center ** 2))
            alpha = max(0, min(255, alpha))
            
            for y in range(height):
                draw.point((x, y), fill=(r, g, b, alpha))
                
        photo = ImageTk.PhotoImage(img)
        self.keep_images.append(photo)
        return photo

    def draw_apple_gear_icon(self, size=16, color=(119, 119, 119)):
        scale = 4
        s = size * scale
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        cx, cy = s / 2, s / 2
        r_outer = s * 0.45
        r_inner = s * 0.32
        r_hole = s * 0.16

        teeth = 6
        for i in range(teeth):
            angle = i * (2 * math.pi / teeth)
            for w in [-0.22, 0.22]:
                a = angle + w
                x_out = cx + r_outer * math.cos(a)
                y_out = cy + r_outer * math.sin(a)
                draw.line([(cx, cy), (x_out, y_out)], fill=color + (255,), width=int(s * 0.14))

        draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=color + (255,))
        draw.ellipse([cx - r_hole, cy - r_hole, cx + r_hole, cy + r_hole], fill=(0, 0, 0, 0))

        smooth_img = img.resize((size, size), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(smooth_img)
        self.keep_images.append(photo)
        return photo

    def minimize_window(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state('iconic')

    def on_restore(self, event):
        if self.root.state() == 'normal':
            self.root.overrideredirect(True)
            enable_native_rounded_corners(self.root)

    def open_options(self):
        print("Opzioni cliccate!")

    def open_github(self):
        webbrowser.open("https://github.com/Ak3nyke")

    def align_title_center(self, event=None):
        """ Calcola il centro esatto dello spazio libero tra il blocco sinistro e quello destro """
        self.root.update_idletasks()
        left_width = self.left_info_frame.winfo_reqwidth()
        right_width = self.btns_frame.winfo_reqwidth()
        
        left_edge = 22 + left_width
        right_edge = self.width - 18 - right_width
        
        center_x = left_edge + (right_edge - left_edge) / 2
        self.lbl_title.place(x=center_x, rely=0.5, anchor=tk.CENTER)

    def setup_ui(self):
        # BARRA DEL TITOLO
        self.title_bar = tk.Frame(self.root, bg=self.BG_COLOR, height=52)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        # 1. BLOCCO SINISTRA: v1.0.0 e GitHub
        self.left_info_frame = tk.Frame(self.title_bar, bg=self.BG_COLOR)
        self.left_info_frame.place(relx=0.0, rely=0.5, x=22, anchor=tk.W)

        lbl_version = tk.Label(
            self.left_info_frame,
            text="v1.0.0",
            bg=self.BG_COLOR,
            fg="#555555",
            font=("Segoe UI", 8, "bold")
        )
        lbl_version.pack(side=tk.TOP, anchor=tk.W)

        lbl_github = tk.Label(
            self.left_info_frame,
            text="GitHub",
            bg=self.BG_COLOR,
            fg="#555555",
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        lbl_github.pack(side=tk.TOP, anchor=tk.W, pady=(1, 0))
        lbl_github.bind("<Button-1>", lambda e: self.open_github())
        lbl_github.bind("<Enter>", lambda e: lbl_github.config(fg="#A0A0A0"))
        lbl_github.bind("<Leave>", lambda e: lbl_github.config(fg="#555555"))

        # 2. CONTENITORE PULSANTI SULLA DESTRA (⚙  ─  ✕)
        self.btns_frame = tk.Frame(self.title_bar, bg=self.BG_COLOR)
        self.btns_frame.place(relx=1.0, rely=0.5, x=-18, anchor=tk.E)

        self.gear_icon_norm = self.draw_apple_gear_icon(size=16, color=(119, 119, 119))
        self.gear_icon_hover = self.draw_apple_gear_icon(size=16, color=(221, 221, 221))

        btn_opts = tk.Label(self.btns_frame, image=self.gear_icon_norm, bg=self.BG_COLOR, cursor="hand2")
        btn_opts.pack(side=tk.LEFT, padx=(0, 12))
        btn_opts.bind("<Button-1>", lambda e: self.open_options())
        btn_opts.bind("<Enter>", lambda e: btn_opts.config(image=self.gear_icon_hover))
        btn_opts.bind("<Leave>", lambda e: btn_opts.config(image=self.gear_icon_norm))

        self.btn_min_canvas = tk.Canvas(self.btns_frame, width=20, height=20, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.btn_min_canvas.pack(side=tk.LEFT, padx=(0, 12))
        
        self.min_line = self.btn_min_canvas.create_line(4, 10, 16, 10, fill="#777777", width=2)
        
        self.btn_min_canvas.bind("<Button-1>", lambda e: self.minimize_window())
        self.btn_min_canvas.bind("<Enter>", lambda e: self.btn_min_canvas.itemconfig(self.min_line, fill="#FFCC00"))
        self.btn_min_canvas.bind("<Leave>", lambda e: self.btn_min_canvas.itemconfig(self.min_line, fill="#777777"))

        btn_close = tk.Label(self.btns_frame, text="✕", bg=self.BG_COLOR, fg="#777777", font=("Arial", 11, "bold"), cursor="hand2")
        btn_close.pack(side=tk.LEFT)
        btn_close.bind("<Button-1>", lambda e: self.quit_app())
        btn_close.bind("<Enter>", lambda e: btn_close.config(fg="#FF5555"))
        btn_close.bind("<Leave>", lambda e: btn_close.config(fg="#777777"))

        # 3. TITOLO "WORK IN PROGRESS" (Font pulito e ben visibile)
        title_text = "WORK IN PROGRESS"
        self.lbl_title = tk.Label(
            self.title_bar, 
            text=title_text, 
            bg=self.BG_COLOR, 
            fg="#E0E0E0", 
            font=("Segoe UI", 11, "bold")
        )
        
        # Posizionamento dinamico al centro
        self.align_title_center()

        # Trascinamento finestra
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.lbl_title.bind("<Button-1>", self.start_move)
        self.lbl_title.bind("<B1-Motion>", self.do_move)
        lbl_version.bind("<Button-1>", self.start_move)
        lbl_version.bind("<B1-Motion>", self.do_move)

        # LINEA DI DIVISIONE SFUMATA
        self.fade_line_top = self.generate_fade_line(width=400, height=2, color=(100, 100, 100))
        self.divider_top = tk.Label(self.root, image=self.fade_line_top, bg=self.BG_COLOR, bd=0, highlightthickness=0)
        self.divider_top.pack(fill=tk.X, padx=20, pady=(0, 5))

        # CONTENUTO PRINCIPALE
        content_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True)

    def start_move(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self._offset_x
        y = self.root.winfo_y() + event.y - self._offset_y
        self.root.geometry(f"+{x}+{y}")

KirbyBomber = KirbyBomberApp

if __name__ == "__main__":
    root = tk.Tk()
    app = KirbyBomberApp(root)
    root.mainloop()