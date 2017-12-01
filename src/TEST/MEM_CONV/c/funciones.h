/*
 * funciones.h
 *
 *  Created on: Sep 8, 2015
 *      Author: gbergero
 */



#ifndef FUNCIONES_H_
#define FUNCIONES_H_

//POSICIONES [5:0] ocupadas por select_log
#define select_log 					0
#define enable_noise 				6
#define enable_codewords			6
#define enable_ber_channel			6
#define enable_ber_decoder			6
#define enable_log		 			7
#define sel_ruido 					8
#define set_sigma 					9
#define enable_to_log_error			10
#define reset_from_cpu 				11
#define enable_seed 				12
#define start_decoding 				13
#define set_factor 					14
#define set_prmt_resolucion			15
#define procesar_1_word 			16
#define reset_error_word 			17
#define num_cw_error_to_reset 		18 //[20:18]
#define set_prmt_iteraciones 		21
#define reset_numeros_aleatorios 	22

 //PARAMETROS
#define NB_SIGMA 			14
#define NB_FACTOR 			14
#define NB_ADDR_CODEWORD	12
#define NB_RESOLUCIONES 	3
#define NB_ITERACIONES		6

//-----------------------------DEFINICION DE FUNCIONES--------------------------------------
void set_pin(short int Value,short int desplazamiento);
void set_prmt_sigma(int Value,int Value2);
void resetear();
void inicializar();
void loguear(short int ,short int );
void send_log(u32 *value,short int num_deco,short int to_channel);//la posicion es para avisar q parte del dato estoy enviando
void set_loguer(short int value);
void procesar_word();
void send_codeword_with_error(int);
void send_data_log_iteraciones();
void set_resolucion(short int);
void reset_error_word_func(int num_deco);
void set_iteraciones(unsigned char num_iteraciones);

void set_gpio(unsigned char data[]);
void send_log_ber(u32 *value,short int num_deco);
void loguear_ber(short int num_deco);

void set_coeff_ch(int length,unsigned char data[]);
void set_coeff_ffe(int length,unsigned char data[]);
void set_coeff_dffe(int length,unsigned char data[]);

void read_ram_block64(int device);
void send_read_ram(u32 *value,int device);
void read_ram_block64_one(int device);
void read_ram_block32(int device);
//---------------------------------------------------------------------------------------

void reset_error_word_func(int num_deco)
{
	u32 valor = (num_deco & 0x07) << num_cw_error_to_reset;
	u32 mascara = 0xFFFFFFFF ^ (0x07 << num_cw_error_to_reset);
	GPO_Value = valor | (GPO_Value & mascara);
	XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value);
	set_pin(1,reset_error_word);
	set_pin(0,reset_error_word);
}

void set_resolucion(short int value)
{
	GPO_Param = value;

	XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);

	set_pin(1,set_prmt_resolucion);
	MB_Sleep(1);
	set_pin(0,set_prmt_resolucion);

}

void send_log(u32 *value,short int num_deco,short int to_channel)
{
	const int tam=17;
	unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
	unsigned char datos[tam];
	unsigned char fin_trama[1]={0x40};

	cabecera[0]=cabecera[0] | 0x10;//TRAMA LARGA
	cabecera[2]=tam;
	fin_trama[0]=fin_trama[0] | 0x10;

	cabecera[3]=(to_channel==1)? def_ANS_LOG_CHA:def_ANS_LOG_DEC;
	int i;
	datos[0] = (num_deco & 0xFF);
	for(i=0;i<4;i++)
	{
		datos[4+(i*4)]=value[i]&(0x000000FF);
		datos[3+(i*4)]=(value[i]&(0x0000FF00))>>8;
		datos[2+(i*4)]=(value[i]&(0x00FF0000))>>16;
		datos[1+(i*4)]=(value[i]&(0xFF000000))>>24;
	}

	XUartLite_Send(&uart_module, cabecera,4);
	for(i=0;i<tam;i++)
	{
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos[i]),1);
	}

	while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, fin_trama,1);
}

void send_log_ber(u32 *value,short int num_ber) // apola
{
	const int tam=17;
	unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
	unsigned char datos[tam];
	unsigned char fin_trama[1]={0x40};

	cabecera[0]=cabecera[0] | 0x10;//TRAMA LARGA
	cabecera[2]=tam;
	fin_trama[0]=fin_trama[0] | 0x10;

	cabecera[3]=def_BER_READ;
	int i;
	datos[0] = (num_ber & 0xFF);
	for(i=0;i<4;i++)
	{
		datos[4+(i*4)]=value[i]&(0x000000FF);
		datos[3+(i*4)]=(value[i]&(0x0000FF00))>>8;
		datos[2+(i*4)]=(value[i]&(0x00FF0000))>>16;
		datos[1+(i*4)]=(value[i]&(0xFF000000))>>24;
	}

	XUartLite_Send(&uart_module, cabecera,4);
	for(i=0;i<tam;i++)
	{
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos[i]),1);
	}

	while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, fin_trama,1);
}


