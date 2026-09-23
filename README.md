<div align="center">

# 🎧 Gunout Player

**Lecteur radio & TV multi-plateformes — Réunion & Outre-mer**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5%2B-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt6/)
[![mpv](https://img.shields.io/badge/mpv-libmpv-691F69?style=for-the-badge&logo=mpv&logoColor=white)](https://mpv.io/)
[![OpenGL](https://img.shields.io/badge/OpenGL-Render_API-5586A4?style=for-the-badge&logo=opengl&logoColor=white)](https://www.opengl.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-000000?style=for-the-badge&logo=linux&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()
[![Made in Réunion](https://img.shields.io/badge/Made%20in-🇷🇪%20Réunion-ff3b3b?style=for-the-badge)]()

*Interface sombre, sans cadre, avec visualiseur audio et rendu vidéo OpenGL natif.*

</div>

---

## 📖 Sommaire

- [Aperçu](#-aperçu)
- [Fonctionnalités](#-fonctionnalités)
- [Stations incluses](#-stations-incluses)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Raccourcis & contrôles](#-raccourcis--contrôles)
- [Architecture](#-architecture)
- [Dépendances](#-dépendances)
- [Compilation](#-compilation)
- [Contribuer](#-contribuer)
- [Licence](#-licence)
- [Auteur](#-auteur)

---

## 🎬 Aperçu

**Gunout Player** est un lecteur multimédia léger conçu pour écouter les radios et regarder les chaînes TV de La Réunion et de l'Outre-mer français. Il combine :

- 🎵 **Lecture audio** via `libmpv` avec visualiseur animé
- 📺 **Lecture vidéo HLS** via `MpvRenderContext` + OpenGL
- 🌑 **Interface frameless** moderne, style "glassmorphism"
- ⚡ **Lancement instantané** et faible empreinte mémoire

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| 🎨 **UI frameless** | Fenêtre sans bordure, coins arrondis, drag & resize natif |
| 🔊 **Visualiseur audio** | 32 barres animées réactives à l'état de lecture |
| 🎥 **Rendu vidéo OpenGL** | Intégration directe de `libmpv` dans un `QOpenGLWidget` |
| 📻 **23 stations préconfigurées** | Radios & TV de La Réunion, Antilles, Outre-mer |
| 🌐 **Accès direct aux sites** | Popup dédiée vers Gunout Webradio |
| 🎚️ **Contrôle du volume** | Slider + bouton mute |
| 📌 **Fenêtre pliable** | Mode compact (repli) pour économiser l'espace |
| 🕹️ **Contrôles auto-masqués** | La barre disparaît après 3,5 s d'inactivité |
| 🔄 **Support HLS / AAC / MP3** | Compatible `.m3u8`, `.aac`, `.mp3` |

---

## 📡 Stations incluses

<details>
<summary><b>Cliquez pour voir les 23 stations</b></summary>

### 🎙️ Radios (audio)

| # | Station | Format |
|---|---------|--------|
| 1 | ExoFM | AAC |
| 2 | France Bleu Creuse | MP3 |
| 3 | Freedom1 | MP3 |
| 4 | KreolFM | AAC |
| 5 | NeoFM | MP3 |
| 6 | Réunion 1ère | MP3 |
| 7 | Martinique 1ère | MP3 |
| 8 | Guyane 1ère | MP3 |
| 9 | Guadeloupe 1ère | MP3 |
| 10 | Mayotte 1ère | MP3 |
| 11 | Nouvelle-Calédonie 1ère | MP3 |
| 12 | Wallis et Futuna 1ère | MP3 |
| 13 | Saint-Pierre et Miquelon 1ère | MP3 |
| 14 | Outremer 1ère | MP3 |
| 15 | Polynésie 1ère | MP3 |
| 16 | Skyrock | MP3 |
| 18 | Urban Hit Réunion | MP3 |
| 19 | Gleaphe Radio | MP3 |
| 20 | Radio Pikan | MP3 |
| 21 | Antenne Réunion Radio | AAC |

### 📺 Chaînes TV (vidéo HLS)

| # | Chaîne | Format |
|---|--------|--------|
| 17 | Generation TV | HLS |
| 22 | Antenne Réunion TV | HLS |
| 23 | EXO TV | HLS |

</details>

---

## 🚀 Installation

### Prérequis

- **Python 3.10+**
- **libmpv** installé sur le système
- **PyQt6** avec support OpenGL

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-user/gunout-player.git
cd gunout-player
```

### 2. Installer libmpv

**Debian / Ubuntu**
```bash
sudo apt install libmpv-dev mpv
```

**Fedora**
```bash
sudo dnf install mpv-libs-devel
```

**Arch Linux**
```bash
sudo pacman -S mpv
```

**macOS (Homebrew)**
```bash
brew install mpv
```

**Windows**
Télécharger `libmpv` depuis [mpv.io/installation](https://mpv.io/installation/) et placer `libmpv-2.dll` à côté du script.

### 3. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows
```

### 4. Installer les dépendances Python

```bash
pip install PyQt6 python-mpv
```

---

## 🎮 Utilisation

### Lancement

```bash
python gunout_player.py
```

### Contrôles

| Action | Comment |
|--------|---------|
| ▶️ Lancer une station | **Double-clic** sur un élément de la liste |
| ⏸️ Pause / Reprise | Bouton ▶️ / ⏸️ |
| ⏹️ Arrêter | Bouton ⏹️ |
| 🔊 Volume | Slider horizontal |
| 🔇 Mute | Bouton haut-parleur |
| 📌 Replier fenêtre | Chevron en haut à droite |
| 🌐 Ouvrir le site | Bouton **SITES** |
| 🖱️ Déplacer fenêtre | Clic-glisser sur la zone supérieure |
| 📐 Redimensionner | Glisser sur les bords / coins |

---

## 🏗️ Architecture

```
gunout_player.py
│
├── STATIONS              → Catalogue des flux (audio / vidéo)
├── SITE_LINKS            → Liens externes (Gunout Webradio)
├── STYLE                 → Feuille QSS globale (thème sombre)
│
├── _make_icon()          → Génération d'icônes vectorielles
├── Visualizer            → Widget de visualisation audio (32 barres)
├── MPVVideoWidget        → Rendu vidéo OpenGL via MpvRenderContext
├── SitePopup             → Popup modale pour les liens externes
└── GunoutPlayer          → Fenêtre principale (QMainWindow)
```

**Points clés techniques :**

- `MpvRenderContext` avec `get_proc_address` pour l'intégration OpenGL
- `locale.setlocale(LC_NUMERIC, 'C')` **avant** l'init de mpv (obligatoire)
- Deux instances mpv distinctes : une audio (`vo=null`) et une vidéo (`vo=libmpv`)
- Gestion custom du drag/resize (fenêtre frameless)
- Animations `QPropertyAnimation` pour le repli et l'auto-masquage

---

## 📦 Dépendances

| Paquet | Version | Rôle |
|--------|---------|------|
| `PyQt6` | ≥ 6.5 | Interface graphique |
| `python-mpv` | ≥ 1.0 | Binding Python vers libmpv |
| `libmpv` | ≥ 0.35 | Moteur de lecture |
| `OpenGL` | 3.3+ | Rendu vidéo |

---

## 🔨 Compilation

### Linux / macOS

```bash
pyinstaller --noconfirm --windowed \
  --name "Gunout Player" \
  --icon logo.png \
  gunout_player.py
```

### Windows

```bash
pyinstaller --noconfirm --windowed ^
  --name "Gunout Player" ^
  --icon logo.ico ^
  --add-binary "libmpv-2.dll;." ^
  gunout_player.py
```

---

## 🤝 Contribuer

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commit (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Push (`git push origin feature/ma-fonctionnalite`)
5. Ouvrir une **Pull Request**

---

## 📄 Licence

Ce projet est sous licence **MIT** — voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

<div align="center">

**Gleaphe**

[![Website](https://img.shields.io/badge/Website-gradio--gleaphe.duckdns.org-ff3b3b?style=for-the-badge&logo=googlechrome&logoColor=white)](https://gradio-gleaphe.duckdns.org/)
[![Made in Réunion](https://img.shields.io/badge/🇷🇪-La%20Réunion-ff3b3b?style=for-the-badge)]()

</div>

---

<div align="center">

**⭐ Si ce projet vous plaît, n'hésitez pas à laisser une étoile ! ⭐**

*Fait avec ❤️ à La Réunion*

</div>
