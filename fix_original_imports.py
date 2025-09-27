import os
import re

# Fix api/auth.py
auth_file = "api/auth.py"
with open(auth_file, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("from models import", "from src.models import")
with open(auth_file, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Fixed {auth_file}")

# Fix api/wisdom.py
wisdom_file = "api/wisdom.py"
if os.path.exists(wisdom_file):
    with open(wisdom_file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("from models import", "from src.models import")
    content = content.replace("from intelligent_agents import", "from src.intelligent_agents import")
    with open(wisdom_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {wisdom_file}")

# Fix api/revenue.py  
revenue_file = "api/revenue.py"
if os.path.exists(revenue_file):
    with open(revenue_file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("from models import", "from src.models import")
    with open(revenue_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {revenue_file}")

# Fix api/legal.py
legal_file = "api/legal.py"
if os.path.exists(legal_file):
    with open(legal_file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("from models import", "from src.models import")
    content = content.replace("from z_protocol_enhanced import", "from src.z_protocol_enhanced import")
    with open(legal_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {legal_file}")

print("\nAll original files fixed!")
