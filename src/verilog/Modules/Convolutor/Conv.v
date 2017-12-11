`timescale 1ns / 1ps

`define BIT_LEN 8
`define CONV_LEN 20
`define CONV_LPOS 13
`define M_LEN 3

module Conv #(
    parameter BIT_LEN =`BIT_LEN,
    parameter CONV_LEN =`CONV_LEN,
    parameter CONV_LPOS = `CONV_LPOS,
    parameter M_LEN = `M_LEN,
    localparam BIT_ARRAY = BIT_LEN*3
    )(
    output [CONV_LPOS-1:0] o_data,
    input [BIT_LEN-1:0] i_dato0,
    input [BIT_LEN-1:0] i_dato1,
    input [BIT_LEN-1:0] i_dato2,
    input i_selecK_I, //KI=0 modo kernle k=1 modo imagen
    input i_reset,
    input i_valid,
    input CLK100MHZ
    );
    // registros del kernel
    // [j][i] Primero columnas luego filas
    reg signed [BIT_ARRAY-1:0] kernel [0:M_LEN-1];    
    // registros de la imagen
    reg signed [BIT_ARRAY-1:0] imagen [0:M_LEN-1];
    // resultado
    reg signed [CONV_LPOS-1:0]  conv_reg;
    // reg de la convolucion
    reg signed [CONV_LEN-1:0] resultado;
    
    integer ptr_row;
    integer ptr_column;

    //Asigancion de Convolucion a la salida
    assign {o_data[CONV_LPOS-1],o_data[CONV_LPOS-2:0]}= {~conv_reg[CONV_LPOS-1], conv_reg[CONV_LPOS-2:0]};
    integer shift;
    always @( posedge CLK100MHZ) begin
        if(i_reset) begin
            //reset valores de imagen
            for(shift=0; shift < M_LEN; shift = shift +1) begin
                imagen[shift]<={BIT_ARRAY{1'b0}};
                kernel[shift]<={BIT_ARRAY{1'b0}};
            end 
            //reser valores de kernel . modif
            /*
            kernel[0]<=24'h002000;
            kernel[1]<=24'h208020;
            kernel[2]<=24'h002000;
            */
            //regitro de la convolucion
            conv_reg<={CONV_LPOS{1'b0}};
        end
        else if(i_valid)begin
            case (i_selecK_I)
                1'b1: begin
                    // imagen
                    for( shift = 0; shift < M_LEN-1; shift = shift +1)
                        imagen[shift]<=imagen[shift+1];
                    imagen[M_LEN-1]<={i_dato2,i_dato1,i_dato0};
                    //latcheo de la salida 
                    conv_reg<= resultado[CONV_LEN-1:CONV_LEN-CONV_LPOS];
                    //conv_reg<= resultado;
                end
                1'b0: begin
                    //kernel
                    for( shift = 0; shift < M_LEN-1; shift = shift +1)
                        kernel[shift]<=kernel[shift+1];
                    kernel[M_LEN-1]<={i_dato2,i_dato1,i_dato0};
                    //salida
                    conv_reg<=conv_reg;

                end
            endcase
        end
        else begin 
            //imagen 
            for (shift =0 ; shift<M_LEN;shift=shift+1) begin: elseequ
                imagen[shift]<=imagen[shift];
                kernel[shift]<=kernel[shift];
            end
            //matengo el lacheo
            conv_reg<=conv_reg;
        end
    end
    
    //Arbol de Suma
    always @(*) begin
        resultado = 20'h0;
        for(ptr_row = 0 ; ptr_row < M_LEN ; ptr_row=ptr_row+1) 
        begin : SumaYMult
            for (ptr_column = 0 ; ptr_column < M_LEN ; ptr_column=ptr_column+1) 
            begin: SumaTop
                resultado = resultado + $signed(kernel[ptr_row][(ptr_column+1)*BIT_LEN-1 -: BIT_LEN])*
                                        $signed(imagen[ptr_row][(ptr_column+1)*BIT_LEN-1 -: BIT_LEN]);
            end
        end
    end
endmodule