// ============================================================
// AquaMonitorSoC v1.0 — SPI Slave Interface
// 16-bit frame, CPOL=0, CPHA=0 (Mode 0)
// Frame format: [15:12]=CH_ID[3:0] | [11:8]=RESULT[3:0] | [7:0]=STATUS[7:0]
// Author: Matheus Serrão Uchôa  — PADIS Unidade 7, Cap 5
// ============================================================
`timescale 1ns/1ps

module spi_slave (
    // SPI bus
    input  logic        sclk,       // SPI clock from master
    input  logic        mosi,       // Master Out Slave In
    input  logic        cs_n,       // Chip Select (active-low)

    // Parallel data interface (from SoC registers)
    input  logic [15:0] data_in,    // 16-bit word to shift out on MISO

    // Outputs
    output logic        miso,       // Master In Slave Out
    output logic [15:0] data_out,   // received word from master
    output logic        valid       // 1 = data_out holds a complete frame
);

    // --------------------------------------------------------
    // Shift register and bit counter
    // --------------------------------------------------------
    logic [15:0] shift_rx;          // incoming (MOSI) shift register
    logic [15:0] shift_tx;          // outgoing (MISO) shift register
    logic [4:0]  bit_cnt;           // counts 0..15

    // Load TX shift register on falling edge of cs_n (before transaction)
    // We detect cs_n deassertion to latch data_in
    logic cs_n_prev;

    // --------------------------------------------------------
    // RX: sample MOSI on rising edge of sclk
    // TX: update MISO on falling edge of sclk (or cs_n assert)
    // --------------------------------------------------------

    // Rising-edge: sample MOSI and shift RX register
    always_ff @(posedge sclk or posedge cs_n) begin
        if (cs_n) begin
            bit_cnt   <= 5'd0;
            shift_rx  <= 16'h0000;
            valid     <= 1'b0;
        end else begin
            // Shift in MSB first
            shift_rx <= {shift_rx[14:0], mosi};
            bit_cnt  <= bit_cnt + 5'd1;
            if (bit_cnt == 5'd15) begin
                data_out <= {shift_rx[14:0], mosi}; // latch on last bit
                valid    <= 1'b1;
            end else begin
                valid <= 1'b0;
            end
        end
    end

    // --------------------------------------------------------
    // TX: load shift_tx when CS asserts, shift on falling SCLK
    // --------------------------------------------------------
    always_ff @(negedge sclk or posedge cs_n) begin
        if (cs_n) begin
            shift_tx <= data_in;    // pre-load parallel data
        end else begin
            shift_tx <= {shift_tx[14:0], 1'b0}; // shift left, MSB out
        end
    end

    // MISO drives MSB of TX shift register when selected
    assign miso = cs_n ? 1'bz : shift_tx[15];

    // --------------------------------------------------------
    // Frame format reference:
    //   Bits [15:12] = CH_ID[3:0]   (which sensor channel)
    //   Bits [11:8]  = RESULT[3:0]  (4-bit ADC code)
    //   Bits [7:0]   = STATUS[7:0]
    //     [7]   = EOC (end of conversion)
    //     [6]   = OVERRUN (new result before read)
    //     [5:2] = reserved
    //     [1:0] = CH_SEL_ECHO[1:0]
    // --------------------------------------------------------

endmodule
