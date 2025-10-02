# Test White Paper System
import sys
import os

# Add the src directory to the path
sys.path.append('src')

try:
    from whitepaper_system import WhitePaperSystem
    
    print("🧪 Testing White Paper System...")
    
    # Create instance
    wp = WhitePaperSystem()
    
    # Check available methods
    methods = [method for method in dir(wp) if not method.startswith('_')]
    print(f"✅ Available methods: {methods}")
    
    # Test each method
    if hasattr(wp, 'get_whitepaper_content'):
        content = wp.get_whitepaper_content()
        print(f"✅ get_whitepaper_content(): {len(content)} characters")
    else:
        print("❌ get_whitepaper_content() not found")
    
    if hasattr(wp, 'get_whitepaper_abstract'):
        abstract = wp.get_whitepaper_abstract()
        print(f"✅ get_whitepaper_abstract(): {len(abstract)} characters")
    else:
        print("❌ get_whitepaper_abstract() not found")
    
    if hasattr(wp, 'get_pdf_content'):
        pdf = wp.get_pdf_content()
        print(f"✅ get_pdf_content(): {len(pdf)} bytes")
    else:
        print("❌ get_pdf_content() not found")
    
    print("🎉 White Paper System test complete!")
    
except Exception as e:
    print(f"❌ Error testing white paper system: {e}")
    import traceback
    traceback.print_exc()





