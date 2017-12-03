`timescale 1ns / 1ps

`define NB_ADDRESS      10
`define NB_IMAGE        10


module Fsmv#(
    parameter NB_ADDRESS= `NB_ADDRESS,
    parameter NB_IMAGE  = `NB_IMAGE

    )(
    //Definicion de puertos
    output [NB_ADDRESS-1:0]  o_writeAdd,
    output [NB_ADDRESS-1:0]  o_readAdd,
    output                   o_EoP,
    output                   o_changeBlock,
    output                   o_fms2conVld,
    input  [NB_IMAGE-1:0]    i_imgLength,
    input                    i_CLK,
    input                    i_reset,
    input                    i_SoP,
    input                    i_valid
    );
    //Latcheo de salidas 
    reg [NB_ADDRESS-1:0]                     counterAdd;
    reg [NB_ADDRESS-1:0]           counter_with_latency;
    reg [NB_IMAGE-1:0]					      imgHeight;
    reg                                    endOfProcess;
    //registro utulizado para el estado de carga a las memoriras
    reg 								 beginigProcess; 
    reg                                     changeBlock;
    reg                                      sopControl;
    reg                            valid_previous_state;
    reg 							   	     rest_count;
    //registro utilizado para el valid de convolucionador
    reg                                      fms2conVld;
    //Ni bien se crean los registros, toman esos valores.
    initial begin
        counterAdd              = `NB_ADDRESS'd0;
        counter_with_latency    = `NB_ADDRESS'd0;
        imgHeight               = `NB_ADDRESS'd0;
        endOfProcess            = 1'b0;
        changeBlock             = 1'b0;
        sopControl              = 1'b0;
        beginigProcess		    = 1'b0;
        valid_previous_state    = 1'b0;
        rest_count 			    = 1'b0;
        fms2conVld              = 1'b0;
    end        
    
    always @(posedge i_CLK) begin  
      	valid_previous_state<=i_valid;
      	if(i_reset==1'b1)begin
        	counterAdd           <= `NB_ADDRESS'd0;
        	counter_with_latency <= `NB_ADDRESS'd0;
        	endOfProcess         <= 1'b0;
        	changeBlock          <= 1'b0;
        	sopControl           <= 1'b0;
        	beginigProcess		 <= 1'b1;
        	imgHeight			 <= i_imgLength;
        	rest_count 			 <= 1'b0;
            fms2conVld           <= 1'b0;
      	end
      	else begin
            //estado de carga de vaores la memoria o de lectura de la memoria pos convolcion
      		if((endOfProcess==1'b1 || beginigProcess==1'b1)&& sopControl == 1'b0 && rest_count ==1'b0) begin
                fms2conVld <= 1'b0;
                //utlizado para resetear los contadores
                if(rest_count) rest_count <=1'b0;
                else rest_count <=rest_count;

        	  	//Manejo de direcciones en función del valid
        	  	if (i_valid && !valid_previous_state) counterAdd   <= counterAdd+1;
            	else counterAdd   <= counterAdd;
            	
        	  	//Verificación si termino de leer/cargar un bloque
        	  	if (counterAdd==imgHeight)begin
                	changeBlock <= 1'b1;
        	  
        	  		if(endOfProcess ==1'b1) endOfProcess <= 1'b0;
        	  		else if(beginigProcess==1'b1) beginigProcess <= 1'b0;
        	  		else begin
        	  			endOfProcess <= endOfProcess;
        	  			beginigProcess  <= beginigProcess; 
        	  		end 
        	  	end
        	  	else begin
        	  		changeBlock <= changeBlock;
        	  		endOfProcess <= endOfProcess;
        	  		beginigProcess  <= beginigProcess; 
        	  	end 
			end
      		//Levanto registro de control, ya que una vez que arranca a procesar, no para.
       		else if( (sopControl==1'b0) && i_SoP && beginigProcess==1'b0) begin
        		sopControl            <= 1'b1;
            	counter_with_latency  <=`NB_ADDRESS'd0;
            	counterAdd            <= `NB_ADDRESS'd0;
            	endOfProcess 		  <= 1'b0;
            	beginigProcess		  <= 1'b0;
                changeBlock           <= 1'b0;
                fms2conVld            <= 1'b1; // valid a los convolcionadores
       		end
      		//Estado de procesamiento start of process
      		else if(sopControl==1'b1) begin 
            		beginigProcess <= beginigProcess;
                    changeBlock    <= 1'b0;
            		endOfProcess <= endOfProcess ;
                    fms2conVld <= fms2conVld;
            		
                    if(counterAdd != imgHeight)  counterAdd   <= counterAdd+1;
            		else counterAdd   <= counterAdd;

        			//Shifteo para el write address, teniendo en cuenta la latencia.
          			if(counterAdd>=10'h6 && counter_with_latency < imgHeight-2) begin
        	 			counter_with_latency <= counter_with_latency +1;
        	 			sopControl   <= sopControl;
        	 			endOfProcess <= endOfProcess;
        	 			rest_count <= rest_count ;
          			end
                    //si se llega la tamaño de la imagen reseteo los contadores y 
                    //paso al estado de lectura
        	 		else if(counter_with_latency == imgHeight-2)begin 
        	 			sopControl   <= 1'b0;
        	 			endOfProcess <= 1'b1;
        	 			rest_count   <= 1'b1;
        	 			counter_with_latency <= counter_with_latency;
        	 		end
        	 		else begin
        	 			counter_with_latency <= counter_with_latency;
        	 			sopControl   <= sopControl;
        	 			endOfProcess <= endOfProcess;
        	 			rest_count   <= rest_count ;
        	 		end
            end
            else if(rest_count == 1'b1) begin
                //reseto los contadores y bajo el valid.
            	counter_with_latency  <= `NB_ADDRESS'd0;
            	counterAdd            <= `NB_ADDRESS'd0;
            	rest_count            <= 1'b0;
                changeBlock           <= changeBlock;
                fms2conVld            <= 1'b0;
            end
        	else begin
        			imgHeight            <= imgHeight;
            		sopControl           <= sopControl;
            		counter_with_latency <= counter_with_latency;       
       	    		counterAdd           <= counterAdd;
       	    		endOfProcess         <= endOfProcess;
        			changeBlock          <= 1'b0;
        			beginigProcess       <= beginigProcess;
        			rest_count           <= rest_count ;
                    fms2conVld           <= fms2conVld; 	
       		end
        end 
    end 
    //end always   
 
     //Assign          
    assign     {o_writeAdd} =  (sopControl) ? counter_with_latency:counterAdd;//counter_with_latency[NBlatency-1: NBlatency - NB_ADDRESS] : counterAdd;
    assign     {o_readAdd}  =  counterAdd;
    assign          {o_EoP} =  endOfProcess;
    assign  {o_changeBlock} =  changeBlock;
    assign  o_fms2conVld = fms2conVld;

endmodule
