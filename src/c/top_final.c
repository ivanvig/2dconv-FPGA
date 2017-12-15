#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"
#include "xil_printf.h"
#include "xuartlite.h"
//#include "microblaze_sleep.h"


#define PORT_IN	 		XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_GPIO_0_DEVICE_ID
//Device_ID Operaciones
#define def_SET_SIGMA			1
#define def_START_RUIDO			2
//Device_ID Respuestas
#define def_ACK 				1
#define def_ERROR 				2
#define lengthK					3
#define GPIOdata				1
#define GPIOctrl  				29
#define GPIOvalid 				28
#define GPIOout					31
//Trama case
#define def_reset	0xa0000040
#define def_kernel	0xa0010040
#define def_imgzise 0xa0020040
#define def_load 	0xa0030040
#define def_loadend 0xa1300040
#define def_run		0xa0040040
#define def_dreq	0x9001//0xa0050040
#define def_bufzise 150

//funciones
void send(int id, int bytes);
void send_trama(int id);
void send_ack(void);
void send_num(unsigned char a ,unsigned char b);

void initialize(void);
void loadKernel(unsigned char* cabecera);
void imageZise(unsigned char *cabecera, u32 imageSize);
void loadImage(unsigned char* cabecera, u32 image, u32 end);
void dataReq(unsigned char* cabecera);

XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;
u32 GPO_Value;
u32 GPO_Param;
XUartLite uart_module;

short int num_ber;

int main()
{
	init_platform();
	XUartLite_Initialize(&uart_module, 0);
	GPO_Value=0x00000000;
	GPO_Param=0x00000000;

	int Status;
	u32 trama =0;
	u32 imageSize = 0;
	u32 crt = 0;
	u32 datos =0;
	unsigned char cabecera[4];
	unsigned int contador;

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

	XGpio_SetDataDirection(&GpioOutput, 1, 0x00000000);
	XGpio_SetDataDirection(&GpioInput, 1, 0xFFFFFFFF);

	while(1){

		read(stdin, &cabecera, 4);
		trama = cabecera[3]<<24 | cabecera[2]<<16|cabecera[1]<<8|cabecera[0];
		switch(trama){
			case def_reset:
				imageSize = 0;
				initialize();  //resee all
				send(def_reset,4);
				break;
			case def_kernel:
				//loadKernel((unsigned char *) &cabecera);
				crt = 0<<GPIOctrl;
				datos =0;
				XGpio_DiscreteWrite(&GpioOutput, 1, crt); //0b000,instruccion carga de kernel
				send_ack();
				for (int i =0; i < lengthK ; i++){
					read(stdin,&cabecera,4);
					datos = cabecera[3]<<24 | cabecera[2]<<16 | cabecera[1]<<8 | cabecera[0];
					datos = (datos << GPIOdata) |  crt;
					XGpio_DiscreteWrite(&GpioOutput, 1, datos | 1 <<GPIOvalid); //subo valid
					XGpio_DiscreteWrite(&GpioOutput, 1, datos & ~(1<<GPIOvalid)); // bajo el valid
					send_ack();
				}
				send(def_kernel,4); //echo para finalizado la operacion
				break;
			case def_imgzise:
				//imageZise((unsigned char*)&cabecera, (u32)&imageSize); //cargo la imgaen
				crt = 1<<GPIOctrl;
				XGpio_DiscreteWrite(&GpioOutput, 1, crt);
				send_ack();
				read(stdin, &cabecera, 2);
				imageSize = cabecera[1]<<8 | cabecera[0]; //latch de la imgen
				XGpio_DiscreteWrite(&GpioOutput,1,imageSize<<GPIOdata | crt);
				send(def_imgzise,4); //echo
				break;
			case def_load:
				//loadImage((unsigned char*) &cabecera, imageSize, 0);
					contador = 0;
					datos = 0;
					u32 ctr = 2<<GPIOctrl;
					XGpio_DiscreteWrite(&GpioOutput, 1, ctr);
					send_ack();
					//upload
					while (contador <= imageSize ){
							read(stdin, &cabecera, 1);
							datos = cabecera[0]  <<GPIOdata;
							//send_ack();
							XGpio_DiscreteWrite(&GpioOutput, 1, (datos | ctr )  |  1 <<GPIOvalid);
							XGpio_DiscreteWrite(&GpioOutput, 1, (datos | ctr )  & ~(1<<GPIOvalid)); //bajo el valid
							contador++;
					}
				send(def_load,4); //ack final de caraga de columna
				break;
			case def_loadend:
				//loadImage((unsigned char*) &cabecera, imageSize, 1);
				contador = 0;
				datos = 0;
				ctr = 2<<GPIOctrl;
				XGpio_DiscreteWrite(&GpioOutput, 1, ctr);
				send_ack();
					//upload
				while (contador <= imageSize ){
						read(stdin, &cabecera, 1);
						datos = cabecera[0]  <<GPIOdata;
						//send_ack();
						ctr =(contador == imageSize)? 4<<GPIOctrl : 2<<GPIOctrl;
						XGpio_DiscreteWrite(&GpioOutput, 1, (datos | ctr )  |  1 <<GPIOvalid);
						XGpio_DiscreteWrite(&GpioOutput, 1, (datos | ctr )  & ~(1<<GPIOvalid)); //bajo el valid
						contador++;
				}
				send(def_loadend,4);

				while (!(XGpio_DiscreteRead(&GpioOutput,1) & (1<<31))){}
				crt = 3<<GPIOctrl;
				datos =0;
				contador =0;
				while (XGpio_DiscreteRead(&GpioOutput,1) & (1<<31)){
					datos = XGpio_DiscreteRead(&GpioOutput,1) & ~(1<<31);
					XGpio_DiscreteWrite(&GpioOutput, 1, crt |  1 <<GPIOvalid);
					XGpio_DiscreteWrite(&GpioOutput, 1,  crt & ~(1<<GPIOvalid));
					send(datos, 2);

				}
				send(def_dreq, 2);
				XUartLite_ResetFifos(&uart_module);
				//dataReq((unsigned char*) &cabecera);
				break;

			default:
				XUartLite_ResetFifos(&uart_module);
				send(trama,4);
				break;
		}
		XUartLite_ResetFifos(&uart_module);
	}
	cleanup_platform();
	return 0;
}

