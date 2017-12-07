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
    port = 'COM7', #Configurar con el puerto x
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
    user_input =str(input('\n Testeo de varios modulos:\n  Ingrese 1 para setear el reset:   '))


    if(user_input=='1'):
        print("Inicializando seteo de memoria..\n")

    else:
        ser.close()
        enviar = False
        print("\n\nFinalizando programa...")
        time.sleep(3)
        exit()


    reset = int(1)
    codeToSend = struct.pack(b'B', reset)
    # os.system('cls')
    print("Enviando cfg de reset..")
    # print("Tamano byte cadena: ", len(user_input.encode('utf-8')))
    ser.flushInput()
    ser.flushOutput()
    time.sleep(1)
    ser.write(codeToSend)
    time.sleep(2)
    # Espero el feedback del FPGA. Ahora si, el sleep se usa forzadamente para esperar la respuesta

    ##Recibo el succes de si escribio el GPIO
    while (ser.inWaiting() > 10):

        decod = ser.read(11).decode()
        print(decod)


    ##Ahora ingresando 2, se procede a la escritura.

    user_input = str(input('\n Ahora procederemos a escribir el kernell\n Ingrese 2, para proceder a escribir'))
    if (user_input == '2'):
        print("\nIniciando escritura...\n")
    else:
        ser.close()
        print("Finalizando programa..")
        exit(0)


    knl = int(2)
    knlToSend = struct.pack(b'B', knl)
    ser.flushInput()
    ser.flushOutput()
    ser.write(knlToSend)
    time.sleep(1)
    while (ser.inWaiting() > 6):
        decod = ser.read(7).decode()
        print(decod)


    ser.flushInput()
    ser.flushOutput()

    user_input=(str(input('\nAhora procederemos a cargar img size. Ingrese cualquier tecla')))
    size = int(3)

    sizeToSend = struct.pack(b'B', size)
    ser.flushInput()
    ser.flushOutput()
    time.sleep(1)
    ser.write(sizeToSend)
    time.sleep(1)

    while(ser.inWaiting()>0):

        decod = ser.read(7).decode()
        print(decod)

    ser.flushInput()
    ser.flushOutput()
    print('\n Procediendo a carga de imagen')
    user_input=(str(input('Ingrese cualquier tecla')))

    imgload = int(4)
    imgloadToSend = struct.pack(b'B',imgload)
    ser.write(imgloadToSend)
    time.sleep(1)


    while(ser.inWaiting()>6):

        decod = ser.read(7).decode()
        print(decod)


    ser.flushInput()
    ser.flushOutput()

    print('\n Procediendo a RUN')

    user_input = (str(input('Ingrese cualquier tecla')))

    run = int(5)
    runToSend = struct.pack(b'B', run)
    ser.write(runToSend)
    time.sleep(1)

    while (ser.inWaiting() > 6):

        decod = ser.read(7).decode()
        print(decod)

    print('\n Procediendo a OBTENCION DE DATOS')

    user_input = (str(input('Ingrese cualquier tecla')))

    dataRequest = int(6)
    dataRequestToSend = struct.pack(b'B', dataRequest)

    time.sleep(1)

    f = open('output.txt', 'w')

    for i in range(11):
        ser.write(dataRequestToSend)
        time.sleep(0.1)
        s = ''
        while ser.inWaiting() > 0:
            s += str(ser.read(1).hex())
        f.write(str(i) + ' ' + s + '\n')
    f.close()


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






