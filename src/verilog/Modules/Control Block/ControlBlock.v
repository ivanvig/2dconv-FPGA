`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
//
// Create Date: 02.11.2017 22:55:31
// Design Name: Control Block
// Module Name: controlBlock
// Project Name: Img project
// Target Devices: Arty 7
// Tool Versions: 2017.3
// Description: Register file
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////



module ControlBlock(i_GPIOvalid, i_GPIOctrl, i_GPIOdata, i_rst, i_CLK, i_EoP_FSM, i_MCUdata, o_GPIOdata, o_led, o_imgLength, o_EoP_MCU,o_SoP,o_valid_FSM, o_valid_CONV, o_KNLdata, o_KNorIMG);

    
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
      
  //Parametrización
  localparam Kernel_load     = 0; 
  localparam ImgSize_load    = 1; 
  localparam Img_load        = 2;
  localparam Data_request    = 3;
  localparam ImgFinished= 4;  

 //Definicion de puertos
  input  [23:0] i_GPIOdata;
  input  [12:0] i_MCUdata;
  input   [2:0] i_GPIOctrl;
  input         i_GPIOvalid;
  input         i_rst;
  input         i_CLK;
  input         i_EoP_FSM;
 
 
  output [31:0] o_GPIOdata;
  output [23:0] o_KNLdata;
  output  [10:0] o_imgLength;
  output  [2:0] o_led; //o_estado
  output        o_EoP_MCU;
  output        o_SoP;
  output        o_valid_FSM;
  output        o_valid_CONV;
  output        o_KNorIMG;

  reg    [23:0] dataKERNEL;
  reg    [23:0] dataGPIO;
  reg    [12:0] dataMCU;  
  reg    [10:0] imgLength;
  reg     [2:0] go_to_led;     
  reg           validFSM;
  reg           validCONV;
  reg           GPIO_valid_previous_state;
  reg           KI;
  reg           SoP_reg;
  reg           EoPMCU_reg;
  // En principio no haria falta el latcheo: reg [3:0] controlGPIO;
    
 //Registers:
  assign {o_valid_FSM}  = validFSM;
  assign {o_valid_CONV} = validCONV;
  assign {o_KNorIMG}    = KI;
  assign {o_imgLength}  = imgLength;
  assign {o_GPIOdata}   = (i_GPIOctrl==Data_request ? dataMCU:dataGPIO);
  assign {o_SoP}        = SoP_reg;
  assign {o_EoP_MCU}    = EoPMCU_reg;
  assign {o_KNLdata}    = dataKERNEL;
  //Falta o_led para determinar en que estado estoy   
     
         
    always @(posedge i_CLK) begin
    
       GPIO_valid_previous_state<=i_GPIOvalid;
       dataMCU<=i_MCUdata;
       dataGPIO<=i_GPIOdata;
    
       if(i_rst) begin
                      
                dataKERNEL  <= 24'd0;
                   dataMCU  <= 13'd0;
                  imgLength <=  9'd0;
                 go_to_led  <=  3'd0;
                  validFSM  <=  1'b0;
                 validCONV  <=  1'b0;
                    SoP_reg <=  1'b0;
                 EoPMCU_reg <=  1'b0;   
                        KI  <=  1'b1; //definido asi
       end
       else begin    
              //!SoP_reg => no estoy en estado RUN (si estoy en el mismo, este modulo no cede el control)
              if(!SoP_reg) begin  
               
                case (i_GPIOctrl)
               
                        //Carga kernell
                        Kernel_load:  begin
                                         //Modo kernell activo por bajo
                                         KI<=1'b0;
                                         dataKERNEL<=i_GPIOdata;
                                         if (i_GPIOvalid && !GPIO_valid_previous_state)
                                                validCONV<=1'b1;
                                         else 
                                                validCONV<=1'b0;
                                 
                                      end
                                
                        //Carga del tamano de la imagen Img_length
                        ImgSize_load: begin
                                        KI<=1'b1;
                                        imgLength<=i_GPIOdata[10:0];
                                      
                                      end 
            
                       //Cargar imagen
                        Img_load:     begin
                                         KI<=1'b1;
                                         if (i_GPIOvalid && GPIO_valid_previous_state==1'b0)
                                             validFSM<=1'b1;
                                         else 
                                             validFSM<=1'b0;
                                        
                                      end 
                        
                        //Pedir dato
                        Data_request: ; // No se si iria algo mas en el cuerpo, porque lo implemente en el assign
                                        //assign {o_GPIOdata}   = (i_GPIOctrl==Data_request ? dataMCU:dataGPIO);//;
                                        // Es decir, si i_GPIOctrl esta en data_request, mi salida toma los valores de i_MCUdata
                                        // Sino, toma los valores de gpio (tengo dos entradas de datos, la del gpio y mcu
                                        
                        ImgFinished: begin
                                    
                                        //Termino carga, paso a estado RUN. Se delega el control del sistema
                                         SoP_reg<=1'b1;
                                     
                                     end
                        default :;
                            
                endcase 
                
                end
                else if (i_EoP_FSM) begin
                            //Estando en RUN, al recibir la senal End Of Process del FSM, debo SALIR del estado mencionado
                            //Es decir, se termino la etapa de procesamiento, y se pasa a la etapa OUT poniendo en alto EoP_MCU
                            
                            EoPMCU_reg<=1'b1;
                            SoP_reg<=1'b0;
              
                end
 
        end//End if/else rst
        
    end //End always
    
    
endmodule
