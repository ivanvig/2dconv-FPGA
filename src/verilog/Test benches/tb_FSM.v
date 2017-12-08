`timescale 1ns / 10ps

module tb_FSM();	

	parameter NB_ADDRESS= 10;
	//Para ver mas rapido si llega a completarse
    parameter NB_IMAGE  = 10;
    parameter N_CONV  = 2;
	//Todo puerto de salida del modulo es un cable.
	//Todo puerto de estímulo o generación de entrada es un registro.
	//Definición de puertos
    reg                    	CLK;
    reg                    	reset;
    reg                    	SOP;
    reg [NB_IMAGE-1:0]     	imgLength;
    reg                    	valid;
    reg 					load;

    wire [NB_ADDRESS-1:0]  	writeAddress;
    wire [NB_ADDRESS-1:0]  	readAddress;
    wire                   	EOP;
    wire                   	chblock;
    wire 					vld;

	initial	begin
		CLK       = 1'b0;
		SOP       = 1'b0;	
		imgLength = 10'h9;
		valid     = 1'b0;
		reset     = 1'b1;
		load  	  = 1'b0;

		#10 reset = 1'b0;
		// etapa de carga 
		#50 load = 1'b1;
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;

		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;		
		
		#50 valid = 1'b1;
		//load = 1'b0;
		#50 valid = 1'b0;

		//memem 2 0 n

		#50 valid = 1'b1;
		#50 valid = 1'b0;

		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		load = 1'b0;
		#50 valid = 1'b0;


		//Carga/lectura --> testeo del valid.
		//Emulo arranque de sistema, deberían cargarse los parametros correspondientes
		
		#100 SOP = 1'b1;
		#100 SOP = 1'b0;

		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;

		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;

		//lecura de la mem 2
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;

		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;	
		
		#50 valid = 1'b1;
		#50 valid = 1'b0;



		#200 $finish;
	end
	always #2.5 CLK=~CLK;
	//Módulo para pasarle los estímulos del banco de pruebas.
	Fsmv#(  
		.NB_ADDRESS(NB_ADDRESS),
		.NB_IMAGE (NB_IMAGE),
		.N_CONV(N_CONV))
		u_Fsmv(
			.o_readAdd(readAddress),
			.o_writeAdd(writeAddress),
			.o_EoP(EOP),
			.o_changeBlock(chblock),
			.o_fms2conVld(vld),
			.i_CLK(CLK),
			.i_reset(reset),
			.i_SoP(SOP),
			.i_load(load),
			.i_imgLength(imgLength),
			.i_valid(valid));


endmodule
