# Snakepit

A Python remake of the classic C64 game Snakepit, built with Pygame.

## Description

Snakepit is a game where you control a player character trying to collect eggs while avoiding snakes. The snakes move around in their enclosures, and one special snake can eat eggs and grow longer.

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```
   pip install pygame numpy
   ```

## How to Play

1. Run the game:
   ```
   python -m main
   ```
2. Click the "Play" button to start
3. Use the arrow keys to move your player
4. Collect eggs to increase your score
5. Avoid the snakes - if you touch one, it's game over!
6. Press P to pause the game
7. Press ESC to quit

## Controls

- Arrow Keys: Move player
- P: Pause game
- ESC: Quit game

## Mobile Support

This game is currently designed for desktop computers with keyboard controls. However, there are several ways to make it available on mobile devices:

### Web Deployment (Playable on Mobile Browsers)

The easiest way to make this game accessible on mobile devices is to deploy it as a web application using Pygbag:

1. Install Pygbag:
   ```
   pip install pygbag
   ```

2. Run the deployment tool:
   ```
   pygbag main.py
   ```

3. This will create a web-compatible version in the `build/web` directory that you can:
   - Test locally by opening the URL shown in the terminal
   - Deploy to GitHub Pages or any web hosting service
   - Share the link with friends to play in their mobile browsers

Pygbag automatically adds touch controls for mobile devices, making the game playable without a keyboard.

#### Free Hosting Options

1. **GitHub Pages (Recommended)**
   - Create a GitHub account if you don't have one
   - Create a new repository named `snakepit`
   - Push your code including the `build/web` directory
   - Go to repository Settings → Pages
   - Enable GitHub Pages and select the branch containing your web files
   - Your game will be available at `https://[your-username].github.io/snakepit`

2. **Netlify Drop**
   - Go to [app.netlify.com/drop](https://app.netlify.com/drop)
   - Drag and drop your `build/web` directory
   - Get a URL like `https://your-game-name.netlify.app`

3. **Vercel**
   - Create a Vercel account
   - Install Vercel CLI: `npm i -g vercel`
   - Run `vercel` in your `build/web` directory
   - Get a URL like `https://your-game-name.vercel.app`

4. **Cloudflare Pages**
   - Create a Cloudflare account
   - Go to Pages → Create a project
   - Connect your GitHub repository
   - Set the build directory to `build/web`
   - Get a URL like `https://your-game-name.pages.dev`

All these options are completely free and provide:
- HTTPS security
- Global CDN for fast loading
- Automatic updates when you push changes
- Custom domain support (optional)

### Native Mobile Apps

For a more polished mobile experience, you could convert the game using:

1. **Briefcase (part of BeeWare)**: Package Python apps for iOS, Android, Windows, macOS, and Linux
   ```
   pip install briefcase
   briefcase new
   # Follow the prompts to set up your project
   briefcase create android
   briefcase build android
   ```

2. **Kivy/KivyMD**: Reimplement the game using this cross-platform framework
   
3. **Commercial Services**: Use services like GamePix or CrazyGames that can convert HTML5 games for various platforms

## Credits

- Original C64 game: Snakepit
- Sound effects created with NumPy

## Project Structure
```
snakepit/
├── main.py           # Main game entry point
├── game/
│   ├── __init__.py
│   ├── game.py      # Main game logic
│   ├── player.py    # Player character
│   ├── snake.py     # Snake behavior
│   ├── egg.py       # Egg and wall mechanics
│   └── sound.py     # Sound effects
├── assets/
│   ├── sounds/      # Sound effects
│   └── graphics/    # Game sprites
└── requirements.txt  # Python dependencies
```

## Technologies Used
- Python 3.8+
- Pygame (for graphics and sound)
- NumPy (for efficient array operations) 