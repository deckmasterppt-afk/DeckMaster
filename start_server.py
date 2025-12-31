#!/usr/bin/env python3
# start_server.py
# Simple startup script for DeckMaster

import sys
import os

def check_system():
    """Check if system is ready"""
    print("🔍 Checking DeckMaster system...")
    
    # Check critical imports
    try:
        from config import SUBSCRIPTION_PLANS, AVAILABLE_DESIGN_STYLES
        print(f"✅ Config: {len(SUBSCRIPTION_PLANS)} plans, {len(AVAILABLE_DESIGN_STYLES)} designs")
        
        from user_manager import user_manager
        print("✅ User manager ready")
        
        from presentation_service import presentation_service
        print("✅ Presentation service ready")
        
        from design_styles import list_available_designs
        designs = list_available_designs()
        print(f"✅ Design styles: {len(designs)} available")
        
        from app import app
        print("✅ Flask app ready")
        
        return True
    except Exception as e:
        print(f"❌ System check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main startup function"""
    print("🚀 DeckMaster - PPT Generation Service")
    print("=" * 50)
    
    if not check_system():
        print("❌ System check failed. Please fix the errors above.")
        return False
    
    print("\n✅ All systems ready!")
    print("\n🌐 Starting Flask server...")
    print("   Server will be available at: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)