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
    wire [BITS_DATA-1:0]     ctrl_Data_mcu;
    wire [(N+2)*BITS_IMAGEN-1:0] mem_MemData_mcu;
    wire [NB_ADDRESS-1:0]         fsm_WAddr_mcu, fsm_RAddr_mcu;
    wire                         fsm_chblk_mcu, fsm_sop_mcu, fsm_eop_mcu, rst, clk;
    
    wire [3*N*BITS_IMAGEN-1:0]  mcu_DataConv_conv;
    wire [BITS_DATA-1:0]        mcu_Data_ctrl;
    wire [N+1:0]                mcu_we_mem;
    wire [NB_ADDRESS-1:0]        mcu_WAddr_mem, mcu_RAddr_mem;
    wire [(N+2)*BITS_IMAGEN-1:0] mcu_MemData_mem;

    ////////////////////////////////////////////
    
    wire k_i; //selector de K/I
    wire valid;
    wire dato0, dato1, dato2;
    

    // Microconotrolador
    
    assign rst      = gpio_o_data_tri_o[0]; //primeo en 1 despues en 0 res top y conv
    assign k_i      = gpio_o_data_tri_o[1]; //K/I en 1 para la conv
    assign valid    = gpio_o_data_tri_o[2]; //en 1 para la conv
        

    //asignacion de la salida del convolucionador a la primera memoria 
    assign i_mem0 = reg_aux;
    // asignacon de la direccion de lectura de un registro local o del gpio
    assign read_address_MEM = (rstm==1'b0)?gpio_o_data_tri_o[NB_ADDRESS+7:8]:read_add;
    // asignacion de la direccion de escritura de un registro local
    assign write_address_MEM = write_add;
    // asignacion de la salida de la memoria 0 al micro
    assign gpio_i_data_tri_i[RAM_WIDTH-1:0] = mem0_o;
    assign gpio_i_data_tri_i[GPIO_D-1:RAM_WIDTH] = 19'h0;
    //asignacion de la finalizacion al led para un udicador visual.
    assign o_led = ~ending;

    initial begin
        dmicro0     = 13'h0;
        dmicro1     = 13'h0;
        dmicro2     = 13'h0;
        read_add    = {NB_ADDRESS{1'b1}};
        write_add   = {NB_ADDRESS{1'b1}};
        ending      = 1'b1;
        i_data_mem1 = 13'h0;
        i_data_mem2 = 13'h0;
    end

    always @(posedge CLK100MHZ ) begin
        if (rst) begin
            // reset
            read_add    <= 10'h0;//{NB_ADDRESS{1'b1}};
            write_add   <= 10'h0;//10'h3fa;
            ending      <= 1'b1;
            dmicro0     <= 8'h94;
            dmicro1     <= 8'h0;
            dmicro2     <= 8'h0;
            i_data_mem1 <= 13'h0;
            i_data_mem2 <= 13'h0;
            reg_aux     <= {RAM_WIDTH{1'b0}};
        end
        else if (valid==1'b1 && ending==1'b1) begin
            dmicro0     <= dmicro0;
            dmicro1     <= dmicro1;
            dmicro2     <= dmicro2;
            reg_aux     <= data_oc;
            read_add    <= read_add +1;
            if (read_add >= 10'h6 && read_add <= 10'h25)
                write_add   <= write_add +1;
            else write_add   <= write_add;

            if(read_add == 10'h25) ending <=0;           
            else ending <= ending;
        end
        else begin
            read_add    <= read_add;
            write_add   <= write_add;
            ending      <= ending;
            i_data_mem1 <= i_data_mem1;
            i_data_mem2 <= i_data_mem2;
            dmicro0     <= dmicro0;
            dmicro1     <= dmicro1;
            dmicro2     <= dmicro2;
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
                  .i_selecK_I(k_i),
                  .i_reset(rst),
                  .i_valid(valid),
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
