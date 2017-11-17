`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: Casabella Martín
// 
// Create Date: 09/27/2016 04:45:38 PM
// Design Name: 
// Module Name: top_instancia_microNuevo
// Project Name: BRAM_CASABELLA
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module top_microblaze
    (
        input           	 CLK,
        input 	[3:0]        sw,
        input 	[3:0]        btn,
        output 	[3:0]        o_led,
        output          	 uart_rxd_out,
        input           	 uart_txd_in 
    );
        
        
        
        wire [31:0]gpio_i_data_tri_i;
        wire [31:0]gpio_o_data_tri_o;
        wire reset;
        wire sys_clock;
        wire uart_rtl_rxd;
        wire uart_rtl_txd;
        
        
        
        //Senales nuevas
        wire led_warning;
        wire [1:0]led_mem;
        wire valid;
        wire writeEnable;
        wire reset_sw;
        wire [9:0] i_write_address_MEM;
        wire [9:0] i_read_address_MEM;
        wire clock1;
        wire clock2;
        wire  [7:0]  memoryData;
        
               
        
        
        
    ///Prueba asignacion de datos fijos
     assign memoryData = 8'b00111100;
    
        
        //Assigns:
        assign  reset                = sw[0];
        assign  sys_clock            = CLK;
        assign  uart_rtl_rxd         = uart_txd_in;
        assign  uart_rxd_out         = uart_rtl_txd;
        assign  reset_sw             = gpio_o_data_tri_o[0];
        assign  valid                = gpio_o_data_tri_o[1];
        assign  writeEnable          = gpio_o_data_tri_o[2];        
        assign  i_write_address_MEM  = gpio_o_data_tri_o[12:3];
        assign  i_read_address_MEM   = gpio_o_data_tri_o[23:13];
        assign  o_led[3:2]           = led_mem;
        assign  o_led[0]             = led_warning;
        
        
        
        

//MICRO NUEVO
  design_1
        u_MCU
           (.clock100(clock2),
            .gpio_rtl_tri_i(gpio_i_data_tri_i),
            .gpio_rtl_tri_o(gpio_o_data_tri_o),
            .o_lock_clock(led_warning),
            .reset(reset),
            .sys_clock(sys_clock),
            .usb_uart_rxd(uart_rtl_rxd),
            .usb_uart_txd(uart_rtl_txd)
            );
    
                    
    //memory instances
        bram_memory
        u_bram_1
          
           ( .i_wrEnable(writeEnable),
            .i_data(memoryData),
            .i_writeAdd(i_write_address_MEM),
            .i_readAdd(i_read_address_MEM),
            .i_CLK(clock2),
            .o_data(gpio_i_data_tri_i[7:0]),
            .o_led(led_mem)
            );
            
        /*    clk_wiz_0
                 u_clk_wiz 
                 (
                  .clk_out1(clock1),
                  .clk_out2(clock2),
                  .resetn(reset),
                  .locked(led_warning),
                  .clk_in1(sys_clock)
                 );
        */


endmodule
