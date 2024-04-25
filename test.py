# multiline.py
import re
p = re.compile("^0x[0-9a-fA-F]{40}$", re.MULTILINE | re.DOTALL | re.IGNORECASE)

data = """0x742d35cc6634c0532925a3b844bc454e4438f44e
0x808F0EaD04E1C5F58EF0d260FD3854d3cA6D45C5
0x595063172C85B1e8AC2f
e74Fcb6b7dC26844CC2D
you need python
python three"""

print(p.findall(data))