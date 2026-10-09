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

ORIGINAL_TITLE = "KIRBY BOMBER : DESTROYER OF PC"

TRANSLATIONS = {
    "English": {
        "code": "gb",
        "lang_label": "Language",
        "title": ORIGINAL_TITLE,
        "slider_label": "How many Kirby do you want?",
        "rand_header": "Randomizer",
        "rand_btn": "Randomize",
        "num_header": "Kirby Number",
        "mode_header": "Kirby Mode"
    },
    "Italian": {
        "code": "it",
        "lang_label": "Lingua",
        "title": ORIGINAL_TITLE,
        "slider_label": "Quanti Kirby vuoi?",
        "rand_header": "Randomizzatore",
        "rand_btn": "Randomizza",
        "num_header": "Numero Kirby",
        "mode_header": "Modalità Kirby"
    },
    "Portuguese": {
        "code": "pt",
        "lang_label": "Idioma",
        "title": ORIGINAL_TITLE,
        "slider_label": "Quantos Kirby você quer?",
        "rand_header": "Randomizador",
        "rand_btn": "Randomizar",
        "num_header": "Número Kirby",
        "mode_header": "Modo Kirby"
    },
    "Spanish": {
        "code": "es",
        "lang_label": "Idioma",
        "title": ORIGINAL_TITLE,
        "slider_label": "¿Cuántos Kirby quieres?",
        "rand_header": "Aleatorio",
        "rand_btn": "Randomizar",
        "num_header": "Número Kirby",
        "mode_header": "Modo Kirby"
    },
    "Japanese": {
        "code": "jp",
        "lang_label": "言語",
        "title": ORIGINAL_TITLE,
        "slider_label": "カービィは何体欲しいですか？",
        "rand_header": "ランダム",
        "rand_btn": "ランダム",
        "num_header": "カービィの数",
        "mode_header": "カービィモード"
    },
    "Korean": {
        "code": "kr",
        "lang_label": "언어",
        "title": ORIGINAL_TITLE,
        "slider_label": "얼마나 많은 커비를 원하십니까?",
        "rand_header": "랜덤",
        "rand_btn": "랜덤",
        "num_header": "커비 수",
        "mode_header": "커비 모드"
    },
    "Chinese": {
        "code": "cn",
        "lang_label": "语言",
        "title": ORIGINAL_TITLE,
        "slider_label": "你想要多少个星之卡比？",
        "rand_header": "随机",
        "rand_btn": "随机化",
        "num_header": "卡比数量",
        "mode_header": "卡比模式"
    }
}

KIRBY_MODES = ["Modern", "Retro"]

