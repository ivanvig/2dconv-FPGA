`timescale 1ns / 1ps

`define NB_ADDRESS      10
`define NB_IMAGE        10


module FSM(i_CLK, i_reset, i_SoP, i_imgLength, i_valid, o_readAdd, o_writeAdd, o_EoP, o_changeBlock);

    parameter NB_ADDRESS= `NB_ADDRESS;
    parameter NB_IMAGE  = `NB_IMAGE;
    
    //Altura(o largo) en pixel de la imagen
    localparam imgHeight =(2**NB_IMAGE)-1;
    localparam latency   = 5;
    localparam NBlatency = `NB_ADDRESS*latency;
     
    //Definición de puertos
    input                    i_CLK;
    input                    i_reset;
    input                    i_SoP;
    input  [NB_IMAGE-1:0]    i_imgLength;
    input                    i_valid;
    
    output [NB_ADDRESS-1:0]  o_writeAdd;
    output [NB_ADDRESS-1:0]  o_readAdd;
    output                   o_EoP;
    output                   o_changeBlock;
    
    
    //Latcheo de salidas 
    reg [NB_ADDRESS-1:0]                     counterAdd;
    reg  [NBlatency-1:0]           counter_with_latency;
    reg                                    endOfProcess;
    reg                                     changeBlock;
    reg                                      sopControl;
    
    //Ni bien se crean los registros, toman esos valores.
    initial begin
        counterAdd           = 'd0;
        counter_with_latency = 'd0;
        endOfProcess         = 1'b0;
        changeBlock          = 1'b0;
        sopControl           = 1'b0;
    end        
    
 
 
        
    always @(posedge i_CLK) begin
          
      if(i_reset==1'b1)begin
        counterAdd           <=`NB_ADDRESS'd0;
        counter_with_latency <='d0;
        endOfProcess         <=1'b0;
        changeBlock          <=1'b0;
        sopControl           <=1'b0;
      end
      else begin
        counterAdd           <= counterAdd;
        counter_with_latency <= counter_with_latency;
        endOfProcess         <= endOfProcess;
        changeBlock          <= changeBlock;
        sopControl           <= sopControl;    
      end
      
      
      //Levanto registro de control, ya que una vez que arranca a procesar, no para.
       if( (sopControl==1'b0) && i_SoP) begin
                  sopControl            <= 1'b1;
                  counter_with_latency  <='d0;
       
       end
       else begin
                  sopControl           <= sopControl;
                  counter_with_latency <=  counter_with_latency;       
       end
      
      
                 
      //Estado de procesamiento
      if(sopControl==1'b1) begin 
      
          counterAdd   <= counterAdd+1;
          //Shifteo para el write address, teniendo en cuenta la latencia.
          counter_with_latency<= {counter_with_latency[(NBlatency-NB_ADDRESS)-1:0],counterAdd};
          if(counterAdd==imgHeight) begin
                endOfProcess <= 1'b1;
                counterAdd   <= 'd0;
                sopControl   <=1'b0;
          end
          
      end
      
      //Estado de lectura y carga. En ambos la lógica es la misma.
      else begin
        
        //Manejo de direcciones en función del valid
        if (i_valid)
            counterAdd<=counterAdd+1;
        else
            counterAdd<=counterAdd;
        
        //Verificación si termino de leer/cargar un bloque
        if (counterAdd==imgHeight)begin
            changeBlock<= 1'b1;
            counterAdd <= 'd0;
        end
               
        
      end
      //end else      
 
  end 
 //end always   
 
     //Assign          
    assign     {o_writeAdd} =  sopControl ? counter_with_latency[NBlatency-1: NBlatency - NB_ADDRESS] : counterAdd;
    assign     {o_readAdd}  =  counterAdd;
    assign          {o_EoP} =  endOfProcess;
    assign  {o_changeBlock} =  changeBlock;
    



endmodule
