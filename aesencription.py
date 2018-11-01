
import onetimepad
import sys


filename = sys.argv[1]
if filename.endswith(".sql"):
    cipher = onetimepad.encrypt(filename, 'randomkey')
    print("A chave e: " + cipher)
else:
    print("parametro tem que ser ficheiro sql")

