`timescale 1ns / 1ps

`define NB_ADDRESS      10
`define NB_IMAGE        10
`define NB_STATES       2

module Fsmv#(
    parameter NB_ADDRESS= `NB_ADDRESS,
    parameter NB_IMAGE  = `NB_IMAGE,
    parameter NB_STATES = `NB_STATES

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
    input                    i_valid,
    input                    i_load
    );
    //Latcheo de salidas 
    reg [NB_ADDRESS-1:0]                     counterAdd;
    reg [NB_ADDRESS-1:0]           counter_with_latency;
    reg [NB_IMAGE-1:0]					      imgHeight;
    reg                                    endOfProcess;
    //registro utulizado para el estado de carga a las memoriras
    reg                                   beginigProcess; 
    reg                                     changeBlock;
    reg                                      sopControl;
    reg                            valid_previous_state;
    //registro utilizado para el valid de convolucionador
    reg                                      fms2conVld;
    //Ni bien se crean los registros, toman esos valores.
    reg [NB_STATES-1:0]  states;

    initial begin
        counterAdd              = `NB_ADDRESS'd0;
        counter_with_latency    = `NB_ADDRESS'd0;
        imgHeight               = `NB_ADDRESS'd0;
        endOfProcess            = 1'b0;
        changeBlock             = 1'b0;
        sopControl              = 1'b0;
        beginigProcess		    = 1'b0;
        valid_previous_state    = 1'b0;
        fms2conVld              = 1'b0;
        states                  = `NB_STATES'd0;
    end        
    
    always @(posedge i_CLK) begin  
      	valid_previous_state<=i_valid;
      	if(i_reset==1'b1)begin
        	counterAdd           <= `NB_ADDRESS'd0;
        	counter_with_latency <= `NB_ADDRESS'd0;
        	endOfProcess         <= 1'b0;
        	changeBlock          <= 1'b0;
        	sopControl           <= 1'b0;
        	beginigProcess		 <= 1'b0;
        	imgHeight			 <= i_imgLength;
            fms2conVld           <= 1'b0;
            states               <= `NB_STATES'd0;
      	end
      	else begin
            imgHeight <= imgHeight;
            if(states == 2'b00) begin
                counter_with_latency  <= `NB_ADDRESS'd0;
                counterAdd            <= `NB_ADDRESS'd0;
                changeBlock           <= 1'b0;
                imgHeight             <= imgHeight;
                if(i_load && ~i_SoP && ~endOfProcess) begin
                    //estado de carga
                    states          <= 2'b01;
                    beginigProcess  <= 1'b1;
                    sopControl      <= 1'b0;
                    fms2conVld      <= 1'b0;
                end
                else if(~i_load  && i_SoP && ~endOfProcess) begin
                    //estado de procesamiento
                    states <= 2'b10;
                    beginigProcess  <= 1'b0;
                    sopControl      <= 1'b1;
                    fms2conVld      <= 1'b1;
                end
                else if(~i_load && ~i_SoP && endOfProcess)begin
                    //estado de lectura
                    states          <= 2'b01;
                    beginigProcess  <= 1'b0;
                    sopControl      <= 1'b0;
                    fms2conVld      <= 1'b0;
                end
                else begin
                    states          <= states;
                    beginigProcess  <= 1'b0;
                    sopControl      <= 1'b0;
                    fms2conVld      <= 1'b0;
                end
            end
            else if(states == 2'b01)begin
                //Manejo de direcciones en función del valid
                if (i_valid && !valid_previous_state) counterAdd <= counterAdd+1;
                else counterAdd   <= counterAdd;
                
                //Verificación si termino de leer/cargar un bloque
                if (counterAdd==imgHeight)begin
                    if(~i_load)begin
                        changeBlock <= 1'b1;
                        states      <= 2'b00;
                    end
                    else begin
                        changeBlock <= changeBlock;
                        states      <= states;
                    end
                    if(endOfProcess == 1'b1) endOfProcess <= 1'b0;
                    else if(beginigProcess>=2'b01) beginigProcess <= 1'b0;
                    else begin
                        endOfProcess      <= endOfProcess;
                        beginigProcess    <= beginigProcess; 
                    end 
                end
                else begin
                    changeBlock     <= changeBlock;
                    endOfProcess    <= endOfProcess;
                    beginigProcess  <= beginigProcess;
                    states          <= states; 
                end 
            end
            else if(states == 2'b10) begin
                beginigProcess <= beginigProcess;
                if(counterAdd != imgHeight)  counterAdd   <= counterAdd+1;
                else counterAdd   <= counterAdd;

                //Shifteo para el write address, teniendo en cuenta la latencia.
                if(counterAdd>=10'h6 && counter_with_latency < imgHeight-2) begin
                    counter_with_latency    <= counter_with_latency +1;
                    fms2conVld              <= fms2conVld;
                    endOfProcess            <= endOfProcess;
                    states                  <= states; 
                end
                else if(counter_with_latency == imgHeight-2)begin 
                    //si se llega la tamaño de la imagen reseteo los contadores 
                    counter_with_latency    <= counter_with_latency;
                    fms2conVld              <= 1'b0;
                    
                    if (~i_SoP) begin
                        endOfProcess    <= 1'b1;
                        states          <= 2'b00;
                        sopControl      <= 1'b0;
                    end
                    else begin
                        endOfProcess    <= endOfProcess;
                        states          <= states;
                        sopControl      <= sopControl;
                    end
                end
                else begin
                    counter_with_latency    <= counter_with_latency;
                    sopControl              <= sopControl;
                    endOfProcess            <= endOfProcess;
                    fms2conVld              <= fms2conVld;
                    states                  <= states; 
                    end
            end
        	else begin
            		sopControl           <= sopControl;
            		counter_with_latency <= counter_with_latency;       
       	    		counterAdd           <= counterAdd;
       	    		endOfProcess         <= endOfProcess;
        			changeBlock          <= 1'b0;
        			beginigProcess       <= beginigProcess;
                    fms2conVld           <= fms2conVld; 	
       		end
        end 
    end 
    //end always   
 
     //Assign          
    assign     {o_writeAdd} =  (sopControl) ? counter_with_latency:counterAdd;//counterAdd;
    assign     {o_readAdd}  =  counterAdd;
    assign          {o_EoP} =  endOfProcess;
    assign  {o_changeBlock} =  changeBlock;
    assign  o_fms2conVld    = fms2conVld;

endmodule
