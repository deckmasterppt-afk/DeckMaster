# config.py
# Configuration settings for DeckMaster

import os

# Server Configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Admin Configuration (Simple Admin Access for Testing)
ADMIN_MODE = True  # Enable admin mode for all users (testing)
ADMIN_PASSWORD = "DeckMaster2024!@#SecureAdmin"  # Keep password for security
ADMIN_SESSION_TIMEOUT = 3600  # 1 hour in seconds

# Admin user detection (only when admin mode is activated)
ADMIN_USER_PREFIXES = [
    'user_',      # All generated user IDs (when admin mode active)
    'admin',      # Admin users
    'test_',      # Test users
]

# Directory Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
WEBSITE_FILE = 'presentation_tool_website.html'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Subscription Plans Configuration
SUBSCRIPTION_PLANS = {
    'free': {
        'name': 'Free',
        'daily_limit': 3,
        'total_limit': 3,  # Lifetime limit for free tier
        'max_slides': 5,
        'has_ads': True,
        'visual_elements': False,
        'price': 0,
        'description': 'Perfect for trying out DeckMaster'
    },
    'elite': {
        'name': 'Elite',
        'daily_limit': 5,
        'total_limit': None,  # No lifetime limit
        'max_slides': 15,  # Elite gets 15 slides
        'has_ads': False,
        'visual_elements': True,
        'price': 10,
        'description': 'Great for regular users'
    },
    'pro': {
        'name': 'Pro',
        'daily_limit': 10,
        'total_limit': None,
        'max_slides': 10,  # Pro gets 10 slides
        'has_ads': False,
        'visual_elements': True,
        'price': 20,
        'description': 'Perfect for professionals'
    },
    'premium': {
        'name': 'Premium',
        'daily_limit': 20,
        'total_limit': None,
        'max_slides': 20,
        'has_ads': False,
        'visual_elements': True,
        'price': 25,
        'description': 'Ultimate presentation power'
    }
}

# Design Styles Configuration (from your design_styles.py)
AVAILABLE_DESIGN_STYLES = {
    # Minimal Designs
    'minimal_1': 'Pure White',
    'minimal_2': 'Soft Gray', 
    'minimal_3': 'Ivory Elegance',
    'minimal_4': 'Light Blue',
    'minimal_5': 'Pale Green',
    'minimal_6': 'Warm Beige',
    
    # Corporate Designs
    'corporate_1': 'Navy Blue',
    'corporate_2': 'Deep Blue',
    'corporate_3': 'Charcoal',
    'corporate_4': 'Royal Blue',
    'corporate_5': 'Slate Gray',
    'corporate_6': 'Business Green',
    'corporate_7': 'Professional Purple',
    'corporate_8': 'Executive Navy',
    
    # Creative Designs
    'creative_1': 'Sunset Orange',
    'creative_2': 'Vibrant Pink',
    'creative_3': 'Electric Blue',
    'creative_4': 'Lime Green',
    'creative_5': 'Purple Dream',
    'creative_6': 'Coral Red',
    'creative_7': 'Turquoise',
    'creative_8': 'Golden Yellow',
    
    # Academic Designs
    'academic_1': 'Forest Green',
    'academic_2': 'Oxford Blue',
    'academic_3': 'Burgundy',
    'academic_4': 'Teal Scholar',
    'academic_5': 'Maroon',
    'academic_6': 'Sage Green',
    'academic_7': 'Royal Purple',
    'academic_8': 'Navy Scholar',
    
    # Tech Designs
    'tech_1': 'Dark Tech',
    'tech_2': 'Cyber Blue',
    'tech_3': 'Matrix Green',
    'tech_4': 'Neon Purple',
    'tech_5': 'Dark Mode',
    'tech_6': 'Electric Blue',
    'tech_7': 'Holographic',
    'tech_8': 'Digital Orange',
    
    # Modern Designs
    'modern_1': 'Gradient Blue',
    'modern_2': 'Sunset Glow',
    'modern_3': 'Ocean Wave',
    'modern_4': 'Forest Mist',
    'modern_5': 'Purple Haze',
    'modern_6': 'Golden Hour',
    'modern_7': 'Arctic Blue',
    'modern_8': 'Coral Reef'
}

# API Configuration
API_PREFIX = '/api'
CORS_ORIGINS = ['*']  # In production, specify exact origins

# External API Configuration
UNSPLASH_ACCESS_KEY = 'eNbrjbqwpr5POrDSZPpQYM12u763_kpTnKWfsXOQwlk'
UNSPLASH_SECRET_KEY = 'JY2q9uFDkw1bB81ItRoVnwngKRiw0MTSVtOhsmmIf8Q'
UNSPLASH_APPLICATION_ID = '849864'

PEXELS_API_KEY = 'rVZGuMgTaTyfgTL08XtLUcl2xfuMJjJL0apbLaypa4ShkXwnOznhYP51'

# Image API Settings
IMAGE_SEARCH_RESULTS_LIMIT = 10
IMAGE_DOWNLOAD_TIMEOUT = 30
IMAGE_MAX_SIZE = 2048  # Max width/height in pixels

# Job Processing Configuration
JOB_TIMEOUT = 300  # 5 minutes timeout for PPT generation
MAX_CONCURRENT_JOBS = 5

# File Configuration
ALLOWED_EXTENSIONS = {'pptx'}
MAX_FILENAME_LENGTH = 100

# Rate Limiting Configuration
RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_HOUR = 100

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'