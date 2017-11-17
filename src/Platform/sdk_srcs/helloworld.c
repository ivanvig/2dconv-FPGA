#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"
#include "xuartlite.h"
#include "microblaze_sleep.h"




//CANALES DE GPIO       XPAR_AXI_GPIO_1_DEVICE_ID
#define PORT_IN	 		XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_GPIO_0_DEVICE_ID
//#define PORT_OUT_PARAM 	XPAR_AXI_GPIO_2_DEVICE_ID

//Device_ID Operaciones
#define def_SET_SIGMA			1
#define def_START_RUIDO			2
#define def_INIT 				3
#define def_LOG_VALUES			5
#define def_START_DECODER 		7
#define def_RUN_LIBRE			8
#define def_RUN_WORD			9
#define def_READ_CW_ERROR		10
#define def_PUENTEAR_DECODER	11
#define def_GEN_CW_0			12
#define def_SET_ITERACIONES		13
#define def_LOG_ITER_RCV		14
#define def_SET_RESOLUCIONES	15
#define def_SOFT_RST            16
#define def_ENABLE_MODULES      17
#define def_BER_CTRL            18
#define def_SIGMA               19
#define def_LOG_BER_READ        20
#define def_SET_COEFF_CH        21
#define def_SET_ADAP_STEP       22
#define def_LOG_RUN             23
#define def_LOG_READ            24
#define def_SET_COEFF_FFE       25
#define def_SET_COEFF_DFFE      26

//Device_ID Respuestas
#define def_ACK 				1
#define def_ERROR 				2
#define def_ANS_LOG_CHA			3
#define def_ID_NOT_FOUND		4
#define def_ANS_LOG_DEC			5
#define def_CW_ERROR			6
#define def_CW_ERROR_NOT_FOUND	7
#define def_ACA_ESTOY			8
#define def_LOG_ITER			9
#define def_BER_READ			10
#define def_LOG_READ_CHANNEL    11
#define def_LOG_READ_FFE        12
#define def_LOG_READ_ERROR      13
#define def_LOG_READ_FFE_COEFF  14
#define def_LOG_READ_DFFE_COEFF 15
#define def_LOG_READ_BITS       16
#define def_LOG_READ_SRRC       17

void send_trama(int id);
void send_ack(int from_id);

XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;
u32 GPO_Value;
u32 GPO_Param;
XUartLite uart_module;
XGpio GPIO_0;

short int num_ber;
#define TEST_BUFFER_SIZE 16
unsigned char SendBuffer[TEST_BUFFER_SIZE];
unsigned char dataBuffer[TEST_BUFFER_SIZE];
static int RAM_WIDTH = (10*1024);

//Funcion para recibir 1 byte bloqueante
//XUartLite_RecvByte((&uart_module)->RegBaseAddress)


