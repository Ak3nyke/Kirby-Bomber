import os
import sys
import ctypes
import math
import colorsys
import webbrowser
import urllib.request
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance

# --- HELPER FONDAMENTALE PER PYINSTALLER ---
def resource_path(relative_path):
    """ Ottiene il percorso assoluto delle risorse, funziona sia in dev sia dentro l'EXE compilato """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Fix per schermi ad alta densità (1080p, 2k, 4k)
try:
    if sys.platform.startswith("win"):
        ctypes.windll.shcore.SetProcessDpiAwareness(2) # PROCESS_PER_MONITOR_DPI_AWARE
except Exception:
    pass

def enable_native_rounded_corners(window):
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

ORIGINAL_TITLE = "KIRBY BOMBER - DESTROYER OF PC"

TRANSLATIONS = {
    "English": {
        "code": "gb",
        "lang_label": "Language",
        "theme_label": "Theme",
        "title": ORIGINAL_TITLE,
        "slider_label": "How many Kirby do you want?",
        "rand_header": "Randomizer",
        "rand_btn": "Randomize",
        "num_header": "Number of Kirby",
        "mode_header": "Kirby Mode",
        "btn_release": "Release all Kirby :)",
        "btn_release_confirm": "Are you really sure?",
        "btn_kill": "Kill all Kirby :(",
        "made_by": "Made by Aken",
        "quote": "True freedom lies in the unhindered flow of ideas whether expressed through open code or spoken words, both are essential languages of human thought that belong to all of humanity.",
        "settings_title": "SETTINGS",
        "settings_sub": "Additional configuration and options",
        "opt_retro": "Full retro mode (BETA)",
        "opt_bsod": "BSOD mode",
        "opt_destroy": "Destroy mode",
        "opt_dislike": "I don't like this software",
        "themes": {"Dark": "Dark", "Light": "Light"},
        "modes": {"Modern": "Modern", "Retro": "Retro"}
    },
    "Italian": {
        "code": "it",
        "lang_label": "Lingua",
        "theme_label": "Tema",
        "title": ORIGINAL_TITLE,
        "slider_label": "Quanti Kirby vuoi?",
        "rand_header": "Randomizzatore",
        "rand_btn": "Randomizza",
        "num_header": "Numero di Kirby",
        "mode_header": "Modalità Kirby",
        "btn_release": "Rilascia tutti i Kirby :)",
        "btn_release_confirm": "Sei davvero sicuro?",
        "btn_kill": "Elimina tutti i Kirby :(",
        "made_by": "Creato da Aken",
        "quote": "La vera libertà risiede nel flusso ininterrotto delle idee sia che siano espresse tramite codice aperto o parole parlate, entrambe sono linguaggi essenziali del pensiero umano che appartengono all'intera umanità.",
        "settings_title": "IMPOSTAZIONI",
        "settings_sub": "Configurazioni e opzioni aggiuntive",
        "opt_retro": "Modalità Full Retro (BETA)",
        "opt_bsod": "Modalità BSOD",
        "opt_destroy": "Modalità Destroy",
        "opt_dislike": "Non mi piace questo software",
        "themes": {"Dark": "Scuro", "Light": "Chiaro"},
        "modes": {"Modern": "Moderno", "Retro": "Retro"}
    },
    "Portuguese": {
        "code": "pt",
        "lang_label": "Idioma",
        "theme_label": "Tema",
        "title": ORIGINAL_TITLE,
        "slider_label": "Quantos Kirby você quer?",
        "rand_header": "Randomizador",
        "rand_btn": "Aleatório",
        "num_header": "Número de Kirby",
        "mode_header": "Modo Kirby",
        "btn_release": "Liberar todos os Kirby :)",
        "btn_release_confirm": "Você tem certeza?",
        "btn_kill": "Eliminar todos os Kirby :(",
        "made_by": "Feito por Aken",
        "quote": "A verdadeira liberdade reside no fluxo desimpedido de ideias quer expressas por código aberto ou palavras faladas, ambos são linguagens essenciais do pensamento humano que pertencem a toda a humanidade.",
        "settings_title": "CONFIGURAÇÕES",
        "settings_sub": "Configurações e opções adicionais",
        "opt_retro": "Modo Full Retro (BETA)",
        "opt_bsod": "Modo BSOD",
        "opt_destroy": "Modo Destroy",
        "opt_dislike": "Não gosto deste software",
        "themes": {"Dark": "Escuro", "Light": "Claro"},
        "modes": {"Modern": "Moderno", "Retro": "Retro"}
    },
    "Spanish": {
        "code": "es",
        "lang_label": "Idioma",
        "theme_label": "Tema",
        "title": ORIGINAL_TITLE,
        "slider_label": "¿Cuántos Kirby quieres?",
        "rand_header": "Aleatorio",
        "rand_btn": "Aleatorio",
        "num_header": "Número de Kirby",
        "mode_header": "Modo Kirby",
        "btn_release": "Liberar todos los Kirby :)",
        "btn_release_confirm": "¿Estás realmente seguro?",
        "btn_kill": "Eliminar todos los Kirby :(",
        "made_by": "Hecho por Aken",
        "quote": "La verdadera libertad reside en el flujo sin obstáculos de las ideas ya sea expresadas a través de código abierto o palabras habladas, ambos son lenguajes esenciales del pensamiento humano que pertenecen a toda la humanidad.",
        "settings_title": "AJUSTES",
        "settings_sub": "Configuraciones y opciones adicionales",
        "opt_retro": "Modo Full Retro (BETA)",
        "opt_bsod": "Modo BSOD",
        "opt_destroy": "Modo Destroy",
        "opt_dislike": "No me gusta este software",
        "themes": {"Dark": "Oscuro", "Light": "Claro"},
        "modes": {"Modern": "Moderno", "Retro": "Retro"}
    },
    "Japanese": {
        "code": "jp",
        "lang_label": "言語",
        "theme_label": "テーマ",
        "title": ORIGINAL_TITLE,
        "slider_label": "カービィは何体欲しいですか？",
        "rand_header": "ランダム",
        "rand_btn": "ランダム",
        "num_header": "カービィの数",
        "mode_header": "カービィモード",
        "btn_release": "すべてのカービィを解放 :)",
        "btn_release_confirm": "本当によろしいですか？",
        "btn_kill": "すべてのカービィを消去 :(",
        "made_by": "Aken によって作成",
        "quote": "真の自由はアイデアの自由な流れにあります オープンコードであれ言葉であれ、どちらも全人類に属する人間思考の不可欠な言語です。",
        "settings_title": "設定",
        "settings_sub": "追加の構成とオプション",
        "opt_retro": "フルレトロモード (BETA)",
        "opt_bsod": "BSODモード",
        "opt_destroy": "デストロイモード",
        "opt_dislike": "このソフトウェアが嫌い",
        "themes": {"Dark": "ダーク", "Light": "ライト"},
        "modes": {"Modern": "モダン", "Retro": "レトロ"}
    },
    "Korean": {
        "code": "kr",
        "lang_label": "언어",
        "theme_label": "테마",
        "title": ORIGINAL_TITLE,
        "slider_label": "얼마나 많은 커비를 원하십니까?",
        "rand_header": "랜덤",
        "rand_btn": "랜덤",
        "num_header": "커비 수",
        "mode_header": "커비 모드",
        "btn_release": "모든 커비 석방 :)",
        "btn_release_confirm": "정말로 확실합니까?",
        "btn_kill": "모든 커비 제거 :(",
        "made_by": "Aken 제작",
        "quote": "진정한 자유는 아이디어의 방해받지 않는 흐름에 있습니다 오픈 코드이든 말이든, 두 가지 모두 전 인류에 속하는 인간 사상의 필수 언어입니다.",
        "settings_title": "설정",
        "settings_sub": "추가 구성 및 옵션",
        "opt_retro": "풀 레트로 모드 (BETA)",
        "opt_bsod": "BSOD 모드",
        "opt_destroy": "파괴 모드",
        "opt_dislike": "이 소프트웨어가 마음에 들지 않습니다",
        "themes": {"Dark": "다크", "Light": "라이트"},
        "modes": {"Modern": "모던", "Retro": "레트로"}
    },
    "Chinese": {
        "code": "cn",
        "lang_label": "语言",
        "theme_label": "主题",
        "title": ORIGINAL_TITLE,
        "slider_label": "你想要多少个星之卡比？",
        "rand_header": "随机",
        "rand_btn": "随机化",
        "num_header": "卡比数量",
        "mode_header": "卡比模式",
        "btn_release": "释放所有卡比 :)",
        "btn_release_confirm": "你确定吗？",
        "btn_kill": "清除所有卡比 :(",
        "made_by": "由 Aken 制作",
        "quote": "真正的自由在于思想的无障碍流动 无论是通过开源代码还是口头言语表达，它们都是属于全人类的人类思想的必备语言。",
        "settings_title": "设置",
        "settings_sub": "其他配置和选项",
        "opt_retro": "全复古模式 (BETA)",
        "opt_bsod": "BSOD模式",
        "opt_destroy": "毁灭模式",
        "opt_dislike": "我不喜欢这个软件",
        "themes": {"Dark": "深色", "Light": "浅色"},
        "modes": {"Modern": "现代", "Retro": "复古"}
    }
}

KIRBY_MODES = ["Modern", "Retro"]
THEMES = ["Dark", "Light"]

