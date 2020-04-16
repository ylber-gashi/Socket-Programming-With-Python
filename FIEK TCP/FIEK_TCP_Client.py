import socket


def socketCreate():
    global HOST
    global PORT
    global TCPclient
    try:
        HOST = input("Jepni IP Adresen (Default - localhost): \n")
        PORT = int(input("Jepni portin (Default - 13000): \n"))
        TCPclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPclient.connect((HOST, PORT))
    except (socket.error, OverflowError, ValueError) as err:
        print("Error while creating socket: " + str(err))
        socketCreate()


socketCreate()

print("\t\t\t\t\t\tFIEK TCP client\n"
      "--------------------------------------------------------------\n"
      "1. IPADDRESS\n"
      "2. PORT\n"
      "3. COUNT text\n"
      "4. REVERSE text\n"
      "5. PALINDROME text\n"
      "6. TIME\n"
      "7. GAME\n"
      "8. GCF number1 number2\n"
      "9. CONVERT number cmtofeet/feettocm/kmtomiles/milestokm\n"
      "10. CALCULATE number1 operator number2   --> operator: +, -, *, /, ^, sqrt, %\n"
      "11. PASSWORD gjatesia\n"
      "Shtyp 0 nese deshironi ta nderroni IP adresen dhe Portin\n")

methods = ["ipaddress", "port", "count", "reverse", "palindrome", "time", "game", "gcf", "convert", "calculate",
           "password", "exit", "0"]
soloMethods = ["ipaddress", "port", "time", "game"]
convertOptions = ["cmtofeet", "feettocm", "kmtomiles", "milestokm"]
operators = ["+", "-", "*", "/", "^", "%"]


def is_num(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


while True:
    kerkesa = (input("Type request: ").lower()).strip()
    listed = kerkesa.split()

    try:
        if len(kerkesa) == 0:
            continue

        elif listed[0] not in methods:
            print("Invalid request...\n")
            continue

        elif kerkesa in soloMethods:
            TCPclient.send(str.encode(kerkesa))

        elif listed[0] == "count" or listed[0] == "palindrome" or listed[0] == "reverse":
            if len(listed) > 1:
                TCPclient.send(str.encode(kerkesa))
            else:
                continue

        elif len(listed) > 1 and listed[0] == "calculate" and is_num(listed[1]):
            if len(listed) == 4 and is_num(listed[3]) and listed[2] in operators:
                TCPclient.send(str.encode(kerkesa))
            elif len(listed) == 3 and listed[2] == "sqrt":
                TCPclient.send(str.encode(kerkesa))
            else:
                print("Invalid request...\n")
                continue

        elif len(listed) == 3 and listed[0] == "gcf" and is_num(listed[1]) and is_num(listed[2]):
            TCPclient.send(str.encode(kerkesa))

        elif len(listed) == 3 and listed[0] == "convert" and is_num(listed[1]) and listed[2] in convertOptions:
            TCPclient.send(str.encode(kerkesa))

        elif len(listed) == 2 and listed[0] == "password" and listed[1].isdigit():
            TCPclient.send(str.encode(kerkesa))

        elif listed[0] == "0":
            HOST = input("Jepni IP adresen: ")
            PORT = int(input("Jepni PORTIN: "))
            TCPclient.send(str.encode("exit"))
            TCPclient.close()
            TCPclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCPclient.connect((HOST, PORT))
            continue

        elif listed[0] == "exit":
            TCPclient.send(str.encode(kerkesa))
            print("Jeni shkeputur nga serveri.")
            break

        else:
            print("Invalid request...\n")
            continue

        data = TCPclient.recv(128)
        data = data.decode()
        data = str(data)
        print("\nPergjigjja nga serveri: " + data + "\n\n")
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as err:
        print("Connection error: ", err)
        break

TCPclient.close()
