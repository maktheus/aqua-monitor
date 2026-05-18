// ============================================================
// AquaMonitorSoC v1.0 — SAR ADC Control FSM
// Moore FSM, 8 states, 4-bit successive approximation
// CMOS TSMC 180nm  VDD=1.8V
// Author: Matheus Serrão Uchôa  — PADIS Unidade 7, Cap 5
// ============================================================
`timescale 1ns/1ps

module sar_ctrl_fsm (
    input  logic        clk,            // 1 MHz ADC clock
    input  logic        rst_n,          // active-low reset
    input  logic        start,          // begin conversion
    input  logic        comparator_out, // 1 = VIN > VDAC

    output logic [3:0]  dac_code,       // current DAC trial word
    output logic        sample_en,      // hold capacitor charge command
    output logic        eoc,            // end-of-conversion pulse (1 cycle)
    output logic [3:0]  result          // latched 4-bit result
);

    // --------------------------------------------------------
    // State encoding (one-hot would also work; binary used here)
    // --------------------------------------------------------
    localparam [3:0] IDLE   = 4'd0;
    localparam [3:0] CH_SEL = 4'd1;
    localparam [3:0] SAMPLE = 4'd2;
    localparam [3:0] BIT3   = 4'd3;
    localparam [3:0] BIT2   = 4'd4;
    localparam [3:0] BIT1   = 4'd5;
    localparam [3:0] BIT0   = 4'd6;
    localparam [3:0] DONE   = 4'd7;

    logic [3:0] state, next_state;

    // Internal trial register (built up bit by bit)
    logic [3:0] trial_reg;

    // --------------------------------------------------------
    // State register (sequential)
    // --------------------------------------------------------
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    // --------------------------------------------------------
    // Next-state logic (combinational)
    // --------------------------------------------------------
    always_comb begin
        next_state = IDLE; // default
        case (state)
            IDLE   : next_state = start ? CH_SEL : IDLE;
            CH_SEL : next_state = SAMPLE;
            SAMPLE : next_state = BIT3;
            BIT3   : next_state = BIT2;
            BIT2   : next_state = BIT1;
            BIT1   : next_state = BIT0;
            BIT0   : next_state = DONE;
            DONE   : next_state = IDLE;
            default: next_state = IDLE;
        endcase
    end

    // --------------------------------------------------------
    // Trial register — updated on clock edges during BIT states
    // Successive approximation: set bit, then keep or clear
    // --------------------------------------------------------
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            trial_reg <= 4'b0000;
        end else begin
            case (state)
                CH_SEL : trial_reg <= 4'b0000;            // clear before conversion
                SAMPLE : trial_reg <= 4'b1000;            // set MSB trial (bit3)
                BIT3   : begin                             // evaluate bit3 result
                    trial_reg[3] <= comparator_out;        // keep if VIN > VDAC
                    trial_reg[2] <= 1'b1;                  // set next trial bit
                end
                BIT2   : begin
                    trial_reg[2] <= comparator_out;
                    trial_reg[1] <= 1'b1;
                end
                BIT1   : begin
                    trial_reg[1] <= comparator_out;
                    trial_reg[0] <= 1'b1;
                end
                BIT0   : begin
                    trial_reg[0] <= comparator_out;
                end
                default: ; // no change
            endcase
        end
    end

    // --------------------------------------------------------
    // Moore outputs (pure function of state)
    // --------------------------------------------------------
    always_comb begin
        // Defaults
        sample_en = 1'b0;
        eoc       = 1'b0;
        dac_code  = trial_reg;

        case (state)
            IDLE   : begin sample_en = 1'b0; end
            CH_SEL : begin sample_en = 1'b0; end
            SAMPLE : begin sample_en = 1'b1; dac_code = 4'b1000; end
            BIT3   : begin dac_code  = trial_reg; end
            BIT2   : begin dac_code  = trial_reg; end
            BIT1   : begin dac_code  = trial_reg; end
            BIT0   : begin dac_code  = trial_reg; end
            DONE   : begin eoc = 1'b1; dac_code = trial_reg; end
            default: begin sample_en = 1'b0; end
        endcase
    end

    // --------------------------------------------------------
    // Result register — latched when in DONE state
    // --------------------------------------------------------
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            result <= 4'b0000;
        else if (state == DONE)
            result <= trial_reg;
    end

endmodule
