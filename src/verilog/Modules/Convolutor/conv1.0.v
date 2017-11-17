`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 06.10.2017 13:27:49
// Design Name: 
// Module Name: Conv
// Project Name: 
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

`define BIT_LEN 8
`define CONV_LEN 20
`define CONV_LPOS 13
`define M_LEN 3

module Conv #(
    parameter BIT_LEN =`BIT_LEN,
    parameter CONV_LEN =`CONV_LEN,
    parameter CONV_LPOS = `CONV_LPOS,
    parameter M_LEN = `M_LEN
    )(
    output [CONV_LPOS-1:0] o_data,
    input [BIT_LEN-1:0] i_dato0,
    input [BIT_LEN-1:0] i_dato1,
    input [BIT_LEN-1:0] i_dato2,
    input i_selecK_I,
    input i_reset,
    input i_valid,
    input CLK100MHZ
    );
    // registros del kernel
    // [j][i] Primero columnas luego filas
    reg signed [3*BIT_LEN-1:0] kernel [0:M_LEN-1];    
    // registros de la imagen
    reg signed [3*BIT_LEN-1:0] imagen [0:M_LEN-1];

    // resultado
    reg [CONV_LEN-1:0]  conv_reg;
    //reg [CONV_LEN-1:0]  result;
    reg signed [CONV_LEN-1:0]  par0;
    reg signed [CONV_LEN-1:0]  par1;
    reg signed [CONV_LEN-1:0]  par2;
    reg signed [2*BIT_LEN-1:0] prod1,prod2,prod3,prod4,prod5,prod6,prod7,prod8,prod9;

    // cable de la convolucion
    wire [CONV_LEN-1:0] conv;
    //  el resto de los cables    
    wire clk, selecK_I, rst, valid;
    wire sat_pos,sat_neg;


    assign clk = CLK100MHZ;
    assign selecK_I = i_selecK_I; //KI=0 modo kernle k=1 modo imagen
    assign rst = i_reset;
    assign valid = i_valid;

    //Convolucion
    assign  conv = par0+par1+par2;
    // se invierte el ultimo bit para el cambio de rango
    // asignacion para la salida del dato 
    assign {o_data[CONV_LPOS-1],o_data[CONV_LPOS-2:0]}= {~conv_reg[CONV_LEN-1], conv_reg[CONV_LEN-2 : CONV_LEN-CONV_LPOS]};

    always @( posedge clk) begin
        if(rst) begin
            //reset valores de imagen
            imagen[0]<=24'h0;
            imagen[1]<=24'h0;
            imagen[2]<=24'h0;
            //reser valores de kernel
            kernel[0]<=24'h0;
            kernel[1]<=24'h0;
            kernel[2]<=24'h0;
            //regitro de la convolucion
            conv_reg<=0;
        end
        else if(valid)begin
            case (selecK_I)
                1'b1: begin
                    // imagen
                    imagen[0]<=imagen[1];
                    imagen[1]<=imagen[2];
                    imagen[2]<={i_dato2,i_dato1,i_dato0};
                    //latcheo de la salida 
                    conv_reg<= conv;
                    //conv_reg<= resultado;
                end
                1'b0: begin
                    //kernel
                    kernel[0]<=kernel[1];
                    kernel[1]<=kernel[2];
                    kernel[2]<={i_dato2,i_dato1,i_dato0};
                    //salida
                    conv_reg<=conv_reg;

                end
            endcase
        end
        else begin 
            //imagen 
            imagen[0]<=imagen[0];
            imagen[1]<=imagen[1];
            imagen[2]<=imagen[2];
            //kernel
            kernel[0]<=kernel[0];
            kernel[1]<=kernel[2];
            kernel[2]<=kernel[1];
            //matengo el lacheo
            conv_reg<=conv_reg;
        end
    end

    always @(posedge clk) begin
        if (rst) begin
            // reset
            prod1<=0; prod2<=0; prod3<=0; prod4<=0;
            prod5<=0; prod6<=0; prod7<=0; prod8<=0;
            prod9<=0;
            par0<=0; par1<=0; par2<=0;
            
        end
        else begin
        prod1 <= $signed(kernel[0][BIT_LEN-1:0])             *   $signed(imagen[0][BIT_LEN-1:0]);
        prod2 <= $signed(kernel[0][2*BIT_LEN-1:BIT_LEN])     *   $signed(imagen[0][2*BIT_LEN-1:BIT_LEN]);
        prod3 <= $signed(kernel[0][3*BIT_LEN-1:2*BIT_LEN])   *   $signed(imagen[0][3*BIT_LEN-1:2*BIT_LEN]); 
        par0 <= prod1+prod2+prod3;

        prod4 <= $signed(kernel[1][BIT_LEN-1:0])             *   $signed(imagen[1][BIT_LEN-1:0]);
        prod5 <= $signed(kernel[1][2*BIT_LEN-1:BIT_LEN])     *   $signed(imagen[1][2*BIT_LEN-1:BIT_LEN]) ; 
        prod6 <= $signed(kernel[1][3*BIT_LEN-1:2*BIT_LEN])   *   $signed(imagen[1][3*BIT_LEN-1:2*BIT_LEN]);
        par1 <= prod4+prod5+prod6;

        prod7 <= $signed(kernel[2][BIT_LEN-1:0])             *   $signed(imagen[2][BIT_LEN-1:0]); 
        prod8 <= $signed(kernel[2][2*BIT_LEN-1:BIT_LEN])     *   $signed(imagen[2][2*BIT_LEN-1:BIT_LEN]); 
        prod9 <= $signed(kernel[2][3*BIT_LEN-1:2*BIT_LEN-1]) *   $signed(imagen[2][3*BIT_LEN-1:2*BIT_LEN]);
        par2 <= prod7+prod8+prod9;

        /*
        par0 <= $signed(kernel[0][BIT_LEN-1:0])             *   $signed(imagen[0][BIT_LEN-1:0])         + 
                $signed(kernel[0][2*BIT_LEN-1:BIT_LEN])     *   $signed(imagen[0][2*BIT_LEN-1:BIT_LEN]) + 
                $signed(kernel[0][3*BIT_LEN-1:2*BIT_LEN])   *   $signed(imagen[0][3*BIT_LEN-1:2*BIT_LEN]);
        
        par1 <= $signed(kernel[1][BIT_LEN-1:0])             *   $signed(imagen[1][BIT_LEN-1:0])         + 
                $signed(kernel[1][2*BIT_LEN-1:BIT_LEN])     *   $signed(imagen[1][2*BIT_LEN-1:BIT_LEN]) + 
                $signed(kernel[1][3*BIT_LEN-1:2*BIT_LEN])   *   $signed(imagen[1][3*BIT_LEN-1:2*BIT_LEN]);
        
        par2 <= $signed(kernel[2][BIT_LEN-1:0])             *   $signed(imagen[2][BIT_LEN-1:0])         + 
                $signed(kernel[2][2*BIT_LEN-1:BIT_LEN])     *   $signed(imagen[2][2*BIT_LEN-1:BIT_LEN]) + 
                $signed(kernel[2][3*BIT_LEN-1:2*BIT_LEN-1]) *   $signed(imagen[2][3*BIT_LEN-1:2*BIT_LEN]);
        */    
        end
    end
endmodule



