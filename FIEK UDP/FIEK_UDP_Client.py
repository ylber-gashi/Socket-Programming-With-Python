import socket


def socketCreate():
    try:
        global HOST
        global PORT
        global UDPclient
        HOST = input("Jepni IP Adresen (Default - localhost): \n")
        PORT = int(input("Jepni portin (Default - 13000): \n"))
        UDPclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except (socket.error, ValueError, OverflowError) as err:
        print("Error while creating socket: ", err)
        socketCreate()


socketCreate()

print("\t\t\t\t\t\tFIEK UDP\n"
      "--------------------------------------------------------------\n"
      "1. IPADDRESS\n"
      "2. PORT\n"
      "3. COUNT text\n"
      "4. REVERSE text\n"
      "5. PALINDROME text\n"
      "6. TIME\n"
      "7. GAME\n"
      "8. GCF number1 number2\n"
      "9. CONVERT number cmtofeet/feettocm/kmtomile/milestokm\n"
      "10. CALCULATE number1 operator number2   --> operator: +, -, *, /, ^, sqrt, %\n"
      "11. PASSWORD gjatesia\n"
      "\nShtyp 0 nese deshironi ta nderroni IP adresen dhe Portin\n")

methods = ["ipaddress", "port", "count", "reverse", "palindrome", "time", "game", "gcf", "convert", "calculate",
           "password", "exit", "0"]
soloMethods = ["ipaddress", "port", "time", "game"]
convertOptions = ["cmtofeet", "feettocm", "kmtomile", "milestokm"]
operators = ["+", "-", "*", "/", "^", "%"]


def is_num(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


while True:
    kerkesa = (input("Type request: ").lower()).strip()

    listed = kerkesa.split()  # Argumentet e dhena si input i ruajme ne nje liste si stringje

    if len(kerkesa) == 0 or len(kerkesa.encode()) > 128:
        continue

    elif listed[0] not in methods:
        print("Invalid request...\n")
        continue

    elif kerkesa in soloMethods:
        UDPclient.sendto(kerkesa.encode(), (HOST, PORT))

    elif listed[0] == "count" or listed[0] == "palindrome" or listed[0] == "reverse":
        if len(listed) > 1:
            UDPclient.sendto(kerkesa.encode(), (HOST, PORT))
        else:
            continue

    elif len(listed) > 1 and listed[0] == "calculate" and is_num(listed[1]):
        if len(listed) == 4 and is_num(listed[3]) and listed[2] in operators:
            UDPclient.sendto(kerkesa.encode(), (HOST, PORT))
        elif len(listed) == 3 and listed[2] == "sqrt":
            UDPclient.sendto(kerkesa.encode(), (HOST, PORT))
        else:
            print("Invalid request...\n")
            continue

    elif len(listed) < 4 and listed[0] == "gcf" and is_num(listed[1]) and is_num(listed[2]):
        UDPclient.sendto(kerkesa.encode(), (HOST, PORT))

    elif len(listed) > 1 and listed[0] == "convert" and is_num(listed[1]) and listed[2] in convertOptions:
        UDPclient.sendto(kerkesa.encode(), (HOST, PORT))

    elif listed[0] == "password" and listed[1].isdigit():
        UDPclient.sendto(kerkesa.encode(), (HOST, PORT))

    elif listed[0] == "0":
        HOST = input("Jepni IP adresen: ")
        PORT = int(input("Jepni PORTIN: "))
        UDPclient.sendto(kerkesa.encode(), (HOST, PORT))
        UDPclient.close()
        UDPclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        continue

    elif listed[0] == "exit":
        UDPclient.sendto(kerkesa.encode(), (HOST, PORT))
        print("Jeni shkeputur nga serveri.")
        break

    else:
        print("Invalid request...\n")
        continue
    dataRecieved, address = UDPclient.recvfrom(128)
    data = dataRecieved.decode()
    data = str(data)

    print("\nPergjigjja nga serveri: " + data + "\n\n")
