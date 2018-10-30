# from Crypto.Cipher import AES
# obj = AES.new('openmrs encr key', AES.MODE_CBC, 'This is an IV456')
# message = "openmrs is owesol"
# ciphertext = obj.encrypt(message)
# print(ciphertext)
#
#
# obj2 = AES.new('openmrs encr key', AES.MODE_CBC, 'This is an IV456')
# print(obj2.decrypt(ciphertext))
import onetimepad

cipher = onetimepad.encrypt('test.sql', 'randomkey')
print("Cipher text is ")
print(cipher)
print("Plain text is ")
msg = onetimepad.decrypt(cipher, 'randomkey')

print(msg)
06041d10411e1a09
/home/asamuel/Documents/test.sql