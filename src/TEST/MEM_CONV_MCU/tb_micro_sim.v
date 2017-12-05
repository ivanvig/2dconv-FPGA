module micro_sim_tb();
    
      parameter GPIO_D        = `GPIO_D;
    

    
    wire [GPIO_D-1:0] gpio_i_data_tri_i;
    wire              o_led;
    reg               CLK100MHZ;
    reg [GPIO_D-1:0]  gpio_o_data_tri_o;

    initial begin
        gpio_o_data_tri_o = {GPIO_D{1'b0}};

        CLK100MHZ = 1'b0;

        #10 gpio_o_data_tri_o[0] = 1'b1;
        #10 gpio_o_data_tri_o[0] = 1'b0;

        #20 gpio_o_data_tri_o[1] = 1'b1;
        #10 gpio_o_data_tri_o[1] = 1'b0;

        #3000 gpio_o_data_tri_o[2] = 1'b1;
        #10 gpio_o_data_tri_o[2] = 1'b0;

        #10 gpio_o_data_tri_o[2] = 1'b1;
        #10 gpio_o_data_tri_o[2] = 1'b0;
        
        #10 gpio_o_data_tri_o[2] = 1'b1;
        #10 gpio_o_data_tri_o[2] = 1'b0;

        #10 gpio_o_data_tri_o[2] = 1'b1;
        #10 gpio_o_data_tri_o[2] = 1'b0;
    end

    always #2 CLK100MHZ = ~CLK100MHZ;

    micro_sim
        (
         .gpio_o_data_tri_o(gpio_o_data_tri_o),
         .gpio_i_data_tri_i(gpio_i_data_tri_i),
         .o_led(o_led),
         .CLK100MHZ(CLK100MHZ)
         );
    

endmodule
