import socket

import random
import string
from time import localtime, strftime

# METODAT

""" Metoda qe kthen IP adresen e klientit perkates.
    Kjo metode, ashtu si edhe metoda PORTI si parameter e marrin adresen e
    klientit e cila i permban dy vlera (HOSTin dhe PORTin).
"""


def IPADDRESS(address):
    return address[0]


def PORTI(address):
    return address[1]


def COUNT(text):
    text = text.lower()
    nrz = 0
    nrb = 0
    for x in text:
        if x == 'a' or x == 'e' or x == 'i' or x == 'u' or x == 'o':
            nrz += 1
        elif x >= 'a' and x <= 'z':
            nrb += 1
    final = "Teksti i pranuar permban " + str(nrz) + " zanore dhe " + str(nrb) + " bashketingellore."
    return final


def REVERSE(text):
    backw = ""
    gjatesia = len(text)
    for x in range(gjatesia):
        backw += text[gjatesia - 1]
        gjatesia -= 1
    return backw.strip()  # e kthen tekstin reverse me hapesirat e fillimit dhe te fundit te larguara


# Kërkon nje fjali dhe tregon a eshte fjalia palindrome (True) apo jo (False)

def PALINDROME(text):
    backw = ""
    gjatesia = len(text)
    for x in range(gjatesia):
        backw += text[gjatesia - 1]
        gjatesia -= 1
    if text == backw:
        return str(True)
    else:
        return str(False)


def TIME():
    return strftime("%Y-%m-%d %H:%M:%S PM", localtime())


def GAME():
    lista = []

    while len(lista) != 5:
        y = random.randint(1, 36)
        if y not in lista:
            lista.append(y)

    listToStr = ', '.join([str(elem) for elem in lista])
    return listToStr


def CONVERT(number, option):
    if option == "CMTOFEET":
        return str(round((number * 0.0328084), 2)) + "ft"
    elif option == "FEETTOCM":
        return str(round((number / 0.0328084), 2)) + "cm"
    elif option == "KMTOMILES":
        return str(round((number * 0.621371), 2)) + "miles"
    elif option == "MILESTOKM":
        return str(round((number / 0.621371), 2)) + "km"
    else:
        return "Invalid option choosen."


def GCF(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return str(x)


def CALCULATE(x, op,
              *n):  # *n nenkupton qe parametrat pas x dhe op jane opsional. Kjo sepse metoda CALCULATE ka operacione ku nuk duhet argumenti i trete
    x = float(x)
    if len(n) > 1:
        return ("CALCULATE pranon vetem tre argumente.")
        pass
    y = 0
    for nr in n:
        y = float(nr)
    if op == "SQRT":
        return round((x ** (1 / 2)), 2)
    elif op == "%":
        return (x * (0.01) * y)
    elif op == "+":
        return x + y
    elif op == "-":
        return x - y
    elif op == "*":
        return x * y
    elif op == "/":
        return x / y
    elif op == "^":
        return x ** y


def password(gjatesia):
    gjatesia = int(gjatesia)
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(gjatesia))


# ----------------------------------------------------------------------------------------


# SOCKET

try:
    HOST = 'localhost'
    PORT = 13000
    UDPserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Socket is being created...")
except socket.error as err:
    print("Error while creating socket", err)


def socketBinding():
    try:
        global HOST
        global PORT
        global UDPserver
        UDPserver.bind((HOST, PORT))
        print("\nServeri eshte startuar ne localhost me portin: " + str(PORT))
        print("Serveri eshte duke pritur per ndonje kerkese\n"
              "---------------------------------------------")
    except socket.error as err:
        print("Bind failed. Error: ", err)
        print("\nKontrolloni IP adresen dhe PORTIN qe e keni dhene.\n")
        HOST = input("Jepni IP adresen perseri: ")
        try:
            PORT = int(input("Jepni PORTin perseri: "))
        except (ValueError, OverflowError):
            PORT = int(input("Ju lutem sigurohuni qe PORT te jete nje numer (1024 - 65535): "))
        socketBinding()


socketBinding()

while True:
    try:
        dataRecieved, address = UDPserver.recvfrom(128)
        data = dataRecieved.decode()
        data = data.upper()
        print("\nKerkesa: " + data)

        args = data.split()
        gjatesia = len(args)
        kerkesa = args[0]

        if kerkesa == "IPADDRESS":
            pergjigjja = "IP Adresa e klientit eshte: " + str(IPADDRESS(address))
            UDPserver.sendto(pergjigjja.encode(), address)
        elif kerkesa == "PORT":
            pergjigjja = "Klienti eshte duke perdorur portin: " + str(PORTI(address))
            UDPserver.sendto(pergjigjja.encode(), address)
        elif kerkesa == "TIME":
            UDPserver.sendto(str(TIME()).encode(), address)
        elif kerkesa == "GAME":
            UDPserver.sendto(GAME().encode(), address)
        elif kerkesa == "EXIT":
            print("Lidhja me klientin eshte shkeputur.")
            break
        elif kerkesa == "COUNT":
            text = data[len(kerkesa):]
            UDPserver.sendto(COUNT(text).encode(), address)
        elif kerkesa == "REVERSE":
            text = args[1]
            UDPserver.sendto(REVERSE(text).encode(), address)
        elif kerkesa == "PALINDROME":
            text = args[1]
            UDPserver.sendto(PALINDROME(text).encode(), address)
        elif kerkesa == "CONVERT":
            number = int(args[1])
            option = args[2]
            UDPserver.sendto(CONVERT(number, option).encode(), address)
        elif kerkesa == "GCF":
            x = (int)(args[1])
            y = (int)(args[2])
            UDPserver.sendto(GCF(x, y).encode(), address)
        elif kerkesa == "CALCULATE":
            x = args[1]
            op = args[2]
            if gjatesia > 3:  # kjo eshte bere per shkak se sqrt kerkon vetem nje numer dhe operatorin
                y = args[3]
                UDPserver.sendto(str(CALCULATE(x, op, y)).encode(), address)
            elif gjatesia == 3:
                UDPserver.sendto(str(CALCULATE(x, op)).encode(), address)
        elif kerkesa == "PASSWORD":
            gjatesia = args[1]
            UDPserver.sendto(str(password(gjatesia)).encode(), address)
    except (ConnectionError, ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError) as err:
        print("Server side error... ", err)
