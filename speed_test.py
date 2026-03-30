"""
Basic Speed Test - Modern Internet Speed Testing Application
A sleek, dark-themed speed test application with animated gauges.
"""

import sys
import os

# ─── EXE Fix for speedtest-cli (Python 3.10+ & PyInstaller) ────────────────────
# This avoids the 'NoneType object has no attribute fileno' and '__builtin__' errors
# which occur in windowed EXE environments.

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

if not hasattr(builtins, '__builtin__'):
    builtins.__builtin__ = builtins

# Ensure standard streams exist for libraries that expect a terminal (fileno)
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')
if sys.stdin is None:
    sys.stdin = open(os.devnull, 'r')

import customtkinter as ctk
import threading
import speedtest
import requests
import time
import math
import json
import os
from datetime import datetime
from tkinter import Canvas

# ─── Translations & Languages ─────────────────────────────────────────────────

TRANSLATIONS = {
    "TR": {
        "title": "Basic Speed Test",
        "ip_lbl": "IP Adresi",
        "loc_lbl": "Konum",
        "isp_lbl": "ISP",
        "srv_lbl": "Sunucu",
        "sec_lbl": "Güvenlik",
        "coord_lbl": "Koordinatlar",
        "zip_lbl": "Posta Kodu",
        "as_lbl": "AS Numarası",
        "sec_safe": "🟢 Güvenli (Yerel)",
        "sec_vpn": "🔴 VPN / Proxy / DC",
        "dl_lbl": "Download",
        "ul_lbl": "Upload",
        "ping_lbl": "Ping",
        "jit_lbl": "Jitter",
        "sched_lbl": "⏱ Zamanlanmış Test:",
        "sch_1m": "1 Dakika", "sch_10m": "10 Dakika", "sch_30m": "30 Dakika", 
        "sch_1h": "1 Saat", "sch_2h": "2 Saat", "sch_4h": "4 Saat",
        "toggle_on": "Açık", "toggle_off": "Kapalı", "toggle_text": "Aç/Kapat",
        "start_btn": "▶  Testi Başlat",
        "ready": "Teste hazır",
        "history_btn": "📋 Geçmiş",
        "not_found": "Bulunamadı",
        "finding_srv": "Sunucu aranıyor...",
        "best_srv": "En iyi sunucu seçiliyor...",
        "dl_test": "Download testi yapılıyor...",
        "ul_test": "Upload testi yapılıyor...",
        "success": "✅ Test tamamlandı!",
        "error": "❌ Hata: {}",
        "testing": "⏳ Test Yapılıyor...",
        "test_starting": "⏳ Test Başlıyor...",
        "next_test": "Sonraki Test: {}",
        "test_running_next": "Sürüyor... (Sonraki: {})",
        "hist_title": "Test Geçmişi",
        "clear_btn": "🗑 Temizle",
        "date_lbl": "Tarih",
        "no_hist": "Henüz test geçmişi yok",
        "no_hist_desc": "İlk testi başlatmak için ana ekrandaki butona tıklayın."
    },
    "EN": {
        "title": "Basic Speed Test",
        "ip_lbl": "IP Address",
        "loc_lbl": "Location",
        "isp_lbl": "ISP",
        "srv_lbl": "Server",
        "sec_lbl": "Security",
        "coord_lbl": "Coordinates",
        "zip_lbl": "ZIP Code",
        "as_lbl": "AS Number",
        "sec_safe": "🟢 Safe (Local)",
        "sec_vpn": "🔴 VPN / Proxy / DC",
        "dl_lbl": "Download",
        "ul_lbl": "Upload",
        "ping_lbl": "Ping",
        "jit_lbl": "Jitter",
        "sched_lbl": "⏱ Scheduled Test:",
        "sch_1m": "1 Minute", "sch_10m": "10 Minutes", "sch_30m": "30 Minutes", 
        "sch_1h": "1 Hour", "sch_2h": "2 Hours", "sch_4h": "4 Hours",
        "toggle_on": "On", "toggle_off": "Off", "toggle_text": "On/Off",
        "start_btn": "▶  Start Test",
        "ready": "Ready to test",
        "history_btn": "📋 History",
        "not_found": "Not Found",
        "finding_srv": "Finding server...",
        "best_srv": "Selecting best server...",
        "dl_test": "Testing download...",
        "ul_test": "Testing upload...",
        "success": "✅ Test completed!",
        "error": "❌ Error: {}",
        "testing": "⏳ Testing...",
        "test_starting": "⏳ Test Starting...",
        "next_test": "Next Test: {}",
        "test_running_next": "Running... (Next: {})",
        "hist_title": "Test History",
        "clear_btn": "🗑 Clear",
        "date_lbl": "Date",
        "no_hist": "No test history yet",
        "no_hist_desc": "Click the button on the main screen to start your first test."
    }
}

SCHED_MAP = {
    "TR": ["1 Dakika", "10 Dakika", "30 Dakika", "1 Saat", "2 Saat", "4 Saat"],
    "EN": ["1 Minute", "10 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours"]
}

def translate_time(val_str, to_lang="EN"):
    if to_lang == "EN":
        return val_str.replace("Dakika", "Minute").replace("Minutes", "Minutes").replace("Saat", "Hour").replace("Hours", "Hours")
    else:
        return val_str.replace("Minute", "Dakika").replace("Minutes", "Dakika").replace("Hour", "Saat").replace("Hours", "Saat")

# ─── Theme & Color Configuration ───────────────────────────────────────────────

