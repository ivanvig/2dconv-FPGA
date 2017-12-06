module MUX_ARRAY
    #(
      parameter N = 2,
      parameter BITS_IMAGEN = 8,
      parameter BITS_DATA = 13,
      parameter STATES = 3
      )(
        input [N*BITS_DATA-1:0]          i_DataConv,
        input [(N+2)*BITS_DATA-1:0]      i_MemData,
        input [BITS_IMAGEN-1:0]          i_Data,

        input [clog2(STATES-1)-1:0]      i_state,
        input [clog2(N/2) - 1:0]         i_substate, //PARA N PAR
        input [clog2(N+1)-1:0]           i_memSelect, //Elige memoria para escribir / leer
        output [N*3*BITS_IMAGEN-1:0]     o_DataConv,
        //output reg [3*N*BITS_IMAGEN-1:0] o_DataConv,
        output reg [(N+2)*BITS_DATA-1:0] o_MemData,
        output reg [BITS_DATA-1:0]       o_Data
    );
    
    integer                              i, j, mem_ptr, mem_ptr1;
    reg [3*BITS_IMAGEN-1:0]              DataConv [0:N-1];
    reg [(N+2)*BITS_DATA-1:0]            zeros_DataConv;

    genvar                               x;

    generate
        for (x = 0; x < N; x = x + 1)
            assign o_DataConv[3*BITS_IMAGEN*(x+1)-1 -: 3*BITS_IMAGEN] = DataConv[x];
    endgenerate

    always @ (*) begin
        zeros_DataConv = {{2*BITS_DATA{1'b0}}, i_DataConv};
        case (i_state)
            2'b00: begin//LOAD
                o_Data = {BITS_DATA{1'b0}};
                //DataConv = {(3*N*BITS_IMAGEN){1'b0}};
                for (i = 0; i < N; i = i + 1)
                    DataConv[i] = {3*BITS_IMAGEN{1'b0}};

                for (i = 0; i < (N+2); i = i + 1) begin
                    if (i == i_memSelect)
                        o_MemData[BITS_DATA*(i+1)-1 -: BITS_DATA] = {{(BITS_DATA-BITS_IMAGEN){1'b0}}, i_Data};
                    else
                        o_MemData[BITS_DATA*(i+1)-1 -: BITS_DATA] = {BITS_DATA{1'b0}};
                end
                
                /*case (i_memSelect) 
                    2'b00: o_MemData = i_Data;
                    2'b01: o_MemData = {i_Data, {1*BITS_IMAGEN{1'b0}}};
                    2'b10: o_MemData = {i_Data, {2*BITS_IMAGEN{1'b0}}};
                    2'b11: o_MemData = {i_Data, {3*BITS_IMAGEN{1'b0}}};
                endcase*/
            end

            2'b01: begin //PROCESAMIENTO
                o_Data = {BITS_DATA{1'b0}};

                for (i = 0; i < N+2; i = i+1) begin
                    mem_ptr1 = i_substate*N+i;
                    if (mem_ptr1 > N + 1)
                        //mem_ptr = mem_ptr - (N + 2);
                        o_MemData[BITS_DATA*(i+1)-1 -: BITS_DATA] = zeros_DataConv[(mem_ptr1-N-1)*BITS_DATA-1 -: BITS_DATA];
                    else
                        o_MemData[BITS_DATA*(i+1)-1 -: BITS_DATA] = zeros_DataConv[(mem_ptr1+1)*BITS_DATA-1 -: BITS_DATA];
                end
                
                for (i = 0; i < N; i = i + 1) begin : asd

                    //mem_ptr = ((i_substate*N+i+1) > N+1) ? i_substate*N+i+1 : i_substate*N+i+j - (N+2);

                    //o_MemData[BITS_DATA*(i+1)-1 -: BITS_DATA] = zeros_DataConv[mem_ptr*BITS_DATA-1 -: BITS_DATA];

                    for (j = 0; j < 3; j = j + 1) begin : asd1
                        mem_ptr = i_substate*N + i + j;
                        if (mem_ptr > N+1)
                            DataConv[i][BITS_IMAGEN*(j+1)-1 -: BITS_IMAGEN] = i_MemData[BITS_DATA*(mem_ptr-N-2)+BITS_IMAGEN-1 -: BITS_IMAGEN];
                        else
                            DataConv[i][BITS_IMAGEN*(j+1)-1 -: BITS_IMAGEN] = i_MemData[BITS_DATA*mem_ptr+BITS_IMAGEN-1 -: BITS_IMAGEN];
                            //mem_ptr = mem_ptr - N + 2;
                        //mem_ptr = ((i_substate*N+i+j) > N+1) ? i_substate*N+i+j : i_substate*N+i+j - (N+2);
                        //DataConv[i][BITS_IMAGEN*(j+1)-1 -: BITS_IMAGEN] = i_MemData[BITS_DATA*mem_ptr+BITS_IMAGEN-1 -: BITS_IMAGEN];
                    end
                end
                
                
                /*
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
                endcase*/
            end

            2'b10: begin//OUT
                o_MemData = {(N+2)*BITS_DATA{1'b0}};
                for (i = 0; i < N; i = i + 1)
                    DataConv[i] = {3*BITS_IMAGEN{1'b0}};

                o_Data = i_MemData[BITS_DATA*(i_memSelect+1)-1 -: BITS_DATA];
                
                /*case (i_memSelect)
                    2'b00: o_Data = i_MemData[BITS_IMAGEN-1:0];
                    2'b01: o_Data = i_MemData[2*BITS_IMAGEN-1:BITS_IMAGEN];
                    2'b10: o_Data = i_MemData[3*BITS_IMAGEN-1:2*BITS_IMAGEN];
                    2'b11: o_Data = i_MemData[4*BITS_IMAGEN-1:3*BITS_IMAGEN];
                endcase*/
                //o_Data = i_MemData[(1+i_memSelect)*BITS_IMAGEN-1:i_memSelect*BITS_IMAGEN];
            end

            default: begin
                o_MemData = {(N+2)*BITS_DATA{1'b0}};
                o_Data = {BITS_DATA{1'b0}};
                for (i = 0; i < N; i = i + 1)
                    DataConv[i] = {3*BITS_IMAGEN{1'b0}};
            end
        endcase
    end

    function integer clog2;
        input integer depth;
        for (clog2=0; depth>0; clog2=clog2+1)
            depth = depth >> 1;
    endfunction

endmodule
