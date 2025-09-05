# 🐦 Flappy Bird - Welcome Tambay Edition v1.0

A unique version of Flappy Bird with character selection, animated sprites, and personalized sky banners!

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Version](https://img.shields.io/badge/Version-1.0-red)

## ✨ Features

### 🎮 Dual Character System
- **Flappy Bird**: Classic bird with animated flapping wings
- **Super Mario**: Detailed Mario sprite with dynamic arm movements

### 🎯 Special Features
- **Sky Banners**: Jets fly across with "Welcome Tambay" banners
- **Animated Contrails**: Realistic smoke trails behind jets
- **Character Selection Screen**: Choose your character before playing
- **Dynamic Backgrounds**: Beautiful sky with clouds and ground

### 🕹️ Gameplay
- Navigate through green pipes
- Score points for each pipe passed
- Increasing difficulty as you progress
- Smooth physics and collision detection

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/flappy-bird-welcome-tambay.git
cd flappy-bird-welcome-tambay
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the game**
```bash
python flappy_bird.py
```

## 🎮 How to Play

### Controls
| Key | Action |
|-----|--------|
| `1` | Select Bird character |
| `2` | Select Mario character |
| `SPACE` | Jump/Flap wings |
| `C` | Change character (when not playing) |
| `ESC` | Quit game |

### Gameplay Instructions
1. **Start**: Choose your character (1 for Bird, 2 for Mario)
2. **Play**: Press SPACE to make your character jump
3. **Avoid**: Don't hit the pipes or ground
4. **Score**: Pass through pipes to earn points
5. **Restart**: Press SPACE after game over

## 🏗️ Project Structure

```
flappy-bird-welcome-tambay/
│
├── flappy_bird.py          # Main game file
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore file
```

## 🎨 Game Components

### Character Classes
- `Character` (Abstract Base Class)
- `Bird` - Flappy bird with wing animation
- `Mario` - Super Mario with arm animations

### Environment Classes
- `Pipe` - Obstacle generation and movement
- `JetPlane` - Background jets with banners
- `Game` - Main game loop and state management

## 🚀 Features in Detail

### Animated Bird Character
- 3-state wing animation (up, middle, down)
- Smooth flapping motion
- Yellow body with orange accents
- Detailed eye and beak

### Super Mario Character
- Red cap with "M" logo
- Blue overalls with yellow buttons
- Iconic mustache
- Arms that move when jumping
- White gloves and brown shoes

### Sky Banner System
- Jets spawn randomly every 5-10 seconds
- Red banners with "Welcome Tambay" text
- Wave animation for realistic flutter
- Rope connection to plane
- Bidirectional flight paths

## 📈 Version History

### v1.0 (Current)
- Initial release
- Dual character system (Bird & Mario)
- Sky banner feature with "Welcome Tambay"
- Complete gameplay mechanics
- Score tracking
- Character selection screen

## 🔧 Configuration

### Game Constants (Customizable)
```python
SCREEN_WIDTH = 400          # Game window width
SCREEN_HEIGHT = 600         # Game window height
FPS = 60                    # Frames per second
GRAVITY = 0.5              # Gravity strength
JUMP_STRENGTH = -8         # Jump power
PIPE_GAP = 180            # Gap between pipes
PIPE_SPEED = 3            # Pipe movement speed
```

## 🐛 Known Issues
- None reported yet

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original Flappy Bird game by Dong Nguyen
- Pygame community for the excellent game development framework
- "Welcome Tambay" - Special greeting for our community

## 📧 Contact

Your Name - [@BenLorenzoDev](https://www.messenger.com/t/benlorenzodev)

Project Link: ([https://github.com/benlorenzodev/flappy-bird-welcome-tambay](https://github.com/BenLorenzoDev/flappy-bird-tambay))

---

**Made with ❤️ for Tambay**

*Enjoy the game and try to beat the high score!*
