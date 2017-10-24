 module MUX_ARRAY #(
        parameter N = 2,
        parameter BITS_IMAGEN = 8
    )(
        input [N*BITS_IMAGEN-1:0]      i_DataConv,
        input [(N+2)*BITS_IMAGEN-1:0]  i_MemData,
        input [23:0]                   i_Data,

        input                          i_inputCtrl,
		    input                          i_memCtrl,
		    input                          i_convCtrl,
        //CONFIGURAR BIEN LAS SELECTORAS
        output [3*N*BITS_IMAGEN-1:0]   o_DataConv,
        output [(N+2)*BITS_IMAGEN-1:0] o_MemData,
        output [3*BITS_IMAGEN-1:0]     o_Data     //Revisar esto
    );

    wire	[N*8-1:0]	tomemory;

    assign o_DataConv[23:0] = i_convCtrl ? {i_MemData[7:0],i_MemData[31:16]} : i_MemData[23:0];
    assign o_DataConv[47:24] = i_convCtrl ? {i_MemData[15:0],i_MemData[31:24]} : i_MemData[31:8];

    assign tomemory	= i_inputCtrl ? i_DataConv : i_Data[15:0];

	  assign o_MemData[15:0] 	= i_memCtrl ? 16'b0 : tomemory;
	  assign o_MemData[31:16] = i_memCtrl ? tomemory : 16'b0;


    assign o_Data[15:0] = i_memCtrl ? i_MemData[31:16] : i_MemData[15:0];
    assign o_Data[23:16] = 8'b0;
/*

ASDASD
    always@(*) begin

    	//SALIDAS A LA MEMORIA
        case (i_inputCtrl)
        	1'b0 : assign tomemory	= i_Data[15:0];
        	1'b1 : assign tomemory = i_DataConv;
        endcase

        case (i_memCtrl)
        	1'b0 : begin
        		assign o_MemData[15:0] 	= tomemory;
        		assign o_MemData[31:16] = 16'h0;
        	end
        	1'b1 : begin
        		assign o_MemData[15:0] 	= 16'h0;
        		assign o_MemData[31:16] = tomemory;
        	end
        endcase

        //SALIDAS AL CONV
        case(i_convCtrl)
        	1'b0 : begin
        		assign o_DataConv[23:0]	 = i_MemData[23:0];
        		assign o_DataConv[47:24] = i_MemData[31:8];
        	end
        	1'b1 : begin
        		assign o_DataConv[23:0] = {i_MemData[7:0],i_MemData[31:16]};
        		assign o_DataConv[47:24] = {i_MemData[15:0],i_MemData[31:24]};
        		end
        endcase
    
    end*/

endmodule