class KirbyBomberApp:
    def __init__(self, root):
        self.root = root
        self.root.title(ORIGINAL_TITLE)
        
        self.width = 440
        self.height = 600
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.overrideredirect(True)

        self.BG_COLOR = "#1A1A1A"
        self.TEXT_COLOR = "#888888"
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
        self.kb_base_img = None
        self.thumb_cache = {}
        self.dropdown_canvas = None

        self.download_flags()
        self.setup_ui()
        self.center_window()
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        enable_native_rounded_corners(self.root)

        self.root.bind("<Map>", self.on_restore)

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

        self.slider_canvas.create_line(margin, cy, margin + usable_w, cy, fill="#333333", width=3, capstyle="round")
        
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
            screenshot = Image.new("RGBA", (w, h), (26, 26, 26, 255))

        blurred = screenshot.filter(ImageFilter.GaussianBlur(radius=8))
        enhancer = ImageEnhance.Brightness(blurred)
        self.blurred_dark = enhancer.enhance(0.65).convert("RGBA")

        if active_dropdown == "language":
            widgets_to_reveal = [(self.lbl_lang_header, None), (self.divider_lang, None), (self.btn_lang_canvas, 8)]
        else:
            widgets_to_reveal = [(self.lbl_mode_header, None), (self.btn_mode_canvas, 8)]

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
        
        # Chiamata alla classe base tk.Widget per sollevare il widget Canvas
        tk.Widget.tkraise(self.lbl_blur_overlay)

    def remove_blur_overlay(self):
        self.lbl_blur_overlay.place_forget()

    def show_dropdown(self, dropdown_type):
        self.active_dropdown_type = dropdown_type
        if dropdown_type == "language":
            items = [(lang, f"  {lang}", self.flag_images.get(lang)) for lang in TRANSLATIONS.keys()]
            target_canvas = self.btn_lang_canvas
        else:
            items = [(mode, f"  {mode}", None) for mode in KIRBY_MODES]
            target_canvas = self.btn_mode_canvas

        width = 110
        box_x = target_canvas.winfo_rootx() - self.root.winfo_rootx()
        box_center_x = box_x + (target_canvas.winfo_width() / 2)
        x = int(box_center_x - (width / 2))
        y = target_canvas.winfo_rooty() - self.root.winfo_rooty() + target_canvas.winfo_height() + 4

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
        draw.rounded_rectangle([scale, scale, sw - scale, sh - scale], radius=sr, fill=(37, 37, 37, 255), outline=(68, 68, 68, 255), width=scale)
        mask_small = mask.resize((width, height), Image.Resampling.LANCZOS)

        combined = Image.alpha_composite(crop, mask_small)
        self.dd_bg_img = ImageTk.PhotoImage(combined)

        self.dropdown_canvas = tk.Canvas(self.root, width=width, height=height, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.dropdown_canvas.create_image(0, 0, image=self.dd_bg_img, anchor=tk.NW)

        self.hover_img = self.create_rounded_rect_image(width - 12, item_h, radius=6, fill_color=(80, 80, 80), outline_color=(80, 80, 80))
        self.hover_canvas_img = self.dropdown_canvas.create_image(6, -100, image=self.hover_img, anchor=tk.NW)

        self.dropdown_items_data = []
        for i, item in enumerate(items):
            id_str, text, img = item
            iy = pad_y + i * item_h
            if img:
                self.dropdown_canvas.create_image(12, iy + item_h // 2, image=img, anchor=tk.W)
                text_id = self.dropdown_canvas.create_text(36, iy + item_h // 2, text=text, fill="#DDDDDD", font=("Segoe UI", 8, "bold"), anchor=tk.W)
            else:
                text_id = self.dropdown_canvas.create_text(width // 2, iy + item_h // 2, text=text, fill="#DDDDDD", font=("Segoe UI", 8, "bold"), anchor=tk.CENTER)

            self.dropdown_items_data.append({"id": id_str, "y1": iy, "y2": iy + item_h})

        self.dropdown_canvas.place(x=x, y=y)
        
        # Chiamata alla classe base tk.Widget per sollevare il widget Canvas
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

    def select_language(self, lang_name):
        self.current_language = lang_name
        data = TRANSLATIONS[lang_name]

        flag_img = self.flag_images.get(lang_name)
        if flag_img:
            self.btn_lang_lbl.config(image=flag_img, text=f"  {lang_name}  ▼", compound="left")
        else:
            self.btn_lang_lbl.config(image="", text=f"{lang_name}  ▼")

        self.lbl_lang_header.config(text=data['lang_label'])
        self.lbl_title.config(text=data['title'])
        self.lbl_slider_title.config(text=data['slider_label'])
        
        self.lbl_rand_header.config(text=data['rand_header'])
        self.btn_rand_lbl.config(text=f"  {data['rand_btn']}")
        
        self.lbl_num_header.config(text=data['num_header'])
        self.lbl_mode_header.config(text=data['mode_header'])
        
        self.align_title_center()
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
        self.btn_mode_lbl.config(text=f"{mode_name}  ▼")
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

        self.btns_frame = tk.Frame(self.title_bar, bg=self.BG_COLOR)
        self.btns_frame.place(relx=1.0, rely=0.5, x=-18, anchor=tk.E)

        self.gear_icon_norm = self.draw_simple_gear_icon(size=16, color=(119, 119, 119))
        self.gear_icon_hover = self.draw_simple_gear_icon(size=16, color=(221, 221, 221))

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

        title_text = TRANSLATIONS[self.current_language]["title"]
        self.lbl_title = tk.Label(
            self.title_bar, 
            text=title_text, 
            bg=self.BG_COLOR, 
            fg="#ECECEC", 
            font=("Bahnschrift SemiCondensed", 13)
        )
        self.align_title_center()

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.lbl_title.bind("<Button-1>", self.start_move)
        self.lbl_title.bind("<B1-Motion>", self.do_move)
        lbl_version.bind("<Button-1>", self.start_move)

        self.fade_line_top = self.generate_fade_line(width=400, height=2, color=(100, 100, 100))
        self.divider_top = tk.Label(self.root, image=self.fade_line_top, bg=self.BG_COLOR, bd=0, highlightthickness=0)
        self.divider_top.pack(fill=tk.X, padx=20, pady=(0, 5))

        content_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True)

        for lang, data in TRANSLATIONS.items():
            self.flag_images[lang] = self.get_flag_image(data["code"])

        self.bg_box_norm = self.create_rounded_rect_image(110, 32, radius=8, fill_color=(42, 42, 42), outline_color=(68, 68, 68))
        self.bg_box_hover = self.create_rounded_rect_image(110, 32, radius=8, fill_color=(53, 53, 53), outline_color=(90, 90, 90))
        
        self.bg_lang_norm = self.create_rounded_rect_image(110, 32, radius=8, fill_color=(42, 42, 42), outline_color=(68, 68, 68))
        self.bg_lang_hover = self.create_rounded_rect_image(110, 32, radius=8, fill_color=(53, 53, 53), outline_color=(90, 90, 90))

        # --- SEZIONE LINGUA ---
        self.lang_container = tk.Frame(content_frame, bg=self.BG_COLOR)
        self.lang_container.place(x=20, y=5)

        self.lbl_lang_header = tk.Label(
            self.lang_container,
            text=TRANSLATIONS[self.current_language]["lang_label"],
            bg=self.BG_COLOR,
            fg="#777777",
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        self.lbl_lang_header.pack(fill=tk.X, pady=(0, 2))

        self.fade_line_lang = self.generate_fade_line(width=110, height=1, color=(100, 100, 100))
        self.divider_lang = tk.Label(self.lang_container, image=self.fade_line_lang, bg=self.BG_COLOR, bd=0, highlightthickness=0)
        self.divider_lang.pack(fill=tk.X, pady=(0, 4))

        self.btn_lang_canvas = tk.Canvas(self.lang_container, width=110, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.btn_lang_canvas.pack(anchor=tk.CENTER)
        self.lang_bg_img_id = self.btn_lang_canvas.create_image(0, 0, image=self.bg_lang_norm, anchor=tk.NW)

        self.btn_lang_lbl = tk.Label(
            self.btn_lang_canvas,
            image=self.flag_images.get("English"),
            text="  English  ▼",
            compound="left",
            bg="#2A2A2A",
            fg="#DDDDDD",
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        self.btn_lang_canvas.create_window(55, 16, window=self.btn_lang_lbl)

        for widget in (self.btn_lang_canvas, self.btn_lang_lbl):
            widget.bind("<Button-1>", self.toggle_language_dropdown)
            widget.bind("<Enter>", lambda e: (self.btn_lang_canvas.itemconfig(self.lang_bg_img_id, image=self.bg_lang_hover), self.btn_lang_lbl.config(bg="#353535")))
            widget.bind("<Leave>", lambda e: (self.btn_lang_canvas.itemconfig(self.lang_bg_img_id, image=self.bg_lang_norm), self.btn_lang_lbl.config(bg="#2A2A2A")))

        # --- IMMAGINE KBOMB ---
        img_path = os.path.join("images", "kbomb.png")
        if os.path.exists(img_path):
            try:
                self.kb_base_img = Image.open(img_path)
                self.lbl_kb_img = tk.Label(content_frame, bg=self.BG_COLOR)
                self.lbl_kb_img.place(relx=0.5, y=5, anchor=tk.N)
            except Exception as e:
                print(f"Errore caricamento kbomb.png: {e}")

        self.fade_line_mid = self.generate_fade_line(width=360, height=2, color=(90, 90, 90))
        self.divider_mid = tk.Label(content_frame, image=self.fade_line_mid, bg=self.BG_COLOR, bd=0, highlightthickness=0)

        # --- SEZIONE SLIDER ---
        self.slider_frame = tk.Frame(content_frame, bg=self.BG_COLOR)

        self.lbl_slider_title = tk.Label(
            self.slider_frame,
            text=TRANSLATIONS[self.current_language]["slider_label"],
            bg=self.BG_COLOR,
            fg="#CCCCCC",
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
        bottom_controls = tk.Frame(self.slider_frame, bg=self.BG_COLOR, width=360)
        bottom_controls.pack(fill=tk.X, pady=(15, 0))

        # 1. SINISTRA: "Kirby Number"
        left_box = tk.Frame(bottom_controls, bg=self.BG_COLOR)
        left_box.pack(side=tk.LEFT)

        self.lbl_num_header = tk.Label(
            left_box,
            text=TRANSLATIONS[self.current_language]["num_header"],
            bg=self.BG_COLOR,
            fg="#777777",
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        self.lbl_num_header.pack(fill=tk.X, pady=(0, 3))

        num_canvas = tk.Canvas(left_box, width=110, height=32, bg=self.BG_COLOR, highlightthickness=0)
        num_canvas.pack()
        num_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)

        self.ent_kirby_num = tk.Entry(
            num_canvas,
            bg="#2A2A2A",
            fg="#0078D4",
            font=("Segoe UI Black", 10),
            width=6,
            bd=0,
            highlightthickness=0,
            insertbackground="#FFFFFF",
            justify="center"
        )
        num_canvas.create_window(55, 16, window=self.ent_kirby_num)
        self.ent_kirby_num.bind("<Return>", self.on_number_input_change)
        self.ent_kirby_num.bind("<FocusOut>", self.on_number_input_change)

        # 3. DESTRA: "Kirby mode"
        right_box = tk.Frame(bottom_controls, bg=self.BG_COLOR)
        right_box.pack(side=tk.RIGHT)

        self.lbl_mode_header = tk.Label(
            right_box,
            text=TRANSLATIONS[self.current_language]["mode_header"],
            bg=self.BG_COLOR,
            fg="#777777",
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        self.lbl_mode_header.pack(fill=tk.X, pady=(0, 3))

        self.btn_mode_canvas = tk.Canvas(right_box, width=110, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.btn_mode_canvas.pack()
        self.mode_bg_img_id = self.btn_mode_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)

        self.btn_mode_lbl = tk.Label(
            self.btn_mode_canvas,
            text="Modern  ▼",
            bg="#2A2A2A",
            fg="#DDDDDD",
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        self.btn_mode_canvas.create_window(55, 16, window=self.btn_mode_lbl)

        for widget in (self.btn_mode_canvas, self.btn_mode_lbl):
            widget.bind("<Button-1>", self.toggle_mode_dropdown)
            widget.bind("<Enter>", lambda e: (self.btn_mode_canvas.itemconfig(self.mode_bg_img_id, image=self.bg_box_hover), self.btn_mode_lbl.config(bg="#353535")))
            widget.bind("<Leave>", lambda e: (self.btn_mode_canvas.itemconfig(self.mode_bg_img_id, image=self.bg_box_norm), self.btn_mode_lbl.config(bg="#2A2A2A")))

        # 2. CENTRO: "Randomize"
        center_box = tk.Frame(bottom_controls, bg=self.BG_COLOR)
        center_box.pack(side=tk.LEFT, expand=True)

        self.lbl_rand_header = tk.Label(
            center_box,
            text=TRANSLATIONS[self.current_language]["rand_header"],
            bg=self.BG_COLOR,
            fg="#777777",
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        self.lbl_rand_header.pack(fill=tk.X, pady=(0, 3))

        self.dice_icon = self.draw_dice_icon(size=14)

        self.btn_rand_canvas = tk.Canvas(center_box, width=110, height=32, bg=self.BG_COLOR, highlightthickness=0, cursor="hand2")
        self.btn_rand_canvas.pack(anchor=tk.CENTER)
        self.rand_bg_img_id = self.btn_rand_canvas.create_image(0, 0, image=self.bg_box_norm, anchor=tk.NW)

        self.btn_rand_lbl = tk.Label(
            self.btn_rand_canvas,
            image=self.dice_icon,
            text=f"  {TRANSLATIONS[self.current_language]['rand_btn']}",
            compound="left",
            bg="#2A2A2A",
            fg="#DDDDDD",
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        self.btn_rand_canvas.create_window(55, 16, window=self.btn_rand_lbl)

        for widget in (self.btn_rand_canvas, self.btn_rand_lbl):
            widget.bind("<Button-1>", self.on_randomize_click)
            widget.bind("<Enter>", lambda e: (self.btn_rand_canvas.itemconfig(self.rand_bg_img_id, image=self.bg_box_hover), self.btn_rand_lbl.config(bg="#353535")))
            widget.bind("<Leave>", lambda e: (self.btn_rand_canvas.itemconfig(self.rand_bg_img_id, image=self.bg_box_norm), self.btn_rand_lbl.config(bg="#2A2A2A")))

        self.update_kirby_image()
        self.draw_custom_slider()

if __name__ == "__main__":
    root = tk.Tk()
    app = KirbyBomberApp(root)
    root.mainloop()