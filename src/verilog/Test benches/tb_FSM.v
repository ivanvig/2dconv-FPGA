`timescale 1ns / 10ps



module tb_FSM();	
	
	    
	parameter NB_ADDRESS= 10;
	//Para ver mas rapido si llega a completarse
    parameter NB_IMAGE  = 4;
   
	
	//Todo puerto de salida del modulo es un cable.
	//Todo puerto de estímulo o generación de entrada es un registro.
	
	//Definición de puertos
        reg                    CLK;
        reg                    reset;
        reg                    SOP;
        reg  [NB_IMAGE-1:0]    imgLength;
        reg                    valid;
        
        wire [NB_ADDRESS-1:0]  writeAddress;
        wire [NB_ADDRESS-1:0]  readAddress;
        wire                   EOP;
        wire                   chblock;
	
	
	initial	begin
	       
	      
		SOP       = 1'b0;	
		imgLength = 4'b1111;
		valid     = 1'b0;
		reset     = 1'b0;		
		//inicializo clock (si o si)
		CLK       = 1'b0;
		
	    //Emulo arranque de sistema, deberían cargarse los parametros correspondientes
		#5 reset = 1'b1;
		#1 reset  = 1'b0;
			
		//Carga/lectura --> testeo del valid.
		#10 valid = 1'b1;
		#10 valid = 1'b0;
		#10 valid = 1'b1;
		#10 valid = 1'b1;
		#10 valid = 1'b0;
		#10 valid = 1'b0;
		#10 valid = 1'b1;
		
		#35 SOP = 1'b1;
		
		
		#100000000 $finish;
	end
	
	always #2.5 CLK=~CLK;
	
//Módulo para pasarle los estímulos del banco de pruebas.

FSM
	#(  
	    .NB_ADDRESS(NB_ADDRESS),
		.NB_IMAGE (NB_IMAGE)
		)
	u_FSM
		(
		.i_CLK(CLK),
		.i_reset(reset),
		.i_SoP(SOP),
		.i_imgLength(imgLength),
		.i_valid(valid),
		.o_readAdd(readAddress),
		.o_writeAdd(writeAddress),
		.o_EoP(EOP),
		.o_changeBlock(chblock)
		);
endmodule
