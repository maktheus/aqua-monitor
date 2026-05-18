// ============================================================
// AquaMonitorSoC v1.0 — 4-bit Capacitive DAC Controller
// Models an R-2R / binary-weighted capacitor DAC
// VDD = 1.8V,  16 levels,  LSB = 1800mV/16 = 112.5mV
// C_unit = 20 fF (from layout sizing)
// Author: Matheus Serrão Uchôa  — PADIS Unidade 7, Cap 5
// ============================================================
`timescale 1ns/1ps

module dac_4bit_ctrl (
    input  logic [3:0]  code,        // digital input word

    output logic [3:0]  vout_ctrl,   // switch positions (1=connect to VDD, 0=GND)
    output integer      nominal_mv   // nominal output voltage in mV (0–1800)
);

    // LSB voltage in millivolts: 1800 / 16 = 112.5 → integer approx 112
    localparam integer LSB_MV = 113; // rounded (actual 112.5 mV)

    // Direct pass-through: each switch bit drives VDD (1) or GND (0)
    assign vout_ctrl = code;

    // Nominal output voltage calculation
    // V_out = code * VDD / 16  →  in mV = code * 1800 / 16
    always_comb begin
        nominal_mv = code * 1800 / 16;
    end

    // --------------------------------------------------------
    // Synthesis note:
    //   In actual silicon the 4 switches drive the bottom plates
    //   of a binary-weighted capacitor array:
    //     C3=8*C_unit (160 fF), C2=4*C_unit (80 fF),
    //     C1=2*C_unit (40 fF),  C0=1*C_unit (20 fF)
    //   Total array = 15*C_unit + C_term = 300 fF + 20 fF
    //   The digital bits are the gate drives for the NMOS switches.
    // --------------------------------------------------------

endmodule
