#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"

#include "xil_printf.h"

#include "xuartlite.h"
//#include "encender_led.h"
#include "microblaze_sleep.h"


#define PORT_IN	 		XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_GPIO_0_DEVICE_ID

//Device_ID Operaciones
#define def_SET_SIGMA			1
#define def_START_RUIDO			2


//Device_ID Respuestas
#define def_ACK 				1
#define def_ERROR 				2
#define mascara 3


void send_trama(int id);
void send_ack(int from_id);
void send_num(unsigned char a ,unsigned char b);

XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;
u32 GPO_Value;
u32 GPO_Param;
XUartLite uart_module;

short int num_ber;


//Funcion para recibir 1 byte bloqueante
//send buffer usignedd char

int main()
{
	init_platform();

	int Status;
	//unsigned int operacion=0;

	XUartLite_Initialize(&uart_module, 0);

	GPO_Value=0x00000000;
	GPO_Param=0x00000000;

	unsigned char cabecera[4];
	unsigned char sendBuffer[2]= {0x00,0x00};
	//u16 tamano_datos;
	u32 direccion = 0x00000000;
	u32 datos = 0x00000000;


	Status=XGpio_Initialize(&GpioInput, PORT_IN);
	if(Status!=XST_SUCCESS){
        send_trama(def_ERROR);
        return XST_FAILURE;
    }
	//Status=XGpio_Initialize(&GpioParameter, PORT_OUT_PARAM);
	//if(Status!=XST_SUCCESS){
	//	send_trama(def_ERROR);
	//	return XST_FAILURE;
	//}
	Status=XGpio_Initialize(&GpioOutput, PORT_OUT);
	if(Status!=XST_SUCCESS){
		send_trama(def_ERROR);
		return XST_FAILURE;
	}



	XGpio_SetDataDirection(&GpioOutput, 1, 0x00000000);
	//XGpio_SetDataDirection(&GpioParameter, 1, 0x00000000);
	XGpio_SetDataDirection(&GpioInput, 1, 0xFFFFFFFF);

	while(1){
		read(stdin,&cabecera[0],1);

		switch(cabecera[0]){

			case '0': //reset
				datos = 0x00000000 | 0b01001; //reset conv y en modo imagen
				direccion = 0x00000000 | 0b01001; //en modo reg top
				XGpio_DiscreteWrite(&GpioOutput,1,datos);
				//datos &= ~(1<<3); //bajo el rest de la momoria
				//XGpio_DiscreteWrite(&GpioOutput,1,datos);
				//XUartLite_Send(&uart_module,0x30,1);
				break;
			case '1':
				datos = 0x00000000 | 0b11110; //mem_add en modo top
				XGpio_DiscreteWrite(&GpioOutput,1,datos);
				//datos |= 0b1110; //bajo el rst conv y valid en 1
				//XGpio_DiscreteWrite(&GpioOutput,1,datos);
				//XUartLite_Send(&uart_module,0x31,1);
				break;
			case '2':
				// addres en modo pgio
				datos = 0x00000000;
				direccion = 0x00000000;
				XGpio_DiscreteWrite(&GpioOutput,1,datos);
				//XUartLite_Send(&uart_module,0x32,1);
				break;
			case '3':
				if (direccion < 0x1B400){ //0x1B400
					XGpio_DiscreteWrite(&GpioOutput,1,direccion);
					datos = XGpio_DiscreteRead(&GpioOutput,1);
		    		for(int con=0;con<4;con++){
		    			sendBuffer[con]=(datos>>(8*(3-con)))&0xFF;
		    		}
		    		XUartLite_Send(&uart_module, sendBuffer,4);
		    		while(XUartLite_IsSending(&uart_module)){}
		    		direccion += 0x100;
				}
				else{
					send_trama(9);
				}

				/*
				XGpio_DiscreteWrite(&GpioOutput,1,direccion);
				XUartLite_Send(&uart_module,0x33,1);
				datos = XGpio_DiscreteRead(&GpioOutput,1);
				direccion += 0x100;
				*/
				break;
			case '9':
				datos  = 0x00000000 | 0b10000;
				XGpio_DiscreteWrite(&GpioOutput,1,datos);
				break;
		}
	}
	cleanup_platform();
	return 0;
}


void send_ack(int from_id){
	unsigned char cabecera[4]={0xA1,0x00,0x00,0x00};
	unsigned char fin_trama[1]={0x41};
	unsigned char datos[1];
	datos[0]=from_id;
	cabecera[3]=def_ACK;
	XUartLite_Send(&uart_module, cabecera,4);
	while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, datos,1);
	XUartLite_Send(&uart_module, fin_trama,1);
}

void send_trama(int id){
	unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
	unsigned char fin_trama[1]={0x40};
	cabecera[3]=id;
	XUartLite_Send(&uart_module, cabecera,4);
	while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, fin_trama,1);
}

void send_num(unsigned char a ,unsigned char b){
	unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
	unsigned char fin_trama[1]={0x40};
	cabecera[2]=a;
	cabecera[3]=b;
	XUartLite_Send(&uart_module, cabecera,4);
	while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, fin_trama,1);
}

