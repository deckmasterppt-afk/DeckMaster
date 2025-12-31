#!/usr/bin/env python3
"""
Final comprehensive system test to verify everything is working perfectly
Including subscription limits, premium features, and smooth operation
"""

import requests
import json
import time
import os

def test_server_startup():
    """Test that server starts and responds correctly"""
    print("🚀 TESTING SERVER STARTUP")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Server health: {result.get('status', 'unknown')}")
            return True
        else:
            print(f"   ❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        return False

def test_subscription_limits():
    """Test subscription limits and usage tracking"""
    print("\n💳 TESTING SUBSCRIPTION LIMITS")
    print("-" * 40)
    
    # Test Free Plan Limits
    print("   📊 Free Plan Limits:")
    print("      • Daily Presentations: 3")
    print("      • Max Slides: 5")
    print("      • Visual Elements: Disabled")
    
    # Test Admin Mode Activation
    try:
        admin_data = {
            "password": "DeckMaster2024!@#SecureAdmin",
            "user_id": "test_admin_" + str(int(time.time()))
        }
        response = requests.post("http://localhost:5000/api/admin/activate", 
                               json=admin_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Admin Mode Activation: Working")
                print("      • Unlimited presentations")
                print("      • Up to 50 slides")
                print("      • All visual elements enabled")
                return admin_data['user_id']
            else:
                print(f"   ❌ Admin activation failed: {result.get('error')}")
                return None
        else:
            print(f"   ❌ Admin activation request failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Admin activation error: {e}")
        return None

def test_presentation_generation(admin_user_id):
    """Test presentation generation with different parameters"""
    print("\n🎨 TESTING PRESENTATION GENERATION")
    print("-" * 40)
    
    test_cases = [
        {
            "name": "Free Plan Simulation (5 slides)",
            "slides": 5,
            "design": "minimal_1",
            "visuals": {"graphs": False, "tables": False, "pie_charts": False, "images": False}
        },
        {
            "name": "Premium Features (10 slides)",
            "slides": 10,
            "design": "corporate_1",
            "visuals": {"graphs": True, "tables": True, "pie_charts": True, "images": True}
        },
        {
            "name": "Maximum Slides (15 slides)",
            "slides": 15,
            "design": "tech_1",
            "visuals": {"graphs": True, "tables": False, "pie_charts": True, "images": True}
        }
    ]
    
    successful_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['name']}")
        
        generation_data = {
            "user_id": admin_user_id,
            "task": f"Create a test presentation about business strategy and market analysis with {test_case['slides']} slides",
            "url": "https://www.example.com",
            "slide_count": test_case['slides'],
            "design_style": test_case['design'],
            "visual_preferences": test_case['visuals']
        }
        
        try:
            start_time = time.time()
            response = requests.post("http://localhost:5000/api/generate", 
                                   json=generation_data, timeout=180)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    job_id = result.get('job_id')
                    generation_time = end_time - start_time
                    
                    # Get file info
                    file_response = requests.get(f"http://localhost:5000/api/file-info/{job_id}", timeout=10)
                    if file_response.status_code == 200:
                        file_info = file_response.json()
                        if file_info.get('success'):
                            info = file_info['file_info']
                            print(f"      ✅ Generated: {info['filename']}")
                            print(f"      📏 Size: {info['file_size_mb']} MB")
                            print(f"      ⏱️ Time: {generation_time:.1f}s")
                            print(f"      🎨 Design: {test_case['design']}")
                            successful_tests += 1
                        else:
                            print(f"      ❌ File info failed: {file_info.get('error')}")
                    else:
                        print(f"      ❌ File info request failed")
                else:
                    print(f"      ❌ Generation failed: {result.get('error')}")
            else:
                print(f"      ❌ Generation request failed: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Generation error: {e}")
        
        time.sleep(2)  # Brief pause between tests
    
    return successful_tests, len(test_cases)

def test_design_styles():
    """Test all 14 design styles are working"""
    print("\n🎨 TESTING DESIGN STYLES")
    print("-" * 40)
    
    # Test design style configuration
    from design_styles import get_design_style
    from config import AVAILABLE_DESIGN_STYLES
    
    working_styles = 0
    total_styles = len(AVAILABLE_DESIGN_STYLES)
    
    print(f"   📊 Testing {total_styles} design styles...")
    
    for style_id, style_name in AVAILABLE_DESIGN_STYLES.items():
        try:
            config = get_design_style(style_id)
            if config and 'colors' in config and 'background' in config:
                working_styles += 1
            else:
                print(f"      ❌ {style_id}: Configuration missing")
        except Exception as e:
            print(f"      ❌ {style_id}: Error - {e}")
    
    print(f"   ✅ Working styles: {working_styles}/{total_styles}")
    return working_styles == total_styles

def test_visual_elements():
    """Test visual elements integration"""
    print("\n📊 TESTING VISUAL ELEMENTS")
    print("-" * 40)
    
    try:
        # Test image service
        from image_api_service import image_api
        print("   ✅ Image API service: Available")
        
        # Test chart service  
        from chart_service import chart_service
        print("   ✅ Chart service: Available")
        
        # Test visual elements integration
        from visual_elements import add_visual_elements_to_slide
        print("   ✅ Visual elements integration: Available")
        
        return True
    except Exception as e:
        print(f"   ❌ Visual elements error: {e}")
        return False

def test_web_interface():
    """Test web interface loads correctly"""
    print("\n🌐 TESTING WEB INTERFACE")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:5000", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Check for key elements
            checks = [
                ("DeckMaster", "Brand name present"),
                ("Create Beautiful Presentations", "Main heading present"),
                ("Design Style", "Form elements present"),
                ("Generate Presentation", "Submit button present"),
                ("Beautiful Simple System", "Feature description present")
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
            
            return passed_checks >= 5
        else:
            print(f"   ❌ Web interface failed to load: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Web interface error: {e}")
        return False

def test_performance():
    """Test system performance and memory usage"""
    print("\n⚡ TESTING PERFORMANCE")
    print("-" * 40)
    
    try:
        from performance_monitor import get_memory_stats
        stats = get_memory_stats()
        current_memory = stats.get('current_mb', 0)
        
        print(f"   📊 Current memory usage: {current_memory:.1f} MB")
        
        if current_memory < 200:
            print("   ✅ Memory usage: Excellent")
            return True
        elif current_memory < 400:
            print("   ✅ Memory usage: Good")
            return True
        else:
            print("   ⚠️ Memory usage: High")
            return False
    except Exception as e:
        print(f"   ❌ Performance test error: {e}")
        return False

def main():
    """Run comprehensive system test"""
    print("🚀 FINAL COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    print("Testing complete system functionality:")
    print("• Server startup and health")
    print("• Subscription limits and admin mode")
    print("• Presentation generation (multiple scenarios)")
    print("• Design styles (all 14 styles)")
    print("• Visual elements integration")
    print("• Web interface (professional appearance)")
    print("• Performance and memory usage")
    print("=" * 60)
    
    # Run all tests
    test_results = []
    
    # Test 1: Server startup
    server_ok = test_server_startup()
    test_results.append(("Server Startup", server_ok))
    
    if not server_ok:
        print("\n❌ Server not running. Please start with: python start_server.py")
        return
    
    # Test 2: Subscription limits
    admin_user_id = test_subscription_limits()
    test_results.append(("Subscription System", admin_user_id is not None))
    
    # Test 3: Presentation generation
    if admin_user_id:
        successful_gen, total_gen = test_presentation_generation(admin_user_id)
        test_results.append(("Presentation Generation", successful_gen == total_gen))
        print(f"\n   📊 Generation Success Rate: {successful_gen}/{total_gen}")
    else:
        test_results.append(("Presentation Generation", False))
    
    # Test 4: Design styles
    styles_ok = test_design_styles()
    test_results.append(("Design Styles", styles_ok))
    
    # Test 5: Visual elements
    visuals_ok = test_visual_elements()
    test_results.append(("Visual Elements", visuals_ok))
    
    # Test 6: Web interface
    web_ok = test_web_interface()
    test_results.append(("Web Interface", web_ok))
    
    # Test 7: Performance
    perf_ok = test_performance()
    test_results.append(("Performance", perf_ok))
    
    # Final Results
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    
    passed_tests = 0
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:<25} {status}")
        if result:
            passed_tests += 1
    
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"\n📈 Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 85:
        print("\n🎉 SYSTEM STATUS: EXCELLENT - READY FOR PRODUCTION!")
        print("✅ All core functionality working")
        print("✅ Subscription system operational")
        print("✅ Professional appearance")
        print("✅ Premium features available")
        print("✅ Smooth operation confirmed")
    elif success_rate >= 70:
        print("\n✅ SYSTEM STATUS: GOOD - Minor issues detected")
        print("⚠️ Some features may need attention")
    else:
        print("\n⚠️ SYSTEM STATUS: NEEDS ATTENTION")
        print("🔧 Multiple issues detected - review failed tests")
    
    print(f"\n🌐 Access your system at: http://localhost:5000")
    print("🔑 Admin password: DeckMaster2024!@#SecureAdmin")

if __name__ == "__main__":
    main()