class KirbyBomberApp:
    def __init__(self, root):
        self.root = root
        self.root.title(ORIGINAL_TITLE)
        
        self.width = 440
        self.height = 575
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.overrideredirect(True)

        self.aken_click_count = 0

        self.opt_full_retro = False
        self.opt_bsod = False
        self.opt_destroy = False
        self.opt_dislike = False
        
        self.toggle_anim_data = {}

        self.base_font = "Segoe UI"

        self.current_theme = "Dark"
        self.set_theme_colors()
        self.root.config(bg=self.BG_COLOR)

        self._offset_x = 0
        self._offset_y = 0

        self.current_language = "English"
        self.current_mode = "Modern"
        self.active_dropdown_type = None

        self.min_kirby = 1
        self.max_kirby = 500
        self.kirby_count = 50

        self.current_page = "home"
        self.animating = False

        self.release_confirmed = False
        self.release_timer_id = None
        self.opened_kirby_windows = []

        self.keep_images = []
        self.flag_images = {}
        self.theme_icons = {}
        self.kb_base_img = None
        self.thumb_cache = {}
        self.dropdown_canvas = None
        self.cached_spawn_photo = None

        self.generate_theme_icons()
        self.download_flags()
        self.setup_ui()
        self.center_window()
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        enable_native_rounded_corners(self.root)
        self.root.bind("<Map>", self.on_restore)
        self.root.bind_all("<Button-1>", self.on_global_click_handler)
        self.update_fonts()

    def process_retro_pil_image(self, img):
        if not self.opt_full_retro:
            return img
        w, h = img.size
        small_w, small_h = max(8, w // 4), max(8, h // 4)
        pixelated = img.resize((small_w, small_h), Image.Resampling.NEAREST).resize((w, h), Image.Resampling.NEAREST)
        return pixelated.filter(ImageFilter.GaussianBlur(radius=0.5))

    def get_current_font(self, size, weight="normal", italic=False):
        fnt = self.base_font
        if self.opt_full_retro:
            fnt = "Courier New"
        
        style = weight
        if italic:
            style += " italic"
            
        return (fnt, size, style.strip())

    def update_fonts(self):
        self.lbl_version.config(font=self.get_current_font(8, "bold"))
        self.lbl_github.config(font=self.get_current_font(8, "bold"))
        self.btn_close.config(font=self.get_current_font(11, "bold"))
        self.lbl_title.config(font=self.get_current_font(10, "bold"))
        
        self.lbl_lang_header.config(font=self.get_current_font(8, "bold"))
        self.btn_lang_lbl.config(font=self.get_current_font(8, "bold"))
        
        self.lbl_theme_header.config(font=self.get_current_font(8, "bold"))
        self.btn_theme_lbl.config(font=self.get_current_font(8, "bold"))
        
        self.lbl_slider_title.config(font=self.get_current_font(11, "bold"))
        
        self.lbl_num_header.config(font=self.get_current_font(8, "bold"))
        self.ent_kirby_num.config(font=self.get_current_font(9, "bold"))
        
        self.lbl_mode_header.config(font=self.get_current_font(8, "bold"))
        self.btn_mode_lbl.config(font=self.get_current_font(8, "bold"))
        
        self.lbl_rand_header.config(font=self.get_current_font(8, "bold"))
        self.btn_rand_lbl.config(font=self.get_current_font(8, "bold"))
        
        self.btn_release_lbl.config(font=self.get_current_font(8, "bold"))
        self.btn_kill_lbl.config(font=self.get_current_font(8, "bold"))
        
        self.lbl_made_by.config(font=self.get_current_font(8, "bold"))
        self.lbl_quote.config(font=self.get_current_font(8, italic=True))
        
        self.lbl_settings_title.config(font=self.get_current_font(14, "bold"))
        self.lbl_settings_sub.config(font=self.get_current_font(9))
        self.lbl_disclaimer.config(font=self.get_current_font(7, italic=True))
        
        self.lbl_opt_retro.config(font=self.get_current_font(10, "bold"))
        self.lbl_opt_bsod.config(font=self.get_current_font(10, "bold"))
        self.lbl_opt_destroy.config(font=self.get_current_font(10, "bold"))
        self.lbl_opt_dislike.config(font=self.get_current_font(10, "bold"))

    def set_theme_colors(self):
        if self.current_theme == "Dark":
            self.BG_COLOR = "#1A1A1A"
            self.BG_RGB = (26, 26, 26)
            self.TEXT_COLOR = "#ECECEC"
            self.SUBTEXT_COLOR = "#777777"
            self.BTN_BG = "#2A2A2A"
            self.BTN_HOVER = "#353535"
            self.BORDER_COLOR = "#444444"
            self.SLIDER_TRACK = "#333333"
            self.ICON_NORM = (119, 119, 119)
            self.ICON_HOVER = (221, 221, 221)
            self.CLOSE_FG = "#777777"
            self.LINE_COLOR = (100, 100, 100)
            self.SOLID_LINE_COLOR = "#333333"
        else:
            self.BG_COLOR = "#F5F5F7"
            self.BG_RGB = (245, 245, 247)
            self.TEXT_COLOR = "#1D1D1F"
            self.SUBTEXT_COLOR = "#666666"
            self.BTN_BG = "#E5E5EA"
            self.BTN_HOVER = "#D1D1D6"
            self.BORDER_COLOR = "#C7C7CC"
            self.SLIDER_TRACK = "#D1D1D6"
            self.ICON_NORM = (100, 100, 100)
            self.ICON_HOVER = (30, 30, 30)
            self.CLOSE_FG = "#555555"
            self.LINE_COLOR = (180, 180, 180)
            self.SOLID_LINE_COLOR = "#D1D1D6"

    def draw_ios_toggle_frame(self, canvas, progress):
        canvas.delete("all")
        
        bg_off_rgb = (57, 57, 61) if self.current_theme == "Dark" else (233, 233, 234)
        bg_on_rgb = (52, 199, 89)
        
        r = int(bg_off_rgb[0] + (bg_on_rgb[0] - bg_off_rgb[0]) * progress)
        g = int(bg_off_rgb[1] + (bg_on_rgb[1] - bg_off_rgb[1]) * progress)
        b = int(bg_off_rgb[2] + (bg_on_rgb[2] - bg_off_rgb[2]) * progress)
        current_bg = f"#{r:02x}{g:02x}{b:02x}"
        
        knob_color = "#FFFFFF"
        
        h = 26
        w = 50
        r_pill = h / 2
        canvas.create_oval(0, 0, h, h, fill=current_bg, outline=current_bg)
        canvas.create_oval(w - h, 0, w, h, fill=current_bg, outline=current_bg)
        canvas.create_rectangle(r_pill, 0, w - r_pill, h, fill=current_bg, outline=current_bg)
        
        padding = 2
        knob_s = h - (padding * 2)
        travel = w - h
        circle_x = padding + (travel * progress)
        canvas.create_oval(circle_x, padding, circle_x + knob_s, padding + knob_s, fill=knob_color, outline=knob_color)

    def animate_toggle(self, canvas, target_state):
        c_id = id(canvas)
        if c_id not in self.toggle_anim_data:
            self.toggle_anim_data[c_id] = 1.0 if target_state else 0.0

        current_p = self.toggle_anim_data[c_id]
        target_p = 1.0 if target_state else 0.0

        if abs(current_p - target_p) < 0.01:
            self.toggle_anim_data[c_id] = target_p
            self.draw_ios_toggle_frame(canvas, target_p)
            return

        new_p = current_p + (target_p - current_p) * 0.2
        self.toggle_anim_data[c_id] = new_p
        self.draw_ios_toggle_frame(canvas, new_p)
        self.root.after(12, lambda: self.animate_toggle(canvas, target_state))

    def toggle_retro(self, event=None):
        self.opt_full_retro = not self.opt_full_retro
        self.animate_toggle(self.canvas_opt_retro, self.opt_full_retro)
        if self.opt_full_retro:
            self.select_mode("Retro")
        else:
            self.select_mode("Modern")
        self.update_fonts()
        self.update_ui_theme()

    def toggle_bsod(self, event=None):
        self.opt_bsod = not self.opt_bsod
        self.animate_toggle(self.canvas_opt_bsod, self.opt_bsod)
        if self.opt_bsod:
            self.bsod_frame.lift()
        else:
            self.bsod_frame.lower()

    def toggle_destroy(self, event=None):
        self.opt_destroy = not self.opt_destroy
        self.animate_toggle(self.canvas_opt_destroy, self.opt_destroy)
        if self.opt_destroy:
            self.max_kirby = 10000
        else:
            self.max_kirby = 500
            if self.kirby_count > 500:
                self.kirby_count = 500
        self.draw_custom_slider()

    def toggle_dislike(self, event=None):
        self.opt_dislike = not self.opt_dislike
        self.animate_toggle(self.canvas_opt_dislike, self.opt_dislike)
        if self.opt_dislike:
            self.show_system32_error_dialog()

    def show_system32_error_dialog(self):
        err_win = tk.Toplevel(self.root)
        err_win.title("System Error")
        err_win.geometry("380x150")
        err_win.resizable(False, False)
        err_win.attributes("-topmost", True)
        
        bg_color = "#202020" if self.current_theme == "Dark" else "#F0F0F0"
        fg_color = "#FFFFFF" if self.current_theme == "Dark" else "#000000"
        err_win.config(bg=bg_color)
        
        enable_native_rounded_corners(err_win)
        
        frame_main = tk.Frame(err_win, bg=bg_color)
        frame_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        lbl_icon = tk.Label(frame_main, text="❌", font=("Segoe UI", 28), bg=bg_color)
        lbl_icon.pack(side=tk.LEFT, padx=(0, 15))
        
        lbl_msg = tk.Label(
            frame_main, 
            text="I'm deleting all system32, fuck you.", 
            font=("Segoe UI", 10, "bold"), 
            bg=bg_color, 
            fg=fg_color,
            wraplength=260,
            justify="left"
        )
        lbl_msg.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        btn_ok = tk.Button(
            err_win, 
            text="OK", 
            width=10, 
            command=lambda: (err_win.destroy(), self.toggle_dislike()),
            bg="#0078D4", 
            fg="#FFFFFF", 
            bd=0, 
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        )
        btn_ok.pack(side=tk.BOTTOM, pady=(0, 15))

        err_win.update_idletasks()
        sw = err_win.winfo_screenwidth()
        sh = err_win.winfo_screenheight()
        ew = err_win.winfo_width()
        eh = err_win.winfo_height()
        err_win.geometry(f"+{int((sw - ew) / 2)}+{int((sh - eh) / 2)}")

    def on_aken_click(self, event=None):
        self.aken_click_count += 1
        if self.aken_click_count >= 10:
            self.aken_click_count = 0
            self.open_keasteregg_window()

    def on_global_click_handler(self, event):
        if event.widget != self.lbl_made_by:
            self.aken_click_count = 0
        self.on_global_click(event)

    def open_keasteregg_window(self):
        img_path = resource_path(os.path.join("images", "keasteregg.jpg"))
        if not os.path.exists(img_path):
            print("Immagine keasteregg.jpg non trovata!")
            return

        try:
            top = tk.Toplevel(self.root)
            top.overrideredirect(True)
            top.attributes("-topmost", True)
            
            sw = top.winfo_screenwidth()
            sh = top.winfo_screenheight()
            top.geometry(f"{sw}x{sh}+0+0")
            
            egg_img = Image.open(img_path)
            egg_img = egg_img.resize((sw, sh), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(egg_img)
            lbl = tk.Label(top, image=photo, bg="#000000", cursor="hand2")
            lbl.pack(fill=tk.BOTH, expand=True)
            lbl.image = photo
            
            close_action = lambda e=None: top.destroy()
            lbl.bind("<Button-1>", close_action)
            top.bind("<Escape>", close_action)
        except Exception as e:
            print(f"Errore caricamento keasteregg.jpg: {e}")

    def generate_theme_icons(self):
        scale = 4
        size = 16
        s = size * scale
        img_moon = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_moon)
        draw.ellipse([s*0.1, s*0.1, s*0.9, s*0.9], fill=(240, 230, 140, 255))
        draw.ellipse([s*0.3, s*0.05, s*0.98, s*0.85], fill=(0, 0, 0, 0))
        
        moon_proc = self.process_retro_pil_image(img_moon)
        self.theme_icons["Dark"] = ImageTk.PhotoImage(moon_proc.resize((size, size), Image.Resampling.LANCZOS))

        img_sun = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_sun)
        cx, cy = s / 2, s / 2
        r_sun = s * 0.25
        for i in range(8):
            angle = i * (math.pi / 4)
            x1 = cx + (r_sun + s*0.08) * math.cos(angle)
            y1 = cy + (r_sun + s*0.08) * math.sin(angle)
            x2 = cx + (r_sun + s*0.22) * math.cos(angle)
            y2 = cy + (r_sun + s*0.22) * math.sin(angle)
            draw.line([(x1, y1), (x2, y2)], fill=(255, 165, 0, 255), width=int(s*0.08))
        draw.ellipse([cx - r_sun, cy - r_sun, cx + r_sun, cy + r_sun], fill=(255, 204, 0, 255), outline=(255, 140, 0, 255), width=int(s*0.04))
        
        sun_proc = self.process_retro_pil_image(img_sun)
        self.theme_icons["Light"] = ImageTk.PhotoImage(sun_proc.resize((size, size), Image.Resampling.LANCZOS))
        
        self.keep_images.extend([self.theme_icons["Dark"], self.theme_icons["Light"]])

    def draw_fade_line_on_canvas(self, canvas, width, height, line_color, bg_color):
        canvas.delete("all")
        canvas.config(bg=self.BG_COLOR)
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        r, g, b = line_color
        br, bg_c, bb = bg_color
        for x in range(width):
            dist = abs(x - (width / 2)) / (width / 2)
            alpha = max(0.0, min(1.0, 1.0 - dist ** 2))
            pr = int(r * alpha + br * (1.0 - alpha))
            pg = int(g * alpha + bg_c * (1.0 - alpha))
            pb = int(b * alpha + bb * (1.0 - alpha))
            for y in range(height):
                draw.point((x, y), fill=(pr, pg, pb))
        photo = ImageTk.PhotoImage(img)
        self.keep_images.append(photo)
        canvas.create_image(width // 2, height // 2, image=photo, anchor=tk.CENTER)

    def update_ui_theme(self):
        self.generate_theme_icons()
        self.set_theme_colors()
        self.root.config(bg=self.BG_COLOR)
        self.lbl_blur_overlay.config(bg=self.BG_COLOR)
        self.title_bar.config(bg=self.BG_COLOR)
        self.left_info_frame.config(bg=self.BG_COLOR)
        self.lbl_version.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.lbl_github.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.btns_frame.config(bg=self.BG_COLOR)
        self.gear_icon_norm = self.draw_simple_gear_icon(size=16, color=self.ICON_NORM)
        self.gear_icon_hover = self.draw_simple_gear_icon(size=16, color=self.ICON_HOVER)
        self.btn_opts.config(image=self.gear_icon_norm, bg=self.BG_COLOR)
        self.btn_back_large.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR, activebackground=self.BG_COLOR)
        self.btn_min_canvas.config(bg=self.BG_COLOR)
        self.btn_min_canvas.itemconfig(self.min_line, fill="#777777" if self.current_theme == "Dark" else "#555555")
        self.btn_close.config(bg=self.BG_COLOR, fg=self.CLOSE_FG)
        self.lbl_title.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.draw_fade_line_on_canvas(self.divider_top, 400, 2, self.LINE_COLOR, self.BG_RGB)
        self.viewport.config(bg=self.BG_COLOR)
        self.home_frame.config(bg=self.BG_COLOR)
        self.settings_frame.config(bg=self.BG_COLOR)
        self.content_frame.config(bg=self.BG_COLOR)
        self.lang_container.config(bg=self.BG_COLOR)
        self.lbl_lang_header.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.btn_lang_canvas.config(bg=self.BG_COLOR)
        self.theme_container.config(bg=self.BG_COLOR)
        self.lbl_theme_header.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.btn_theme_canvas.config(bg=self.BG_COLOR)
        if hasattr(self, 'lbl_kb_img'):
            self.lbl_kb_img.config(bg=self.BG_COLOR)
        self.draw_fade_line_on_canvas(self.divider_mid, 360, 2, self.LINE_COLOR, self.BG_RGB)
        self.slider_frame.config(bg=self.BG_COLOR)
        self.lbl_slider_title.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.slider_canvas.config(bg=self.BG_COLOR)
        self.bottom_controls.config(bg=self.BG_COLOR)
        self.left_box.config(bg=self.BG_COLOR)
        self.lbl_num_header.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.num_canvas.config(bg=self.BG_COLOR)
        self.ent_kirby_num.config(bg=self.BTN_BG, insertbackground=self.TEXT_COLOR)
        self.right_box.config(bg=self.BG_COLOR)
        self.lbl_mode_header.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.btn_mode_canvas.config(bg=self.BG_COLOR)
        self.center_box.config(bg=self.BG_COLOR)
        self.lbl_rand_header.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.btn_rand_canvas.config(bg=self.BG_COLOR)
        self.draw_fade_line_on_canvas(self.divider_bottom, 360, 2, self.LINE_COLOR, self.BG_RGB)
        self.draw_fade_line_on_canvas(self.divider_footer, 360, 2, self.LINE_COLOR, self.BG_RGB)
        self.action_buttons_frame.config(bg=self.BG_COLOR)
        self.btn_release_canvas.config(bg=self.BG_COLOR)
        self.btn_kill_canvas.config(bg=self.BG_COLOR)
        self.footer_frame.config(bg=self.BG_COLOR)
        self.lbl_made_by.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.short_solid_line.config(bg=self.BG_COLOR)
        self.short_solid_line.itemconfig(self.solid_line_id, fill=self.SOLID_LINE_COLOR)
        self.lbl_quote.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)

        fill_col = (42, 42, 42) if self.current_theme == "Dark" else (229, 229, 234)
        outline_col = (68, 68, 68) if self.current_theme == "Dark" else (199, 199, 204)
        fill_hov = (53, 53, 53) if self.current_theme == "Dark" else (209, 209, 214)
        outline_hov = (90, 90, 90) if self.current_theme == "Dark" else (180, 180, 184)
        self.bg_box_norm = self.create_rounded_rect_image(115, 32, radius=8, fill_color=fill_col, outline_color=outline_col)
        self.bg_box_hover = self.create_rounded_rect_image(115, 32, radius=8, fill_color=fill_hov, outline_color=outline_hov)
        text_fg = "#DDDDDD" if self.current_theme == "Dark" else "#1D1D1F"

        self.btn_lang_canvas.itemconfig(self.lang_bg_img_id, image=self.bg_box_norm)
        self.btn_lang_lbl.config(bg=self.BTN_BG, fg=text_fg)
        
        self.btn_theme_canvas.itemconfig(self.theme_bg_img_id, image=self.bg_box_norm)
        self.btn_theme_lbl.config(bg=self.BTN_BG, fg=text_fg, image=self.theme_icons.get(self.current_theme))
        
        self.num_canvas.itemconfig(self.num_bg_img_id, image=self.bg_box_norm)
        self.btn_mode_canvas.itemconfig(self.mode_bg_img_id, image=self.bg_box_norm)
        self.btn_mode_lbl.config(bg=self.BTN_BG, fg=text_fg)
        
        self.dice_icon = self.draw_dice_icon(size=14)
        self.btn_rand_canvas.itemconfig(self.rand_bg_img_id, image=self.bg_box_norm)
        self.btn_rand_lbl.config(bg=self.BTN_BG, fg=text_fg, image=self.dice_icon)

        self.lbl_settings_title.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_settings_sub.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.lbl_disclaimer.config(bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.opt_frame.config(bg=self.BG_COLOR)
        self.opt_row1.config(bg=self.BG_COLOR)
        self.opt_row2.config(bg=self.BG_COLOR)
        self.opt_row3.config(bg=self.BG_COLOR)
        self.opt_row4.config(bg=self.BG_COLOR)
        self.lbl_opt_retro.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_opt_bsod.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_opt_destroy.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_opt_dislike.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.canvas_opt_retro.config(bg=self.BG_COLOR)
        self.canvas_opt_bsod.config(bg=self.BG_COLOR)
        self.canvas_opt_destroy.config(bg=self.BG_COLOR)
        self.canvas_opt_dislike.config(bg=self.BG_COLOR)
        
        self.draw_ios_toggle_frame(self.canvas_opt_retro, 1.0 if self.opt_full_retro else 0.0)
        self.draw_ios_toggle_frame(self.canvas_opt_bsod, 1.0 if self.opt_bsod else 0.0)
        self.draw_ios_toggle_frame(self.canvas_opt_destroy, 1.0 if self.opt_destroy else 0.0)
        self.draw_ios_toggle_frame(self.canvas_opt_dislike, 1.0 if self.opt_dislike else 0.0)
        self.draw_custom_slider()

    def start_move(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self._offset_x
        y = self.root.winfo_y() + event.y - self._offset_y
        self.root.geometry(f"+{x}+{y}")

    def get_color_for_fraction(self, fraction):
        hue = 0.6 * (1.0 - fraction)
        r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 0.95)
        r_int, g_int, b_int = int(r * 255), int(g * 255), int(b * 255)
        hex_color = f"#{r_int:02x}{g_int:02x}{b_int:02x}"
        return (r_int, g_int, b_int), hex_color

    def generate_dynamic_circle(self, diameter=16, fill_color=(0, 120, 212)):
        scale = 4
        d = diameter * scale
        img = Image.new("RGBA", (d, d), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        border_width = 2 * scale
        r, g, b = fill_color
        outline_color = (min(255, int(r * 1.2)), min(255, int(g * 1.2)), min(255, int(b * 1.2)))
        draw.ellipse([border_width, border_width, d - border_width, d - border_width], 
                     fill=fill_color + (255,), outline=outline_color + (255,), width=border_width)
        return ImageTk.PhotoImage(img.resize((diameter, diameter), Image.Resampling.LANCZOS))

    def create_rounded_rect_image(self, width, height, radius=8, fill_color=(42, 42, 42), outline_color=(68, 68, 68)):
        scale = 4
        sw, sh = width * scale, height * scale
        sr = radius * scale
        img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([scale, scale, sw - scale, sh - scale], radius=sr, fill=fill_color + (255,), outline=outline_color + (255,), width=scale)
        photo = ImageTk.PhotoImage(img.resize((width, height), Image.Resampling.LANCZOS))
        self.keep_images.append(photo)
        return photo

    def download_flags(self):
        flags_dir = resource_path(os.path.join("images", "flags"))
        if not os.path.exists(flags_dir):
            try:
                os.makedirs(flags_dir)
            except Exception:
                pass
        headers = {'User-Agent': 'Mozilla/5.0'}
        for lang, data in TRANSLATIONS.items():
            code = data["code"]
            filepath = resource_path(os.path.join("images", "flags", f"{code}.png"))
            if not os.path.exists(filepath):
                try:
                    url = f"https://flagcdn.com/w40/{code}.png"
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                        out_file.write(response.read())
                except Exception:
                    pass

    def get_flag_image(self, code):
        filepath = resource_path(os.path.join("images", "flags", f"{code}.png"))
        if os.path.exists(filepath):
            try:
                img = Image.open(filepath).resize((18, 12), Image.Resampling.LANCZOS)
                img = self.process_retro_pil_image(img)
                photo = ImageTk.PhotoImage(img)
                self.keep_images.append(photo)
                return photo
            except Exception:
                pass
        return None

    def quit_app(self):
        self.close_all_kirby_photos()
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

    def draw_simple_gear_icon(self, size=16, color=(119, 119, 119)):
        scale = 4
        s = size * scale
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = s / 2, s / 2
        r_outer = s * 0.4
        r_inner = s * 0.25
        r_hole = s * 0.12
        teeth = 8
        for i in range(teeth):
            angle = i * (2 * math.pi / teeth)
            x_out = cx + r_outer * math.cos(angle)
            y_out = cy + r_outer * math.sin(angle)
            draw.line([(cx, cy), (x_out, y_out)], fill=color + (255,), width=int(s * 0.2))
        draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=color + (255,))
        draw.ellipse([cx - r_hole, cy - r_hole, cx + r_hole, cy + r_hole], fill=(0, 0, 0, 0))
        photo = ImageTk.PhotoImage(img.resize((size, size), Image.Resampling.LANCZOS))
        self.keep_images.append(photo)
        return photo

    def draw_dice_icon(self, size=16):
        scale = 4
        s = size * scale
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([s * 0.1, s * 0.1, s * 0.9, s * 0.9], radius=s * 0.2, fill=(240, 240, 240, 255), outline=(180, 180, 180, 255), width=int(s*0.06))
        dot_r = s * 0.09
        for dx, dy in [(s * 0.3, s * 0.3), (s * 0.7, s * 0.3), (s * 0.5, s * 0.5), (s * 0.3, s * 0.7), (s * 0.7, s * 0.7)]:
            draw.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r], fill=(220, 50, 50, 255))
        
        img = self.process_retro_pil_image(img)
        photo = ImageTk.PhotoImage(img.resize((size, size), Image.Resampling.LANCZOS))
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

    def open_options(self, event=None):
        if self.current_page == "settings" or self.animating:
            return
        self.animating = True
        self.close_all_dropdowns()
        self.current_page = "settings"
        self.settings_frame.lift()
        self.home_frame.place(x=0, y=0, width=self.width, height=self.height - 54)
        self.settings_frame.place(x=self.width, y=0, width=self.width, height=self.height - 54)
        self.animate_transition_step(0, self.width, -self.width, 0)

    def go_back_home(self, event=None):
        if self.current_page == "home" or self.animating:
            return
        self.animating = True
        self.close_all_dropdowns()
        self.current_page = "home"
        self.home_frame.lift()
        self.bsod_frame.lift() if self.opt_bsod else self.bsod_frame.lower()
        self.home_frame.place(x=-self.width, y=0, width=self.width, height=self.height - 54)
        self.settings_frame.place(x=0, y=0, width=self.width, height=self.height - 54)
        self.animate_transition_step(-self.width, 0, 0, self.width)

    def animate_transition_step(self, curr_home_x, curr_settings_x, target_home_x, target_settings_x):
        dist_home = target_home_x - curr_home_x
        dist_settings = target_settings_x - curr_settings_x
        if abs(dist_home) < 1.0 and abs(dist_settings) < 1.0:
            self.home_frame.place(x=target_home_x, y=0, width=self.width, height=self.height - 54)
            self.settings_frame.place(x=target_settings_x, y=0, width=self.width, height=self.height - 54)
            self.animating = False
            return
        new_home_x = curr_home_x + (dist_home * 0.3)
        new_settings_x = curr_settings_x + (dist_settings * 0.3)
        self.home_frame.place(x=int(new_home_x), y=0, width=self.width, height=self.height - 54)
        self.settings_frame.place(x=int(new_settings_x), y=0, width=self.width, height=self.height - 54)
        self.root.after(16, lambda: self.animate_transition_step(new_home_x, new_settings_x, target_home_x, target_settings_x))

    def open_github(self):
        webbrowser.open("https://github.com/Ak3nyke")

    def align_title_center(self, event=None):
        self.root.update_idletasks()
        left_width = self.left_info_frame.winfo_reqwidth()
        right_width = self.btns_frame.winfo_reqwidth()
        left_edge = 22 + left_width
        right_edge = self.width - 18 - right_width
        center_x = left_edge + (right_edge - left_edge) / 2
        self.lbl_title.place(x=center_x, rely=0.5, anchor=tk.CENTER)

    def draw_custom_slider(self):
        self.slider_canvas.delete("all")
        self.slider_canvas.config(bg=self.BG_COLOR)
        w = 360
        h = 30
        margin = 12
        usable_w = w - (2 * margin)
        fraction = (self.kirby_count - self.min_kirby) / float(self.max_kirby - self.min_kirby)
        fraction = max(0.0, min(1.0, fraction))
        thumb_x = margin + fraction * usable_w
        cy = h / 2
        rgb, hex_color = self.get_color_for_fraction(fraction)
        self.slider_canvas.create_line(margin, cy, margin + usable_w, cy, fill=self.SLIDER_TRACK, width=3, capstyle="round")
        if thumb_x > margin:
            self.slider_canvas.create_line(margin, cy, thumb_x, cy, fill=hex_color, width=3, capstyle="round")
        if hex_color not in self.thumb_cache:
            self.thumb_cache[hex_color] = self.generate_dynamic_circle(diameter=16, fill_color=rgb)
        self.slider_canvas.create_image(thumb_x, cy, image=self.thumb_cache[hex_color], anchor=tk.CENTER)
        if hasattr(self, 'ent_kirby_num'):
            self.ent_kirby_num.config(fg=hex_color)
            self.ent_kirby_num.delete(0, tk.END)
            self.ent_kirby_num.insert(0, str(self.kirby_count))

    def on_slider_click(self, event):
        self.update_slider_val(event.x)

    def on_slider_drag(self, event):
        self.update_slider_val(event.x)

    def update_slider_val(self, click_x):
        w = 360
        margin = 12
        usable_w = w - (2 * margin)
        clamped_x = max(margin, min(click_x, margin + usable_w))
        fraction = (clamped_x - margin) / usable_w
        self.kirby_count = int(self.min_kirby + round(fraction * (self.max_kirby - self.min_kirby)))
        self.draw_custom_slider()

    def on_number_input_change(self, event=None):
        try:
            val = int(self.ent_kirby_num.get())
            val = max(self.min_kirby, min(self.max_kirby, val))
            self.kirby_count = val
        except ValueError:
            pass
        self.draw_custom_slider()

    def apply_blur_overlay(self, active_dropdown):
        self.root.update_idletasks()
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h), all_screens=True).convert("RGBA")
        except Exception:
            screenshot = Image.new("RGBA", (w, h), (26, 26, 26, 255) if self.current_theme=="Dark" else (245, 245, 247, 255))

        blurred = screenshot.filter(ImageFilter.GaussianBlur(radius=8))
        enhancer = ImageEnhance.Brightness(blurred)
        factor = 0.65 if self.current_theme == "Dark" else 0.85
        self.blurred_dark = enhancer.enhance(factor).convert("RGBA")

        if active_dropdown == "language":
            widgets_to_reveal = [(self.lbl_lang_header, 6), (self.btn_lang_canvas, 8)]
        elif active_dropdown == "theme":
            widgets_to_reveal = [(self.lbl_theme_header, 6), (self.btn_theme_canvas, 8)]
        else:
            widgets_to_reveal = [(self.lbl_mode_header, 6), (self.btn_mode_canvas, 8)]

        for wdg, radius in widgets_to_reveal:
            if not wdg or not wdg.winfo_viewable(): continue
            wx = wdg.winfo_rootx() - x
            wy = wdg.winfo_rooty() - y
            ww = wdg.winfo_width()
            wh = wdg.winfo_height()
            if ww <= 0 or wh <= 0: continue
            try:
                crop = screenshot.crop((wx, wy, wx + ww, wy + wh)).convert("RGBA")
                if radius:
                    scale = 4
                    mask = Image.new("L", (ww * scale, wh * scale), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.rounded_rectangle([scale, scale, ww * scale - scale, wh * scale - scale], radius=radius * scale, fill=255)
                    self.blurred_dark.paste(crop, (wx, wy), mask.resize((ww, wh), Image.Resampling.LANCZOS))
                else:
                    self.blurred_dark.paste(crop, (wx, wy))
            except Exception:
                pass

        self.blur_tk_img = ImageTk.PhotoImage(self.blurred_dark)
        self.lbl_blur_overlay.config(image=self.blur_tk_img)
        self.lbl_blur_overlay.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        tk.Widget.tkraise(self.lbl_blur_overlay)

    def remove_blur_overlay(self):
        self.lbl_blur_overlay.place_forget()

    def show_dropdown(self, dropdown_type):
        self.active_dropdown_type = dropdown_type
        lang_data = TRANSLATIONS[self.current_language]

        if dropdown_type == "language":
            items = [(lang, f"  {lang}", self.flag_images.get(lang)) for lang in TRANSLATIONS.keys()]
            target_canvas = self.btn_lang_canvas
        elif dropdown_type == "theme":
            items = [(thm, f"  {lang_data['themes'][thm]}", self.theme_icons.get(thm)) for thm in THEMES]
            target_canvas = self.btn_theme_canvas
        else:
            items = [(mode, f"  {lang_data['modes'][mode]}", None) for mode in KIRBY_MODES]
            target_canvas = self.btn_mode_canvas

        width = 115
        box_x = target_canvas.winfo_rootx() - self.root.winfo_rootx()
        x = int(box_x + (target_canvas.winfo_width() / 2) - (width / 2))
        y = target_canvas.winfo_rooty() - self.root.winfo_rooty() + target_canvas.winfo_height()
        item_h, pad_y = 32, 6
        height = len(items) * item_h + pad_y * 2
        img_w, img_h = self.blurred_dark.size
        crop = self.blurred_dark.crop((max(0, x), max(0, y), min(x + width, img_w), min(y + height, img_h))).convert("RGBA")
        
        scale, sr = 4, 8 * 4
        mask = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
        bg_fill = (37, 37, 37, 255) if self.current_theme == "Dark" else (240, 240, 245, 255)
        border_outline = (68, 68, 68, 255) if self.current_theme == "Dark" else (199, 199, 204, 255)
        ImageDraw.Draw(mask).rounded_rectangle([scale, scale, width * scale - scale, height * scale - scale], radius=sr, fill=bg_fill, outline=border_outline, width=scale)
        self.dd_bg_img = ImageTk.PhotoImage(Image.alpha_composite(crop, mask.resize((width, height), Image.Resampling.LANCZOS)))

        self.dropdown_canvas = tk.Canvas(self.root, width=width, height=height, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.dropdown_canvas.create_image(0, 0, image=self.dd_bg_img, anchor=tk.NW)

        hov_fill = (80, 80, 80) if self.current_theme == "Dark" else (210, 210, 215)
        self.hover_img = self.create_rounded_rect_image(width - 12, item_h, radius=6, fill_color=hov_fill, outline_color=hov_fill)
        self.hover_canvas_img = self.dropdown_canvas.create_image(6, -100, image=self.hover_img, anchor=tk.NW)

        text_color = "#DDDDDD" if self.current_theme == "Dark" else "#1D1D1F"
        self.dropdown_items_data = []
        for i, item in enumerate(items):
            iy = pad_y + i * item_h
            if item[2]:
                self.dropdown_canvas.create_image(12, iy + item_h // 2, image=item[2], anchor=tk.W)
                self.dropdown_canvas.create_text(36, iy + item_h // 2, text=item[1], fill=text_color, font=self.get_current_font(8, "bold"), anchor=tk.W)
            else:
                self.dropdown_canvas.create_text(width // 2, iy + item_h // 2, text=item[1], fill=text_color, font=self.get_current_font(8, "bold"), anchor=tk.CENTER)
            self.dropdown_items_data.append({"id": item[0], "y1": iy, "y2": iy + item_h})

        self.dropdown_canvas.place(x=x, y=y)
        tk.Widget.tkraise(self.dropdown_canvas)
        self.dropdown_canvas.bind("<Motion>", self.on_dropdown_hover)
        self.dropdown_canvas.bind("<Button-1>", self.on_dropdown_click)

    def on_dropdown_hover(self, e):
        for data in self.dropdown_items_data:
            if data["y1"] <= e.y <= data["y2"]:
                self.dropdown_canvas.coords(self.hover_canvas_img, 6, data["y1"])
                return
        self.dropdown_canvas.coords(self.hover_canvas_img, 6, -100)

    def on_dropdown_click(self, event):
        for data in self.dropdown_items_data:
            if data["y1"] <= event.y <= data["y2"]:
                if self.active_dropdown_type == "language": self.select_language(data["id"])
                elif self.active_dropdown_type == "theme": self.select_theme(data["id"])
                elif self.active_dropdown_type == "mode": self.select_mode(data["id"])
                return

    def toggle_language_dropdown(self, event=None):
        if self.active_dropdown_type == "language": self.close_all_dropdowns()
        else: self.close_all_dropdowns(); self.apply_blur_overlay("language"); self.show_dropdown("language")

    def toggle_theme_dropdown(self, event=None):
        if self.active_dropdown_type == "theme": self.close_all_dropdowns()
        else: self.close_all_dropdowns(); self.apply_blur_overlay("theme"); self.show_dropdown("theme")

    def toggle_mode_dropdown(self, event=None):
        if self.active_dropdown_type == "mode": self.close_all_dropdowns()
        else: self.close_all_dropdowns(); self.apply_blur_overlay("mode"); self.show_dropdown("mode")

    def on_randomize_click(self, event=None):
        self.kirby_count = random.randint(self.min_kirby, self.max_kirby)
        self.draw_custom_slider()

    def reset_release_button(self):
        self.release_confirmed = False
        self.btn_release_canvas.itemconfig(self.release_bg_id, image=self.bg_green_norm)
        self.btn_release_lbl.config(text=TRANSLATIONS[self.current_language]["btn_release"], bg="#28A745")

    def on_release_kirby(self, event=None):
        if not self.release_confirmed:
            self.release_confirmed = True
            self.btn_release_canvas.itemconfig(self.release_bg_id, image=self.bg_orange_norm)
            self.btn_release_lbl.config(text=TRANSLATIONS[self.current_language]["btn_release_confirm"], bg="#FD7E14")
            if self.release_timer_id: self.root.after_cancel(self.release_timer_id)
            self.release_timer_id = self.root.after(4000, self.reset_release_button)
        else:
            if self.release_timer_id: self.root.after_cancel(self.release_timer_id)
            self.reset_release_button()
            self.spawn_kirby_photos()

    def spawn_kirby_photos(self, remaining=None):
        if remaining is None:
            remaining = self.kirby_count
            self.cached_spawn_photo = None

        if self.cached_spawn_photo is None:
            img_name = "kirbybomb.png" if self.current_mode == "Modern" else "kirbyretro.png"
            img_path = resource_path(os.path.join("images", img_name))
            if not os.path.exists(img_path):
                print(f"Immagine {img_name} non trovata!")
                return
            try:
                pil_img = Image.open(img_path)
            except Exception as e:
                print(f"Errore apertura {img_name}: {e}")
                return

            target_w, target_h = 160, int(160 * (pil_img.height / pil_img.width))

            if self.current_mode == "Modern" and not self.opt_full_retro:
                resized = pil_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            else:
                small_pixel_size = 16 if self.opt_full_retro else 32
                pixel_img = pil_img.resize((small_pixel_size, int(small_pixel_size * (pil_img.height / pil_img.width))), Image.Resampling.BILINEAR)
                resized = pixel_img.resize((target_w, target_h), Image.Resampling.NEAREST)

            resized = self.process_retro_pil_image(resized)
            self.cached_spawn_photo = ImageTk.PhotoImage(resized)

        screen_w, screen_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        target_w, target_h = 160, self.cached_spawn_photo.height()

        batch_size = min(100, remaining)
        for _ in range(batch_size):
            win = tk.Toplevel(self.root)
            win.overrideredirect(True)
            win.attributes("-topmost", True)
            win.geometry(f"{target_w}x{target_h}+{random.randint(0, max(0, screen_w - target_w))}+{random.randint(0, max(0, screen_h - target_h))}")
            lbl = tk.Label(win, image=self.cached_spawn_photo, bg="#000001")
            lbl.pack(fill=tk.BOTH, expand=True)
            lbl.image = self.cached_spawn_photo
            try: win.wm_attributes("-transparentcolor", "#000001")
            except Exception: pass
            self.opened_kirby_windows.append(win)

        remaining -= batch_size
        if remaining > 0:
            self.root.after(1, lambda: self.spawn_kirby_photos(remaining))

    def on_kill_kirby(self, event=None):
        self.close_all_kirby_photos()

    def close_all_kirby_photos(self):
        for win in self.opened_kirby_windows:
            try: win.destroy()
            except Exception: pass
        self.opened_kirby_windows.clear()

    def select_language(self, lang_name):
        self.current_language = lang_name
        data = TRANSLATIONS[lang_name]
        
        flag_img = self.flag_images.get(lang_name)
        self.btn_lang_lbl.config(image=flag_img if flag_img else "", text=f"  {lang_name}  ▼" if flag_img else f"{lang_name}  ▼", compound="left")
        self.btn_theme_lbl.config(image=self.theme_icons.get(self.current_theme), text=f"  {data['themes'][self.current_theme]}  ▼", compound="left")
        self.btn_mode_lbl.config(text=f"{data['modes'][self.current_mode]}  ▼")

        self.lbl_lang_header.config(text=data['lang_label'])
        self.lbl_theme_header.config(text=data['theme_label'])
        self.lbl_title.config(text=data['title'])
        self.lbl_slider_title.config(text=data['slider_label'])
        self.lbl_rand_header.config(text=data['rand_header'])
        self.btn_rand_lbl.config(text=f"  {data['rand_btn']}")
        self.lbl_num_header.config(text=data['num_header'])
        self.lbl_mode_header.config(text=data['mode_header'])
        
        self.btn_release_lbl.config(text=data['btn_release'] if not self.release_confirmed else data['btn_release_confirm'])
        self.btn_kill_lbl.config(text=data['btn_kill'])
        self.lbl_made_by.config(text=data['made_by'])
        self.lbl_quote.config(text=data['quote'])

        self.lbl_settings_title.config(text=data['settings_title'])
        self.lbl_settings_sub.config(text=data['settings_sub'])
        self.lbl_opt_retro.config(text=data['opt_retro'])
        self.lbl_opt_bsod.config(text=data['opt_bsod'])
        self.lbl_opt_destroy.config(text=data['opt_destroy'])
        self.lbl_opt_dislike.config(text=data['opt_dislike'])

        self.align_title_center()
        self.close_all_dropdowns()

    def select_theme(self, theme_name):
        self.current_theme = theme_name
        self.btn_theme_lbl.config(image=self.theme_icons.get(theme_name), text=f"  {TRANSLATIONS[self.current_language]['themes'][theme_name]}  ▼", compound="left")
        self.update_ui_theme()
        self.close_all_dropdowns()

    def update_kirby_image(self):
        img_path = resource_path(os.path.join("images", "kbomb.png"))
        if os.path.exists(img_path):
            try: self.kb_base_img = Image.open(img_path)
            except Exception: return
        if not self.kb_base_img: return

        target_width = 130
        aspect_ratio = self.kb_base_img.height / self.kb_base_img.width
        target_height = int(target_width * aspect_ratio)

        if self.current_mode == "Modern" and not self.opt_full_retro:
            resized_img = self.kb_base_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        else:
            px_size = 18 if self.opt_full_retro else 36
            small_w, small_h = px_size, int(px_size * aspect_ratio)
            resized_img = self.kb_base_img.resize((small_w, small_h), Image.Resampling.BILINEAR).resize((target_width, target_height), Image.Resampling.NEAREST)

        resized_img = self.process_retro_pil_image(resized_img)

        self.kb_tk_img = ImageTk.PhotoImage(resized_img)
        self.lbl_kb_img.config(image=self.kb_tk_img)

        self.root.update_idletasks()
        line_y = self.lbl_kb_img.winfo_y() + self.lbl_kb_img.winfo_height() + 12
        self.divider_mid.place(relx=0.5, y=line_y, anchor=tk.N)
        self.slider_frame.place(relx=0.5, y=line_y + 18, anchor=tk.N)

    def select_mode(self, mode_name):
        self.current_mode = mode_name
        self.btn_mode_lbl.config(text=f"{TRANSLATIONS[self.current_language]['modes'][mode_name]}  ▼")
        self.update_kirby_image()
        self.close_all_dropdowns()

    def close_all_dropdowns(self):
        if hasattr(self, 'dropdown_canvas') and self.dropdown_canvas:
            self.dropdown_canvas.destroy()
            self.dropdown_canvas = None
        self.remove_blur_overlay()
        self.active_dropdown_type = None

    def on_global_click(self, event):
        if not self.active_dropdown_type: return
        widget = event.widget
        valid = []
        if self.active_dropdown_type == "language": valid = [self.btn_lang_canvas, self.btn_lang_lbl]
        elif self.active_dropdown_type == "theme": valid = [self.btn_theme_canvas, self.btn_theme_lbl]
        elif self.active_dropdown_type == "mode": valid = [self.btn_mode_canvas, self.btn_mode_lbl]
        if self.dropdown_canvas: valid.append(self.dropdown_canvas)
        if widget not in valid: self.close_all_dropdowns()

    def setup_ui(self):
        self.lbl_blur_overlay = tk.Label(self.root, bg=self.BG_COLOR)
        self.lbl_blur_overlay.bind("<Button-1>", self.on_global_click)

        self.title_bar = tk.Frame(self.root, bg=self.BG_COLOR, height=52)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        self.left_info_frame = tk.Frame(self.title_bar, bg=self.BG_COLOR)
        self.left_info_frame.place(relx=0.0, rely=0.5, x=22, anchor=tk.W)

        self.lbl_version = tk.Label(self.left_info_frame, text="v1.0.0", bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.lbl_version.pack(side=tk.TOP, anchor=tk.W)
        self.lbl_github = tk.Label(self.left_info_frame, text="GitHub", bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR, cursor="hand2")
        self.lbl_github.pack(side=tk.TOP, anchor=tk.W, pady=(1, 0))
        self.lbl_github.bind("<Button-1>", lambda e: self.open_github())
        self.lbl_github.bind("<Enter>", lambda e: self.lbl_github.config(fg="#A0A0A0"))
        self.lbl_github.bind("<Leave>", lambda e: self.lbl_github.config(fg=self.SUBTEXT_COLOR))

        self.btns_frame = tk.Frame(self.title_bar, bg=self.BG_COLOR)
        self.btns_frame.place(relx=1.0, rely=0.5, x=-18, anchor=tk.E)

        self.gear_icon_norm = self.draw_simple_gear_icon(size=16, color=self.ICON_NORM)
        self.gear_icon_hover = self.draw_simple_gear_icon(size=16, color=self.ICON_HOVER)

        self.btn_opts = tk.Label(self.btns_frame, image=self.gear_icon_norm, bg=self.BG_COLOR, cursor="hand2")
        self.btn_opts.pack(side=tk.LEFT, padx=(0, 12))
        self.btn_opts.bind("<Button-1>", lambda e: self.open_options())
        self.btn_opts.bind("<Enter>", lambda e: self.btn_opts.config(image=self.gear_icon_hover))
        self.btn_opts.bind("<Leave>", lambda e: self.btn_opts.config(image=self.gear_icon_norm))

        self.btn_min_canvas = tk.Canvas(self.btns_frame, width=20, height=20, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.btn_min_canvas.pack(side=tk.LEFT, padx=(0, 12))
        self.min_line = self.btn_min_canvas.create_line(4, 10, 16, 10, fill="#777777", width=2)
        self.btn_min_canvas.bind("<Button-1>", lambda e: self.minimize_window())
        self.btn_min_canvas.bind("<Enter>", lambda e: self.btn_min_canvas.itemconfig(self.min_line, fill="#FFCC00"))
        self.btn_min_canvas.bind("<Leave>", lambda e: self.btn_min_canvas.itemconfig(self.min_line, fill="#777777" if self.current_theme=="Dark" else "#555555"))

        self.btn_close = tk.Label(self.btns_frame, text="✕", bg=self.BG_COLOR, fg=self.CLOSE_FG, cursor="hand2")
        self.btn_close.pack(side=tk.LEFT)
        self.btn_close.bind("<Button-1>", lambda e: self.quit_app())
        self.btn_close.bind("<Enter>", lambda e: self.btn_close.config(fg="#FF5555"))
        self.btn_close.bind("<Leave>", lambda e: self.btn_close.config(fg=self.CLOSE_FG))

        self.lbl_title = tk.Label(self.title_bar, text=TRANSLATIONS[self.current_language]["title"], bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.align_title_center()

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.lbl_title.bind("<Button-1>", self.start_move)
        self.lbl_title.bind("<B1-Motion>", self.do_move)
        self.lbl_version.bind("<Button-1>", self.start_move)

        self.divider_top = tk.Canvas(self.root, width=400, height=2, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.divider_top.pack(fill=tk.NONE, pady=(0, 5))
        self.draw_fade_line_on_canvas(self.divider_top, 400, 2, self.LINE_COLOR, self.BG_RGB)

        self.viewport = tk.Frame(self.root, bg=self.BG_COLOR, width=self.width, height=self.height - 54)
        self.viewport.pack(fill=tk.BOTH, expand=True)

        self.home_frame = tk.Frame(self.viewport, bg=self.BG_COLOR, width=self.width, height=self.height - 54)
        self.home_frame.place(x=0, y=0, width=self.width, height=self.height - 54)

        self.bsod_frame = tk.Frame(self.home_frame, bg="#0000AA")
        self.bsod_frame.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        lbl_bsod_text = tk.Label(self.bsod_frame, text="ERROR 404", font=("Arial", 42, "bold"), bg="#0000AA", fg="#FFFFFF")
        lbl_bsod_text.pack(expand=True)
        self.bsod_frame.lower()

        self.settings_frame = tk.Frame(self.viewport, bg=self.BG_COLOR, width=self.width, height=self.height - 54)
        self.settings_frame.place(x=self.width, y=0, width=self.width, height=self.height - 54)

        self.content_frame = tk.Frame(self.home_frame, bg=self.BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        for lang, data in TRANSLATIONS.items():
            self.flag_images[lang] = self.get_flag_image(data["code"])

        self.bg_box_norm = self.create_rounded_rect_image(115, 32, radius=8, fill_color=(42, 42, 42), outline_color=(68, 68, 68))
        self.bg_box_hover = self.create_rounded_rect_image(115, 32, radius=8, fill_color=(53, 53, 53), outline_color=(90, 90, 90))

        self.lang_container = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        self.lang_container.place(x=20, y=5)
        self.lbl_lang_header = tk.Label(self.lang_container, text=TRANSLATIONS[self.current_language]["lang_label"], bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR, anchor="center")
        self.lbl_lang_header.pack(fill=tk.X, pady=(0, 2))
        self.btn_lang_canvas = tk.Canvas(self.lang_container, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.btn_lang_canvas.pack(anchor=tk.CENTER)
        self.lang_bg_img_id = self.btn_lang_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)
        self.btn_lang_lbl = tk.Label(self.btn_lang_canvas, image=self.flag_images.get("English"), text="  English  ▼", compound="left", bg=self.BTN_BG, fg="#DDDDDD", cursor="hand2")
        self.btn_lang_canvas.create_window(57, 16, window=self.btn_lang_lbl)

        for widget in (self.btn_lang_canvas, self.btn_lang_lbl):
            widget.bind("<Button-1>", self.toggle_language_dropdown)
            widget.bind("<Enter>", lambda e: (self.btn_lang_canvas.itemconfig(self.lang_bg_img_id, image=self.bg_box_hover), self.btn_lang_lbl.config(bg=self.BTN_HOVER)))
            widget.bind("<Leave>", lambda e: (self.btn_lang_canvas.itemconfig(self.lang_bg_img_id, image=self.bg_box_norm), self.btn_lang_lbl.config(bg=self.BTN_BG)))

        self.theme_container = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        self.theme_container.place(x=305, y=5)
        self.lbl_theme_header = tk.Label(self.theme_container, text=TRANSLATIONS[self.current_language]["theme_label"], bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR, anchor="center")
        self.lbl_theme_header.pack(fill=tk.X, pady=(0, 2))
        self.btn_theme_canvas = tk.Canvas(self.theme_container, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.btn_theme_canvas.pack(anchor=tk.CENTER)
        self.theme_bg_img_id = self.btn_theme_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)
        self.btn_theme_lbl = tk.Label(self.btn_theme_canvas, image=self.theme_icons.get("Dark"), text=f"  {TRANSLATIONS[self.current_language]['themes'][self.current_theme]}  ▼", compound="left", bg=self.BTN_BG, fg="#DDDDDD", cursor="hand2")
        self.btn_theme_canvas.create_window(57, 16, window=self.btn_theme_lbl)

        for widget in (self.btn_theme_canvas, self.btn_theme_lbl):
            widget.bind("<Button-1>", self.toggle_theme_dropdown)
            widget.bind("<Enter>", lambda e: (self.btn_theme_canvas.itemconfig(self.theme_bg_img_id, image=self.bg_box_hover), self.btn_theme_lbl.config(bg=self.BTN_HOVER)))
            widget.bind("<Leave>", lambda e: (self.btn_theme_canvas.itemconfig(self.theme_bg_img_id, image=self.bg_box_norm), self.btn_theme_lbl.config(bg=self.BTN_BG)))

        img_path = resource_path(os.path.join("images", "kbomb.png"))
        if os.path.exists(img_path):
            try:
                self.kb_base_img = Image.open(img_path)
                self.lbl_kb_img = tk.Label(self.content_frame, bg=self.BG_COLOR)
                self.lbl_kb_img.place(relx=0.5, y=5, anchor=tk.N)
            except Exception: pass

        self.divider_mid = tk.Canvas(self.content_frame, width=360, height=2, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.draw_fade_line_on_canvas(self.divider_mid, 360, 2, self.LINE_COLOR, self.BG_RGB)

        self.slider_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        self.lbl_slider_title = tk.Label(self.slider_frame, text=TRANSLATIONS[self.current_language]["slider_label"], bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_slider_title.pack(pady=(0, 6))

        self.slider_canvas = tk.Canvas(self.slider_frame, width=360, height=30, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.slider_canvas.pack()
        self.slider_canvas.bind("<Button-1>", self.on_slider_click)
        self.slider_canvas.bind("<B1-Motion>", self.on_slider_drag)

        self.bottom_controls = tk.Frame(self.slider_frame, bg=self.BG_COLOR, width=360)
        self.bottom_controls.pack(fill=tk.X, pady=(15, 0))

        self.left_box = tk.Frame(self.bottom_controls, bg=self.BG_COLOR, width=115)
        self.left_box.pack(side=tk.LEFT)
        self.lbl_num_header = tk.Label(self.left_box, text=TRANSLATIONS[self.current_language]["num_header"], bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR, anchor="center")
        self.lbl_num_header.pack(fill=tk.X, pady=(0, 2))
        self.num_canvas = tk.Canvas(self.left_box, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.num_canvas.pack(anchor=tk.CENTER)
        self.num_bg_img_id = self.num_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)
        self.ent_kirby_num = tk.Entry(self.num_canvas, bg=self.BTN_BG, fg="#0078D4", bd=0, highlightthickness=0, insertbackground="#FFFFFF", justify="center")
        self.num_canvas.create_window(57, 16, window=self.ent_kirby_num, width=70, height=20)
        self.ent_kirby_num.bind("<Return>", self.on_number_input_change)
        self.ent_kirby_num.bind("<FocusOut>", self.on_number_input_change)

        self.right_box = tk.Frame(self.bottom_controls, bg=self.BG_COLOR, width=115)
        self.right_box.pack(side=tk.RIGHT)
        self.lbl_mode_header = tk.Label(self.right_box, text=TRANSLATIONS[self.current_language]["mode_header"], bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR, anchor="center")
        self.lbl_mode_header.pack(fill=tk.X, pady=(0, 2))
        self.btn_mode_canvas = tk.Canvas(self.right_box, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.btn_mode_canvas.pack(anchor=tk.CENTER)
        self.mode_bg_img_id = self.btn_mode_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)
        self.btn_mode_lbl = tk.Label(self.btn_mode_canvas, text=f"{TRANSLATIONS[self.current_language]['modes'][self.current_mode]}  ▼", bg=self.BTN_BG, fg="#DDDDDD", cursor="hand2")
        self.btn_mode_canvas.create_window(57, 16, window=self.btn_mode_lbl)

        for widget in (self.btn_mode_canvas, self.btn_mode_lbl):
            widget.bind("<Button-1>", self.toggle_mode_dropdown)
            widget.bind("<Enter>", lambda e: (self.btn_mode_canvas.itemconfig(self.mode_bg_img_id, image=self.bg_box_hover), self.btn_mode_lbl.config(bg=self.BTN_HOVER)))
            widget.bind("<Leave>", lambda e: (self.btn_mode_canvas.itemconfig(self.mode_bg_img_id, image=self.bg_box_norm), self.btn_mode_lbl.config(bg=self.BTN_BG)))

        self.center_box = tk.Frame(self.bottom_controls, bg=self.BG_COLOR, width=115)
        self.center_box.pack(side=tk.LEFT, expand=True)
        self.lbl_rand_header = tk.Label(self.center_box, text=TRANSLATIONS[self.current_language]["rand_header"], bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR, anchor="center")
        self.lbl_rand_header.pack(fill=tk.X, pady=(0, 2))
        self.dice_icon = self.draw_dice_icon(size=14)
        self.btn_rand_canvas = tk.Canvas(self.center_box, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.btn_rand_canvas.pack(anchor=tk.CENTER)
        self.rand_bg_img_id = self.btn_rand_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)
        self.btn_rand_lbl = tk.Label(self.btn_rand_canvas, image=self.dice_icon, text=f"  {TRANSLATIONS[self.current_language]['rand_btn']}", compound="left", bg=self.BTN_BG, fg="#DDDDDD", cursor="hand2")
        self.btn_rand_canvas.create_window(57, 16, window=self.btn_rand_lbl)

        for widget in (self.btn_rand_canvas, self.btn_rand_lbl):
            widget.bind("<Button-1>", self.on_randomize_click)
            widget.bind("<Enter>", lambda e: (self.btn_rand_canvas.itemconfig(self.rand_bg_img_id, image=self.bg_box_hover), self.btn_rand_lbl.config(bg=self.BTN_HOVER)))
            widget.bind("<Leave>", lambda e: (self.btn_rand_canvas.itemconfig(self.rand_bg_img_id, image=self.bg_box_norm), self.btn_rand_lbl.config(bg=self.BTN_BG)))

        self.divider_bottom = tk.Canvas(self.slider_frame, width=360, height=2, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.divider_bottom.pack(pady=(14, 0))
        self.draw_fade_line_on_canvas(self.divider_bottom, 360, 2, self.LINE_COLOR, self.BG_RGB)

        self.bg_green_norm = self.create_rounded_rect_image(170, 36, radius=10, fill_color=(40, 167, 69), outline_color=(30, 130, 50))
        self.bg_green_hover = self.create_rounded_rect_image(170, 36, radius=10, fill_color=(48, 195, 82), outline_color=(35, 150, 60))
        self.bg_red_norm = self.create_rounded_rect_image(170, 36, radius=10, fill_color=(220, 53, 69), outline_color=(175, 35, 50))
        self.bg_red_hover = self.create_rounded_rect_image(170, 36, radius=10, fill_color=(240, 70, 85), outline_color=(195, 45, 60))
        self.bg_orange_norm = self.create_rounded_rect_image(170, 36, radius=10, fill_color=(253, 126, 20), outline_color=(200, 95, 10))

        self.action_buttons_frame = tk.Frame(self.slider_frame, bg=self.BG_COLOR, width=360)
        self.action_buttons_frame.pack(fill=tk.X, pady=(14, 0))

        self.btn_release_canvas = tk.Canvas(self.action_buttons_frame, width=170, height=36, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.btn_release_canvas.pack(side=tk.LEFT)
        self.release_bg_id = self.btn_release_canvas.create_image(0, 0, image=self.bg_green_norm, anchor=tk.NW)
        self.btn_release_lbl = tk.Label(self.btn_release_canvas, text=TRANSLATIONS[self.current_language]["btn_release"], bg="#28A745", fg="#FFFFFF", cursor="hand2")
        self.btn_release_canvas.create_window(85, 18, window=self.btn_release_lbl)
        for widget in (self.btn_release_canvas, self.btn_release_lbl):
            widget.bind("<Button-1>", self.on_release_kirby)

        self.btn_kill_canvas = tk.Canvas(self.action_buttons_frame, width=170, height=36, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.btn_kill_canvas.pack(side=tk.RIGHT)
        self.kill_bg_id = self.btn_kill_canvas.create_image(0, 0, image=self.bg_red_norm, anchor=tk.NW)
        self.btn_kill_lbl = tk.Label(self.btn_kill_canvas, text=TRANSLATIONS[self.current_language]["btn_kill"], bg="#DC3545", fg="#FFFFFF", cursor="hand2")
        self.btn_kill_canvas.create_window(85, 18, window=self.btn_kill_lbl)
        for widget in (self.btn_kill_canvas, self.btn_kill_lbl):
            widget.bind("<Button-1>", self.on_kill_kirby)
            widget.bind("<Enter>", lambda e: (self.btn_kill_canvas.itemconfig(self.kill_bg_id, image=self.bg_red_hover), self.btn_kill_lbl.config(bg="#F04655")))
            widget.bind("<Leave>", lambda e: (self.btn_kill_canvas.itemconfig(self.kill_bg_id, image=self.bg_red_norm), self.btn_kill_lbl.config(bg="#DC3545")))

        self.divider_footer = tk.Canvas(self.slider_frame, width=360, height=2, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.divider_footer.pack(pady=(10, 0))
        self.draw_fade_line_on_canvas(self.divider_footer, 360, 2, self.LINE_COLOR, self.BG_RGB)

        self.footer_frame = tk.Frame(self.slider_frame, bg=self.BG_COLOR)
        self.footer_frame.pack(pady=(4, 0))
        self.lbl_made_by = tk.Label(self.footer_frame, text=TRANSLATIONS[self.current_language]["made_by"], bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR, cursor="hand2")
        self.lbl_made_by.pack(side=tk.TOP)
        self.lbl_made_by.bind("<Button-1>", self.on_aken_click)

        self.short_solid_line = tk.Canvas(self.footer_frame, width=260, height=1, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.short_solid_line.pack(pady=(3, 3))
        self.solid_line_id = self.short_solid_line.create_line(0, 0, 260, 0, fill=self.SOLID_LINE_COLOR, width=1)
        
        self.lbl_quote = tk.Label(self.footer_frame, text=TRANSLATIONS[self.current_language]["quote"], bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR, wraplength=350, justify="center")
        self.lbl_quote.pack(side=tk.TOP)

        # ---------------- SETTINGS FRAME ----------------
        self.btn_back_large = tk.Button(self.settings_frame, text="←", command=self.go_back_home, bg=self.BG_COLOR, fg=self.TEXT_COLOR, activebackground=self.BG_COLOR, activeforeground="#0078D4", bd=0, highlightthickness=0, font=("Segoe UI", 22, "bold"), cursor="hand2")
        self.btn_back_large.place(x=15, y=10, width=50, height=40)

        self.lbl_settings_title = tk.Label(self.settings_frame, text=TRANSLATIONS[self.current_language]["settings_title"], bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_settings_title.pack(pady=(10, 2))
        self.lbl_settings_sub = tk.Label(self.settings_frame, text=TRANSLATIONS[self.current_language]["settings_sub"], bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR)
        self.lbl_settings_sub.pack(pady=(0, 10))

        self.opt_frame = tk.Frame(self.settings_frame, bg=self.BG_COLOR)
        self.opt_frame.pack(fill=tk.X, padx=40, pady=5)

        # Option 1: Retro
        self.opt_row1 = tk.Frame(self.opt_frame, bg=self.BG_COLOR)
        self.opt_row1.pack(fill=tk.X, pady=6)
        self.canvas_opt_retro = tk.Canvas(self.opt_row1, width=50, height=26, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.canvas_opt_retro.pack(side=tk.LEFT, padx=(0, 15))
        self.canvas_opt_retro.bind("<Button-1>", self.toggle_retro)
        self.lbl_opt_retro = tk.Label(self.opt_row1, text=TRANSLATIONS[self.current_language]["opt_retro"], bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_opt_retro.pack(side=tk.LEFT)
        self.draw_ios_toggle_frame(self.canvas_opt_retro, 1.0 if self.opt_full_retro else 0.0)

        # Option 2: BSOD
        self.opt_row2 = tk.Frame(self.opt_frame, bg=self.BG_COLOR)
        self.opt_row2.pack(fill=tk.X, pady=6)
        self.canvas_opt_bsod = tk.Canvas(self.opt_row2, width=50, height=26, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.canvas_opt_bsod.pack(side=tk.LEFT, padx=(0, 15))
        self.canvas_opt_bsod.bind("<Button-1>", self.toggle_bsod)
        self.lbl_opt_bsod = tk.Label(self.opt_row2, text=TRANSLATIONS[self.current_language]["opt_bsod"], bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_opt_bsod.pack(side=tk.LEFT)
        self.draw_ios_toggle_frame(self.canvas_opt_bsod, 1.0 if self.opt_bsod else 0.0)

        # Option 3: Destroy
        self.opt_row3 = tk.Frame(self.opt_frame, bg=self.BG_COLOR)
        self.opt_row3.pack(fill=tk.X, pady=6)
        self.canvas_opt_destroy = tk.Canvas(self.opt_row3, width=50, height=26, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.canvas_opt_destroy.pack(side=tk.LEFT, padx=(0, 15))
        self.canvas_opt_destroy.bind("<Button-1>", self.toggle_destroy)
        self.lbl_opt_destroy = tk.Label(self.opt_row3, text=TRANSLATIONS[self.current_language]["opt_destroy"], bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_opt_destroy.pack(side=tk.LEFT)
        self.draw_ios_toggle_frame(self.canvas_opt_destroy, 1.0 if self.opt_destroy else 0.0)

        # Option 4: Dislike
        self.opt_row4 = tk.Frame(self.opt_frame, bg=self.BG_COLOR)
        self.opt_row4.pack(fill=tk.X, pady=6)
        self.canvas_opt_dislike = tk.Canvas(self.opt_row4, width=50, height=26, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.canvas_opt_dislike.pack(side=tk.LEFT, padx=(0, 15))
        self.canvas_opt_dislike.bind("<Button-1>", self.toggle_dislike)
        self.lbl_opt_dislike = tk.Label(self.opt_row4, text=TRANSLATIONS[self.current_language]["opt_dislike"], bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.lbl_opt_dislike.pack(side=tk.LEFT)
        self.draw_ios_toggle_frame(self.canvas_opt_dislike, 1.0 if self.opt_dislike else 0.0)

        # Disclaimer
        disclaimer_text = ("Disclaimer\nThis project is a non-commercial, fan-made creation made purely for entertainment "
                           "and educational purposes. All rights, logos, trademarks, and intellectual property belong to "
                           "their respective owners. No copyright infringement is intended.\n"
                           "If you are a copyright owner or an authorized agent and believe that any content used here "
                           "infringes upon your intellectual property rights, please contact me at shakuhachiyugen@gmail.com, "
                           "and I will promptly review and remove the material upon request.")
        self.lbl_disclaimer = tk.Label(self.settings_frame, text=disclaimer_text, bg=self.BG_COLOR, fg=self.SUBTEXT_COLOR, wraplength=380, justify="center")
        self.lbl_disclaimer.pack(side=tk.BOTTOM, pady=20)

        self.update_kirby_image()
        self.draw_custom_slider()

if __name__ == "__main__":
    root = tk.Tk()
    app = KirbyBomberApp(root)
    root.mainloop()