void set_pin(short int Value,short int desplazamiento)
{
	u32 valor_dato = (Value<<desplazamiento) ;
	u32 mascara=0xFFFFFFFF ^ (1<<desplazamiento);
	GPO_Value=valor_dato | (mascara & GPO_Value);
	XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value);
}

void set_gpio(unsigned char data[]) // apola
{
	/* GPO_Value=0x01000000 | Value; */
	/* XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value); */
	/* GPO_Value=0x01800000 | Value; */
	/* XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value); */
	/* GPO_Value=0x01000000 | Value; */
	/* XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value); */
    
    GPO_Value=data[3]<<24;
    GPO_Value|=data[2]<<16;
    GPO_Value|=data[1]<<8;
    GPO_Value|=data[0];
	XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value);
	GPO_Value|=0x80 << 16;
	XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value);
	GPO_Value|=0x00 << 16;
	XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value);
}

void set_prmt_sigma(int Val_Sigma, int Val_Factor)
{

	GPO_Param = Val_Sigma ;
	XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
	set_pin(1,set_sigma);
	MB_Sleep(1);
	set_pin(0,set_sigma);

	GPO_Param = Val_Factor ;
	XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
	set_pin(1,set_factor);
	MB_Sleep(1);
	set_pin(0,set_factor);

}

void resetear()
{
	set_pin(1,reset_from_cpu);
	set_pin(0,enable_codewords);
	set_pin(0,reset_from_cpu);
}

void inicializar()
{
	GPO_Value=(1<<reset_from_cpu)|(1<<enable_noise)|(1<<enable_ber_channel)|(1<<enable_ber_decoder);
	XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value);
	set_pin(0,reset_from_cpu);
}


void loguear(short int to_channel,short int num_deco)
{
	u32 valor_leido[4];
	set_pin(1,enable_log);
	set_pin(0,enable_log);
	if(to_channel==1)
	{
		set_loguer(0);
		valor_leido[0]=XGpio_DiscreteRead(&GpioInput, 1);
		set_loguer(1);
		valor_leido[1]=XGpio_DiscreteRead(&GpioInput, 1);
		set_loguer(2);
		valor_leido[2]=XGpio_DiscreteRead(&GpioInput, 1);
		set_loguer(3);
		valor_leido[3]=XGpio_DiscreteRead(&GpioInput, 1);
	}
	else
	{
		set_loguer(4 + (num_deco * 4));
		valor_leido[0]=XGpio_DiscreteRead(&GpioInput, 1);
		set_loguer(5 + (num_deco * 4));
		valor_leido[1]=XGpio_DiscreteRead(&GpioInput, 1);
		set_loguer(6 + (num_deco * 4));
		valor_leido[2]=XGpio_DiscreteRead(&GpioInput, 1);
		set_loguer(7 + (num_deco * 4));
		valor_leido[3]=XGpio_DiscreteRead(&GpioInput, 1);
	}
	send_log(valor_leido,num_deco,to_channel);
}

void loguear_ber(short int num_ber){
	u32 valor_leido[4];
    unsigned char datos_rec[4];
    datos_rec[3]=0x00;datos_rec[2]=0x00;datos_rec[1]=0x00;datos_rec[0]=0x02;
    set_gpio(datos_rec);
    valor_leido[0]=XGpio_DiscreteRead(&GpioInput, 1);
    datos_rec[3]=0x00;datos_rec[2]=0x00;datos_rec[1]=0x00;datos_rec[0]=0x01;
    set_gpio(datos_rec);
    valor_leido[1]=XGpio_DiscreteRead(&GpioInput, 1);
    datos_rec[3]=0x00;datos_rec[2]=0x00;datos_rec[1]=0x00;datos_rec[0]=0x04;
    set_gpio(datos_rec);
    valor_leido[2]=XGpio_DiscreteRead(&GpioInput, 1);
    datos_rec[3]=0x00;datos_rec[2]=0x00;datos_rec[1]=0x00;datos_rec[0]=0x03;
    set_gpio(datos_rec);
    valor_leido[3]=XGpio_DiscreteRead(&GpioInput, 1);
	
    //set_pin(1,enable_log);
	//set_pin(0,enable_log);
    //set_loguer(0);
    //valor_leido[0]=XGpio_DiscreteRead(&GpioInput, 1);
    //set_loguer(1);
    //valor_leido[1]=XGpio_DiscreteRead(&GpioInput, 1);
    //set_loguer(2);
    //valor_leido[2]=XGpio_DiscreteRead(&GpioInput, 1);
    //set_loguer(3);
    //valor_leido[3]=XGpio_DiscreteRead(&GpioInput, 1);

	send_log_ber(valor_leido,num_ber);
}

