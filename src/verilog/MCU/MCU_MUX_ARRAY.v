module MUX_ARRAY
    #(
      parameter N = 2,
      parameter BITS_IMAGEN = 11,
      parameter BITS_DATA = BITS_IMAGEN,
      parameter STATES = 3
      )(
        input [N*BITS_IMAGEN-1:0]      i_DataConv,
        input [(N+2)*BITS_IMAGEN-1:0]  i_MemData,
        input [BITS_DATA-1:0]          i_Data,

        input [$clog2(STATES)-1:0]     i_state,
        input [$clog2(N/2 + 1):0]      i_substate, //PARA N PAR
        input [$clog2(N+2)-1:0]        i_memSelect,
        //input                          i_inputCtrl,
		    //input [$clog2(N/2 + 1)-1:0]    i_memCtrl, //Para N par
		    //input                          i_convCtrl,
        //CONFIGURAR BIEN LAS SELECTORAS
        output reg [3*N*BITS_IMAGEN-1:0]   o_DataConv,
        output reg [(N+2)*BITS_IMAGEN-1:0] o_MemData,
        output reg [BITS_DATA-1:0]         o_Data
    );
    
    wire [N*BITS_IMAGEN-1:0]           tomemory;

    always @ (*) begin
        case (i_state)
            2'b00: begin//LOAD
                o_Data = 0;
                o_DataConv = 0;
                case (i_memSelect) 
                    2'b00: o_MemData = i_Data;
                    2'b01: o_MemData = {i_Data, {1*BITS_IMAGEN{1'b0}}};
                    2'b10: o_MemData = {i_Data, {2*BITS_IMAGEN{1'b0}}};
                    2'b11: o_MemData = {i_Data, {3*BITS_IMAGEN{1'b0}}};
                endcase
            end

            2'b01: begin //PROCESAMIENTO
                o_Data = 0;
                case (i_substate) 
                    1'b0: begin
                        o_DataConv[3*BITS_IMAGEN-1:0] = i_MemData[3*BITS_IMAGEN-1:0];
                        o_DataConv[6*BITS_IMAGEN-1:3*BITS_IMAGEN] = i_MemData[4*BITS_IMAGEN-1:BITS_IMAGEN];
                        o_MemData = i_DataConv;
                    end
                    1'b1: begin
                        o_DataConv[3*BITS_IMAGEN-1:0] = {i_MemData[BITS_IMAGEN-1:0],i_MemData[4*BITS_IMAGEN-1:2*BITS_IMAGEN]};
                        o_DataConv[6*BITS_IMAGEN-1:3*BITS_IMAGEN] = {i_MemData[2*BITS_IMAGEN-1:0] ,i_MemData[4*BITS_IMAGEN-1:3*BITS_IMAGEN]};
                        o_MemData = {i_DataConv, {2*BITS_IMAGEN{1'b0}}};
                    end
                endcase
            end

            2'b10: begin//OUT
                o_MemData = 0;
                o_DataConv = 0;
                
                case (i_memSelect)
                    2'b00: o_Data = i_MemData[BITS_IMAGEN-1:0];
                    2'b01: o_Data = i_MemData[2*BITS_IMAGEN-1:BITS_IMAGEN];
                    2'b10: o_Data = i_MemData[3*BITS_IMAGEN-1:2*BITS_IMAGEN];
                    2'b11: o_Data = i_MemData[4*BITS_IMAGEN-1:3*BITS_IMAGEN];
                endcase
                //o_Data = i_MemData[(1+i_memSelect)*BITS_IMAGEN-1:i_memSelect*BITS_IMAGEN];
            end

            default: begin
                o_MemData = 0;
                o_DataConv = 0;
                o_Data = 0;
            end
        endcase
    end
endmodule