/*
 * Envia ACK para para la comunicacion orientada a la conexion
 * por UART
 */
void send_ack(void){
	unsigned char cabecera[4]={0xA1,0x00,0x00,0x41};
	/*unsigned char fin_trama[1]={0x41};
	unsigned char datos[1];
	datos[0]=from_id;*/
	cabecera[2]=def_ACK;
	XUartLite_Send(&uart_module, cabecera,4);
	while(XUartLite_IsSending(&uart_module)){}
	/*XUartLite_Send(&uart_module, datos,1);
	XUartLite_Send(&uart_module, fin_trama,1);
	*/
}

/*
 * envia datos por el puerto uart
 * @param id dato de 4 bytes para enviar
 */
void send(int id, int bytes){
	unsigned char sendBuffer[bytes];
	for(int i=0;i<bytes;i++){
		sendBuffer[i]=(id>>(8*(bytes-1-i)))&0xFF;
	}
	XUartLite_Send(&uart_module, sendBuffer,bytes);
	while(XUartLite_IsSending(&uart_module)){}
}

/*
 * Reset todos los modulos FMS, CONV, File Reg
 */
void initialize(void){
	XGpio_DiscreteWrite(&GpioOutput, 1, 0x1);
	XGpio_DiscreteWrite(&GpioOutput, 1, 0x0);
}

/*
 * carga el kernel a la placa
 */
