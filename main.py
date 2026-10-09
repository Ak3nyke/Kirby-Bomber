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
        "rand_btn": "Randomizar",
        "num_header": "Número de Kirby",
        "mode_header": "Modo Kirby",
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
        "rand_btn": "Randomizar",
        "num_header": "Número de Kirby",
        "mode_header": "Modo Kirby",
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

        self.keep_images = []
        self.flag_images = {}
        self.theme_icons = {}
        self.kb_base_img = None
        self.thumb_cache = {}
        self.dropdown_canvas = None

        self.generate_theme_icons()
        self.download_flags()
        self.setup_ui()
        self.center_window()
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        enable_native_rounded_corners(self.root)

        self.root.bind("<Map>", self.on_restore)

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

    def generate_theme_icons(self):
        scale = 4
        size = 16
        s = size * scale
        img_moon = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_moon)
        
        draw.ellipse([s*0.1, s*0.1, s*0.9, s*0.9], fill=(240, 230, 140, 255))
        draw.ellipse([s*0.3, s*0.05, s*0.98, s*0.85], fill=(0, 0, 0, 0))
        
        moon_smooth = img_moon.resize((size, size), Image.Resampling.LANCZOS)
        self.theme_icons["Dark"] = ImageTk.PhotoImage(moon_smooth)

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
        
        sun_smooth = img_sun.resize((size, size), Image.Resampling.LANCZOS)
        self.theme_icons["Light"] = ImageTk.PhotoImage(sun_smooth)

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

        self.btn_min_canvas.config(bg=self.BG_COLOR)
        self.btn_min_canvas.itemconfig(self.min_line, fill="#777777" if self.current_theme == "Dark" else "#555555")

        self.btn_close.config(bg=self.BG_COLOR, fg=self.CLOSE_FG)

        self.lbl_title.config(bg=self.BG_COLOR, fg=self.TEXT_COLOR)

        self.draw_fade_line_on_canvas(self.divider_top, 400, 2, self.LINE_COLOR, self.BG_RGB)

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
        self.ent_kirby_num.config(bg=self.BTN_BG)

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
        self.btn_theme_lbl.config(bg=self.BTN_BG, fg=text_fg)

        self.num_canvas.itemconfig(self.num_bg_img_id, image=self.bg_box_norm)

        self.btn_mode_canvas.itemconfig(self.mode_bg_img_id, image=self.bg_box_norm)
        self.btn_mode_lbl.config(bg=self.BTN_BG, fg=text_fg)

        self.btn_rand_canvas.itemconfig(self.rand_bg_img_id, image=self.bg_box_norm)
        self.btn_rand_lbl.config(bg=self.BTN_BG, fg=text_fg)

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
        smooth_img = img.resize((diameter, diameter), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(smooth_img)
        return photo

    def create_rounded_rect_image(self, width, height, radius=8, fill_color=(42, 42, 42), outline_color=(68, 68, 68)):
        scale = 4
        sw, sh = width * scale, height * scale
        sr = radius * scale
        
        img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        draw.rounded_rectangle(
            [scale, scale, sw - scale, sh - scale],
            radius=sr,
            fill=fill_color + (255,),
            outline=outline_color + (255,),
            width=scale
        )
        
        smooth_img = img.resize((width, height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(smooth_img)
        self.keep_images.append(photo)
        return photo

    def download_flags(self):
        flags_dir = os.path.join("images", "flags")
        if not os.path.exists(flags_dir):
            os.makedirs(flags_dir)

        headers = {'User-Agent': 'Mozilla/5.0'}

        for lang, data in TRANSLATIONS.items():
            code = data["code"]
            filepath = os.path.join(flags_dir, f"{code}.png")
            if not os.path.exists(filepath):
                try:
                    url = f"https://flagcdn.com/w40/{code}.png"
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                        out_file.write(response.read())
                except Exception as e:
                    print(f"Errore download bandiera {code}: {e}")

    def get_flag_image(self, code):
        filepath = os.path.join("images", "flags", f"{code}.png")
        if os.path.exists(filepath):
            try:
                img = Image.open(filepath)
                img = img.resize((18, 12), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                return photo
            except Exception as e:
                print(f"Errore caricamento {filepath}: {e}")
        return None

    def quit_app(self):
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
        
        smooth_img = img.resize((size, size), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(smooth_img)
        self.keep_images.append(photo)
        return photo

    def draw_dice_icon(self, size=16):
        scale = 4
        s = size * scale
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        rbox = [s * 0.1, s * 0.1, s * 0.9, s * 0.9]
        draw.rounded_rectangle(rbox, radius=s * 0.2, fill=(240, 240, 240, 255), outline=(180, 180, 180, 255), width=int(s*0.06))
        
        dot_r = s * 0.09
        dots = [
            (s * 0.3, s * 0.3),
            (s * 0.7, s * 0.3),
            (s * 0.5, s * 0.5),
            (s * 0.3, s * 0.7),
            (s * 0.7, s * 0.7)
        ]
        for dx, dy in dots:
            draw.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r], fill=(220, 50, 50, 255))
            
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
        self.root.update_idletasks()
        left_width = self.left_info_frame.winfo_reqwidth()
        right_width = self.btns_frame.winfo_reqwidth()
        left_edge = 22 + left_width
        right_edge = self.width - 18 - right_width
        center_x = left_edge + (right_edge - left_edge) / 2
        self.lbl_title.place(x=center_x, rely=0.5, anchor=tk.CENTER)

    def draw_custom_slider(self):
        self.slider_canvas.delete("all")
        
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
        
        current_thumb = self.thumb_cache[hex_color]
        self.slider_canvas.create_image(thumb_x, cy, image=current_thumb, anchor=tk.CENTER)

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
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h)).convert("RGBA")
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
            if not wdg or not wdg.winfo_viewable():
                continue

            wx = wdg.winfo_rootx() - x
            wy = wdg.winfo_rooty() - y
            ww = wdg.winfo_width()
            wh = wdg.winfo_height()

            if ww <= 0 or wh <= 0:
                continue

            try:
                crop = screenshot.crop((wx, wy, wx + ww, wy + wh)).convert("RGBA")
                if radius:
                    scale = 4
                    mask = Image.new("L", (ww * scale, wh * scale), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.rounded_rectangle([scale, scale, ww * scale - scale, wh * scale - scale], radius=radius * scale, fill=255)
                    mask_small = mask.resize((ww, wh), Image.Resampling.LANCZOS)
                    self.blurred_dark.paste(crop, (wx, wy), mask_small)
                else:
                    self.blurred_dark.paste(crop, (wx, wy))
            except Exception as e:
                print(f"Errore overlay blur: {e}")

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
        box_center_x = box_x + (target_canvas.winfo_width() / 2)
        x = int(box_center_x - (width / 2))
        
        y = target_canvas.winfo_rooty() - self.root.winfo_rooty() + target_canvas.winfo_height()

        item_h = 32
        pad_y = 6
        height = len(items) * item_h + pad_y * 2

        img_w, img_h = self.blurred_dark.size
        crop_x1 = max(0, min(x, img_w))
        crop_y1 = max(0, min(y, img_h))
        crop_x2 = max(0, min(x + width, img_w))
        crop_y2 = max(0, min(y + height, img_h))

        crop = self.blurred_dark.crop((crop_x1, crop_y1, crop_x2, crop_y2)).convert("RGBA")
        if crop.size != (width, height):
            new_crop = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            new_crop.paste(crop, (0, 0))
            crop = new_crop

        scale = 4
        sw, sh = width * scale, height * scale
        sr = 8 * scale
        mask = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mask)
        
        bg_fill = (37, 37, 37, 255) if self.current_theme == "Dark" else (240, 240, 245, 255)
        border_outline = (68, 68, 68, 255) if self.current_theme == "Dark" else (199, 199, 204, 255)
        
        draw.rounded_rectangle([scale, scale, sw - scale, sh - scale], radius=sr, fill=bg_fill, outline=border_outline, width=scale)
        mask_small = mask.resize((width, height), Image.Resampling.LANCZOS)

        combined = Image.alpha_composite(crop, mask_small)
        self.dd_bg_img = ImageTk.PhotoImage(combined)

        self.dropdown_canvas = tk.Canvas(self.root, width=width, height=height, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.dropdown_canvas.create_image(0, 0, image=self.dd_bg_img, anchor=tk.NW)

        hov_fill = (80, 80, 80) if self.current_theme == "Dark" else (210, 210, 215)
        self.hover_img = self.create_rounded_rect_image(width - 12, item_h, radius=6, fill_color=hov_fill, outline_color=hov_fill)
        self.hover_canvas_img = self.dropdown_canvas.create_image(6, -100, image=self.hover_img, anchor=tk.NW)

        text_color = "#DDDDDD" if self.current_theme == "Dark" else "#1D1D1F"

        self.dropdown_items_data = []
        for i, item in enumerate(items):
            id_str, text, img = item
            iy = pad_y + i * item_h
            if img:
                self.dropdown_canvas.create_image(12, iy + item_h // 2, image=img, anchor=tk.W)
                text_id = self.dropdown_canvas.create_text(36, iy + item_h // 2, text=text, fill=text_color, font=("Segoe UI", 8, "bold"), anchor=tk.W)
            else:
                text_id = self.dropdown_canvas.create_text(width // 2, iy + item_h // 2, text=text, fill=text_color, font=("Segoe UI", 8, "bold"), anchor=tk.CENTER)

            self.dropdown_items_data.append({"id": id_str, "y1": iy, "y2": iy + item_h})

        self.dropdown_canvas.place(x=x, y=y)
        
        tk.Widget.tkraise(self.dropdown_canvas)
        
        self.dropdown_canvas.bind("<Motion>", self.on_dropdown_hover)
        self.dropdown_canvas.bind("<Button-1>", self.on_dropdown_click)

    def on_dropdown_hover(self, e):
        my_y = e.y
        for data in self.dropdown_items_data:
            if data["y1"] <= my_y <= data["y2"]:
                self.dropdown_canvas.coords(self.hover_canvas_img, 6, data["y1"])
                return
        self.dropdown_canvas.coords(self.hover_canvas_img, 6, -100)

    def on_dropdown_click(self, event):
        my_y = event.y
        for data in self.dropdown_items_data:
            if data["y1"] <= my_y <= data["y2"]:
                selected_id = data["id"]
                if self.active_dropdown_type == "language":
                    self.select_language(selected_id)
                elif self.active_dropdown_type == "theme":
                    self.select_theme(selected_id)
                elif self.active_dropdown_type == "mode":
                    self.select_mode(selected_id)
                return

    def toggle_language_dropdown(self, event=None):
        if self.active_dropdown_type == "language":
            self.close_all_dropdowns()
        else:
            self.close_all_dropdowns()
            self.apply_blur_overlay("language")
            self.show_dropdown("language")

    def toggle_theme_dropdown(self, event=None):
        if self.active_dropdown_type == "theme":
            self.close_all_dropdowns()
        else:
            self.close_all_dropdowns()
            self.apply_blur_overlay("theme")
            self.show_dropdown("theme")

    def toggle_mode_dropdown(self, event=None):
        if self.active_dropdown_type == "mode":
            self.close_all_dropdowns()
        else:
            self.close_all_dropdowns()
            self.apply_blur_overlay("mode")
            self.show_dropdown("mode")

    def on_randomize_click(self, event=None):
        new_val = random.randint(self.min_kirby, self.max_kirby)
        self.kirby_count = new_val
        self.draw_custom_slider()

    def on_release_kirby(self, event=None):
        print(f"Rilasciati {self.kirby_count} Kirby! :)")

    def on_kill_kirby(self, event=None):
        print("Tutti i Kirby eliminati! :(")

    def select_language(self, lang_name):
        self.current_language = lang_name
        data = TRANSLATIONS[lang_name]

        flag_img = self.flag_images.get(lang_name)
        if flag_img:
            self.btn_lang_lbl.config(image=flag_img, text=f"  {lang_name}  ▼", compound="left")
        else:
            self.btn_lang_lbl.config(image="", text=f"{lang_name}  ▼")

        theme_icon = self.theme_icons.get(self.current_theme)
        theme_str = data["themes"][self.current_theme]
        self.btn_theme_lbl.config(image=theme_icon, text=f"  {theme_str}  ▼", compound="left")

        mode_str = data["modes"][self.current_mode]
        self.btn_mode_lbl.config(text=f"{mode_str}  ▼")

        self.lbl_lang_header.config(text=data['lang_label'])
        self.lbl_theme_header.config(text=data['theme_label'])
        self.lbl_title.config(text=data['title'])
        self.lbl_slider_title.config(text=data['slider_label'])
        
        self.lbl_rand_header.config(text=data['rand_header'])
        self.btn_rand_lbl.config(text=f"  {data['rand_btn']}")
        
        self.lbl_num_header.config(text=data['num_header'])
        self.lbl_mode_header.config(text=data['mode_header'])
        
        self.align_title_center()
        self.close_all_dropdowns()

    def select_theme(self, theme_name):
        self.current_theme = theme_name
        theme_icon = self.theme_icons.get(theme_name)
        theme_str = TRANSLATIONS[self.current_language]["themes"][theme_name]
        self.btn_theme_lbl.config(image=theme_icon, text=f"  {theme_str}  ▼", compound="left")
        self.update_ui_theme()
        self.close_all_dropdowns()

    def update_kirby_image(self):
        if not self.kb_base_img:
            return

        target_width = 130
        aspect_ratio = self.kb_base_img.height / self.kb_base_img.width
        target_height = int(target_width * aspect_ratio)

        if self.current_mode == "Modern":
            resized_img = self.kb_base_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        else:
            small_w = 36
            small_h = int(small_w * aspect_ratio)
            pixel_img = self.kb_base_img.resize((small_w, small_h), Image.Resampling.BILINEAR)
            resized_img = pixel_img.resize((target_width, target_height), Image.Resampling.NEAREST)

        self.kb_tk_img = ImageTk.PhotoImage(resized_img)
        self.lbl_kb_img.config(image=self.kb_tk_img)

        self.root.update_idletasks()
        kb_y = self.lbl_kb_img.winfo_y()
        kb_h = self.lbl_kb_img.winfo_height()
        line_y = kb_y + kb_h + 12
        
        self.divider_mid.place(relx=0.5, y=line_y, anchor=tk.N)
        self.slider_frame.place(relx=0.5, y=line_y + 18, anchor=tk.N)

    def select_mode(self, mode_name):
        self.current_mode = mode_name
        mode_str = TRANSLATIONS[self.current_language]["modes"][mode_name]
        self.btn_mode_lbl.config(text=f"{mode_str}  ▼")
        self.update_kirby_image()
        self.close_all_dropdowns()

    def close_all_dropdowns(self):
        if hasattr(self, 'dropdown_canvas') and self.dropdown_canvas:
            self.dropdown_canvas.destroy()
            self.dropdown_canvas = None
        self.remove_blur_overlay()
        self.active_dropdown_type = None

    def on_global_click(self, event):
        if not self.active_dropdown_type:
            return

        widget = event.widget
        if self.active_dropdown_type == "language":
            valid_widgets = [self.btn_lang_canvas, self.btn_lang_lbl]
        elif self.active_dropdown_type == "theme":
            valid_widgets = [self.btn_theme_canvas, self.btn_theme_lbl]
        elif self.active_dropdown_type == "mode":
            valid_widgets = [self.btn_mode_canvas, self.btn_mode_lbl]
        else:
            valid_widgets = []
            
        if self.dropdown_canvas:
            valid_widgets.append(self.dropdown_canvas)

        if widget not in valid_widgets:
            self.close_all_dropdowns()

    def setup_ui(self):
        self.lbl_blur_overlay = tk.Label(self.root, bg=self.BG_COLOR)
        self.lbl_blur_overlay.bind("<Button-1>", self.on_global_click)

        self.title_bar = tk.Frame(self.root, bg=self.BG_COLOR, height=52)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        self.left_info_frame = tk.Frame(self.title_bar, bg=self.BG_COLOR)
        self.left_info_frame.place(relx=0.0, rely=0.5, x=22, anchor=tk.W)

        self.lbl_version = tk.Label(
            self.left_info_frame,
            text="v1.0.0",
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 8, "bold")
        )
        self.lbl_version.pack(side=tk.TOP, anchor=tk.W)

        self.lbl_github = tk.Label(
            self.left_info_frame,
            text="GitHub",
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
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

        self.btn_close = tk.Label(self.btns_frame, text="✕", bg=self.BG_COLOR, fg=self.CLOSE_FG, font=("Arial", 11, "bold"), cursor="hand2")
        self.btn_close.pack(side=tk.LEFT)
        btn_close_action = lambda e: self.quit_app()
        self.btn_close.bind("<Button-1>", btn_close_action)
        self.btn_close.bind("<Enter>", lambda e: self.btn_close.config(fg="#FF5555"))
        self.btn_close.bind("<Leave>", lambda e: self.btn_close.config(fg=self.CLOSE_FG))

        # TITOLO CON FONT CENTURY GOTHIC PULITO
        title_text = TRANSLATIONS[self.current_language]["title"]
        self.lbl_title = tk.Label(
            self.title_bar, 
            text=title_text, 
            bg=self.BG_COLOR, 
            fg=self.TEXT_COLOR, 
            font=("Century Gothic", 10, "bold")
        )
        self.align_title_center()

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.lbl_title.bind("<Button-1>", self.start_move)
        self.lbl_title.bind("<B1-Motion>", self.do_move)
        self.lbl_version.bind("<Button-1>", self.start_move)

        # LINEA SUPERIORE SFUMATA SU CANVAS
        self.divider_top = tk.Canvas(self.root, width=400, height=2, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.divider_top.pack(fill=tk.NONE, pady=(0, 5))
        self.draw_fade_line_on_canvas(self.divider_top, 400, 2, self.LINE_COLOR, self.BG_RGB)

        self.content_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        for lang, data in TRANSLATIONS.items():
            self.flag_images[lang] = self.get_flag_image(data["code"])

        # Dimensione unificata standard a 115x32
        self.bg_box_norm = self.create_rounded_rect_image(115, 32, radius=8, fill_color=(42, 42, 42), outline_color=(68, 68, 68))
        self.bg_box_hover = self.create_rounded_rect_image(115, 32, radius=8, fill_color=(53, 53, 53), outline_color=(90, 90, 90))

        # --- SEZIONE LINGUA ---
        self.lang_container = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        self.lang_container.place(x=20, y=5)

        self.lbl_lang_header = tk.Label(
            self.lang_container,
            text=TRANSLATIONS[self.current_language]["lang_label"],
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        self.lbl_lang_header.pack(fill=tk.X, pady=(0, 2))

        self.btn_lang_canvas = tk.Canvas(self.lang_container, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.btn_lang_canvas.pack(anchor=tk.CENTER)
        self.lang_bg_img_id = self.btn_lang_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)

        self.btn_lang_lbl = tk.Label(
            self.btn_lang_canvas,
            image=self.flag_images.get("English"),
            text="  English  ▼",
            compound="left",
            bg=self.BTN_BG,
            fg="#DDDDDD",
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        self.btn_lang_canvas.create_window(57, 16, window=self.btn_lang_lbl)

        for widget in (self.btn_lang_canvas, self.btn_lang_lbl):
            widget.bind("<Button-1>", self.toggle_language_dropdown)
            widget.bind("<Enter>", lambda e: (self.btn_lang_canvas.itemconfig(self.lang_bg_img_id, image=self.bg_box_hover), self.btn_lang_lbl.config(bg=self.BTN_HOVER)))
            widget.bind("<Leave>", lambda e: (self.btn_lang_canvas.itemconfig(self.lang_bg_img_id, image=self.bg_box_norm), self.btn_lang_lbl.config(bg=self.BTN_BG)))

        # --- SEZIONE TEMA ---
        self.theme_container = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        self.theme_container.place(x=305, y=5)

        self.lbl_theme_header = tk.Label(
            self.theme_container,
            text=TRANSLATIONS[self.current_language]["theme_label"],
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        self.lbl_theme_header.pack(fill=tk.X, pady=(0, 2))

        self.btn_theme_canvas = tk.Canvas(self.theme_container, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.btn_theme_canvas.pack(anchor=tk.CENTER)
        self.theme_bg_img_id = self.btn_theme_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)

        init_theme_str = TRANSLATIONS[self.current_language]["themes"][self.current_theme]
        self.btn_theme_lbl = tk.Label(
            self.btn_theme_canvas,
            image=self.theme_icons.get("Dark"),
            text=f"  {init_theme_str}  ▼",
            compound="left",
            bg=self.BTN_BG,
            fg="#DDDDDD",
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        self.btn_theme_canvas.create_window(57, 16, window=self.btn_theme_lbl)

        for widget in (self.btn_theme_canvas, self.btn_theme_lbl):
            widget.bind("<Button-1>", self.toggle_theme_dropdown)
            widget.bind("<Enter>", lambda e: (self.btn_theme_canvas.itemconfig(self.theme_bg_img_id, image=self.bg_box_hover), self.btn_theme_lbl.config(bg=self.BTN_HOVER)))
            widget.bind("<Leave>", lambda e: (self.btn_theme_canvas.itemconfig(self.theme_bg_img_id, image=self.bg_box_norm), self.btn_theme_lbl.config(bg=self.BTN_BG)))

        # --- IMMAGINE KBOMB CENTRATA ---
        img_path = os.path.join("images", "kbomb.png")
        if os.path.exists(img_path):
            try:
                self.kb_base_img = Image.open(img_path)
                self.lbl_kb_img = tk.Label(self.content_frame, bg=self.BG_COLOR)
                self.lbl_kb_img.place(relx=0.5, y=5, anchor=tk.N)
            except Exception as e:
                print(f"Errore caricamento kbomb.png: {e}")

        # LINEA CENTRALE SFUMATA SU CANVAS
        self.divider_mid = tk.Canvas(self.content_frame, width=360, height=2, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.draw_fade_line_on_canvas(self.divider_mid, 360, 2, self.LINE_COLOR, self.BG_RGB)

        # --- SEZIONE SLIDER ---
        self.slider_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)

        self.lbl_slider_title = tk.Label(
            self.slider_frame,
            text=TRANSLATIONS[self.current_language]["slider_label"],
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            font=("Segoe UI Semibold", 11)
        )
        self.lbl_slider_title.pack(pady=(0, 6))

        self.slider_canvas = tk.Canvas(
            self.slider_frame,
            width=360,
            height=30,
            bg=self.BG_COLOR,
            highlightthickness=0,
            cursor="hand2"
        )
        self.slider_canvas.pack()
        self.slider_canvas.bind("<Button-1>", self.on_slider_click)
        self.slider_canvas.bind("<B1-Motion>", self.on_slider_drag)

        # --- LAYOUT CONTROLLI INFERIORE ---
        self.bottom_controls = tk.Frame(self.slider_frame, bg=self.BG_COLOR, width=360)
        self.bottom_controls.pack(fill=tk.X, pady=(15, 0))

        # 1. SINISTRA: "Number of Kirby"
        self.left_box = tk.Frame(self.bottom_controls, bg=self.BG_COLOR, width=115)
        self.left_box.pack(side=tk.LEFT)

        self.lbl_num_header = tk.Label(
            self.left_box,
            text=TRANSLATIONS[self.current_language]["num_header"],
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        self.lbl_num_header.pack(fill=tk.X, pady=(0, 2))

        self.num_canvas = tk.Canvas(self.left_box, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.num_canvas.pack(anchor=tk.CENTER)
        self.num_bg_img_id = self.num_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)

        self.ent_kirby_num = tk.Entry(
            self.num_canvas,
            bg=self.BTN_BG,
            fg="#0078D4",
            font=("Segoe UI Black", 9),
            bd=0,
            highlightthickness=0,
            insertbackground="#FFFFFF",
            justify="center"
        )
        self.num_canvas.create_window(57, 16, window=self.ent_kirby_num, width=70, height=20)
        self.ent_kirby_num.bind("<Return>", self.on_number_input_change)
        self.ent_kirby_num.bind("<FocusOut>", self.on_number_input_change)

        # 3. DESTRA: "Kirby mode"
        self.right_box = tk.Frame(self.bottom_controls, bg=self.BG_COLOR, width=115)
        self.right_box.pack(side=tk.RIGHT)

        self.lbl_mode_header = tk.Label(
            self.right_box,
            text=TRANSLATIONS[self.current_language]["mode_header"],
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        self.lbl_mode_header.pack(fill=tk.X, pady=(0, 2))

        self.btn_mode_canvas = tk.Canvas(self.right_box, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.btn_mode_canvas.pack(anchor=tk.CENTER)
        self.mode_bg_img_id = self.btn_mode_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)

        init_mode_str = TRANSLATIONS[self.current_language]["modes"][self.current_mode]
        self.btn_mode_lbl = tk.Label(
            self.btn_mode_canvas,
            text=f"{init_mode_str}  ▼",
            bg=self.BTN_BG,
            fg="#DDDDDD",
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        self.btn_mode_canvas.create_window(57, 16, window=self.btn_mode_lbl)

        for widget in (self.btn_mode_canvas, self.btn_mode_lbl):
            widget.bind("<Button-1>", self.toggle_mode_dropdown)
            widget.bind("<Enter>", lambda e: (self.btn_mode_canvas.itemconfig(self.mode_bg_img_id, image=self.bg_box_hover), self.btn_mode_lbl.config(bg=self.BTN_HOVER)))
            widget.bind("<Leave>", lambda e: (self.btn_mode_canvas.itemconfig(self.mode_bg_img_id, image=self.bg_box_norm), self.btn_mode_lbl.config(bg=self.BTN_BG)))

        # 2. CENTRO: "Randomizer"
        self.center_box = tk.Frame(self.bottom_controls, bg=self.BG_COLOR, width=115)
        self.center_box.pack(side=tk.LEFT, expand=True)

        self.lbl_rand_header = tk.Label(
            self.center_box,
            text=TRANSLATIONS[self.current_language]["rand_header"],
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        self.lbl_rand_header.pack(fill=tk.X, pady=(0, 2))

        self.dice_icon = self.draw_dice_icon(size=14)

        self.btn_rand_canvas = tk.Canvas(self.center_box, width=115, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.btn_rand_canvas.pack(anchor=tk.CENTER)
        self.rand_bg_img_id = self.btn_rand_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)

        self.btn_rand_lbl = tk.Label(
            self.btn_rand_canvas,
            image=self.dice_icon,
            text=f"  {TRANSLATIONS[self.current_language]['rand_btn']}",
            compound="left",
            bg=self.BTN_BG,
            fg="#DDDDDD",
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        self.btn_rand_canvas.create_window(57, 16, window=self.btn_rand_lbl)

        for widget in (self.btn_rand_canvas, self.btn_rand_lbl):
            widget.bind("<Button-1>", self.on_randomize_click)
            widget.bind("<Enter>", lambda e: (self.btn_rand_canvas.itemconfig(self.rand_bg_img_id, image=self.bg_box_hover), self.btn_rand_lbl.config(bg=self.BTN_HOVER)))
            widget.bind("<Leave>", lambda e: (self.btn_rand_canvas.itemconfig(self.rand_bg_img_id, image=self.bg_box_norm), self.btn_rand_lbl.config(bg=self.BTN_BG)))

        # LINEA INFERIORE SFUMATA SU CANVAS (SOTTO LE 3 CASELLE)
        self.divider_bottom = tk.Canvas(self.slider_frame, width=360, height=2, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.divider_bottom.pack(pady=(14, 0))
        self.draw_fade_line_on_canvas(self.divider_bottom, 360, 2, self.LINE_COLOR, self.BG_RGB)

        # --- SEZIONE BOTTONI DI AZIONE (RELEASE / KILL) ---
        self.bg_green_norm = self.create_rounded_rect_image(170, 36, radius=10, fill_color=(40, 167, 69), outline_color=(30, 130, 50))
        self.bg_green_hover = self.create_rounded_rect_image(170, 36, radius=10, fill_color=(48, 195, 82), outline_color=(35, 150, 60))

        self.bg_red_norm = self.create_rounded_rect_image(170, 36, radius=10, fill_color=(220, 53, 69), outline_color=(175, 35, 50))
        self.bg_red_hover = self.create_rounded_rect_image(170, 36, radius=10, fill_color=(240, 70, 85), outline_color=(195, 45, 60))

        self.action_buttons_frame = tk.Frame(self.slider_frame, bg=self.BG_COLOR, width=360)
        self.action_buttons_frame.pack(fill=tk.X, pady=(14, 0))

        # 1. BOTTONE VERDE (RELEASE)
        self.btn_release_canvas = tk.Canvas(self.action_buttons_frame, width=170, height=36, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.btn_release_canvas.pack(side=tk.LEFT)
        self.release_bg_id = self.btn_release_canvas.create_image(0, 0, image=self.bg_green_norm, anchor=tk.NW)

        self.btn_release_lbl = tk.Label(
            self.btn_release_canvas,
            text="Release all Kirby :)",
            bg="#28A745",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        )
        self.btn_release_canvas.create_window(85, 18, window=self.btn_release_lbl)

        for widget in (self.btn_release_canvas, self.btn_release_lbl):
            widget.bind("<Button-1>", self.on_release_kirby)
            widget.bind("<Enter>", lambda e: (self.btn_release_canvas.itemconfig(self.release_bg_id, image=self.bg_green_hover), self.btn_release_lbl.config(bg="#30C352")))
            widget.bind("<Leave>", lambda e: (self.btn_release_canvas.itemconfig(self.release_bg_id, image=self.bg_green_norm), self.btn_release_lbl.config(bg="#28A745")))

        # 2. BOTTONE ROSSO (KILL)
        self.btn_kill_canvas = tk.Canvas(self.action_buttons_frame, width=170, height=36, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2", bd=0)
        self.btn_kill_canvas.pack(side=tk.RIGHT)
        self.kill_bg_id = self.btn_kill_canvas.create_image(0, 0, image=self.bg_red_norm, anchor=tk.NW)

        self.btn_kill_lbl = tk.Label(
            self.btn_kill_canvas,
            text="Kill all Kirby :(",
            bg="#DC3545",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        )
        self.btn_kill_canvas.create_window(85, 18, window=self.btn_kill_lbl)

        for widget in (self.btn_kill_canvas, self.btn_kill_lbl):
            widget.bind("<Button-1>", self.on_kill_kirby)
            widget.bind("<Enter>", lambda e: (self.btn_kill_canvas.itemconfig(self.kill_bg_id, image=self.bg_red_hover), self.btn_kill_lbl.config(bg="#F04655")))
            widget.bind("<Leave>", lambda e: (self.btn_kill_canvas.itemconfig(self.kill_bg_id, image=self.bg_red_norm), self.btn_kill_lbl.config(bg="#DC3545")))

        # LINEA INFERIORE SFUMATA (SOTTO I BOTTONI AZIONE)
        self.divider_footer = tk.Canvas(self.slider_frame, width=360, height=2, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.divider_footer.pack(pady=(10, 0))
        self.draw_fade_line_on_canvas(self.divider_footer, 360, 2, self.LINE_COLOR, self.BG_RGB)

        # --- SEZIONE FOOTER ---
        self.footer_frame = tk.Frame(self.slider_frame, bg=self.BG_COLOR)
        self.footer_frame.pack(pady=(4, 0))

        self.lbl_made_by = tk.Label(
            self.footer_frame,
            text="Made by Aken",
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 8, "bold")
        )
        self.lbl_made_by.pack(side=tk.TOP)

        # LINEA DRITTA SOLIDA (NON SFUMATA) CORTE
        self.short_solid_line = tk.Canvas(self.footer_frame, width=260, height=1, bg=self.BG_COLOR, highlightthickness=0, bd=0)
        self.short_solid_line.pack(pady=(3, 3))
        self.solid_line_id = self.short_solid_line.create_line(0, 0, 260, 0, fill=self.SOLID_LINE_COLOR, width=1)

        # CITAZIONE CENTRATA
        quote_text = "True freedom lies in the unhindered flow of ideas—whether expressed through open code or spoken words, both are essential languages of human thought that belong to all of humanity."
        self.lbl_quote = tk.Label(
            self.footer_frame,
            text=quote_text,
            bg=self.BG_COLOR,
            fg=self.SUBTEXT_COLOR,
            font=("Segoe UI", 8, "italic"),
            wraplength=350,
            justify="center"
        )
        self.lbl_quote.pack(side=tk.TOP)

        self.update_kirby_image()
        self.draw_custom_slider()

if __name__ == "__main__":
    root = tk.Tk()
    app = KirbyBomberApp(root)
    root.mainloop()