void set_coeff_ch(int length,unsigned char data[]){
    
    int i;

	for(i=0;i<length;i++){
        GPO_Param  = (0xFF & i)<<24;
        GPO_Param |= 0x00 <<16; 
        GPO_Param |= 0x00 <<8;
        GPO_Param |= 0xFF & data[i];
        XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
        GPO_Param |=0x80 << 16;
        XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
        GPO_Param |=0x00 << 16;
        XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
        MB_Sleep(2);
    }   
}

void set_coeff_ffe(int length,unsigned char data[]){
    
    int i;

	for(i=0;i<length/3;i++){
        GPO_Param  = ((0xFF & i)+15)<<24;
        GPO_Param |= (0x7F & data[(i*3)+2])<<16; 
        GPO_Param |= data[(i*3)+1] <<8;
        GPO_Param |= data[(i*3)+0];
        XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
        GPO_Param |=0x80 << 16;
        XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
        GPO_Param |=0x00 << 16;
        XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
        MB_Sleep(2);
    }   
}

void set_coeff_dffe(int length,unsigned char data[]){
    
    int i;

	for(i=0;i<length/3;i++){
        GPO_Param  = ((0xFF & i)+22)<<24;
        GPO_Param |= (0x7F & data[(i*3)+2])<<16; 
        GPO_Param |= data[(i*3)+1] <<8;
        GPO_Param |= data[(i*3)+0];
        XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
        GPO_Param |=0x80 << 16;
        XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
        GPO_Param |=0x00 << 16;
        XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
        MB_Sleep(2);
    }   
}


void read_ram_block64(int device){
	u32 valor_leido[256*2];
    unsigned char datos_rec[4];
    int ptr;
    for(ptr=0;ptr<256;ptr++){

        datos_rec[3] = 0x07;
        datos_rec[2] = 0x03 & device;            // Sel Device
        datos_rec[1] = ((0x7F00 & ptr)>>8)|0x00; // High Part and Addr
        datos_rec[0] = 0x00FF & ptr;             // Addr
        set_gpio(datos_rec);

        datos_rec[3]=0x00;
        datos_rec[2]=0x00;
        datos_rec[1]=0x00;
        datos_rec[0]=0x00;
        set_gpio(datos_rec);

        valor_leido[(ptr*2)+0] = XGpio_DiscreteRead(&GpioInput, 1);

        datos_rec[3] = 0x07;
        datos_rec[2] = 0x03 & device;            // Sel Device
        datos_rec[1] = ((0x7F00 & ptr)>>8)|0x80; // Low Part and Addr
        datos_rec[0] = 0x00FF & ptr;             // Addr
        set_gpio(datos_rec);

        datos_rec[3]=0x00;
        datos_rec[2]=0x00;
        datos_rec[1]=0x00;
        datos_rec[0]=0x00;
        set_gpio(datos_rec);

        valor_leido[(ptr*2)+1] = XGpio_DiscreteRead(&GpioInput, 1);
    }
	
	send_read_ram(valor_leido,device);
}