void loadKernel(unsigned char *cabecera){
	int ctrl = 0<<GPIOctrl;
	u32 datos =0;
	XGpio_DiscreteWrite(&GpioOutput, 1, ctrl); //0b000,instruccion carga de kernel
	send_ack();
	XUartLite_ResetFifos(&uart_module);
	for (int i =0; i < lengthK ; i++){
		read(stdin,&cabecera,4);
		datos = cabecera[3]<<24 | cabecera[2]<<16 | cabecera[1]<<8 | cabecera[0];
		datos = (datos << GPIOdata) |  ctrl;
		XGpio_DiscreteWrite(&GpioOutput, 1, datos | 1 <<GPIOvalid); //subo valid
		XGpio_DiscreteWrite(&GpioOutput, 1, datos & ~(1<<GPIOvalid)); // bajo el valid
		send_ack();
	}
}

/*
 * Carga la longitud de la imagen en el hard
 * solo lee dos bytes del buff
 * @param cabecera el buffer de recepcion del UART
 * @param image , la varible en donde se almacena la longitud de la imagen
 * para se usada por el micro
 */
void imageZise(unsigned char *cabecera, u32 imageSize){
	//instr = 0x00000a05;
	u32 ctr = 1<<GPIOctrl;
	XGpio_DiscreteWrite(&GpioOutput, 1, ctr);
	send_ack();

	read(stdin, &cabecera, 2);
	imageSize = cabecera[1]<<8 | cabecera[0];
	//0x0001b705 ; //latch de la imgen
	XGpio_DiscreteWrite(&GpioOutput,1,imageSize<<GPIOdata | ctr);
}

/*
 * Carga la imagen y el ultimo dato empieza a procesar.
 */
void loadImage(unsigned char* cabecera, u32 image,u32 end){
	u8 bufImagen[def_bufzise];
	unsigned int contador = 0;
	unsigned int i = 0;
	u32 value = 0;
	u32 imageSize = image;
	u32 ctr = 2<<GPIOctrl;
	XGpio_DiscreteWrite(&GpioOutput, 1, ctr);
	send_ack();
	do{
		XUartLite_ResetFifos(&uart_module);//upload
		i=0;
		while (contador < imageSize && i < def_bufzise){
			read(stdin, &cabecera, 1);
			bufImagen[contador] = cabecera[0] ;
			contador++; i++;
			send_ack();
		}
		//download
		for(int j=0; j<i ; j++){
			//dato mas el valid = 1;
			value = bufImagen[j]<<GPIOdata;
			ctr = (end && contador == imageSize && j==i-1)? 4<<GPIOctrl : 2<<GPIOctrl;
			XGpio_DiscreteWrite(&GpioOutput, 1, (value | ctr )  |  1 <<GPIOvalid);
			XGpio_DiscreteWrite(&GpioOutput, 1, (value | ctr )  & ~(1<<GPIOvalid)); //bajo el valid
		}
	}while(contador < imageSize);
}

/*
 * Data request
 */
/*
void dataReq(unsigned char* cabecera){
	u32 crt = 3<<GPIOctrl;
	u32 datos =0;
	XGpio_DiscreteWrite(&GpioOutput,1,crt);
	while(XGpio_DiscreteRead(&GpioOutput,1) && (1<<GPIOout)){ //0x1B400
		read(stdin,&cabecera,1);
		if(cabecera[0] == '5' ){
			datos = XGpio_DiscreteRead(&GpioOutput,1);
			XGpio_DiscreteWrite(&GpioOutput, 1, crt |  1 <<GPIOvalid);
			XGpio_DiscreteWrite(&GpioOutput, 1,  crt & ~(1<<GPIOvalid));
			send(datos);
			XUartLite_ResetFifos(&uart_module);
		}
	}
	send(def_dreq);
}
*/

void send_trama(int id){
	unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
	unsigned char fin_trama[1]={0x40};
	cabecera[3]=id;
	XUartLite_Send(&uart_module, cabecera,4);
	while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, fin_trama,1);
}
