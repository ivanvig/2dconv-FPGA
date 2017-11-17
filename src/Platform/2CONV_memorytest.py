#CASABELLA MARTIN
#TRAMA COMPLETA
#PROCOM 2017

import os
import time
import serial
import struct

# coding: utf-8


def ValidarTerminar():
    
    caracter  = True
    opc       = 0
    valido    = False
    
    
    print("\n\nQue desea hacer?\n\n1-Volver a enviar una instrucción\n2-Salir del programa")
    
    while caracter is True or valido is False:       
             
        try:
            opt  = int(input("Escoja una opcion: "))
            carac=False            
            ## Se verifica el ingreso acorde a como se designaron las mismas en el programa con el diccionario

            if (opt==1 or opt==2):
                valido = True
                opc    = opt 
                break
                
            else:
                valido = False
                print("\nIngrese una opcion válida acorde a las opciones mostradas en pantalla. \n ")
                
        except ValueError:
                print("\n\n\nERROR -- INVALID INPUT: Opcion no interpretada. Ingrese un numero, por favor\n")
        
    return opc






    
#ser = serial.serial_for_url('loop://', timeout=1)  #loopback virtual

ser=serial.Serial(
    port = 'COM6', #Configurar con el puerto x
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
   )





ser.timeout=None     
ser.flushInput()     
ser.flushOutput()


enviar = True


while enviar is True:    
    

    #Esta el puerto abierto?
    if ser.isOpen() is True:
        print("\nEstado del puerto: PUERTO ABIERTO. \n")
        print("Connected to: ", ser.portstr)
    else:
        #Re abro puerto por si fue cerrado luego de ya haber enviado una cadena
        #O por algun otro motivo
        print("\n\nEstado del puerto: PUERTO CERRADO. \n")
        print("Abriendo puerto..")
        time.sleep(2)
        ser.open()
        if ser.isOpen:
            print("\nOpened succesfully.")
            print("Comunicacion establecida exitosamente. Connected to: " + ser.portstr)
            time.sleep(2)

    os.system('cls')
    user_input =str(input('\nSi desea salir ingrese el comando exit. De lo contrario, ingrese cualquier otra tecla  '))
    if(user_input=='exit'):        

        ser.close()
        enviar = False
        print("\n\nFinalizando programa...")
        time.sleep(3)
        exit()

    else:
        flagControl = 0;


    print("Bienvenido\n")
    user_input =str(input('\n Testeo de memoria:\n  Ingrese 1 para setear el reset '))
    if(user_input=='1'):
        print("Inicializando seteo de memoria..\n")

    else:
        ser.close()
        enviar = False
        print("\n\nFinalizando programa...")
        time.sleep(3)
        exit()


    CharSet = int(1)
    codeToSend = struct.pack(b'B', CharSet)
    # os.system('cls')
    print("Enviando cfg de reset..")
    time.sleep(1)
    # print("Tamano byte cadena: ", len(user_input.encode('utf-8')))
    ser.flushInput()
    ser.flushOutput()

    # Escribo en puerto
    print("\nEscribiendo en puerto..\n")
    time.sleep(1)
    ser.write(codeToSend)
    time.sleep(10)
    # Espero el feedback del FPGA. Ahora si, el sleep se usa forzadamente para esperar la respuesta

    ##Recibo el succes de si escribio el GPIO
    while (ser.inWaiting() > 0):

        decod = ser.read(11).decode()
        print("\nLeyendo puerto.. OPERATION:", decod)
        print("Succesfully written..")

        if decod == 'SUCCESS_CFG':
            print("\nSTATUS [OK]..")
        else:
            print("\nSTATUS [ERROR]")


    ##Ahora ingresando 2, se procede a la escritura.

    user_input = str(input('\n Ahora procederemos a escribir la memoria. Ingrese 2, para proceder a escribir'))
    if (user_input == '2'):
        print("\nIniciando escritura...\n")

    else:
        ser.close()
        print("Finalizando programa..")
        exit(0)


    add_input = int(input('\nIngrese direccion de memoria: '))


    write = int(2)
    writeToSend = struct.pack(b'B', write)
    time.sleep(1)
    ser.flushInput()
    ser.flushOutput()
    ser.write(writeToSend)
    time.sleep(10)


    while (ser.inWaiting() > 6):
        decod = ser.read(7).decode()
        print("\nLeyendo puerto.. OPERATION ESCRITURA:", decod)

        if decod == 'SUCC_WR':
            print("\nSTATUS [OK]..")
        else:
            print("\nSTATUS [ERROR]")


    time.sleep(1)
    ser.flushInput()
    ser.flushOutput()
    Add = int(add_input)
    AddToSend = struct.pack(b'B', Add)

    # os.system('cls')
    print("Enviando address..")
    # print("Tamano byte cadena: ", len(user_input.encode('utf-8')))
    ser.write(AddToSend)
    time.sleep(10)
    # Espero el feedback del FPGA. Ahora si, el sleep se usa forzadamente para esperar la respuesta

    while (ser.inWaiting()>5):
        decod = ser.read(6).decode()
        if decod == 'ADD_WR':
            print("\nSTATUS ADD WR [OK]..")
        else:
            print("\nSTATUS ADD WR [ERR] ")


    print("Inicializando lectura...")
    readd = int(3)
    readToSend = struct.pack(b'B', readd)
    ser.flushInput()
    ser.flushOutput()
    time.sleep(1)
    ser.write(readToSend)
    time.sleep(10)

    while(ser.inWaiting()>0):

        decod = ser.read(7).decode()
        if decod == 'SUCC_rd':
            print("\nSTATUS ADD RD [OK]..")
        else:
            print("\nSTATUS ADD RD[ERR]")
            print(decod)



    print('\n\nLeyendo direccion escrita', str(add_input))
    ser.flushInput()
    ser.flushOutput()
    print('Procediendo a leer')
    time.sleep(1)
    read_d = int(add_input)
    readToSend = struct.pack(b'B',read_d)
    time.sleep(1)
    ser.write(readToSend)
    time.sleep(10)


    while(ser.inWaiting()>0):
        print("Entro")
        dato1 = ser.read(1)
        print(dato1)


    seguir = ValidarTerminar()
    if seguir ==1:
        enviar = True
        os.system('cls')

    else:
        enviar = False
        print("\n\n\nClosing ports..")
        print("\nFinalizando programa..")
        time.sleep(3)
        exit()






