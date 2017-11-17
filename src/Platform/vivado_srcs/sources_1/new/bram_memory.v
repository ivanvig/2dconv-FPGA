`timescale 1ns / 1ps

`define NB_ADDRESS 10
`define RAM_WIDTH 8


module bram_memory( i_wrEnable, i_CLK, i_writeAdd, i_readAdd, i_data, o_data, o_led);

parameter RAM_WIDTH = `RAM_WIDTH;    
parameter NB_ADDRESS= `NB_ADDRESS;
localparam RAM_DEPTH=(2**NB_ADDRESS)-1;


//Definición de puertos
input                    i_wrEnable;
input                    i_CLK;
input  [NB_ADDRESS-1:0]  i_writeAdd;
input  [NB_ADDRESS-1:0]  i_readAdd;
input  [RAM_WIDTH - 1:0] i_data;

output [RAM_WIDTH-1:0]   o_data;
output           [3:0]   o_led;


reg           [1:0] go_to_leds;
reg [RAM_WIDTH-1:0] BRAM [RAM_DEPTH:0];
reg [RAM_WIDTH-1:0] dout_reg;
integer ram_index;

initial 
	for (ram_index = 0; ram_index <= RAM_DEPTH; ram_index = ram_index + 1)
		BRAM[ram_index] = {RAM_WIDTH{1'b1}};
		
		

always @(posedge i_CLK) begin
	dout_reg<=BRAM[i_readAdd];	
	if(i_wrEnable) begin			
			BRAM[i_writeAdd]<=i_data;
	end	
	
end
 
assign{o_data}= dout_reg;
assign {o_led[3:2]}= go_to_leds; 
  
endmodule