void send_read_ram(u32 *value,int device) // apola
{
	const int tam=256*2*4;
	unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
//	unsigned char datos[tam];
	unsigned char datos;
	unsigned char fin_trama[1]={0x40};

	cabecera[0]=cabecera[0] | 0x10;//TRAMA LARGA
	cabecera[1]=(0xFF00 & tam)>>8;
    cabecera[2]=0xFF & tam;
    if(device==0)
        cabecera[3]=def_LOG_READ_CHANNEL;
    else if(device==1)
        cabecera[3]=def_LOG_READ_FFE;
    else{
        cabecera[3]=def_LOG_READ_ERROR;
    }

	fin_trama[0]=fin_trama[0] | 0x10;
	XUartLite_Send(&uart_module, cabecera,4);

	int i;
	for(i=0;i<256*2;i++)
	{

		datos=value[i]&(0x000000FF);
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value[i]&(0x0000FF00))>>8;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value[i]&(0x00FF0000))>>16;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value[i]&(0xFF000000))>>24;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);

		/* datos[3+(i*4)]=value[i]&(0x000000FF); */
		/* while(XUartLite_IsSending(&uart_module)){} */
		/* XUartLite_Send(&uart_module, &(datos[3+(i*4)]),1); */
		/* datos[2+(i*4)]=(value[i]&(0x0000FF00))>>8; */
		/* while(XUartLite_IsSending(&uart_module)){} */
		/* XUartLite_Send(&uart_module, &(datos[2+(i*4)]),1); */
		/* datos[1+(i*4)]=(value[i]&(0x00FF0000))>>16; */
		/* while(XUartLite_IsSending(&uart_module)){} */
		/* XUartLite_Send(&uart_module, &(datos[1+(i*4)]),1); */
		/* datos[0+(i*4)]=(value[i]&(0xFF000000))>>24; */
		/* while(XUartLite_IsSending(&uart_module)){} */
		/* XUartLite_Send(&uart_module, &(datos[0+(i*4)]),1); */
	}
	while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, fin_trama,1);

	/* XUartLite_Send(&uart_module, cabecera,4); */
	/* for(i=0;i<tam;i++) */
	/* { */
	/* 	while(XUartLite_IsSending(&uart_module)){} */
	/* 	XUartLite_Send(&uart_module, &(datos[i]),1); */
	/* } */

	/* while(XUartLite_IsSending(&uart_module)){} */
	/* XUartLite_Send(&uart_module, fin_trama,1); */
}



void read_ram_block64_one(int device){
	u32 value;
    unsigned char datos_rec[4];

	const int tam=512*2*4;
	unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
	unsigned char datos;
	unsigned char fin_trama[1]={0x40};

	cabecera[0]=cabecera[0] | 0x10;//TRAMA LARGA
	cabecera[1]=(0xFF00 & tam)>>8;
    cabecera[2]=0xFF & tam;
    if(device==0)
        cabecera[3]=def_LOG_READ_CHANNEL;
    else if(device==1)
        cabecera[3]=def_LOG_READ_FFE;
    else{
        cabecera[3]=def_LOG_READ_ERROR;
    }
	fin_trama[0]=fin_trama[0] | 0x10;
	XUartLite_Send(&uart_module, cabecera,4);

    int i;
    for(i=0;i<512;i++){

        datos_rec[3] = 0x07;
        datos_rec[2] = 0x03 & device;            // Sel Device
        datos_rec[1] = ((0x7F00 & i)>>8)|0x00; // High Part and Addr
        datos_rec[0] = 0x00FF & i;             // Addr
        set_gpio(datos_rec);

        datos_rec[3]=0x00;
        datos_rec[2]=0x00;
        datos_rec[1]=0x00;
        datos_rec[0]=0x00;
        set_gpio(datos_rec);

        value = XGpio_DiscreteRead(&GpioInput, 1);

		datos=value&(0x000000FF);
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value&(0x0000FF00))>>8;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value&(0x00FF0000))>>16;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value&(0xFF000000))>>24;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);

        datos_rec[3] = 0x07;
        datos_rec[2] = 0x03 & device;            // Sel Device
        datos_rec[1] = ((0x7F00 & i)>>8)|0x80; // Low Part and Addr
        datos_rec[0] = 0x00FF & i;             // Addr
        set_gpio(datos_rec);

        datos_rec[3]=0x00;
        datos_rec[2]=0x00;
        datos_rec[1]=0x00;
        datos_rec[0]=0x00;
        set_gpio(datos_rec);

        value = XGpio_DiscreteRead(&GpioInput, 1);

		datos=value&(0x000000FF);
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value&(0x0000FF00))>>8;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value&(0x00FF0000))>>16;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value&(0xFF000000))>>24;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
    }
    while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, fin_trama,1);
	
}

void read_ram_block32(int device){
	u32 value;
    unsigned char datos_rec[4];

	const int tam=1024*4;
	unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
	unsigned char datos;
	unsigned char fin_trama[1]={0x40};

	cabecera[0]=cabecera[0] | 0x10;//TRAMA LARGA
	cabecera[1]=(0xFF00 & tam)>>8;
    cabecera[2]=0xFF & tam;
    if(device==0)
        cabecera[3]=def_LOG_READ_CHANNEL;
    else if(device==1)
        cabecera[3]=def_LOG_READ_FFE;
    else if(device==2)
        cabecera[3]=def_LOG_READ_ERROR;
    else if(device==3)
        cabecera[3]=def_LOG_READ_FFE_COEFF;
    else if(device==4)
        cabecera[3]=def_LOG_READ_DFFE_COEFF;
    else if(device==5){
        cabecera[3]=def_LOG_READ_BITS;
    }
    else{
    	cabecera[3]=def_LOG_READ_SRRC;
    }
	fin_trama[0]=fin_trama[0] | 0x10;
	XUartLite_Send(&uart_module, cabecera,4);

    int i;
    for(i=0;i<1024;i++){

        datos_rec[3] = 0x07;
        datos_rec[2] = 0x07 & device;            // Sel Device
        datos_rec[1] = ((0x7F00 & i)>>8); // Addr
        datos_rec[0] = 0x00FF & i;             // Addr
        set_gpio(datos_rec);

        datos_rec[3]=0x00;
        datos_rec[2]=0x00;
        datos_rec[1]=0x00;
        datos_rec[0]=0x00;
        set_gpio(datos_rec);

        value = XGpio_DiscreteRead(&GpioInput, 1);

		datos=value&(0x000000FF);
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value&(0x0000FF00))>>8;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value&(0x00FF0000))>>16;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
		datos=(value&(0xFF000000))>>24;
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, &(datos),1);
    }
    while(XUartLite_IsSending(&uart_module)){}
	XUartLite_Send(&uart_module, fin_trama,1);
	
}


