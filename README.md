# DeckMaster - Professional Presentation Generator

A clean, professional presentation generation system that creates beautiful PowerPoint presentations with one visual element per slide.

## Features

- **Beautiful Simple System** - Clean, uncluttered layouts with maximum one visual per slide
- **14 Professional Design Styles** - From minimal to corporate to creative
- **Smart Visual Elements** - Automatic charts, tables, and high-quality images
- **Professional Distribution** - Balanced visual variety throughout presentations
- **Web Interface** - Easy-to-use browser-based interface
- **Admin Mode** - Unlimited features for power users

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server**
   ```bash
   python start_server.py
   ```
   Or on Windows:
   ```bash
   start.bat
   ```

3. **Open Browser**
   Navigate to: `http://localhost:5000`

4. **Create Presentations**
   - Enter your topic and URL
   - Choose design style
   - Select number of slides
   - Generate beautiful presentations!

## Admin Mode

Activate admin mode for unlimited features:
- Password: `DeckMaster2024!@#SecureAdmin`
- Keyboard shortcut: `Ctrl+Shift+A`

## System Requirements

- Python 3.8+
- Internet connection (for image and content APIs)
- Modern web browser

## Project Structure

```
├── app.py                    # Main Flask application
├── start_server.py          # Server startup script
├── pipeline.py              # Presentation generation pipeline
├── beautiful_simple_system.py # Clean layout system
├── design_styles.py         # 14 professional design styles
├── visual_elements.py       # Visual element integration
├── image_api_service.py     # Image API integration
├── chart_service.py         # Chart generation
├── index.html               # Web interface
├── static/                  # CSS and JavaScript files
└── requirements.txt         # Python dependencies
```

## Configuration

Update `config.py` with your API keys for enhanced functionality:
- Image services for high-quality visuals
- Chart generation for data visualization

## License

Professional presentation generation system for creating beautiful, clean presentations.