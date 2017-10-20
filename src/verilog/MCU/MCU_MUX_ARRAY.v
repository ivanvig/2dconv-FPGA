 module MUX_ARRAY #(
        parameter N = 2,
        parameter BITS_IMAGEN = 8
    )(
        input  [N*BITS_IMAGEN-1:0]     i_DataConv,
        input  [(N+2)*BITS_IMAGEN-1:0] i_MemData,
        input  [3*BITS_IMAGEN-1:0]     i_Data,
        input                          i_inputCtrl,
        //CONFIGURAR BIEN LAS SELECTORAS
        output [3*N*BITS_IMAGEN-1:0]   o_DataConv,
        output [(N+2)*BITS_IMAGEN-1:0] o_MemData,
        output [3*BITS_IMAGEN-1:0]     o_Data,     //Revisar esto
    );

    wire tomemory;

    /*
    *   SE TIENE UN MUX POR CONVOLUCIONADOR, CON 4 ENTRADAS:
    *   1_ PRIMEROS 8 BITS DE ENTRADA
    *   2_ SEGUNDOS 8 BITS DE ENTRADA
    *   3_ TERCEROS 8 BITS DE ENTRADA
    *   4_ ENTRADA DESDE LA SALIDA DEL CONVOLUCIONADOR
    *
    *   DE ESTE MUX VA A UN DEMUX QUE ELIGE A QUE MEMORIA ESCRIBIR EL DATO
    *
    *   VER COMO GENERAR LOS "CASES" CON UN BUCLE
    */

    always@(*) begin
        case (i_inputCtrl)
          1'b00 : assign tomemory = i_Data[7:0];
          1'b01 : assign tomemory = i_Data[15:8];
          1'b10 : assign tomemory = i_Data[23:16];
          1'b11 : assign tomemory = i_DataConv;
        endcase
    end
    