void set_loguer(short int value)
{
	u32 valor_dato = 0x3F & value;// value << select_log
	u32 mascara=0xFFFFFFC0;
	GPO_Value=valor_dato | (mascara & GPO_Value);
	XGpio_DiscreteWrite(&GpioOutput,1, (u32) GPO_Value);
}

void procesar_word()
{
	set_pin(1,procesar_1_word);
	set_pin(0,procesar_1_word);
}

void send_codeword_with_error(int num_deco)
{
	set_pin(1,enable_to_log_error);
	set_loguer(0);
	u32	valor_leido=XGpio_DiscreteRead(&GpioInput, 1);

	if( ((valor_leido >> num_deco) & 0x0001) == 1)
	{
		unsigned char cabecera[4]={0xA0,0x00,0x00,0x00};
		cabecera[0]=cabecera[0] | 0x10;//TRAMA LARGA
		cabecera[1]=0x70;
		cabecera[2]=0x80;
		cabecera[3]=def_CW_ERROR;

		unsigned char fin_trama[1]={0x40};
		fin_trama[0]=fin_trama[0] | 0x10;
		XUartLite_Send(&uart_module, cabecera,4);

		int i;

		for(i=0;i<3200;i++)
		{
			GPO_Param = i;
			XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
			unsigned char datos;

			set_loguer(1 + (num_deco * 3));
			while(XUartLite_IsSending(&uart_module)){}
			u32 valor_leido=XGpio_DiscreteRead(&GpioInput, 1);
			datos	= (valor_leido & (0xFF000000))>>24;
			XUartLite_Send(&uart_module,&(datos),1);
			datos	= (valor_leido & (0x00FF0000))>>16;
			XUartLite_Send(&uart_module,&(datos),1);
			datos	= (valor_leido & (0x0000FF00))>>8;
			XUartLite_Send(&uart_module,&(datos),1);
			datos	= valor_leido & (0x000000FF);
			XUartLite_Send(&uart_module,&(datos),1);

			set_loguer(2 + (num_deco * 3));
			while(XUartLite_IsSending(&uart_module)){}
			valor_leido=XGpio_DiscreteRead(&GpioInput, 1);
			datos	= (valor_leido & (0xFF000000))>>24;
			XUartLite_Send(&uart_module,&(datos),1);
			datos	= (valor_leido & (0x00FF0000))>>16;
			XUartLite_Send(&uart_module,&(datos),1);
			datos	= (valor_leido & (0x0000FF00))>>8;
			XUartLite_Send(&uart_module,&(datos),1);
			datos	= valor_leido & (0x000000FF);
			XUartLite_Send(&uart_module,&(datos),1);

			set_loguer(3 + (num_deco * 3));
			while(XUartLite_IsSending(&uart_module)){}
			valor_leido=XGpio_DiscreteRead(&GpioInput, 1);
			datos	= valor_leido & (0x000000FF);
			XUartLite_Send(&uart_module,&(datos),1);
		}
		while(XUartLite_IsSending(&uart_module)){}
		XUartLite_Send(&uart_module, fin_trama,1);
		reset_error_word_func(num_deco);
	}
	else
	{
		send_trama(def_CW_ERROR_NOT_FOUND);
	}
	set_pin(0,enable_to_log_error);
}

void set_iteraciones(unsigned char num_iteraciones)
{
	GPO_Param = num_iteraciones;
	XGpio_DiscreteWrite(&GpioParameter,1, (u32) GPO_Param);
	set_pin(1,set_prmt_iteraciones);
	set_pin(0,set_prmt_iteraciones);
}

#endif /* FUNCIONES_H_ */
