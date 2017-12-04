`timescale 1ns / 1ps

`define BIT_LEN 8
`define CONV_LEN 20
`define CONV_LPOS 13
`define M_LEN 3
`define GPIO_D 32
`define NB_ADDRESS 10

module micro_sim
    #(
      parameter BIT_LEN       = `BIT_LEN,
      parameter CONV_LEN      = `CONV_LEN,
      parameter CONV_LPOS     = `CONV_LPOS,
      parameter M_LEN         = `M_LEN,
      parameter NB_ADDRESS    = `NB_ADDRESS,
      parameter RAM_WIDTH     = 13,
      parameter GPIO_D        = `GPIO_D,
      parameter BITS_DATAIN = 8,
      parameter N = 2,
      parameter BITS_IMAGEN = 11,
      parameter BITS_DATA = BITS_IMAGEN
      )(
        output [GPIO_D-1:0] gpio_i_data_tri_i,
        output              o_led,
        input               CLK100MHZ,
        input [GPIO_D-1:0]  gpio_o_data_tri_o
        );
    
    genvar                  i;
    

    /////////// WIRES AGREGADOS //////////////
    wire [N*BITS_IMAGEN-1:0] conv_DataConv_mcu;
    wire [(N+2)*BITS_IMAGEN-1:0] mem_MemData_mcu;
    wire                         rst, clk;
    
    wire [3*N*BITS_IMAGEN-1:0]   mcu_DataConv_conv;
    wire [BITS_DATA-1:0]         mcu_Data_ctrl;
    wire [N+1:0]                 mcu_we_mem;
    wire [NB_ADDRESS-1:0]        mcu_WAddr_mem, mcu_RAddr_mem;
    wire [(N+2)*BITS_IMAGEN-1:0] mcu_MemData_mem;

    ////////////////////////////////////////////
    
    // REGISTROS MODULOS FALTANTES

    reg  fsm_eop_mcu, fsm_sop_mcu, fsm_chblk_mcu;
    reg [NB_ADDRESS-1:0] fsm_RAddr_mcu, fsm_WAddr_mcu;

    reg                  ctrl_valid_conv, ctrl_ki_conv;
    reg [BITS_DATA-1:0]  ctrl_Data_mcu;

    // Microconotrolador

    wire                 start;
    wire                 next_data;
    reg                  prev;
    reg                  aux;
    
    
    
    
    assign rst = gpio_o_data_tri_o[0]; //primeo en 1 despues en 0 res top y conv
    assign start = gpio_o_data_tri_o[1];
    assign next_data = gpio_o_data_tri_o[2];

    assign gpio_i_data_tri_i[BITS_DATA-1:0] = mcu_Data_ctrl;
    assign gpio_i_data_tri_i[GPIO_D-1:BITS_DATA] = 19'h0;

    

    //asignacion de la finalizacion al led para un udicador visual.
    assign o_led = fsm_eop_mcu;

    initial begin
        fsm_WAddr_mcu    = {NB_ADDRESS{1'b1}};
        fsm_RAddr_mcu   = {NB_ADDRESS{1'b1}};
        fsm_eop_mcu = 1'b1;
        fsm_sop_mcu = 1'b0;
        fsm_chblk_mcu = 1'b0;
        ctrl_valid_conv = 1'b0;
        ctrl_ki_conv = 1'b0;
        ctrl_Data_mcu = {(BITS_DATA/2){2'b01}};
    end
    
    always @(posedge CLK100MHZ ) begin
        if (rst) begin
            // reset
            fsm_RAddr_mcu    <= {NB_ADDRESS{1'b0}};
            fsm_WAddr_mcu    <= {NB_ADDRESS{1'b0}};
            fsm_eop_mcu <= 1'b1;
            fsm_sop_mcu <= 1'b0;
            fsm_chblk_mcu <= 1'b0;
            ctrl_valid_conv <= 1'b0;
            ctrl_ki_conv <= 1'b0;
            ctrl_Data_mcu <= {(BITS_DATA/2){2'b01}};
        end else begin
            
            prev <= next_data;
            aux <= start;

            if ((start && !aux) || fsm_sop_mcu) begin
                fsm_sop_mcu <= 1'b1;
                fsm_eop_mcu <= 1'b0;
                ctrl_valid_conv <= 1'b1;
                
                
                fsm_RAddr_mcu <= fsm_RAddr_mcu + 1;
                fsm_WAddr_mcu <= (fsm_RAddr_mcu < 3) ? {NB_ADDRESS{1'b0}} : fsm_WAddr_mcu + 1; // Cambiar numero segun latencia
                
                if (fsm_RAddr_mcu == {NB_ADDRESS{1'b1}}) begin
                    ctrl_valid_conv <= 1'b0;
                    fsm_sop_mcu <= 1'b0;
                    fsm_eop_mcu <= 1'b1;
                end
            end else if((next_data && !prev) && fsm_eop_mcu) begin // if (start || fsm_sop_mcu)
                fsm_RAddr_mcu <= fsm_WAddr_mcu + 1;
            end else begin
                fsm_WAddr_mcu <= {NB_ADDRESS{1'b0}};
                fsm_RAddr_mcu <= {NB_ADDRESS{1'b0}};
                ctrl_valid_conv <= 1'b0;
            end
        end
    end
    
    // instacia del Microcontrolador
   //inacia de Convolucionador
    generate
        for (i = 0; i < N; i = i+1) begin : gen_conv
            Conv u_conv
                 (.o_data(conv_DataConv_mcu[(i+1)*BITS_DATA-1 -: BITS_DATA]),
                  .i_dato0(mcu_DataConv_conv[(i+1)*BITS_IMAGEN-1 -: BITS_DATAIN]),
                  .i_dato1(mcu_DataConv_conv[(i+2)*BITS_IMAGEN-1 -: BITS_DATAIN]),
                  .i_dato2(mcu_DataConv_conv[(i+3)*BITS_IMAGEN-1 -: BITS_DATAIN]),
                  .i_selecK_I(ctrl_ki_conv),
                  .i_reset(rst),
                  .i_valid(ctrl_valid_conv),
                  .CLK100MHZ(CLK100MHZ)
                  );
        end
    endgenerate
    
    
    //instancia MCU
    MCU
        u_MemCU
            (
             .i_DataConv(conv_DataConv_mcu),
             .i_Data(ctrl_Data_mcu),
             .i_MemData(mem_MemData_mcu),
             .i_WAddr(fsm_WAddr_mcu),
             .i_RAddr(fsm_WAddr_mcu),
             .i_chblk(fsm_chblk_mcu),
             .i_sop(fsm_sop_mcu),
             .i_eop(fsm_eop_mcu),
             .rst(rst),
             .clk(CLK100MHZ),

             .o_DataConv(mcu_DataConv_conv),
             .o_Data(mcu_Data_ctrl),
             .o_we(mcu_we_mem),
             .o_WAddr(mcu_WAddr_mem),
             .o_RAddr(mcu_RAddr_mem),
             .o_MemData(mcu_MemData_mem)
             );


    //intancia de la memoria

    
    generate
        for (i = 0; i < (N+2); i = i+1) begin : gen_memory
            memory u_mem
                 (
                  .i_wrEnable(mcu_we_mem[i]),
                  .i_CLK(CLK100MHZ),
                  .i_writeAdd(mcu_WAddr_mem),
                  .i_readAdd(mcu_RAddr_mem),
                  .i_data(mcu_MemData_mem),
                  
                  .o_data(mem_MemData_mcu[(i+1)*BITS_DATA-1 -: BITS_DATA])
                  );
            
        end
        
    endgenerate
                

endmodule