COLORS = {
    "bg_dark":       "#0D0D0D",
    "bg_card":       "#1A1A1A",
    "bg_card_hover": "#222222",
    "bg_input":      "#2A2A2A",
    "border":        "#333333",
    "border_light":  "#444444",
    "text_primary":  "#FFFFFF",
    "text_secondary":"#AAAAAA",
    "text_muted":    "#666666",
    "accent_cyan":   "#00D4FF",
    "accent_purple": "#8B5CF6",
    "accent_green":  "#10B981",
    "accent_orange": "#F59E0B",
    "accent_red":    "#EF4444",
    "accent_pink":   "#EC4899",
    "gauge_bg":      "#1F1F1F",
    "gauge_track":   "#2D2D2D",
    "gradient_start":"#00D4FF",
    "gradient_end":  "#8B5CF6",
}


# ─── Animated Gauge Widget ─────────────────────────────────────────────────────

class SpeedGauge(Canvas):
    """A custom animated speed gauge widget with arc display."""

    def __init__(self, master, size=220, max_speed=1000, label="Speed", unit="Mbps",
                 color_start="#00D4FF", color_end="#8B5CF6", bg_color=None, **kwargs):
        bg = bg_color or COLORS["bg_dark"]
        super().__init__(
            master, width=size, height=size,
            bg=bg, highlightthickness=0, **kwargs
        )
        self.bg_color = bg
        self.size = size
        self.max_speed = max_speed
        self.label = label
        self.unit = unit
        self.color_start = color_start
        self.color_end = color_end
        self.current_value = 0.0
        self.target_value = 0.0
        self.animation_running = False
        
        self._draw_gauge(0)

    def _interpolate_color(self, color1, color2, factor):
        """Interpolate between two hex colors."""
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw_gauge(self, value):
        """Draw the gauge with the given value."""
        self.delete("all")
        cx, cy = self.size // 2, self.size // 2
        radius = self.size // 2 - 24
        track_width = 10

        start_angle = 225
        sweep = -270

        pad = 4
        self.create_arc(
            cx - radius - pad, cy - radius - pad,
            cx + radius + pad, cy + radius + pad,
            start=start_angle, extent=sweep,
            outline=COLORS["gauge_track"], width=track_width + 8,
            style="arc"
        )

        self.create_arc(
            cx - radius, cy - radius, cx + radius, cy + radius,
            start=start_angle, extent=sweep,
            outline=COLORS["gauge_track"], width=track_width,
            style="arc"
        )

        if value > 0:
            fraction = min(value / self.max_speed, 1.0)
            value_sweep = sweep * fraction
            segments = max(int(abs(value_sweep) / 3), 1)

            for i in range(segments):
                seg_start = start_angle + (value_sweep * i / segments)
                seg_extent = value_sweep / segments
                color_factor = i / max(segments - 1, 1)
                color = self._interpolate_color(self.color_start, self.color_end, color_factor)
                self.create_arc(
                    cx - radius, cy - radius, cx + radius, cy + radius,
                    start=seg_start, extent=seg_extent,
                    outline=color, width=track_width, style="arc"
                )

            tip_angle = math.radians(start_angle + value_sweep)
            tip_x = cx + radius * math.cos(tip_angle)
            tip_y = cy - radius * math.sin(tip_angle)
            glow_r = 6
            tip_color = self._interpolate_color(self.color_start, self.color_end, fraction)
            self.create_oval(
                tip_x - glow_r, tip_y - glow_r,
                tip_x + glow_r, tip_y + glow_r,
                fill=tip_color, outline=""
            )

        num_markers = 10
        for i in range(num_markers + 1):
            angle = math.radians(start_angle + sweep * i / num_markers)
            inner_r = radius - 16
            outer_r = radius - 10
            x1 = cx + inner_r * math.cos(angle)
            y1 = cy - inner_r * math.sin(angle)
            x2 = cx + outer_r * math.cos(angle)
            y2 = cy - outer_r * math.sin(angle)

            marker_color = COLORS["text_muted"] if i % 2 != 0 else COLORS["text_secondary"]
            self.create_line(x1, y1, x2, y2, fill=marker_color, width=1)

            if i % 2 == 0:
                label_r = radius - 27
                lx = cx + label_r * math.cos(angle)
                ly = cy - label_r * math.sin(angle)
                speed_val = int(self.max_speed * i / num_markers)
                self.create_text(
                    lx, ly, text=str(speed_val),
                    fill=COLORS["text_muted"], font=("Segoe UI", 7)
                )

        display_val = f"{value:.1f}" if value < 100 else f"{value:.0f}"
        self.create_text(
            cx, cy - 8, text=display_val,
            fill=COLORS["text_primary"],
            font=("Segoe UI Semibold", 28)
        )
        self.create_text(
            cx, cy + 20, text=self.unit,
            fill=COLORS["text_secondary"],
            font=("Segoe UI", 10)
        )
        self.create_text(
            cx, cy + 38, text=self.label,
            fill=COLORS["text_muted"],
            font=("Segoe UI", 9)
        )

    def set_value(self, value, animate=True):
        self.target_value = value
        if animate and not self.animation_running:
            self.animation_running = True
            self._animate()
        elif not animate:
            self.current_value = value
            self._draw_gauge(value)
            
    def update_label(self, new_label):
        self.label = new_label
        self._draw_gauge(self.current_value)

    def _animate(self):
        diff = self.target_value - self.current_value
        if abs(diff) < 0.1:
            self.current_value = self.target_value
            self._draw_gauge(self.current_value)
            self.animation_running = False
            return
        self.current_value += diff * 0.15
        self._draw_gauge(self.current_value)
        self.after(16, self._animate)


# ─── Main Application ──────────────────────────────────────────────────────────

