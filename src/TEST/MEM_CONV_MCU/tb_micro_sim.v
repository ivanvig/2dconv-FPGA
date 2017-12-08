`define GPIO_D 32

module micro_sim_tb();
    
      parameter GPIO_D        = `GPIO_D;
    

    
    wire [GPIO_D-1:0] gpio_i_data_tri_i;
    wire              o_led;
    reg               CLK100MHZ;
    wire [GPIO_D-1:0] gpio_o_data_tri_o;


    reg [23:0]       i_GPIOdata;
    reg [2:0]        i_GPIOctrl;
    reg              i_GPIOvalid;
    reg              rst;

    integer           i;

    assign gpio_o_data_tri_o = {i_GPIOctrl,i_GPIOvalid, 3'b0, i_GPIOdata, rst};
    
    initial begin

        CLK100MHZ = 1'b0;
        i_GPIOdata = 24'b0;
        i_GPIOctrl = 3'b0;
        i_GPIOvalid = 1'b0;
        rst = 1'b0;

        //RESET
        #100 rst = 1'b1;
        #100 rst = 1'b0;

        //CARGO KERNEL
        #200 i_GPIOctrl = 3'b000;

        i_GPIOdata = 24'h000;
        #100 i_GPIOvalid = 1'b1;
        #100 i_GPIOvalid = 1'b0;
        
        #100 i_GPIOdata = 24'h010;
        #100 i_GPIOvalid = 1'b1;
        #100 i_GPIOvalid = 1'b0;

        #100 i_GPIOdata = 24'h000;
        #100 i_GPIOvalid = 1'b1;
        #100 i_GPIOvalid = 1'b0;

        //CARGO IMAGE LENGTH
        #500 i_GPIOctrl = 3'b001;
        i_GPIOdata = 24'h00A;
        
        //CARGO IMAGEN EN MEMORIA
        #500 i_GPIOctrl = 3'b010;
        for (i = 0; i < 4*10-1; i = i+1) begin
            #100 i_GPIOdata = i;
            #100 i_GPIOvalid = 1'b1;
            #100 i_GPIOvalid = 1'b0;
        end

        #100 i_GPIOctrl = 100; //ultimo dato a cargar
        i_GPIOdata = 24'h27; //39 en hexa (ultimo dato)
        #100 i_GPIOvalid = 1'b1; //arranco procesamiento
        #100 i_GPIOvalid = 1'b0;

        
        //PIDO DATOS
        #3000 i_GPIOctrl = 011;
        for (i = 0; i < 4*10; i = i+1) begin
            #100 i_GPIOvalid = 1'b1;
            #100 i_GPIOvalid = 1'b0;
        end
        $finish;
        
    end

    always #2 CLK100MHZ = ~CLK100MHZ;

    micro_sim
        u_micro
            (
             .gpio_o_data_tri_o(gpio_o_data_tri_o),
             .gpio_i_data_tri_i(gpio_i_data_tri_i),
             .o_led(o_led),
             .CLK100MHZ(CLK100MHZ)
             );
    

endmodule
