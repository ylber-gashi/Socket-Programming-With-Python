import socket
import threading
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

# Funksioni me ane te cilit e mundesojme casjen disa klienteve njekohesisht ne server
# Ky funksion thirret nga funksioni run() i modulit threading kur ne e bejme start() thread-in
def ThreadedServer(conn, address):
    try:
        while True:

            data = (conn.recv(128)).upper()  # te dhenat qe i ka derguar klienti pranohen dhe cdo shkronje behet e madhe
            data = data.decode()
            print("\nKerkesa: " + data)
            args = data.split()
            gjatesia = len(
                args)  # ketu e ruajme numrin e argumenteve qe i ka derguar klienti, me ane te se ciles validohet kerkesa me poshte
            kerkesa = args[0]

            if kerkesa == "IPADDRESS":
                pergjigjja = "IP Adresa e klientit eshte: " + str(IPADDRESS(address))
                conn.send(str.encode(pergjigjja))
            elif kerkesa == "PORT":
                pergjigjja = "Klienti eshte duke perdorur portin: " + str(PORTI(address))
                conn.send(str.encode(pergjigjja))
            elif kerkesa == "TIME":
                conn.send(str.encode(str(TIME())))
            elif kerkesa == "GAME":
                conn.send(str.encode(GAME()))
            elif kerkesa == "EXIT":
                print("\nLidhja me klientin" + " IP: ", address[0], " PORT: ", address[1], " eshte shkeputur.")
                break
            elif kerkesa == "COUNT":
                text = data[len(kerkesa):]
                conn.send(str.encode(COUNT(text)))
            elif kerkesa == "REVERSE":
                text = data[len(kerkesa):]
                conn.send(str.encode(REVERSE(text)))
            elif kerkesa == "PALINDROME":
                text = args[1]
                conn.send(str.encode(PALINDROME(text)))
            elif kerkesa == "CONVERT":
                number = int(args[1])
                option = args[2]
                conn.send(str.encode(CONVERT(number, option)))
            elif kerkesa == "GCF":
                x = (int)(args[1])
                y = (int)(args[2])
                conn.send(str.encode(GCF(x, y)))
            elif kerkesa == "CALCULATE":
                x = args[1]
                op = args[2]
                if (gjatesia > 3):  # kjo eshte bere per shkak se sqrt kerkon vetem nje numer dhe operatorin
                    y = args[3]
                    conn.send(str.encode(str(CALCULATE(x, op, y))))
                elif (gjatesia == 3):
                    conn.send(str.encode(str(CALCULATE(x, op))))
            elif kerkesa == "PASSWORD":
                size = args[1]
                conn.send(str.encode(str(password(size))))
    except (ConnectionError, ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError) as msg:
        print("Connection error: ", msg)


try:
    HOST = 'localhost'
    PORT = 13000
    print("\n\t\t\t\t\t\tFIEK TCP Server\n"
          "--------------------------------------------------------------\n")
    TCPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("\nSocket is being created...")
except socket.error as err:
    print("Error while creating socket" + str(err))


# SocketBinding()
def socketBinding():
    try:
        global HOST
        global PORT
        TCPserver.bind((HOST, PORT))
        print("\nServeri eshte startuar ne HOST: " + HOST + ", me PORT: ", PORT)
        TCPserver.listen(8)
        print("Serveri eshte duke pritur per ndonje kerkese nga klientet")
    except (socket.error, TypeError) as err:
        print("Bind failed. Error: " + str(err))
        print("\nKontrolloni IP adresen dhe PORTIN qe e keni dhene.\n")
        HOST = input("Jepeni IP adresen perseri: ")
        try:
            PORT = int(input("Jepni PORTin perseri: "))
        except (ValueError, OverflowError):
            PORT = int(input("Ju lutem sigurohuni qe PORT te jete nje numer: "))
        socketBinding()


socketBinding()

# Accepting client requests
while True:
    conn, address = TCPserver.accept()
    print('---------------------------------------')
    print('Klienti u lidh me %s me portin %s' % address)
    th = threading.Thread(target=ThreadedServer,
                          args=(conn, address))  # Klientet e lidhur i pason tek metoda ThreadedServer,
    th.start()  # e cila na ndihmon qe t'i sherbejme disa klienteve ne te njejten kohe
    print("\nKliente aktiv: ",
          threading.activeCount() - 1)  # Na jep numrin e klienteve aktiv ne server, sa here qe kycet ndonje klient

conn.close()