class SpeedTestApp(ctk.CTk):
    """Main Speed Test Application."""

    def _get_resource_path(self, relative_path):
        if getattr(sys, 'frozen', False):
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def __init__(self):
        super().__init__()
        
        # Load logic/data config
        self._load_history()

        # Window configuration
        self.title("Basic Speed Test")
        self.geometry("720x680")  # slightly taller for two-row info
        self.minsize(680, 620)
        self.configure(fg_color=COLORS["bg_dark"])

        # Try to load icon
        icon_png = self._get_resource_path("sphere.png")
        icon_ico = self._get_resource_path("sphere.ico")
        
        try:
            if os.path.exists(icon_ico):
                self.iconbitmap(icon_ico)
            elif os.path.exists(icon_png):
                from PIL import Image, ImageTk
                img = Image.open(icon_png)
                self._icon_img = ImageTk.PhotoImage(img)
                self.iconphoto(True, self._icon_img)
        except Exception as e:
            print(f"Icon loading failed: {e}")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # State variables
        self.is_testing = False
        self.auto_test_running = False
        self.remaining_seconds = 0
        self.timer_id = None
        self.lang = self.config.get("lang", "TR")

        # UI Element References
        self._labels = {}

        # Build UI
        self._create_ui()

        # Fetch IP on startup
        threading.Thread(target=self._fetch_ip_info, daemon=True).start()
        
    def _t(self, key):
        return TRANSLATIONS[self.lang].get(key, key)

    # ── UI Construction ─────────────────────────────────────────────────────

    def _create_ui(self):
        """Build the complete user interface."""

        # ── Main Content ────────────────────────────────────────────────────
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=16, pady=10)

        # ── IP & Server Info Card ───────────────────────────────────────────
        info_card = ctk.CTkFrame(
            main_container, fg_color=COLORS["bg_card"],
            corner_radius=10, border_width=1, border_color=COLORS["border"]
        )
        info_card.pack(fill="x", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=14, pady=12)

        info_items_r1 = [
            ("ip_lbl", "ip_value", "—"),
            ("loc_lbl", "location_value", "—"),
            ("isp_lbl", "isp_value", "—"),
            ("srv_lbl", "server_value", "—"),
        ]
        info_items_r2 = [
            ("sec_lbl", "security_value", "—"),
            ("coord_lbl", "coord_value", "—"),
            ("zip_lbl", "zip_value", "—"),
            ("as_lbl", "as_value", "—"),
        ]

        def create_info_row(parent, items, add_padding):
            row_frame = ctk.CTkFrame(parent, fg_color="transparent")
            row_frame.pack(fill="x", pady=(0, 12) if add_padding else 0)
            
            for i, (key, attr, default) in enumerate(items):
                col = ctk.CTkFrame(row_frame, fg_color="transparent")
                col.pack(side="left", expand=True, fill="x")

                title_lbl = ctk.CTkLabel(
                    col, text=self._t(key),
                    font=("Segoe UI", 9), text_color=COLORS["text_muted"]
                )
                title_lbl.pack(anchor="w")
                self._labels[key] = title_lbl # store ref for lang switch

                value_label = ctk.CTkLabel(
                    col, text=default,
                    font=("Segoe UI Semibold", 11), text_color=COLORS["text_primary"]
                )
                value_label.pack(anchor="w", pady=(1, 0))
                setattr(self, attr, value_label)

                if i < len(items) - 1:
                    sep = ctk.CTkFrame(
                        row_frame, fg_color=COLORS["border"],
                        width=1, height=30
                    )
                    sep.pack(side="left", padx=10, fill="y")

        create_info_row(info_inner, info_items_r1, True)
        create_info_row(info_inner, info_items_r2, False)

        # ── Live Speed Numbers Area ─────────────────────────────────────────
        live_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        live_frame.pack(fill="x", pady=(10, 20))

        # Download Gauge
        self.dl_gauge = SpeedGauge(
            live_frame, size=240, max_speed=1000, 
            label=self._t("dl_lbl"), unit="Mbps",
            color_start=COLORS["accent_cyan"], color_end=COLORS["accent_purple"],
            bg_color=COLORS["bg_dark"]
        )
        self.dl_gauge.pack(side="left", expand=True, padx=10)

        # Upload Gauge
        self.ul_gauge = SpeedGauge(
            live_frame, size=240, max_speed=1000, 
            label=self._t("ul_lbl"), unit="Mbps",
            color_start=COLORS["accent_green"], color_end=COLORS["accent_cyan"],
            bg_color=COLORS["bg_dark"]
        )
        self.ul_gauge.pack(side="left", expand=True, padx=10)

        # ── Stats Row ───────────────────────────────────────────────────────
        stats_frame = ctk.CTkFrame(
            main_container, fg_color=COLORS["bg_card"],
            corner_radius=10, border_width=1, border_color=COLORS["border"]
        )
        stats_frame.pack(fill="x", pady=(4, 10))

        stats_inner = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_inner.pack(fill="x", padx=14, pady=10)

        stat_items = [
            ("⬇", "dl_lbl", "dl_stat", "— Mbps", COLORS["accent_cyan"]),
            ("⬆", "ul_lbl", "ul_stat", "— Mbps", COLORS["accent_green"]),
            ("📶", "ping_lbl", "ping_stat", "— ms", COLORS["accent_orange"]),
            ("📊", "jit_lbl", "jitter_stat", "— ms", COLORS["accent_pink"]),
        ]

        for i, (icon, key, attr, default, color) in enumerate(stat_items):
            col = ctk.CTkFrame(stats_inner, fg_color="transparent")
            col.pack(side="left", expand=True, fill="x")

            row = ctk.CTkFrame(col, fg_color="transparent")
            row.pack(anchor="w")

            ctk.CTkLabel(
                row, text=icon, font=("Segoe UI Emoji", 11),
                text_color=color
            ).pack(side="left", padx=(0, 4))

            title_lbl = ctk.CTkLabel(
                row, text=self._t(key),
                font=("Segoe UI", 9), text_color=COLORS["text_muted"]
            )
            title_lbl.pack(side="left")
            self._labels[f"{key}_stat"] = title_lbl

            value_label = ctk.CTkLabel(
                col, text=default,
                font=("Segoe UI Semibold", 13), text_color=color
            )
            value_label.pack(anchor="w", pady=(2, 0))
            setattr(self, attr, value_label)

            if i < len(stat_items) - 1:
                sep = ctk.CTkFrame(
                    stats_inner, fg_color=COLORS["border"],
                    width=1, height=32
                )
                sep.pack(side="left", padx=10, fill="y")

        # ── Schedule Bar ────────────────────────────────────────────────────
        schedule_frame = ctk.CTkFrame(main_container, fg_color=COLORS["bg_input"], corner_radius=10, height=44)
        schedule_frame.pack(fill="x", pady=(8, 12))
        schedule_frame.pack_propagate(False)

        self.sched_title = ctk.CTkLabel(
            schedule_frame, text=self._t("sched_lbl"),
            font=("Segoe UI Semibold", 12), text_color=COLORS["text_primary"]
        )
        self.sched_title.pack(side="left", padx=(14, 10), pady=10)

        self.schedule_var = ctk.StringVar(value=SCHED_MAP[self.lang][2])
        self.schedule_cb = ctk.CTkComboBox(
            schedule_frame, values=SCHED_MAP[self.lang],
            variable=self.schedule_var, width=110, height=28,
            state="readonly", font=("Segoe UI", 11),
            fg_color=COLORS["bg_card"], border_color=COLORS["border"], button_color=COLORS["border_light"]
        )
        self.schedule_cb.pack(side="left", padx=5, pady=8)

        self.schedule_switch_var = ctk.StringVar(value="off")
        self.schedule_switch = ctk.CTkSwitch(
            schedule_frame, text=self._t("toggle_text"), font=("Segoe UI", 11), text_color=COLORS["text_secondary"],
            variable=self.schedule_switch_var, onvalue="on", offvalue="off",
            command=self._toggle_schedule,
            progress_color=COLORS["accent_purple"]
        )
        self.schedule_switch.pack(side="left", padx=15, pady=8)

        self.countdown_label = ctk.CTkLabel(
            schedule_frame, text="",
            font=("Segoe UI Semibold", 11), text_color=COLORS["accent_cyan"]
        )
        self.countdown_label.pack(side="right", padx=14, pady=10)

        # ── Bottom Bar: Button + Provider + Status + History ──────────────────
        bottom_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(2, 0))

        # Start button
        self.start_btn = ctk.CTkButton(
            bottom_frame,
            text=self._t("start_btn"),
            font=("Segoe UI Semibold", 13),
            height=38, width=160,
            corner_radius=19,
            fg_color=COLORS["accent_cyan"],
            hover_color=COLORS["accent_purple"],
            text_color=COLORS["bg_dark"],
            command=self._start_test
        )
        self.start_btn.pack(side="left")

        # Provider Selector
        self.provider_var = ctk.StringVar(value=self.config.get("provider", "Speedtest (Ookla)"))
        self.provider_cb = ctk.CTkComboBox(
            bottom_frame, values=["Speedtest (Ookla)", "Cloudflare", "LibreSpeed"],
            variable=self.provider_var, command=self._save_provider,
            width=150, height=38, font=("Segoe UI", 11), state="readonly",
            fg_color=COLORS["bg_input"], border_width=1, border_color=COLORS["border"],
            dropdown_font=("Segoe UI", 11)
        )
        self.provider_cb.pack(side="left", padx=(10, 0))

        # Status label
        self.status_label = ctk.CTkLabel(
            bottom_frame, text=self._t("ready"),
            font=("Segoe UI", 11), text_color=COLORS["text_secondary"]
        )
        self.status_label.pack(side="left", padx=(14, 10))

        # Progress bar
        self.progress = ctk.CTkProgressBar(
            bottom_frame, width=100, height=4,
            corner_radius=2,
            fg_color=COLORS["gauge_track"],
            progress_color=COLORS["accent_cyan"]
        )
        self.progress.pack(side="left", padx=(0, 10))
        self.progress.set(0)

        # History button
        self.history_btn = ctk.CTkButton(
            bottom_frame,
            text=self._t("history_btn"),
            font=("Segoe UI", 11),
            height=32, width=90,
            corner_radius=8,
            fg_color=COLORS["bg_input"],
            hover_color=COLORS["border_light"],
            text_color=COLORS["text_secondary"],
            border_width=1,
            border_color=COLORS["border"],
            command=self._show_history
        )
        self.history_btn.pack(side="right")

        # ── Footer: Branding ────────────────────────────────────────────────
        footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=24)
        footer_frame.pack(fill="x", side="bottom", padx=16, pady=(0, 6))
        footer_frame.pack_propagate(False)

        ctk.CTkLabel(
            footer_frame, text="v1.1",
            font=("Segoe UI", 10), text_color=COLORS["text_secondary"]
        ).pack(side="left")

        self.lang_var = ctk.StringVar(value=self.lang)
        self.lang_cb = ctk.CTkComboBox(
            footer_frame, values=["TR", "EN"],
            variable=self.lang_var, command=self._change_language,
            width=65, height=22, font=("Segoe UI Semibold", 10), state="readonly",
            fg_color=COLORS["bg_dark"], border_width=1, border_color=COLORS["border"],
            dropdown_font=("Segoe UI", 10)
        )
        self.lang_cb.pack(side="left", padx=10)

        ctk.CTkLabel(
            footer_frame, text="WebAdHere Technologies",
            font=("Segoe UI", 9), text_color=COLORS["text_muted"]
        ).pack(side="right")

    def _change_language(self, new_lang):
        """Update language on the fly without restart."""
        if new_lang == self.lang: return
        self.lang = new_lang
        self.config["lang"] = self.lang
        self._save_history()
        
        # Update generic references
        for key, lbl in self._labels.items():
            true_key = key.replace("_stat", "")
            lbl.configure(text=self._t(true_key))
            
        # Update dynamic security alert
        if getattr(self.security_value, "_dynamic_key", None):
            self.security_value.configure(text=self._t(self.security_value._dynamic_key))

        self.sched_title.configure(text=self._t("sched_lbl"))
        self.schedule_switch.configure(text=self._t("toggle_text"))
        
        if not self.is_testing:
            self.start_btn.configure(text=self._t("start_btn"))
            if self.status_label.cget("text") in [TRANSLATIONS["TR"]["ready"], TRANSLATIONS["EN"]["ready"]]:
                self.status_label.configure(text=self._t("ready"))
                
        self.history_btn.configure(text=self._t("history_btn"))
        self.dl_gauge.update_label(self._t("dl_lbl"))
        self.ul_gauge.update_label(self._t("ul_lbl"))

        # Map schedule options safely
        old_val = self.schedule_var.get()
        new_val = translate_time(old_val, to_lang=self.lang)
        self.schedule_cb.configure(values=SCHED_MAP[self.lang])
        self.schedule_var.set(new_val)
        
        if not self.auto_test_running:
            self.countdown_label.configure(text="")

    # ── IP Info ─────────────────────────────────────────────────────────────

    def _fetch_ip_info(self):
        """Fetch public IP and related info with ip-api.com."""
        try:
            url = "http://ip-api.com/json/?fields=status,country,city,zip,lat,lon,timezone,isp,org,as,query,proxy,hosting"
            resp = requests.get(url, timeout=8)
            data = resp.json()
            if data.get("status") == "success":
                ip = data.get("query", "—")
                city = data.get("city", "")
                country = data.get("country", "")
                isp_name = data.get("isp", "—")
                location_str = ", ".join(filter(None, [city, country]))
                
                # Analyze Security / Proxy / Data Center VPN
                is_proxy = data.get("proxy", False) or data.get("hosting", False)
                sec_key = "sec_vpn" if is_proxy else "sec_safe"
                
                lat = data.get("lat", "")
                lon = data.get("lon", "")
                coord = f"{lat}, {lon}" if lat and lon else "—"
                
                zip_code = data.get("zip", "—")
                as_no = data.get("as", "—").split()[0] if data.get("as") else "—"

                self.after(0, lambda: self._update_ip_ui(
                    ip, location_str, isp_name, sec_key, coord, zip_code, as_no
                ))
            else:
                raise Exception("Failed API status")
        except Exception:
            self.after(0, lambda: self._update_ip_ui(
                self._t("not_found"), "—", "—", "—", "—", "—", "—"
            ))

    def _update_ip_ui(self, ip, location, isp, sec_key, coord, zip_code, as_no):
        """Update the IP information labels."""
        self.ip_value.configure(text=ip)
        self.location_value.configure(text=location if location else "—")
        self.isp_value.configure(text=isp)
        
        # update new fields
        if sec_key in ["sec_vpn", "sec_safe"]:
            self.security_value.configure(text=self._t(sec_key))
            self.security_value._dynamic_key = sec_key
            if sec_key == "sec_vpn":
                self.security_value.configure(text_color=COLORS["accent_red"])
            else:
                self.security_value.configure(text_color=COLORS["accent_green"])
        else:
            self.security_value.configure(text=sec_key, text_color=COLORS["text_primary"])
            self.security_value._dynamic_key = None
            
        self.coord_value.configure(text=coord)
        self.zip_value.configure(text=zip_code if zip_code else "—")
        self.as_value.configure(text=as_no)

    # ── Schedule Logic ──────────────────────────────────────────────────────

    def _parse_interval(self, val_str):
        if "Dakika" in val_str or "Minute" in val_str:
            return int(val_str.split()[0]) * 60
        elif "Saat" in val_str or "Hour" in val_str:
            return int(val_str.split()[0]) * 3600
        return 1800

    def _toggle_schedule(self):
        if self.schedule_switch_var.get() == "on":
            self.schedule_cb.configure(state="disabled")
            self.auto_test_running = True
            self.remaining_seconds = self._parse_interval(self.schedule_var.get())
            self._update_timer()
        else:
            self.schedule_cb.configure(state="readonly")
            self.auto_test_running = False
            self.countdown_label.configure(text="")
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None

    def _update_timer(self):
        if not self.auto_test_running:
            return
            
        if self.remaining_seconds <= 0:
            self.countdown_label.configure(text=self._t("test_starting"))
            if not self.is_testing:
                self._start_test()
            self.remaining_seconds = self._parse_interval(self.schedule_var.get())
            self.timer_id = self.after(1000, self._update_timer)
            return

        m, s = divmod(self.remaining_seconds, 60)
        h, m = divmod(m, 60)
        
        time_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
            
        if self.is_testing:
            self.countdown_label.configure(text=self._t("test_running_next").format(time_str))
        else:
            self.countdown_label.configure(text=self._t("next_test").format(time_str))
            
        self.remaining_seconds -= 1
        self.timer_id = self.after(1000, self._update_timer)

    # ── Speed Test Logic ────────────────────────────────────────────────────

    def _save_provider(self, new_val):
        self.config["provider"] = new_val
        self._save_history()

    def _start_test(self):
        """Start the speed test in a background thread."""
        if self.is_testing:
            return
        self.is_testing = True
        self.start_btn.configure(
            text=self._t("testing"),
            state="disabled",
            fg_color=COLORS["border_light"]
        )
        self.status_label.configure(text=self._t("finding_srv"), text_color=COLORS["accent_orange"])
        self.progress.set(0)

        # Reset labels
        self.dl_gauge.set_value(0)
        self.ul_gauge.set_value(0)
        self.dl_stat.configure(text="— Mbps")
        self.ul_stat.configure(text="— Mbps")
        self.ping_stat.configure(text="— ms")
        self.jitter_stat.configure(text="— ms")

        threading.Thread(target=self._run_auto_routed_test, daemon=True).start()

    def _run_auto_routed_test(self):
        provider = self.provider_var.get()
        if provider == "Cloudflare":
            self._run_cloudflare_test()
        elif provider == "LibreSpeed":
            self._run_librespeed_test()
        else:
            self._run_ookla_test()

    def _handle_error(self, e):
        error_str = str(e)[:60]
        self.after(0, lambda msg=error_str: self.status_label.configure(
            text=self._t("error").format(msg), text_color=COLORS["accent_red"]
        ))
        
    def _update_speed_ui(self, current_speed, peak_speed, is_download=True):
        if is_download:
            self.dl_gauge.set_value(current_speed)
            self.dl_stat.configure(text=f"{peak_speed:.1f} Mbps")
        else:
            self.ul_gauge.set_value(current_speed)
            self.ul_stat.configure(text=f"{peak_speed:.1f} Mbps")

    def _finish_test(self, ping_val, jitter, server_name):
        self.after(0, lambda: self.progress.set(1.0))
        self.after(0, lambda: self.status_label.configure(
            text=self._t("success"), text_color=COLORS["accent_green"]
        ))
        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "download": round(getattr(self, '_dl_peak_mbps', 0), 2),
            "upload": round(getattr(self, '_ul_peak_mbps', 0), 2),
            "ping": round(ping_val, 1),
            "jitter": round(jitter, 1),
            "server": server_name,
        }
        self.test_history.insert(0, result)
        if len(self.test_history) > 20:
            self.test_history = self.test_history[:20]
        self._save_history()

    def _timed_download(self, url, duration=15.0, threads_count=16, base_prog=0.2, len_prog=0.35):
        self._global_cumulative_dl = 0
        self._dl_peak_mbps = 0
        self._dl_monitoring = True
        self.dl_active = True
        
        def dl_worker():
            try:
                session = requests.Session()
                while self.dl_active:
                    try:
                        with session.get(url, stream=True, timeout=5) as r:
                            for chunk in r.iter_content(chunk_size=131072):
                                if not self.dl_active: break
                                if chunk: self._global_cumulative_dl += len(chunk)
                    except Exception:
                        pass
            except Exception:
                pass

        threads = []
        for _ in range(threads_count):
            t = threading.Thread(target=dl_worker, daemon=True)
            t.start()
            threads.append(t)
            
        start_time = time.time()
        
        def monitor_dl():
            if not self._dl_monitoring: return
            now = time.time()
            elapsed = now - start_time
            if elapsed >= duration:
                self.dl_active = False
                return

            bytes_now = self._global_cumulative_dl
            last_bytes = getattr(self, '_last_dl_bytes', 0)
            last_time = getattr(self, '_last_dl_time', start_time)
            
            bytes_delta = bytes_now - last_bytes
            time_delta = now - last_time
            
            if time_delta > 0:
                speed_mbps = (bytes_delta * 8) / time_delta / 1_000_000
                if speed_mbps > self._dl_peak_mbps:
                    self._dl_peak_mbps = speed_mbps
                self.after(0, lambda s=speed_mbps, p=self._dl_peak_mbps: self._update_speed_ui(s, p, True))
            
            self._last_dl_bytes = bytes_now
            self._last_dl_time = now
            prog = base_prog + (elapsed / duration) * len_prog
            self.progress.set(prog)
            self.after(200, monitor_dl)

        self._last_dl_bytes = 0
        self._last_dl_time = start_time
        self.after(0, monitor_dl)
        
        while time.time() - start_time < duration:
            time.sleep(0.1)
            
        self.dl_active = False
        self._dl_monitoring = False
        self.after(0, lambda: self.dl_gauge.set_value(self._dl_peak_mbps))
        return self._dl_peak_mbps

    def _timed_upload(self, url, duration=15.0, threads_count=12, base_prog=0.55, len_prog=0.40):
        self._global_cumulative_ul = 0
        self._ul_peak_mbps = 0
        self._ul_monitoring = True
        self.ul_active = True
        
        def ul_worker():
            try:
                session = requests.Session()
                while self.ul_active:
                    data = os.urandom(1024 * 1024) # 1MB chunks
                    try:
                        session.post(url, data=data, timeout=5)
                        if self.ul_active:
                            self._global_cumulative_ul += len(data)
                    except Exception:
                        pass
            except Exception:
                pass

        threads = []
        for _ in range(threads_count):
            t = threading.Thread(target=ul_worker, daemon=True)
            t.start()
            threads.append(t)
            
        start_time = time.time()
        
        def monitor_ul():
            if not self._ul_monitoring: return
            now = time.time()
            elapsed = now - start_time
            if elapsed >= duration:
                self.ul_active = False
                return

            bytes_now = self._global_cumulative_ul
            last_bytes = getattr(self, '_last_ul_bytes', 0)
            last_time = getattr(self, '_last_ul_time', start_time)
            
            bytes_delta = bytes_now - last_bytes
            time_delta = now - last_time
            
            if time_delta > 0:
                speed_mbps = (bytes_delta * 8) / time_delta / 1_000_000
                if speed_mbps > self._ul_peak_mbps:
                    self._ul_peak_mbps = speed_mbps
                self.after(0, lambda s=speed_mbps, p=self._ul_peak_mbps: self._update_speed_ui(s, p, False))
            
            self._last_ul_bytes = bytes_now
            self._last_ul_time = now
            prog = base_prog + (elapsed / duration) * len_prog
            self.progress.set(prog)
            self.after(200, monitor_ul)

        self._last_ul_bytes = 0
        self._last_ul_time = start_time
        self.after(0, monitor_ul)
        
        while time.time() - start_time < duration:
            time.sleep(0.1)
            
        self.ul_active = False
        self._ul_monitoring = False
        self.after(0, lambda: self.ul_gauge.set_value(self._ul_peak_mbps))
        return self._ul_peak_mbps

    def _run_cloudflare_test(self):
        try:
            self.after(0, lambda: self.status_label.configure(text="Cloudflare bağlanıyor..."))
            self.after(0, lambda: self.server_value.configure(text="Cloudflare CDN"))
            self.after(0, lambda: self.progress.set(0.1))
            
            # Ping
            pings = []
            for _ in range(5):
                t0 = time.time()
                try: requests.get("https://speed.cloudflare.com/cdn-cgi/trace", timeout=3)
                except: pass
                pings.append((time.time() - t0) * 1000)
            
            if not pings: raise Exception("No internet")
            ping_val = min(pings)
            jitter = sum(abs(pings[i] - pings[i-1]) for i in range(1, len(pings))) / (len(pings)-1) if len(pings) > 1 else 0
            
            self.after(0, lambda: self.ping_stat.configure(text=f"{ping_val:.1f} ms"))
            self.after(0, lambda: self.jitter_stat.configure(text=f"{jitter:.1f} ms"))
            self.after(0, lambda: self.progress.set(0.2))
            
            self.after(0, lambda: self.status_label.configure(text=self._t("dl_test"), text_color=COLORS["accent_cyan"]))
            self._timed_download("https://speed.cloudflare.com/__down?bytes=25000000", duration=15.0)
            
            self.after(0, lambda: self.progress.set(0.55))
            self.after(0, lambda: self.status_label.configure(text=self._t("ul_test"), text_color=COLORS["accent_green"]))
            
            self._timed_upload("https://speed.cloudflare.com/__up", duration=15.0)
            
            self._finish_test(ping_val, jitter, "Cloudflare CDN")
        except Exception as e:
            self._handle_error(e)
        finally:
            self.after(0, self._reset_button)

    def _run_librespeed_test(self):
        try:
            self.after(0, lambda: self.status_label.configure(text="LibreSpeed sunucu bulunuyor..."))
            self.after(0, lambda: self.progress.set(0.1))
            
            try:
                # The correct public server list for LibreSpeed is:
                backends = requests.get("https://librespeed.org/backend-servers/servers.php", timeout=10).json()
            except:
                raise Exception("LibreSpeed public list unavailable")
                
            best_ping = 9999
            best_backend = None
            jitter = 0
            
            for b in backends[:15]: # Check a few backends
                server_url = b.get("server", "")
                if not server_url: continue
                # Ensure trailing slash
                if not server_url.endswith("/"): server_url += "/"
                ping_url = b.get("pingURL", "empty.php")
                
                pings = []
                for _ in range(3):
                    t0 = time.time()
                    try: 
                        requests.get(f"{server_url}{ping_url}", timeout=2)
                        pings.append((time.time() - t0) * 1000)
                    except: pass
                if pings:
                    avg_p = sum(pings) / len(pings)
                    if avg_p < best_ping:
                        best_ping = avg_p
                        best_backend = b
                        jitter = sum(abs(pings[i] - pings[i-1]) for i in range(1, len(pings))) / (len(pings)-1) if len(pings)>1 else 0
            
            if not best_backend: raise Exception("No valid LibreSpeed server")
            
            server_name = best_backend.get("name", "LibreSpeed Sunucu")
            self.after(0, lambda: self.server_value.configure(text=server_name))
            self.after(0, lambda: self.ping_stat.configure(text=f"{best_ping:.1f} ms"))
            self.after(0, lambda: self.jitter_stat.configure(text=f"{jitter:.1f} ms"))
            self.after(0, lambda: self.progress.set(0.2))
            
            server_url = best_backend.get("server", "")
            if not server_url.endswith("/"): server_url += "/"
            dl_url = f"{server_url}{best_backend.get('dlURL', 'garbage.php')}?ckSize=100"
            ul_url = f"{server_url}{best_backend.get('ulURL', 'empty.php')}"
            
            self.after(0, lambda: self.status_label.configure(text=self._t("dl_test"), text_color=COLORS["accent_cyan"]))
            self._timed_download(dl_url, duration=15.0)
            
            self.after(0, lambda: self.progress.set(0.55))
            self.after(0, lambda: self.status_label.configure(text=self._t("ul_test"), text_color=COLORS["accent_green"]))
            
            self._timed_upload(ul_url, duration=15.0)
            
            self._finish_test(best_ping, jitter, server_name)
        except Exception as e:
            self._handle_error(e)
        finally:
            self.after(0, self._reset_button)

    def _run_ookla_test(self):
        """Execute the speed test by choosing the best Ookla server and then performing manual measurement."""
        try:
            st = speedtest.Speedtest()

            self.after(0, lambda: self.status_label.configure(text=self._t("best_srv")))
            self.after(0, lambda: self.progress.set(0.1))
            st.get_servers([])  
            st.get_best_server() 

            server = st.best
            server_name = f"{server.get('sponsor', '—')} ({server.get('name', '')})"
            self.after(0, lambda: self.server_value.configure(text=server_name))

            ping_val = server.get("latency", 0)
            self.after(0, lambda: self.ping_stat.configure(text=f"{ping_val:.1f} ms"))
            self.after(0, lambda: self.progress.set(0.2))

            # Base URL logic for Ookla (usually derived from upload URL)
            upload_url = server.get('url', '')
            if not upload_url: raise Exception("Ookla server URL not found")
            
            # Extract base path (e.g., http://host/speedtest/)
            base_url = upload_url.rsplit('/', 1)[0] + "/"
            dl_url = f"{base_url}random4000x4000.jpg"

            # DOWNLOAD PHASE
            self.after(0, lambda: self.status_label.configure(text=self._t("dl_test"), text_color=COLORS["accent_cyan"]))
            self._timed_download(dl_url, duration=15.0, base_prog=0.2, len_prog=0.35)
            
            self.after(0, lambda: self.progress.set(0.55))

            # UPLOAD PHASE
            self.after(0, lambda: self.status_label.configure(text=self._t("ul_test"), text_color=COLORS["accent_green"]))
            self._timed_upload(upload_url, duration=15.0, base_prog=0.55, len_prog=0.40)
            
            self.after(0, lambda: self.progress.set(0.95))

            # Latency check (Jitter)
            try:
                pings = []
                for _ in range(5):
                    t0 = time.time()
                    requests.get(f"http://{server['host']}", timeout=3)
                    pings.append((time.time() - t0) * 1000)
                if len(pings) > 1:
                    jitter = sum(abs(pings[i] - pings[i-1]) for i in range(1, len(pings))) / (len(pings) - 1)
                else:
                    jitter = 0
            except Exception:
                jitter = 0
            self.after(0, lambda: self.jitter_stat.configure(text=f"{jitter:.1f} ms"))

            self._finish_test(ping_val, jitter, server_name)

        except Exception as e:
            self._handle_error(e)
        finally:
            self.after(0, self._reset_button)

    def _reset_button(self):
        """Reset the start button after test completion."""
        self.is_testing = False
        self.start_btn.configure(
            text=self._t("start_btn"),
            state="normal",
            fg_color=COLORS["accent_cyan"]
        )

    # ── History Management ──────────────────────────────────────────────────

    def _get_history_path(self):
        import sys
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "speed_history.json")

    def _load_history(self):
        try:
            with open(self._get_history_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    self.test_history = data
                    self.config = {"lang": "TR"}
                else:
                    self.test_history = data.get("history", [])
                    self.config = data.get("config", {"lang": "TR"})
        except (FileNotFoundError, json.JSONDecodeError):
            self.test_history = []
            self.config = {"lang": "TR"}

    def _save_history(self):
        data = {
            "config": self.config,
            "history": self.test_history
        }
        try:
            with open(self._get_history_path(), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _show_history(self):
        """Show a modal window with test history."""
        if not self.test_history:
            self._show_empty_history()
            return

        win = ctk.CTkToplevel(self)
        win.title(self._t("hist_title"))
        win.geometry("640x500")
        win.configure(fg_color=COLORS["bg_dark"])
        win.transient(self)
        win.grab_set()

        # Header
        header = ctk.CTkFrame(win, fg_color=COLORS["bg_card"], corner_radius=0, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text=f"📋  {self._t('hist_title')}",
            font=("Segoe UI Semibold", 16), text_color=COLORS["text_primary"]
        ).pack(side="left", padx=20, pady=12)

        # Clear button
        ctk.CTkButton(
            header, text=self._t("clear_btn"), width=90, height=30,
            font=("Segoe UI", 11), corner_radius=8,
            fg_color=COLORS["accent_red"], hover_color="#DC2626",
            text_color="white",
            command=lambda: self._clear_history(win)
        ).pack(side="right", padx=20, pady=12)

        # Scrollable content
        scroll = ctk.CTkScrollableFrame(
            win, fg_color=COLORS["bg_dark"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["border_light"]
        )
        scroll.pack(fill="both", expand=True, padx=16, pady=12)

        # Table header
        cols = [self._t("date_lbl"), self._t("dl_lbl"), self._t("ul_lbl"), self._t("ping_lbl"), self._t("srv_lbl")]
        col_widths = [130, 100, 100, 70, 200]
        hdr_row = ctk.CTkFrame(scroll, fg_color=COLORS["bg_input"], corner_radius=8, height=36)
        hdr_row.pack(fill="x", pady=(0, 8))
        hdr_row.pack_propagate(False)
        for col_name, w in zip(cols, col_widths):
            ctk.CTkLabel(
                hdr_row, text=col_name, width=w,
                font=("Segoe UI Semibold", 11), text_color=COLORS["text_secondary"]
            ).pack(side="left", padx=6, pady=6)

        for entry in self.test_history:
            row = ctk.CTkFrame(
                scroll, fg_color=COLORS["bg_card"],
                corner_radius=8, border_width=1, border_color=COLORS["border"]
            )
            row.pack(fill="x", pady=2)

            values = [
                entry.get("date", "—"),
                f"{entry.get('download', 0):.2f} Mbps",
                f"{entry.get('upload', 0):.2f} Mbps",
                f"{entry.get('ping', 0):.1f} ms",
                entry.get("server", "—")[:30],
            ]
            colors = [
                COLORS["text_secondary"],
                COLORS["accent_cyan"],
                COLORS["accent_green"],
                COLORS["accent_orange"],
                COLORS["text_secondary"],
            ]
            for val, w, c in zip(values, col_widths, colors):
                ctk.CTkLabel(
                    row, text=val, width=w,
                    font=("Segoe UI", 11), text_color=c
                ).pack(side="left", padx=6, pady=8)

    def _show_empty_history(self):
        """Show a message when there's no history."""
        win = ctk.CTkToplevel(self)
        win.title(self._t("hist_title"))
        win.geometry("400x200")
        win.configure(fg_color=COLORS["bg_dark"])
        win.transient(self)
        win.grab_set()

        ctk.CTkLabel(
            win, text="📋", font=("Segoe UI Emoji", 40)
        ).pack(pady=(30, 8))
        ctk.CTkLabel(
            win, text=self._t("no_hist"),
            font=("Segoe UI", 14), text_color=COLORS["text_secondary"]
        ).pack()
        ctk.CTkLabel(
            win, text=self._t("no_hist_desc"),
            font=("Segoe UI", 11), text_color=COLORS["text_muted"]
        ).pack(pady=(4, 0))

    def _clear_history(self, window):
        """Clear all test history."""
        self.test_history = []
        self._save_history()
        window.destroy()


# ─── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = SpeedTestApp()
    app.mainloop()