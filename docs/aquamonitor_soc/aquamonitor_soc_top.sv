// ============================================================
// AquaMonitorSoC v1.0 — Top-Level Integration
// Mixed-Signal SoC for aquaculture water quality monitoring
// CMOS TSMC 180nm  VDD=1.8V
// Author: Matheus Serrão Uchôa  — PADIS Unidade 7, Cap 5
// ============================================================
`timescale 1ns/1ps

module aquamonitor_soc_top (
    // System clock and reset
    input  logic        clk_8mhz,       // 8 MHz system clock (from crystal/PLL)
    input  logic        rst_n,          // active-low synchronous reset

    // Analog interface placeholders (real signals are analog)
    input  logic [2:0]  analog_in,      // placeholder: digital proxy for 3 analog inputs
    input  logic        comparator_out, // output of off-chip dynamic comparator

    // SPI slave interface
    input  logic        spi_sclk,
    input  logic        spi_mosi,
    output logic        spi_miso,
    input  logic        spi_cs_n,

    // Analog control outputs
    output logic [3:0]  dac_sw,         // DAC switch positions (to capacitor array)
    output logic [2:0]  mux_sel,        // one-hot analog MUX select

    // Control/status
    output logic        sample_en,      // hold-mode command to S/H capacitor
    output logic        eoc,            // end-of-conversion indicator
    output logic        led_ready       // status LED: conversion complete
);

    // --------------------------------------------------------
    // Internal signals
    // --------------------------------------------------------
    logic        clk_1mhz;          // ADC clock after /8 divider
    logic [2:0]  clk_div_cnt;       // divider counter
    logic        sar_start;         // start pulse to FSM
    logic [3:0]  sar_dac_code;      // FSM → DAC code
    logic [3:0]  sar_result;        // latched ADC result
    logic [1:0]  ch_sel;            // current channel selector
    logic        mux_en;            // MUX enable

    // Channel sequencer state
    logic [1:0]  ch_counter;        // 0,1,2 round-robin channel counter
    logic        conv_running;      // FSM busy flag

    // SPI data word
    logic [15:0] spi_tx_data;
    logic [15:0] spi_rx_data;
    logic        spi_valid;

    // Result registers (one per channel)
    logic [3:0]  result_ch [0:2];
    logic [7:0]  status_reg;

    // --------------------------------------------------------
    // Clock Divider: 8 MHz → 1 MHz  (/8)
    // --------------------------------------------------------
    always_ff @(posedge clk_8mhz or negedge rst_n) begin
        if (!rst_n) begin
            clk_div_cnt <= 3'd0;
            clk_1mhz    <= 1'b0;
        end else begin
            if (clk_div_cnt == 3'd3) begin
                clk_1mhz    <= ~clk_1mhz;
                clk_div_cnt <= 3'd0;
            end else begin
                clk_div_cnt <= clk_div_cnt + 3'd1;
            end
        end
    end

    // --------------------------------------------------------
    // Channel sequencer: auto-start conversions, round-robin
    // --------------------------------------------------------
    always_ff @(posedge clk_1mhz or negedge rst_n) begin
        if (!rst_n) begin
            ch_counter   <= 2'd0;
            sar_start    <= 1'b0;
            conv_running <= 1'b0;
        end else begin
            sar_start <= 1'b0; // default: single-cycle pulse
            if (!conv_running) begin
                sar_start    <= 1'b1;
                conv_running <= 1'b1;
            end else if (eoc) begin
                // Save result for current channel
                result_ch[ch_counter] <= sar_result;
                // Advance to next channel
                ch_counter   <= (ch_counter == 2'd2) ? 2'd0 : ch_counter + 2'd1;
                conv_running <= 1'b0;
            end
        end
    end

    assign ch_sel  = ch_counter;
    assign mux_en  = conv_running;

    // --------------------------------------------------------
    // SAR Control FSM instance
    // --------------------------------------------------------
    sar_ctrl_fsm u_sar_fsm (
        .clk            (clk_1mhz),
        .rst_n          (rst_n),
        .start          (sar_start),
        .comparator_out (comparator_out),
        .dac_code       (sar_dac_code),
        .sample_en      (sample_en),
        .eoc            (eoc),
        .result         (sar_result)
    );

    // --------------------------------------------------------
    // 3-Channel Analog MUX Controller
    // --------------------------------------------------------
    mux3_ctrl u_mux (
        .ch_sel  (ch_sel),
        .en      (mux_en),
        .mux_sel (mux_sel)
    );

    // --------------------------------------------------------
    // 4-bit Capacitive DAC Controller
    // --------------------------------------------------------
    logic [3:0] dac_vout_ctrl;
    integer     dac_nominal_mv;

    dac_4bit_ctrl u_dac (
        .code       (sar_dac_code),
        .vout_ctrl  (dac_vout_ctrl),
        .nominal_mv (dac_nominal_mv)
    );

    assign dac_sw = dac_vout_ctrl;

    // --------------------------------------------------------
    // SPI TX word assembly
    // Format: [15:12]=CH_ID | [11:8]=RESULT | [7:0]=STATUS
    // --------------------------------------------------------
    always_comb begin
        status_reg    = 8'h00;
        status_reg[7] = eoc;
        status_reg[1:0] = ch_sel;

        spi_tx_data = {2'b00, ch_sel,        // [15:12] channel ID
                       sar_result,            // [11:8]  ADC result
                       status_reg};           // [7:0]   status
    end

    // --------------------------------------------------------
    // SPI Slave instance
    // --------------------------------------------------------
    spi_slave u_spi (
        .sclk     (spi_sclk),
        .mosi     (spi_mosi),
        .cs_n     (spi_cs_n),
        .data_in  (spi_tx_data),
        .miso     (spi_miso),
        .data_out (spi_rx_data),
        .valid    (spi_valid)
    );

    // --------------------------------------------------------
    // LED ready: pulses on each EOC
    // --------------------------------------------------------
    always_ff @(posedge clk_1mhz or negedge rst_n) begin
        if (!rst_n)
            led_ready <= 1'b0;
        else
            led_ready <= eoc;
    end

endmodule
