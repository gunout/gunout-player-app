import sys
import math
import os
import random
import webbrowser
import locale
import mpv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QListWidget,
                              QListWidgetItem, QLabel, QFrame, QSlider,
                              QDialog, QGridLayout, QStackedWidget)
from PyQt6.QtCore import (Qt, QTimer, QSize, QPropertyAnimation,
                          QEasingCurve, QRectF, QPoint, QByteArray)
from PyQt6.QtGui import (QFont, QColor, QIcon, QPixmap, QPainter, QPainterPath,
                         QPen, QCursor, QLinearGradient, QBrush, QOpenGLContext)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from mpv import MpvRenderContext, MpvGlGetProcAddressFn

# --- IMPORTANT : corriger le locale AVANT de créer mpv ---
locale.setlocale(locale.LC_NUMERIC, 'C')


# ============================================================
#  GUNOUT PLAYER — Stations radio & TV
# ============================================================
STATIONS = [
    {"name": "1. ExoFM",                        "url": "https://exofmreunion.ice.infomaniak.ch/exofmreunion-64.aac", "type": "audio"},
    {"name": "2. France Bleu Creuse",           "url": "http://direct.francebleu.fr/live/fbcreuse-midfi.mp3", "type": "audio"},
    {"name": "3. Freedom1",                     "url": "http://freedomice.streamakaci.com/freedom.mp3", "type": "audio"},
    {"name": "4. KreolFM",                      "url": "http://kreolfm.ice.infomaniak.ch/kreolfm-96.aac", "type": "audio"},
    {"name": "5. NeoFM",                        "url": "http://neofming.streamakaci.com/neofm.mp3", "type": "audio"},
    {"name": "6. Réunion 1ère",                 "url": "https://reunion.ice.infomaniak.ch/reunion-128.mp3", "type": "audio"},
    {"name": "7. Martinique 1ère",              "url": "https://martinique.ice.infomaniak.ch/martinique-128.mp3", "type": "audio"},
    {"name": "8. Guyane 1ère",                  "url": "https://guyane.ice.infomaniak.ch/guyane-128.mp3", "type": "audio"},
    {"name": "9. Guadeloupe 1ère",              "url": "https://guadeloupe.ice.infomaniak.ch/guadeloupe-128.mp3", "type": "audio"},
    {"name": "10. Mayotte 1ère",                "url": "https://mayotte.ice.infomaniak.ch/mayotte-128.mp3", "type": "audio"},
    {"name": "11. Nouvelle-Calédonie 1ère",     "url": "https://nouvelle-caledonie.ice.infomaniak.ch/nouvelle-caledonie-128.mp3", "type": "audio"},
    {"name": "12. Wallis et Futuna 1ère",       "url": "https://wallisetfutuna.ice.infomaniak.ch/wallisetfutuna-128.mp3", "type": "audio"},
    {"name": "13. Saint-Pierre et Miquelon 1ère", "url": "https://saint-pierreetmiquelon.ice.infomaniak.ch/saint-pierreetmiquelon-128.mp3", "type": "audio"},
    {"name": "14. Outremer 1ère",               "url": "https://outremer.ice.infomaniak.ch/outremer-128.mp3", "type": "audio"},
    {"name": "15. Polynésie 1ère",              "url": "https://polynesie.ice.infomaniak.ch/polynesie-128.mp3", "type": "audio"},
    {"name": "16. Skyrock",                     "url": "http://icecast.skyrock.net/s/natio_mp3_128k", "type": "audio"},
    {"name": "17. Generation TV",               "url": "https://edge11.vedge.infomaniak.com/livecast/ik:generation-tv/manifest.m3u8", "type": "video"},
    {"name": "18. Urban Hit Réunion",           "url": "https://listen.radioking.com/radio/400111/stream/452236", "type": "audio"},
    {"name": "19. Gleaphe Radio",               "url": "https://gradio-gleaphe.duckdns.org/radio/stream", "type": "audio"},
    {"name": "20. Radio Pikan",                 "url": "https://stream4.vestaradio.com/RADIOPIKAN?nocache=89908", "type": "audio"},
    {"name": "21. Antenne Réunion Radio",       "url": "https://rtlre.ice.infomaniak.ch/rtlre-64.aac", "type": "audio"},
    {"name": "22. Antenne Réunion TV",          "url": "https://live-antenne-reunion.zeop.tv/live/c3eds/antreunihd/hls_fta/antreunihd.m3u8?location=ZEOP01", "type": "video"},
    {"name": "23. EXO TV",                      "url": "https://eu-west-3-antenne-reunion-msl.akamaized.net/hls/live/20000128/main/ch1.m3u8", "type": "video"},
]

