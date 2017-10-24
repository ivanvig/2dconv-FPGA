module tb_MUX_ARRAY();

    parameter N_CONV = 2;
    parameter BITS_IMAGEN = 8;
    
    reg [N_CONV*BITS_IMAGEN-1:0] i_DataConv;
    reg [(N_CONV+2)*BITS_IMAGEN-1:0]  i_MemData;
    reg [23:0]                   Data_in;
    reg                          inputCtrl, memCtrl, convCtrl;
    
    wire [3*N_CONV*BITS_IMAGEN-1:0] o_DataConv;
    wire [(N_CONV+2)*BITS_IMAGEN-1:0] o_MemData;
    wire [3*BITS_IMAGEN-1:0]        Data_out;


    initial begin

        Data_in    = {12'b1, 12'b0};
        i_MemData    = {8'b0, 8'b1, 8'b0, 8'b1};
        i_DataConv = 16'b1;

        inputCtrl = 0;
        memCtrl   = 0;
        convCtrl  = 0;

        #100 memCtrl = 1;
        #200 memCtrl = 0;
        #200 inputCtrl = 1;
        #300 convCtrl = 1;
        #300 memCtrl = 1;
        #500 $finish;

    end

    MUX_ARRAY
        #(
          .N(N_CONV),
          .BITS_IMAGEN(BITS_IMAGEN)
          )

    u_MUX_ARRAY
        (
         .i_DataConv(i_DataConv),
         .i_MemData(i_MemData),
         .i_Data(Data_in),
         .i_inputCtrl(inputCtrl),
         .i_memCtrl(memCtrl),
         .i_convCtrl(convCtrl),
         .o_DataConv(o_DataConv),
         .o_MemData(o_MemData),
         .o_Data(Data_out)
         );
endmodule
