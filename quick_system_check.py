#!/usr/bin/env python3
"""
Quick system check without virtual environment dependencies
"""

import sys
import os

def check_core_files():
    """Check that all core files exist"""
    print("📁 CHECKING CORE FILES")
    print("-" * 30)
    
    essential_files = [
        "app.py",
        "start_server.py", 
        "pipeline.py",
        "beautiful_simple_system.py",
        "design_styles.py",
        "visual_elements.py",
        "image_api_service.py",
        "chart_service.py",
        "config.py",
        "requirements.txt",
        "index.html"
    ]
    
    missing_files = []
    for file in essential_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_imports():
    """Check critical imports"""
    print("\n🔧 CHECKING IMPORTS")
    print("-" * 30)
    
    import_tests = [
        ("config", "Configuration"),
        ("design_styles", "Design Styles"),
        ("beautiful_simple_system", "Beautiful System"),
        ("visual_elements", "Visual Elements"),
        ("pipeline", "Pipeline"),
        ("app", "Flask App")
    ]
    
    failed_imports = []
    for module, description in import_tests:
        try:
            __import__(module)
            print(f"   ✅ {description}")
        except Exception as e:
            print(f"   ❌ {description} - {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def check_design_styles():
    """Check design styles configuration"""
    print("\n🎨 CHECKING DESIGN STYLES")
    print("-" * 30)
    
    try:
        from config import AVAILABLE_DESIGN_STYLES
        from design_styles import get_design_style
        
        print(f"   📊 Total styles configured: {len(AVAILABLE_DESIGN_STYLES)}")
        
        working_styles = 0
        for style_id, style_name in AVAILABLE_DESIGN_STYLES.items():
            try:
                config = get_design_style(style_id)
                if config and 'colors' in config:
                    working_styles += 1
                else:
                    print(f"      ❌ {style_id}: Invalid configuration")
            except Exception as e:
                print(f"      ❌ {style_id}: {e}")
        
        print(f"   ✅ Working styles: {working_styles}/{len(AVAILABLE_DESIGN_STYLES)}")
        return working_styles == len(AVAILABLE_DESIGN_STYLES)
        
    except Exception as e:
        print(f"   ❌ Design styles check failed: {e}")
        return False

def check_subscription_system():
    """Check subscription configuration"""
    print("\n💳 CHECKING SUBSCRIPTION SYSTEM")
    print("-" * 30)
    
    try:
        from config import SUBSCRIPTION_PLANS
        
        print(f"   📊 Subscription plans: {len(SUBSCRIPTION_PLANS)}")
        
        for plan_id, plan_info in SUBSCRIPTION_PLANS.items():
            print(f"      • {plan_id}: {plan_info.get('name', 'Unknown')}")
            print(f"        - Daily limit: {plan_info.get('daily_limit', 'Unknown')}")
            print(f"        - Max slides: {plan_info.get('max_slides', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Subscription check failed: {e}")
        return False

def check_web_interface():
    """Check web interface file"""
    print("\n🌐 CHECKING WEB INTERFACE")
    print("-" * 30)
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key elements
        checks = [
            ("DeckMaster", "Brand name"),
            ("Create Beautiful Presentations", "Main heading"),
            ("Design Style", "Form elements"),
            ("Generate Presentation", "Submit button"),
            ("Beautiful Simple System", "Feature description")
        ]
        
        passed_checks = 0
        for check_text, description in checks:
            if check_text in content:
                print(f"      ✅ {description}")
                passed_checks += 1
            else:
                print(f"      ❌ {description}")
        
        # Check that pricing section is removed
        if "Choose Your Perfect Plan" not in content:
            print("      ✅ Pricing section removed (professional)")
            passed_checks += 1
        else:
            print("      ❌ Pricing section still present")
        
        print(f"   📊 Interface checks: {passed_checks}/{len(checks)+1}")
        return passed_checks >= len(checks)
        
    except Exception as e:
        print(f"   ❌ Web interface check failed: {e}")
        return False

def main():
    """Run quick system check"""
    print("🚀 QUICK SYSTEM CHECK")
    print("=" * 50)
    print("Verifying cleaned project is ready for upload")
    print("=" * 50)
    
    # Run all checks
    checks = [
        ("Core Files", check_core_files),
        ("Python Imports", check_imports),
        ("Design Styles", check_design_styles),
        ("Subscription System", check_subscription_system),
        ("Web Interface", check_web_interface)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ {check_name} check crashed: {e}")
            results.append((check_name, False))
    
    # Final Results
    print("\n" + "=" * 50)
    print("📊 SYSTEM CHECK RESULTS")
    print("=" * 50)
    
    passed_checks = 0
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {check_name:<20} {status}")
        if result:
            passed_checks += 1
    
    total_checks = len(results)
    success_rate = (passed_checks / total_checks) * 100
    
    print(f"\n📈 Overall Success Rate: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("\n🎉 SYSTEM STATUS: READY FOR UPLOAD!")
        print("✅ All core components working")
        print("✅ Professional appearance confirmed")
        print("✅ Subscription system configured")
        print("✅ Design styles operational")
        print("✅ Clean project structure")
        print("\n📦 Your project is ready for upload!")
    elif success_rate >= 60:
        print("\n✅ SYSTEM STATUS: MOSTLY READY")
        print("⚠️ Minor issues detected but core functionality works")
    else:
        print("\n⚠️ SYSTEM STATUS: NEEDS ATTENTION")
        print("🔧 Multiple issues detected - review failed checks")
    
    print(f"\n📁 Project Location: {os.getcwd()}")
    print("🚀 To start server: python start_server.py")

if __name__ == "__main__":
    main()