# --- Onglet SITES : un seul lien vers Gunout ---
SITE_LINKS = {
    "site": ("Gunout Webradio", "https://gradio-gleaphe.duckdns.org/"),
}

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")

# ----- Palette -----
BG          = "rgba(12, 12, 14, 240)"
POPUP_BG    = "rgba(18, 18, 22, 250)"
SURFACE     = "rgba(255, 255, 255, 6)"
SURFACE_HOV = "rgba(255, 255, 255, 14)"
ACCENT      = "#ff3b3b"
ACCENT_SOFT = "rgba(255, 59, 59, 22)"
TEXT        = "#f5f5f7"
TEXT_DIM    = "rgba(245, 245, 247, 100)"
SIGNATURE   = "rgba(245, 245, 247, 30)"
CHEVRON     = "rgba(245, 245, 247, 150)"


STYLE = f"""
QMainWindow, QWidget#root {{
    background: {BG};
    border-radius: 14px;
    border: none;
}}
QLabel#logo {{ background: transparent; padding: 2px 4px; }}
QLabel#signature {{ color: {SIGNATURE}; font-size: 9px; letter-spacing: 3px; padding: 0 8px 4px 8px; }}
QListWidget#stations {{
    background: rgba(255, 255, 255, 4);
    color: {TEXT};
    border: none;
    border-radius: 10px;
    padding: 6px;
    font-size: 12px;
    letter-spacing: 2px;
    outline: none;
}}
QListWidget#stations::item {{ padding: 10px 14px; border-radius: 8px; margin: 2px 0; }}
QListWidget#stations::item:hover {{ background: {SURFACE_HOV}; }}
QListWidget#stations::item:selected {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
QFrame#stage {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0a0d12, stop:0.5 #06080b, stop:1 #04060a);
    border: none;
    border-radius: 12px;
}}
QFrame#controls {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(0,0,0,0), stop:0.4 rgba(0,0,0,120), stop:1 rgba(0,0,0,180));
    border: none;
    border-bottom-left-radius: 12px;
    border-bottom-right-radius: 12px;
}}
QPushButton#ctrl {{
    background: transparent; border: none; border-radius: 15px;
    padding: 4px; min-width: 30px; min-height: 30px;
}}
QPushButton#ctrl:hover {{ background: {SURFACE_HOV}; }}
QPushButton#site {{
    background: {SURFACE}; color: {TEXT}; border: none; border-radius: 15px;
    padding: 5px 12px; font-size: 10px; font-weight: 700; letter-spacing: 2px;
}}
QPushButton#site:hover {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
QDialog#popup {{
    background: {POPUP_BG}; border: 1px solid rgba(255, 255, 255, 12); border-radius: 14px;
}}
QLabel#popup_title {{ color: {TEXT}; font-size: 13px; font-weight: 700; letter-spacing: 4px; padding: 4px; }}
QLabel#popup_sub {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 2px; padding: 0 4px 6px 4px; }}
QPushButton#popup_item {{
    background: {SURFACE}; color: {TEXT}; border: none; border-radius: 10px;
    padding: 12px 14px; font-size: 11px; letter-spacing: 1px; text-align: left;
}}
QPushButton#popup_item:hover {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
QPushButton#popup_item:pressed {{ background: rgba(255, 59, 59, 40); }}
QPushButton#popup_close {{
    background: transparent; color: {TEXT_DIM}; border: none; border-radius: 15px;
    padding: 4px; min-width: 30px; min-height: 30px;
}}
QPushButton#popup_close:hover {{ background: {SURFACE_HOV}; color: {TEXT}; }}
QSlider::groove:horizontal {{ height: 3px; background: rgba(255,255,255,12); border-radius: 2px; }}
QSlider::sub-page:horizontal {{ background: {ACCENT}; border-radius: 2px; }}
QSlider::handle:horizontal {{
    background: #fff; width: 10px; height: 10px; margin: -4px 0; border-radius: 5px; border: none;
}}
QSlider::handle:horizontal:hover {{
    background: {ACCENT}; width: 12px; height: 12px; margin: -5px 0; border-radius: 6px;
}}
QLabel#status {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 2px; padding: 2px 6px; }}
QLabel#time {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 0.5px; min-width: 80px; }}
QLabel#nowplaying {{ color: {TEXT}; font-size: 18px; font-weight: 700; letter-spacing: 3px; }}
QLabel#nowmeta {{ color: {TEXT_DIM}; font-size: 10px; letter-spacing: 2px; }}
"""


