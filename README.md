# 2dconv-verilog
Proyecto final de curso: Procesamiento digital de imagen por hardware




Datos/análisis para el desarrollo del proyecto:

Representación complemento a 2:
Ver el tema de agarrar la imagen, pasarla a complemento a 2, sabiendo que los valores positivos van a ser oscuros, y los negativos van a ser claros. Operando, y volviendo a sacarle el complemento a 2, lo volvemos a llevar a un valor entre 0 y 1, se acomodan los colores, y lo podemos desnormalizar para que vuelvan a tomar los valores entre 0 y 255.

Register file: 
El reloj manda el pulso para la escritura, y hay que latchear el dato.. Se encarga el sw (invisible al usuario).
El usuario va a decir, quiero poner el rsst en 1 y yo me tengo que encargar de saber que instrucción/clave es dentro de dicha tabla. Son 3 escrituras seguidas.

Cuantización y punto fijo: 
Primero tomar imagen con mayor precision posible (float). Despues, por ejemplo, asentar resolución en S(8, 7), o la que fuese, y según cierto criterio o métrica,(pérdida de pixeles, nivel de grises inadecuado, deterioro de calidad), DECIDIR/DEFINIR la resolución del filtro. Una vez que está esto, hay que hacer lo mismo con la senal a transmitir (pedazo de imagen convolucionada con el kernel)...(no solo el filtro).
Ver ratio senal ruido o senal error, para determinar las diferentes resoluciones.
Luego de ver los bits del filtro (después de también haber hecho toda la simulacion en punto flotante), es decir: definir la resolucion del filtro, y luego, sabemos que las operaciones las tenemos que sacar en punto flotante para comparar desempeno.

Colocar el filtro (o los filtros de todo el sistema) e ir cuantizando: Ya sea por SNR vs filtro original, o agarrar la senal resultante de salida (esta en punto flotante. La convolución) y analizarla... Empleando tanto el filtro ideal y el filtro cuantizado, para sacar SNR con filtro ideal y como difiere empleando el filtro cuantizado.
La cuantizacion de las muestras va a ser la imagen, (transmitida). Hay que ver todo el procesamiento en punto flotante, y todo el procesamiento en punto fijo.


Throughput: 
Después de implementar la arquitectura planteada, incluir un análisis de la tasa de trabajo. Ej, fcock de 100 MHZ y 5 convolucionadores, logro obtener para un procesammiento de T tamano de imagen, en N cantidad de ciclos, obtengo X tasa.
Suponiendo que tenemos espacio de memoria suficiente, efectuar mismo análisis, y mencionar el tema de la reutilización de hardware.





