# Test PDF File Existence
import os

def test_pdf_file():
    """Test if the PDF file exists and is readable"""
    pdf_path = "assets/YSense™ AI Attribution Infrastructure White Paper v1.0 (Public Release).pdf"
    
    print(f"🔍 Testing PDF file: {pdf_path}")
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"📄 File exists: {os.path.exists(pdf_path)}")
    
    if os.path.exists(pdf_path):
        try:
            with open(pdf_path, 'rb') as f:
                content = f.read()
                print(f"✅ File size: {len(content)} bytes")
                print(f"📋 First 50 bytes: {content[:50]}")
                
                # Check if it's a valid PDF
                if content.startswith(b'%PDF'):
                    print("✅ Valid PDF header found")
                else:
                    print("❌ Invalid PDF header")
                    
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    else:
        print("❌ PDF file not found")
        
        # List files in assets directory
        assets_dir = "assets"
        if os.path.exists(assets_dir):
            print(f"📂 Files in {assets_dir}:")
            for file in os.listdir(assets_dir):
                print(f"  - {file}")
        else:
            print("❌ Assets directory not found")

if __name__ == "__main__":
    test_pdf_file()





