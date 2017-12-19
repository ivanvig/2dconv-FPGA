`timescale 1ns / 1ps

`define BIT_LEN 8
`define CONV_LEN 20
`define CONV_LPOS 13
`define M_LEN 3
`define GPIO_D 32
`define NB_ADDRESS 10

module ControlBlock#(
    parameter BIT_LEN       = `BIT_LEN,
    parameter GPIO_D        = `GPIO_D,
    parameter NB_IMAGE      = `NB_ADDRESS,
    parameter NB_DATA       = `CONV_LPOS,
        //Parametrización
    localparam BIT_ARRAY            = BIT_LEN*`M_LEN,
    localparam DAT_MCU              = BIT_LEN*2,
    localparam Kernel_load          = 0,
    localparam ImgSize_load         = 1, 
    localparam Img_load             = 2,
    localparam Data_request         = 3,
    localparam LoadFinish_goToRun   = 4  
    )(    //Definicion de puertos
    output [GPIO_D-1:0]     o_GPIOdata,
    output [BIT_ARRAY-1:0]  o_KNLdata,
    output [BIT_LEN-1:0]    o_MCUdata,
    output [NB_IMAGE-1:0]   o_imgLength,
    output                  o_run,
    output                  o_valid_to_FSM,
    output                  o_valid_to_CONV,
    output                  o_KNorIMG,
    output                  o_load,

    input [BIT_ARRAY-1:0]   i_GPIOdata,
    input [NB_DATA-1:0]     i_MCUdata,
    input [2:0]             i_GPIOctrl,
    input                   i_GPIOvalid,
    input                   i_rst,
    input                   i_CLK,
    input                   i_EOP_from_FSM
    );

    /*      Register file:
           
           BITS MÁS SIGNIFICATIVOS (GPIO[31:29])
           
                Código instrucción              Acción
                
                     000                      Cargar kernell
                     001                      Cargar Img_size
                     010                      Cargar Imagen
                     011                      Pedir dato
                     100                      Cambio de estado (a precesamiento)
                     -----------------------------------------
                     101-111                  No utilizados
                     ---------------------------------------
           
           LSB ( GPIOctrl) -> VALID (bit 28 desde top_microblaze; están los buses separados)
    
    */
    reg [BIT_ARRAY-1:0]             dataKERNEL;
    reg [NB_DATA-1:0]               dataGPIO;
    reg [BIT_LEN-1:0]               dataMCU;  
    reg [NB_IMAGE-1:0]              imgLength;   
    reg                             validFSM;
    reg                             validCONV;
    reg                             GPIO_valid_previous_state;
    reg                             KI;
    reg                             load_reg;
    reg                             run_reg;
    
  	// En principio no haria falta el latcheo: reg [3:0] controlGPIO;
 	//Registers:
    assign {o_valid_to_FSM}  = validFSM;
    assign {o_valid_to_CONV} = validCONV;
    assign {o_KNorIMG}       = KI;
    assign {o_imgLength}     = imgLength;
    assign {o_GPIOdata}      = {i_EOP_from_FSM, {(GPIO_D-NB_DATA-1){1'b0}},dataGPIO};
    assign {o_MCUdata}       = dataMCU;
    assign {o_run}           = run_reg;
    assign {o_KNLdata}       = dataKERNEL;
    assign {o_load}          = load_reg;   

    always @(posedge i_CLK) begin
        if(i_rst) begin
            dataGPIO    <= {NB_DATA{1'b0}};
            load_reg    <= 1'b0;
            dataKERNEL  <= 24'd0;
            dataMCU     <= 8'd0;
            imgLength   <= 10'd0;
            validFSM    <= 1'b0;
            validCONV   <= 1'b0;
            run_reg     <= 1'b0;
            KI          <= 1'b0; //definido asi en la documentación.
 			GPIO_valid_previous_state  <=   1'b0;
        end
        else begin    
            dataMCU  <= i_GPIOdata;
            dataGPIO <= i_MCUdata;
            GPIO_valid_previous_state <= i_GPIOvalid;
            if (i_GPIOvalid && GPIO_valid_previous_state==1'b0)
                validFSM <= 1'b1;
            else 
                validFSM <= 1'b0;
            //!run_reg => no estoy en estado RUN (si estoy en el mismo, este modulo no cede el control)
            if(!run_reg) begin     
                case (i_GPIOctrl)
                    //Carga kernell
                    Kernel_load:  begin
                        run_reg     <= 1'b0;
                        //Modo kernell activo por bajo
                        load_reg    <= 1'b0;      
                        KI          <= 1'b0;
                        dataKERNEL  <= i_GPIOdata;
                        if (i_GPIOvalid && !GPIO_valid_previous_state)
                            validCONV   <= 1'b1;
                        else 
                            validCONV   <= 1'b0;                 
                    end
                    //Carga del tamano de la imagen Img_length
                    ImgSize_load: begin
                        run_reg     <= 1'b0;
                        KI          <= 1'b1;
                        imgLength   <= i_GPIOdata[NB_IMAGE-1:0];
                        load_reg    <= 1'b0;                 
                    end
                    //Cargar imagen
                    Img_load:     begin
                        run_reg     <= 1'b0;
                        KI          <= 1'b1;
                        //Levanto senal de carga para la FSM
                        load_reg    <= 1'b1;
                    end              
                    LoadFinish_goToRun: begin
                        if(!i_EOP_from_FSM) begin
                            KI          <= 1'b1;
                            //Termino carga, paso a estado RUN. Se delega el control del sistema         
                            run_reg     <= 1 'b1;
                            //Bajo senal de carga para la FSM
                            load_reg    <= 1'b0;
                        end    
                    end
                    default :   ;
                endcase     
            end 
            else if(i_EOP_from_FSM && run_reg)
               run_reg = 1'b0;
            end//End if/else rst
    end //End always
endmodule