# ================= ICÔNES =================
def _make_icon(kind, size=16, color="#f5f5f7"):
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color))
    pen.setWidthF(1.4)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(QColor(color))
    s = size
    if kind == "play":
        path = QPainterPath()
        path.moveTo(s*0.32, s*0.24); path.lineTo(s*0.76, s*0.50)
        path.lineTo(s*0.32, s*0.76); path.closeSubpath()
        p.drawPath(path)
    elif kind == "pause":
        p.drawRoundedRect(int(s*0.32), int(s*0.24), int(s*0.12), int(s*0.52), 2, 2)
        p.drawRoundedRect(int(s*0.56), int(s*0.24), int(s*0.12), int(s*0.52), 2, 2)
    elif kind == "stop":
        p.drawRoundedRect(int(s*0.32), int(s*0.32), int(s*0.36), int(s*0.36), 3, 3)
    elif kind == "volume":
        path = QPainterPath()
        path.moveTo(s*0.20, s*0.42); path.lineTo(s*0.34, s*0.42)
        path.lineTo(s*0.48, s*0.28); path.lineTo(s*0.48, s*0.72)
        path.lineTo(s*0.34, s*0.58); path.lineTo(s*0.20, s*0.58)
        path.closeSubpath()
        p.drawPath(path)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawArc(int(s*0.44), int(s*0.34), int(s*0.24), int(s*0.32), -50*16, 100*16)
    elif kind == "mute":
        path = QPainterPath()
        path.moveTo(s*0.20, s*0.42); path.lineTo(s*0.34, s*0.42)
        path.lineTo(s*0.48, s*0.28); path.lineTo(s*0.48, s*0.72)
        path.lineTo(s*0.34, s*0.58); path.lineTo(s*0.20, s*0.58)
        path.closeSubpath()
        p.drawPath(path)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.60), int(s*0.38), int(s*0.80), int(s*0.62))
        p.drawLine(int(s*0.80), int(s*0.38), int(s*0.60), int(s*0.62))
    elif kind == "close":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.30), int(s*0.30), int(s*0.70), int(s*0.70))
        p.drawLine(int(s*0.70), int(s*0.30), int(s*0.30), int(s*0.70))
    elif kind == "min":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.28), int(s*0.52), int(s*0.72), int(s*0.52))
    elif kind == "chevron-down":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.30), int(s*0.42), int(s*0.50), int(s*0.62))
        p.drawLine(int(s*0.50), int(s*0.62), int(s*0.70), int(s*0.42))
    elif kind == "chevron-up":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.30), int(s*0.58), int(s*0.50), int(s*0.38))
        p.drawLine(int(s*0.50), int(s*0.38), int(s*0.70), int(s*0.58))
    p.end()
    return QIcon(pm)


# ================= VISUALISEUR =================
class Visualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.bars = 32
        self.values = [0.0] * self.bars
        self.targets = [0.0] * self.bars
        self.phase = 0.0
        self.playing = False
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self._tick)
        self.timer.start()

    def set_playing(self, playing):
        self.playing = playing

    def _tick(self):
        self.phase += 0.15
        for i in range(self.bars):
            if self.playing:
                base = 0.35 + 0.35 * abs(math.sin(self.phase + i * 0.35))
                self.targets[i] = base + random.uniform(-0.15, 0.25)
            else:
                self.targets[i] = 0.02
            self.targets[i] = max(0.02, min(1.0, self.targets[i]))
            self.values[i] += (self.targets[i] - self.values[i]) * 0.25
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return
        bar_w = w / self.bars * 0.55
        gap = w / self.bars
        cy = h / 2
        max_h = h * 0.55
        grad = QLinearGradient(0, cy - max_h/2, 0, cy + max_h/2)
        grad.setColorAt(0.0, QColor(255, 59, 59, 220))
        grad.setColorAt(0.5, QColor(255, 59, 59, 140))
        grad.setColorAt(1.0, QColor(255, 59, 59, 40))
        p.setBrush(QBrush(grad))
        p.setPen(Qt.PenStyle.NoPen)
        for i, v in enumerate(self.values):
            bh = max(2, v * max_h)
            x = i * gap + (gap - bar_w) / 2
            y = cy - bh / 2
            p.drawRoundedRect(QRectF(x, y, bar_w, bh), bar_w/2, bar_w/2)
        p.end()


