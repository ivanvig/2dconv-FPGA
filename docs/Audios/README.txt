Audio ariel:

Escritura:
Secuencia correcta:
	
	cont = todos 1	
	- habilito escritura
	- incremento el contador
	- cargo el dato
	- incremento contador
(sincronizar el write)

'25 A 30 todo el tema de las memorias, ahora esta el MC. 

'30 a 34
Sincronizacion y tiempo del GPIO.
-dame dato, incremento contador, y recien ahi lees el gpio.
Mismo flujo (ANALOGIA A VALID EN ESCRITURA), sino hay perdida de datos.\
Le doy valid, voy al gpio de entada a ver el dato.. lo capturo, y devuelta valid, y voy a gpio entrada.
Asi sucesivamente.


'34 a 37 algo de control y fsm

'37 sigue con control, y sincronización lectura/escritura


41' FSM
Ctrl ==> carga parametros
en Run ==> FSM toma el control
En cada estado sus salidas van a ser x cosa: habilta/desabilita modulos segun logica empleada.


48'sigue fsm y dinámica de flujo, hasta el final del audio



