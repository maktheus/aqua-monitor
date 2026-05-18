// ============================================================
// AquaMonitorSoC v1.0 — 3-Channel Analog MUX Controller
// Generates one-hot mux_sel for 3 analog transmission gates
// ch_sel: 00=pH, 01=Conductivity, 10=Temperature
// Author: Matheus Serrão Uchôa  — PADIS Unidade 7, Cap 5
// ============================================================
`timescale 1ns/1ps

module mux3_ctrl (
    input  logic [1:0] ch_sel,     // channel select code
    input  logic       en,         // global enable (active-high)

    output logic [2:0] mux_sel     // one-hot: [2]=Temp, [1]=Cond, [0]=pH
);

    // One-hot decode with enable gate
    always_comb begin
        if (!en) begin
            mux_sel = 3'b000;   // all switches open when disabled
        end else begin
            case (ch_sel)
                2'b00 : mux_sel = 3'b001;   // pH       channel
                2'b01 : mux_sel = 3'b010;   // Conductivity channel
                2'b10 : mux_sel = 3'b100;   // Temperature channel
                default: mux_sel = 3'b000;  // invalid → all open
            endcase
        end
    end

endmodule