int main()
{
	init_platform();
	XUartLite_Initialize(&uart_module, 0);
	GPO_Value=0x00000000;
	GPO_Param=0x00000000;


	u32    choice;
	u32    memory;
	u32      mask;
	u16    fromPython;
	u8 	  bytSend;

	//Trama
	//u8 header    = 'Q';
	//u8 low       = 0x00;
	//u8 high      = 0x00;
	//u8 device    = 0x00;
	//u8 tail      = 0x41;
	u8 RecvBuff [4];


	int Status;
	int LenData;
	int Step;
	int flagEscritura;

	Status=XGpio_Initialize(&GpioInput, PORT_IN);
	if(Status!=XST_SUCCESS){
        send_trama(def_ERROR);
        return XST_FAILURE;
    }
	Status=XGpio_Initialize(&GpioOutput, PORT_OUT);
	if(Status!=XST_SUCCESS){
		send_trama(def_ERROR);
		return XST_FAILURE;
	}


	//Status=XGpio_Initialize(&GpioParameter, PORT_OUT_PARAM);
	//if(Status!=XST_SUCCESS){
	//	send_trama(def_ERROR);
	//	return XST_FAILURE;
	//}


	XGpio_SetDataDirection(&GpioOutput, 1, 0x00000000);
	//XGpio_SetDataDirection(&GpioParameter, 1, 0x00000000);
	XGpio_SetDataDirection(&GpioInput, 1, 0xFFFFFFFF);

    Step     = 0;
    flagEscritura = 3;

    while(1){

    	Step++;
		read(stdin,&RecvBuff[0],1);
		//Loggeo/lectura


		if (Step == 1){

			if(RecvBuff[0]==0x01){
								XGpio_DiscreteWrite(&GpioOutput, 1, 0x00000001);
								//Cfg para los correspondientes bits (en, init, val, etc..)
								XGpio_DiscreteWrite(&GpioOutput, 1, 0x00000000);
								strcpy(SendBuffer,"SUCCESS_CFG");
								LenData=11;
								while(XUartLite_IsSending(&uart_module)){}
								XUartLite_Send(&uart_module, SendBuffer,LenData);
			} else{

							strcpy(SendBuffer,"ERROR_CFG__");
							LenData=11;
							while(XUartLite_IsSending(&uart_module)){}
							XUartLite_Send(&uart_module, SendBuffer,LenData);

		}


	} else if (Step == 2){

		if(RecvBuff[0]==0x02){

			strcpy(SendBuffer,"SUCC_WR");
			LenData=7;
			while(XUartLite_IsSending(&uart_module)){}
			XUartLite_Send(&uart_module, SendBuffer,LenData);

		} else{

			strcpy(SendBuffer,"ERROR_W");
			LenData=7;
			while(XUartLite_IsSending(&uart_module)){}
			XUartLite_Send(&uart_module, SendBuffer,LenData);

		}

	} else if (Step == 3){


			//Debo poner dirección
			u32 addressForWriting = 0x00000000;
			fromPython = RecvBuff[0];
			addressForWriting = fromPython<<3;

			//Me quedo con 10 bits para la address.
			//Escribo la address (primer bit -->sw rst, segundo --> valid, tercero --> enable)
			XGpio_DiscreteWrite(&GpioOutput, 1, addressForWriting);


			//Debo habilitar write enable
			XGpio_DiscreteWrite(&GpioOutput, 1, 0x00000006);

			//Tengo dato puesto desde verilog (un contador), lo escribirá segun interpreto.


			strcpy(SendBuffer,"ADD_WR");
			LenData=7;
			while(XUartLite_IsSending(&uart_module)){}
			XUartLite_Send(&uart_module, SendBuffer,LenData);



	} else if (Step == 4){


		if(RecvBuff[0]==0x03){

					strcpy(SendBuffer,"SUCC_rd");
					LenData=7;
					while(XUartLite_IsSending(&uart_module)){}
					XUartLite_Send(&uart_module, SendBuffer,LenData);

		} else {

					strcpy(SendBuffer,"ERROR_W");
					LenData=7;
					while(XUartLite_IsSending(&uart_module)){}
					XUartLite_Send(&uart_module, SendBuffer,LenData);

		}



	} else if (Step == 5) {

					u32 addressForReading= 0x00000000;
					fromPython = RecvBuff[0];

					addressForReading = fromPython<<13;



					//Me quedo con 10 bits para la address.
					//Escribo la address (primer bit -->sw rst, segundo --> valid, tercero --> enable)
					XGpio_DiscreteWrite(&GpioOutput, 1, addressForReading);


					memory = XGpio_DiscreteRead(&GpioInput, 1);

					for(int ptrMask=0;ptrMask<4;ptrMask++){

						mask=0xFF<<(8*(3-ptrMask));
						bytSend=(memory & mask)>>(8*(3-ptrMask));
						dataBuffer[ptrMask]=bytSend;

					}

					LenData = 4;
					SendBuffer[0]=dataBuffer[0];
					SendBuffer[1]=dataBuffer[1];
					SendBuffer[2]=dataBuffer[2];
					SendBuffer[3]=dataBuffer[3];
					XUartLite_Send(&uart_module, SendBuffer,LenData);
					while(XUartLite_IsSending(&uart_module)){}


	} else {
					strcpy(SendBuffer,"ST_UNKNOWN");
					LenData=10;
	}

	//END IF STEP

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

//Trama nuestra
void send_trama(int id){
	unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
	unsigned char fin_trama[1]={0x40};
	cabecera[3]=id;
	XUartLite_Send(&uart_module, cabecera,4);
	while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, fin_trama,1);
}