# ================= WIDGET VIDÉO OPENGL =================
class MPVVideoWidget(QOpenGLWidget):
    """Widget OpenGL qui rend la vidéo mpv via MpvRenderContext."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mpv = None
        self.ctx = None
        self._proc_addr_wrapper = None
        self._initialized = False
        self._pending_url = None
        self.setUpdateBehavior(QOpenGLWidget.UpdateBehavior.PartialUpdate)

    def _get_process_address(self, _ctx, name):
        glctx = QOpenGLContext.currentContext()
        if glctx is None:
            return 0
        if isinstance(name, str):
            name = name.encode('utf-8')
        addr = glctx.getProcAddress(QByteArray(name))
        if addr is None:
            return 0
        try:
            return int(addr)
        except Exception:
            return 0

    def initializeGL(self):
        self.mpv = mpv.MPV(
            vo='libmpv',
            ao='pulse',
            ytdl=False,
            cache=True,
            cache_secs=3,
            demuxer_max_bytes='5M',
            demuxer_max_back_bytes='2M',
            demuxer_readahead_secs=2,
            network_timeout=15,
            audio_client_name='Gunout Player TV',
            keep_open='yes',
            idle='yes',
        )

        self._proc_addr_wrapper = MpvGlGetProcAddressFn(self._get_process_address)

        self.ctx = MpvRenderContext(
            self.mpv,
            'opengl',
            opengl_init_params={'get_proc_address': self._proc_addr_wrapper}
        )
        self.ctx.update_cb = self._on_mpv_update
        self._initialized = True

        if self._pending_url:
            self.mpv.play(self._pending_url)
            self._pending_url = None

    def _on_mpv_update(self):
        self.update()

    def paintGL(self):
        if not self._initialized or self.ctx is None:
            return

        ratio = self.devicePixelRatioF()
        w = int(self.width() * ratio)
        h = int(self.height() * ratio)
        if w <= 0 or h <= 0:
            return

        fbo = self.defaultFramebufferObject()
        try:
            self.ctx.render(
                flip_y=True,
                opengl_fbo={'w': w, 'h': h, 'fbo': fbo}
            )
        except Exception:
            pass

    def play(self, url):
        if not self._initialized:
            self._pending_url = url
            return
        try:
            self.mpv.command('stop')
            self.mpv.pause = False
            self.mpv.mute = False
            self.mpv.play(url)
        except Exception:
            pass

    def stop(self):
        if self._initialized and self.mpv:
            try:
                self.mpv.command('stop')
            except Exception:
                pass

    def set_pause(self, paused):
        if self._initialized and self.mpv:
            try:
                self.mpv.pause = paused
            except Exception:
                pass

    def set_mute(self, muted):
        if self._initialized and self.mpv:
            try:
                self.mpv.mute = muted
            except Exception:
                pass

    def set_volume(self, vol):
        if self._initialized and self.mpv:
            try:
                self.mpv.volume = vol
            except Exception:
                pass

    def cleanup(self):
        if self.ctx is not None:
            try:
                self.ctx.free()
            except Exception:
                pass
            self.ctx = None
        if self.mpv is not None:
            try:
                self.mpv.terminate()
            except Exception:
                pass
            self.mpv = None
        self._initialized = False


# ================= POPUP MENU SITE =================
class SitePopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("popup")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setModal(True)
        self.setFixedSize(320, 200)
        if parent:
            geo = parent.geometry()
            self.move(geo.center() - self.rect().center())
        self.setStyleSheet(STYLE)
        root = QWidget(self)
        root.setObjectName("popup")
        root.setGeometry(self.rect())
        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)
        header = QHBoxLayout()
        header.setSpacing(6)
        title = QLabel("GUNOUT WEBRADIO")
        title.setObjectName("popup_title")
        header.addWidget(title)
        header.addStretch()
        btn_close = QPushButton()
        btn_close.setObjectName("popup_close")
        btn_close.setIcon(_make_icon("close", 14, TEXT))
        btn_close.setIconSize(QSize(14, 14))
        btn_close.clicked.connect(self.reject)
        header.addWidget(btn_close)
        layout.addLayout(header)
        sub = QLabel("Ouvrir le site officiel Gunout")
        sub.setObjectName("popup_sub")
        layout.addWidget(sub)
        layout.addStretch()
        btn_open = QPushButton("OUVRIR GUNOUT")
        btn_open.setObjectName("popup_item")
        btn_open.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_open.clicked.connect(self._open)
        layout.addWidget(btn_open)
        btn_quit = QPushButton("FERMER")
        btn_quit.setObjectName("popup_item")
        btn_quit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_quit.clicked.connect(self.reject)
        layout.addWidget(btn_quit)

    def _open(self):
        webbrowser.open("https://gradio-gleaphe.duckdns.org/")
        self.accept()


# ================= FENÊTRE PRINCIPALE =================
class GunoutPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUNOUT PLAYER")
        self.resize(520, 480)
        self.setMinimumSize(360, 320)
        self.audio_player = None
        self._drag_pos = None
        self._resize_edge = None
        self._resize_margin = 6
        self._controls_collapsed = False
        self._controls_full_height = 0
        self._window_folded = False
        self._unfolded_height = 480
        self._current_station = "AUCUNE STATION"
        self._current_type = "audio"
        self.setMouseTracking(True)
        self.setStyleSheet(STYLE)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # --- HUD top ---
        top = QHBoxLayout()
        top.setSpacing(8)
        self.logo = QLabel()
        self.logo.setObjectName("logo")
        pix = QPixmap(LOGO_PATH)
        if not pix.isNull():
            pix = pix.scaledToHeight(28, Qt.TransformationMode.SmoothTransformation)
            self.logo.setPixmap(pix)
        else:
            self.logo.setText("GUNOUT")
            self.logo.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 700; letter-spacing: 4px;")
        self.logo.setFixedHeight(30)
        top.addWidget(self.logo)
        btn_site = QPushButton("SITES")
        btn_site.setObjectName("site")
        btn_site.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_site.clicked.connect(self.open_site_popup)
        top.addWidget(btn_site)
        top.addStretch()
        btn_min = QPushButton()
        btn_min.setObjectName("ctrl")
        btn_min.setIcon(_make_icon("min", 14, TEXT))
        btn_min.setIconSize(QSize(14, 14))
        btn_min.clicked.connect(self.showMinimized)
        top.addWidget(btn_min)
        btn_close = QPushButton()
        btn_close.setObjectName("ctrl")
        btn_close.setIcon(_make_icon("close", 14, TEXT))
        btn_close.setIconSize(QSize(14, 14))
        btn_close.clicked.connect(self.close)
        top.addWidget(btn_close)
        self.btn_fold = QPushButton()
        self.btn_fold.setObjectName("ctrl")
        self.btn_fold.setIcon(_make_icon("chevron-up", 14, CHEVRON))
        self.btn_fold.setIconSize(QSize(14, 14))
        self.btn_fold.setToolTip("Replier la fenêtre")
        self.btn_fold.clicked.connect(self.toggle_window_fold)
        top.addWidget(self.btn_fold)
        layout.addLayout(top)

        self.signature = QLabel("by gleaphe — Gunout Player")
        self.signature.setObjectName("signature")
        layout.addWidget(self.signature)

        # --- Stage ---
        self.stage = QFrame()
        self.stage.setObjectName("stage")
        v_layout = QVBoxLayout(self.stage)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        self.media_stack = QStackedWidget()
        self.media_stack.setStyleSheet("background: transparent;")

        # Page 0 : visualiseur audio
        self.viz = Visualizer()
        self.media_stack.addWidget(self.viz)

        # Page 1 : widget vidéo OpenGL
        self.video_widget = MPVVideoWidget()
        self.media_stack.addWidget(self.video_widget)

        v_layout.addWidget(self.media_stack, stretch=1)
        self.stage_body = self.media_stack

        # --- Overlay texte (visible uniquement en audio) ---
        self.overlay = QWidget(self.stage)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        ov = QVBoxLayout(self.overlay)
        ov.setContentsMargins(0, 0, 0, 0)
        ov.addStretch()
        self.lbl_now = QLabel(self._current_station)
        self.lbl_now.setObjectName("nowplaying")
        self.lbl_now.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_now.setStyleSheet("background: transparent;")
        ov.addWidget(self.lbl_now)
        ov.addSpacing(4)
        self.lbl_meta = QLabel("EN ATTENTE")
        self.lbl_meta.setObjectName("nowmeta")
        self.lbl_meta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_meta.setStyleSheet("background: transparent;")
        ov.addWidget(self.lbl_meta)
        ov.addStretch()

        # --- Contrôles ---
        self.controls = QFrame()
        self.controls.setObjectName("controls")
        c_layout = QVBoxLayout(self.controls)
        c_layout.setContentsMargins(12, 6, 12, 8)
        c_layout.setSpacing(4)
        row = QHBoxLayout()
        row.setSpacing(4)
        self.btn_play = QPushButton()
        self.btn_play.setObjectName("ctrl")
        self.btn_play.setIcon(_make_icon("play", 16, TEXT))
        self.btn_play.setIconSize(QSize(16, 16))
        self.btn_play.clicked.connect(self.toggle_pause)
        row.addWidget(self.btn_play)
        self.btn_stop = QPushButton()
        self.btn_stop.setObjectName("ctrl")
        self.btn_stop.setIcon(_make_icon("stop", 12, TEXT))
        self.btn_stop.setIconSize(QSize(12, 12))
        self.btn_stop.clicked.connect(self.stop)
        row.addWidget(self.btn_stop)
        self.time_lbl = QLabel("EN DIRECT")
        self.time_lbl.setObjectName("time")
        row.addWidget(self.time_lbl)
        row.addStretch()
        self.btn_mute = QPushButton()
        self.btn_mute.setObjectName("ctrl")
        self.btn_mute.setIcon(_make_icon("volume", 14, TEXT))
        self.btn_mute.setIconSize(QSize(14, 14))
        self.btn_mute.clicked.connect(self.toggle_mute)
        row.addWidget(self.btn_mute)
        self.vol = QSlider(Qt.Orientation.Horizontal)
        self.vol.setRange(0, 100)
        self.vol.setValue(80)
        self.vol.setFixedWidth(80)
        self.vol.valueChanged.connect(self.set_volume)
        row.addWidget(self.vol)
        self.btn_toggle = QPushButton()
        self.btn_toggle.setObjectName("ctrl")
        self.btn_toggle.setIcon(_make_icon("chevron-down", 12, CHEVRON))
        self.btn_toggle.setIconSize(QSize(12, 12))
        self.btn_toggle.clicked.connect(self.toggle_controls)
        row.addWidget(self.btn_toggle)
        c_layout.addLayout(row)
        v_layout.addWidget(self.controls)

        # Bouton flottant
        self.btn_reopen = QPushButton(self.stage)
        self.btn_reopen.setObjectName("ctrl")
        self.btn_reopen.setIcon(_make_icon("chevron-up", 14, CHEVRON))
        self.btn_reopen.setIconSize(QSize(14, 14))
        self.btn_reopen.setFixedSize(30, 30)
        self.btn_reopen.setStyleSheet("""
            QPushButton { background: rgba(12, 12, 14, 180); border: none; border-radius: 15px; }
            QPushButton:hover { background: rgba(255, 59, 59, 40); }
        """)
        self.btn_reopen.clicked.connect(self.toggle_controls)
        self.btn_reopen.hide()
        layout.addWidget(self.stage, stretch=1)

        # --- Liste stations ---
        header = QLabel("STATIONS GUNOUT PLAYER")
        header.setObjectName("status")
        layout.addWidget(header)
        self.stations = QListWidget()
        self.stations.setObjectName("stations")
        self.stations.setMaximumHeight(120)
        self.stations.itemDoubleClicked.connect(self._play_station_item)
        self.stations.itemActivated.connect(self._play_station_item)
        for station in STATIONS:
            it = QListWidgetItem(station["name"])
            it.setData(Qt.ItemDataRole.UserRole, station)
            self.stations.addItem(it)
        layout.addWidget(self.stations)
        self.status = QLabel("PRÊT")
        self.status.setObjectName("status")
        layout.addWidget(self.status)

        # Timers
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.setInterval(3500)
        self.hide_timer.timeout.connect(self._auto_hide_controls)

    def open_site_popup(self):
        popup = SitePopup(self)
        popup.exec()

    def showEvent(self, event):
        super().showEvent(event)
        if self.audio_player is None:
            self.audio_player = mpv.MPV(
                vo='null', ao='pulse', ytdl=False, cache=True, cache_secs=2,
                demuxer_max_bytes='2M', demuxer_max_back_bytes='1M',
                demuxer_readahead_secs=1, network_timeout=15,
                audio_client_name='Gunout Player', force_window='no', idle='yes',
            )
            self.audio_player.volume = self.vol.value()

    def _play_station_item(self, item):
        station = item.data(Qt.ItemDataRole.UserRole)
        self._play(station["url"], station["name"], station["type"])

    def _play(self, url, name, stream_type):
        self._current_type = stream_type
        self._current_station = name.upper()
        self.lbl_now.setText(self._current_station)

        if stream_type == "video":
            if self.audio_player:
                try: self.audio_player.command('stop')
                except Exception: pass
            self.viz.set_playing(False)
            # --- MASQUER le texte overlay en mode vidéo ---
            self.overlay.hide()
            self.media_stack.setCurrentIndex(1)
            self.btn_play.setIcon(_make_icon("pause", 16, TEXT))
            self.status.setText(f"TV : {name.upper()}")
            self.video_widget.play(url)
            return

        # Audio
        self.video_widget.stop()
        # --- AFFICHER le texte overlay en mode audio ---
        self.overlay.show()
        self.overlay.raise_()
        self.media_stack.setCurrentIndex(0)
        if self.audio_player is None:
            self.status.setText("LECTEUR NON PRÊT")
            return
        try:
            self.audio_player.command('stop')
            self.audio_player.pause = False
            self.audio_player.mute = False
        except Exception: pass
        self.lbl_meta.setText("CONNEXION...")
        self.btn_play.setIcon(_make_icon("pause", 16, TEXT))
        self.viz.set_playing(True)
        self.status.setText(f"LECTURE : {name.upper()}")
        self._reset_auto_hide()
        def _do_play():
            try:
                self.audio_player.play(url)
                self.lbl_meta.setText("EN DIRECT")
            except Exception as ex:
                self.status.setText(f"ERREUR : {ex}")
        QTimer.singleShot(200, _do_play)

    def toggle_pause(self):
        if self._current_type == "video":
            paused = False
            if self.video_widget.mpv and self.video_widget._initialized:
                paused = not self.video_widget.mpv.pause
            self.video_widget.set_pause(paused)
            self.btn_play.setIcon(_make_icon("play" if paused else "pause", 16, TEXT))
            return
        if not self.audio_player: return
        self.audio_player.pause = not self.audio_player.pause
        paused = self.audio_player.pause
        self.btn_play.setIcon(_make_icon("play" if paused else "pause", 16, TEXT))
        self.viz.set_playing(not paused)
        self.lbl_meta.setText("PAUSE" if paused else "EN DIRECT")

    def stop(self):
        if self.audio_player:
            try: self.audio_player.command('stop')
            except Exception: pass
        self.video_widget.stop()
        self.media_stack.setCurrentIndex(0)
        self.overlay.show()
        self.overlay.raise_()
        self.btn_play.setIcon(_make_icon("play", 16, TEXT))
        self.viz.set_playing(False)
        self.lbl_now.setText("AUCUNE STATION")
        self.lbl_meta.setText("EN ATTENTE")
        self.status.setText("ARRÊTÉ")
        self._current_type = "audio"

    def toggle_mute(self):
        if self._current_type == "video":
            if self.video_widget.mpv and self.video_widget._initialized:
                muted = not self.video_widget.mpv.mute
                self.video_widget.set_mute(muted)
                self.btn_mute.setIcon(_make_icon("mute" if muted else "volume", 14, TEXT))
            return
        if not self.audio_player: return
        self.audio_player.mute = not self.audio_player.mute
        self.btn_mute.setIcon(_make_icon("mute" if self.audio_player.mute else "volume", 14, TEXT))

    def set_volume(self, v):
        if self.audio_player:
            try: self.audio_player.volume = v
            except Exception: pass
        self.video_widget.set_volume(v)

    def toggle_window_fold(self):
        if self._window_folded:
            self.stage.show(); self.signature.show()
            self.status.show(); self.stations.show()
            target_h = self._unfolded_height
            self.btn_fold.setIcon(_make_icon("chevron-up", 14, CHEVRON))
            self._window_folded = False
            self.setMinimumSize(360, 320)
        else:
            self._unfolded_height = self.height()
            self.stage.hide(); self.signature.hide()
            self.status.hide(); self.stations.hide()
            target_h = 70
            self.btn_fold.setIcon(_make_icon("chevron-down", 14, CHEVRON))
            self._window_folded = True
            self.setMinimumSize(280, target_h)
        self.anim_fold = QPropertyAnimation(self, b"size")
        self.anim_fold.setDuration(240)
        self.anim_fold.setStartValue(self.size())
        self.anim_fold.setEndValue(QSize(self.width(), target_h))
        self.anim_fold.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim_fold.start()

    def _reset_auto_hide(self):
        if self._controls_collapsed or self._window_folded: return
        self.hide_timer.start()

    def _auto_hide_controls(self):
        if self._controls_collapsed or self._window_folded: return
        if self.controls.underMouse() or self.btn_reopen.underMouse():
            self.hide_timer.start(); return
        self._controls_collapsed = True
        self._controls_full_height = self.controls.height()
        self.btn_toggle.setIcon(_make_icon("chevron-up", 12, CHEVRON))
        self.btn_reopen.show(); self.btn_reopen.raise_()
        self._place_reopen_button()
        self.anim = QPropertyAnimation(self.controls, b"maximumHeight")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.controls.height())
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim.start()

    def toggle_controls(self):
        if self._controls_collapsed:
            target = self._controls_full_height or 60
            self.btn_toggle.setIcon(_make_icon("chevron-down", 12, CHEVRON))
            self._controls_collapsed = False
            self.btn_reopen.hide()
        else:
            self._controls_full_height = self.controls.height()
            target = 0
            self.btn_toggle.setIcon(_make_icon("chevron-up", 12, CHEVRON))
            self._controls_collapsed = True
            self.btn_reopen.show(); self.btn_reopen.raise_()
            self._place_reopen_button()
        self.anim = QPropertyAnimation(self.controls, b"maximumHeight")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.controls.height())
        self.anim.setEndValue(target)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim.start()
        if not self._controls_collapsed:
            self._reset_auto_hide()

    def _place_reopen_button(self):
        w = self.stage.width(); h = self.stage.height()
        self.btn_reopen.move(w - 44, h - 44)

    def _edge_at(self, pos):
        if self._window_folded: return None
        m = self._resize_margin
        r = self.rect()
        x, y = pos.x(), pos.y()
        left, right = x <= m, x >= r.width() - m
        top, bottom = y <= m, y >= r.height() - m
        if top and left: return "NW"
        if top and right: return "NE"
        if bottom and left: return "SW"
        if bottom and right: return "SE"
        if left: return "W"
        if right: return "E"
        if top: return "N"
        if bottom: return "S"
        return None

    def _cursor_for_edge(self, edge):
        return {
            "N": Qt.CursorShape.SizeVerCursor, "S": Qt.CursorShape.SizeVerCursor,
            "E": Qt.CursorShape.SizeHorCursor, "W": Qt.CursorShape.SizeHorCursor,
            "NE": Qt.CursorShape.SizeBDiagCursor, "SW": Qt.CursorShape.SizeBDiagCursor,
            "NW": Qt.CursorShape.SizeFDiagCursor, "SE": Qt.CursorShape.SizeFDiagCursor,
        }.get(edge, Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            edge = self._edge_at(e.position().toPoint())
            if edge:
                self._resize_edge = edge
                self._resize_start_geo = self.geometry()
                self._resize_start_pos = e.globalPosition().toPoint()
                return
            self._drag_pos = e.globalPosition().toPoint()

    def mouseMoveEvent(self, e):
        pos = e.position().toPoint()
        if self._resize_edge and (e.buttons() & Qt.MouseButton.LeftButton):
            delta = e.globalPosition().toPoint() - self._resize_start_pos
            g = self._resize_start_geo
            x, y, w, h = g.x(), g.y(), g.width(), g.height()
            edge = self._resize_edge
            min_w, min_h = self.minimumWidth(), self.minimumHeight()
            if "E" in edge: w = max(min_w, g.width() + delta.x())
            if "S" in edge: h = max(min_h, g.height() + delta.y())
            if "W" in edge:
                new_w = max(min_w, g.width() - delta.x())
                x = g.x() + (g.width() - new_w); w = new_w
            if "N" in edge:
                new_h = max(min_h, g.height() - delta.y())
                y = g.y() + (g.height() - new_h); h = new_h
            self.setGeometry(x, y, w, h)
            return
        edge = self._edge_at(pos)
        self.setCursor(QCursor(self._cursor_for_edge(edge)))
        if self._drag_pos is not None:
            delta = e.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = e.globalPosition().toPoint()
        self._reset_auto_hide()

    def mouseReleaseEvent(self, e):
        self._resize_edge = None
        self._drag_pos = None
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'overlay'):
            self.overlay.setGeometry(self.stage.rect())
        if self.btn_reopen.isVisible():
            self._place_reopen_button()

    def closeEvent(self, event):
        if self.audio_player is not None:
            try: self.audio_player.terminate()
            except Exception: pass
        self.video_widget.cleanup()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Inter", 9))
    w = GunoutPlayer()
    w.show()
    sys.exit(app.exec())