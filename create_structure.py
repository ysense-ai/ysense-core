# create_structure.py
import os

directories = [
    "src",
    "api", 
    "core",
    "ui",
    "scripts",
    "tests",
    "docs"
]

for dir in directories:
    os.makedirs(dir, exist_ok=True)
    
    # Create __init__.py
    init_file = os.path.join(dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write(f'"""YSense v3.0 - {dir} module"""')

print("✅ Project structure created!")