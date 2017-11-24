module MCU_CTRL
    #(
      parameter N = 2,
      parameter STATES = 3,
      localparam LOAD = 2'b00,
      localparam PROC = 2'b01,
      localparam OUT = 2'b10,
      localparam SUB = N/2 + 1 //para N par, numero de estados de direccionamiento de memoria
      )(
        input                          i_sop, i_eop, clk, rst, i_chblk,

        output reg [N+1:0]             o_we,
        output [$clog2(STATES)-1:0]    o_state,
        output [$clog2(SUB) - 1:0]     o_substate,
        output reg [$clog2(N+2) - 1:0] o_memSelect
        );
    
    
    reg [N+1:0]                        we_rw_status;
    reg [N+1:0]                        we_proc_status;
    reg [$clog2(N+2) - 1:0]            memSelect_load, memSelect_out;
    reg [$clog2(SUB) - 1:0]            substate;
    reg [$clog2(STATES)-1:0]           state;
    reg                                just_once, chblk;

    assign o_state = state;
    assign o_substate = substate;
    
    always @ (posedge clk) begin
        if(rst) begin
            substate <= 0;
            memSelect_load <= 0;
            memSelect_out <= 0;
        end
        else begin
            chblk <= i_chblk;
            case(state)
                LOAD: begin // LOAD
                    just_once = 1'b1;
                    if(i_chblk && (i_chblk != chblk)) begin
                        we_rw_status <= {we_rw_status[N:0], we_rw_status[N+1]};
                        if(memSelect_out == N + 1)
                            memSelect_out <= 0;
                        else
                            memSelect_out <= memSelect_out + 1;
                    end
                end

                OUT: begin
                    if(just_once) begin
                        we_rw_status <= {we_rw_status[N:0], we_rw_status[N+1]};
                        we_proc_status <= {we_proc_status[1:0], we_proc_status[N+1:2]};
                        just_once <= 1'b0;

                        if(substate == (SUB))
                            substate <= 0;
                        else
                            substate <= substate + 1;

                    end
                    if(i_chblk && (i_chblk != chblk)) begin
                        if(memSelect_out == N + 1)
                            memSelect_out <= 0;
                    end
                    else begin
                        memSelect_out <= memSelect_out + 1;
                    end
                end
            endcase
        end
    end

    always @ (*)
        state = {i_eop, i_sop};

    always @ (*) begin
        case(state)

            LOAD: begin
                o_memSelect = memSelect_load;
                o_we = we_rw_status;
            end

            PROC: begin
                o_we = we_proc_status;
            end

            OUT: begin
                o_we = {(N+1){1'b0}};
                o_memSelect = memSelect_out;
            end

            default: begin
                o_we = {(N+1){1'b0}};
                o_memSelect = {($clog2(N+2) - 1){1'b0}};
            end
        endcase
    end
endmodule
