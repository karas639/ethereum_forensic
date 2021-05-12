python
import gdb, sys, os

sys.path.insert(0, os.path.expanduser("/mnt/d/ethereum_forensic/.config/gdb"))
def setup_python(event):
	import libpython
gdb.events.new_objfile.connect(setup_python)
end
