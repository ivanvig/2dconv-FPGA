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
    input [BIT_LEN-1:0] i_dato0,
    input [BIT_LEN-1:0] i_dato1,
    input [BIT_LEN-1:0] i_dato2,
    input i_selecK_I,
    input i_reset,
    input i_valid,
    input CLK100MHZ,
    output [CONV_LPOS-1:0] o_data
    );
    // registros del kernel
    reg signed [BIT_LEN-1:0] kernel [0:M_LEN-1][0:M_LEN-1];    
    // registros de la imagen
    reg signed [BIT_LEN-1:0] imagen [0:M_LEN-1][0:M_LEN-1];
    // resultado
    //reg [CONV_LPOS-1:0] result;
    reg [CONV_LEN-1:0]  conv_reg;
        
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
    assign conv = kernel[0][0]*imagen[0][0] + kernel[0][1]*imagen[0][1] + kernel[0][2]*imagen[0][2]+
                   kernel[1][0]*imagen[1][0] + kernel[1][1]*imagen[1][1] + kernel[1][2]*imagen[1][2]+
                   kernel[2][0]*imagen[2][0] + kernel[2][1]*imagen[2][1] + kernel[2][2]*imagen[2][2];

    // se invierte el ultimo bit para el cambio de rango
    // asignacion para la salida del dato 
    assign {o_data[CONV_LPOS-1],o_data[CONV_LPOS-2:0]}= {~conv_reg[CONV_LEN-1], conv_reg[CONV_LEN-2 : CONV_LEN-CONV_LPOS]};

    always @( posedge clk) begin
        if(rst) begin
            //reset valores de imagen
            imagen[0][0]<=0; imagen[0][1]<=0; imagen[0][2]<=0;
            imagen[1][0]<=0; imagen[1][1]<=0; imagen[1][2]<=0;
            imagen[2][0]<=0; imagen[2][1]<=0; imagen[2][2]<=0;
            //reser valores de kernel
            kernel[0][0]<=0; kernel[0][1]<=0; kernel[0][2]<=0;
            kernel[1][0]<=0; kernel[1][1]<=0; kernel[1][2]<=0;
            kernel[2][0]<=0; kernel[2][1]<=0; kernel[2][2]<=0;
            //regitro de la convolucion
            conv_reg<=0;
        end
        else if(valid)begin
            case (selecK_I)
                1'b1: begin
                    // imagen
                    imagen[0][0]<=imagen[1][0]; imagen[0][1]<=imagen[1][1]; imagen[0][2]<=imagen[1][2];
                    imagen[1][0]<=imagen[2][0]; imagen[1][1]<=imagen[2][1]; imagen[1][2]<=imagen[2][2];
                    imagen[2][0]<=i_dato0;      imagen[2][1]<=i_dato1;      imagen[2][2]<=i_dato2;
                    //latcheo de la salida 
                    conv_reg<= conv;
                
                end
                1'b0: begin
                    //kernel
                    kernel[0][0]<=kernel[1][0]; kernel[0][1]<=kernel[1][1]; kernel[0][2]<=kernel[1][2];
                    kernel[1][0]<=kernel[2][0]; kernel[1][1]<=kernel[2][1]; kernel[1][2]<=kernel[2][2];
                    kernel[2][0]<=i_dato0;        kernel[2][1]<=i_dato1;        kernel[2][2]<=i_dato2;
                    //salida
                    conv_reg<=conv_reg;

                end
            endcase
        end
        else begin 
            //imagen 
            imagen[0][0]<=imagen[0][0]; imagen[0][1]<=imagen[0][1]; imagen[0][2]<=imagen[0][2];
            imagen[1][0]<=imagen[1][0]; imagen[1][1]<=imagen[1][1]; imagen[1][2]<=imagen[1][2];
            imagen[2][0]<=imagen[2][0]; imagen[2][1]<=imagen[2][1]; imagen[2][2]<=imagen[2][2];
            //kernel
            kernel[0][0]<=kernel[0][0]; kernel[0][1]<=kernel[0][1]; kernel[0][2]<=kernel[0][2];
            kernel[1][0]<=kernel[1][0]; kernel[1][1]<=kernel[1][1]; kernel[1][2]<=kernel[1][2];
            kernel[2][0]<=kernel[2][0]; kernel[2][1]<=kernel[2][1]; kernel[2][2]<=kernel[2][2];
            //matengo el lacheo
            conv_reg<=conv_reg;
        end
    end
endmodule
