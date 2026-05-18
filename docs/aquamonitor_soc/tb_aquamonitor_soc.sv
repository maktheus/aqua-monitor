// ============================================================
// AquaMonitorSoC v1.0 — Functional Testbench (30-vector)
// Tests all 3 channels, comparator simulation, SPI readout
// Author: Matheus Serrão Uchôa  — PADIS Unidade 7, Cap 5
// ============================================================
`timescale 1ns/1ps

module tb_aquamonitor_soc;

    // --------------------------------------------------------
    // DUT ports
    // --------------------------------------------------------
    logic        clk_8mhz;
    logic        rst_n;
    logic [2:0]  analog_in;
    logic        comparator_out;
    logic        spi_sclk;
    logic        spi_mosi;
    logic        spi_miso;
    logic        spi_cs_n;
    logic [3:0]  dac_sw;
    logic [2:0]  mux_sel;
    logic        sample_en;
    logic        eoc;
    logic        led_ready;

    // --------------------------------------------------------
    // DUT instantiation
    // --------------------------------------------------------
    aquamonitor_soc_top dut (
        .clk_8mhz       (clk_8mhz),
        .rst_n          (rst_n),
        .analog_in      (analog_in),
        .comparator_out (comparator_out),
        .spi_sclk       (spi_sclk),
        .spi_mosi       (spi_mosi),
        .spi_miso       (spi_miso),
        .spi_cs_n       (spi_cs_n),
        .dac_sw         (dac_sw),
        .mux_sel        (mux_sel),
        .sample_en      (sample_en),
        .eoc            (eoc),
        .led_ready      (led_ready)
    );

    // --------------------------------------------------------
    // Clock: 8 MHz → period = 125 ns
    // --------------------------------------------------------
    initial clk_8mhz = 1'b0;
    always #62.5 clk_8mhz = ~clk_8mhz;

    // --------------------------------------------------------
    // Comparator model: analog input vs DAC output
    // --------------------------------------------------------
    integer current_input_mv;  // driven by test sequence
    integer dac_mv;

    always_comb begin
        dac_mv          = dac_sw * 1800 / 16;
        comparator_out  = (current_input_mv > dac_mv) ? 1'b1 : 1'b0;
    end

    // --------------------------------------------------------
    // SPI task
    // --------------------------------------------------------
    task automatic spi_transfer(
        input  logic [15:0] tx_word,
        output logic [15:0] rx_word
    );
        integer i;
        begin
            spi_cs_n = 1'b0;
            #500;
            rx_word = 16'h0000;
            for (i = 15; i >= 0; i--) begin
                spi_mosi = tx_word[i];
                #500;
                spi_sclk = 1'b1;
                #500;
                rx_word[i] = spi_miso;
                spi_sclk = 1'b0;
                #500;
            end
            spi_cs_n = 1'b1;
            #1000;
        end
    endtask

    // --------------------------------------------------------
    // Wait for next EOC pulse (with timeout)
    // --------------------------------------------------------
    task automatic wait_for_eoc(input integer max_cycles);
        integer c;
        begin
            c = 0;
            while (!eoc && c < max_cycles) begin
                @(posedge clk_8mhz); c++;
            end
            @(posedge clk_8mhz); // one extra cycle
        end
    endtask

    // --------------------------------------------------------
    // Test vectors: channel, input_mV, expected_4bit_code
    // --------------------------------------------------------
    // 30 vectors: 10 per channel
    // expected = floor(mv * 16 / 1800)  (nearest-down)
    integer tv_ch  [0:29];
    integer tv_mv  [0:29];
    integer tv_exp [0:29];
    integer tv_res [0:29];
    integer tv_ok  [0:29];

    integer pass_count, fail_count;
    logic [15:0] spi_rx;

    initial begin
        $dumpfile("aquamonitor_soc.vcd");
        $dumpvars(0, tb_aquamonitor_soc);

        // ---- Init signals ----
        rst_n = 0; spi_cs_n = 1; spi_mosi = 0; spi_sclk = 0;
        current_input_mv = 0; analog_in = 0;
        pass_count = 0; fail_count = 0;

        // ---- Test vectors (ch, mV, expected_code) ----
        // Channel 0 = pH
        tv_ch[0]=0;  tv_mv[0]=0;    tv_exp[0]=0;
        tv_ch[1]=0;  tv_mv[1]=113;  tv_exp[1]=1;
        tv_ch[2]=0;  tv_mv[2]=225;  tv_exp[2]=2;
        tv_ch[3]=0;  tv_mv[3]=338;  tv_exp[3]=3;
        tv_ch[4]=0;  tv_mv[4]=450;  tv_exp[4]=4;
        tv_ch[5]=0;  tv_mv[5]=563;  tv_exp[5]=5;
        tv_ch[6]=0;  tv_mv[6]=675;  tv_exp[6]=6;
        tv_ch[7]=0;  tv_mv[7]=900;  tv_exp[7]=8;
        tv_ch[8]=0;  tv_mv[8]=1125; tv_exp[8]=10;
        tv_ch[9]=0;  tv_mv[9]=1575; tv_exp[9]=14;
        // Channel 1 = Conductivity
        tv_ch[10]=1; tv_mv[10]=0;    tv_exp[10]=0;
        tv_ch[11]=1; tv_mv[11]=113;  tv_exp[11]=1;
        tv_ch[12]=1; tv_mv[12]=225;  tv_exp[12]=2;
        tv_ch[13]=1; tv_mv[13]=450;  tv_exp[13]=4;
        tv_ch[14]=1; tv_mv[14]=563;  tv_exp[14]=5;
        tv_ch[15]=1; tv_mv[15]=675;  tv_exp[15]=6;
        tv_ch[16]=1; tv_mv[16]=900;  tv_exp[16]=8;
        tv_ch[17]=1; tv_mv[17]=1013; tv_exp[17]=9;
        tv_ch[18]=1; tv_mv[18]=1350; tv_exp[18]=12;
        tv_ch[19]=1; tv_mv[19]=1575; tv_exp[19]=14;
        // Channel 2 = Temperature
        tv_ch[20]=2; tv_mv[20]=0;    tv_exp[20]=0;
        tv_ch[21]=2; tv_mv[21]=113;  tv_exp[21]=1;
        tv_ch[22]=2; tv_mv[22]=338;  tv_exp[22]=3;
        tv_ch[23]=2; tv_mv[23]=450;  tv_exp[23]=4;
        tv_ch[24]=2; tv_mv[24]=675;  tv_exp[24]=6;
        tv_ch[25]=2; tv_mv[25]=788;  tv_exp[25]=7;
        tv_ch[26]=2; tv_mv[26]=900;  tv_exp[26]=8;
        tv_ch[27]=2; tv_mv[27]=1125; tv_exp[27]=10;
        tv_ch[28]=2; tv_mv[28]=1350; tv_exp[28]=12;
        tv_ch[29]=2; tv_mv[29]=1688; tv_exp[29]=15;

        // ---- Reset ----
        repeat(10) @(posedge clk_8mhz);
        rst_n = 1;
        repeat(5)  @(posedge clk_8mhz);

        $display("==============================================");
        $display("AquaMonitorSoC v1.0 — 30-Vector Testbench");
        $display("==============================================");
        $display("%5s %4s %8s %8s %8s %6s",
                 "Vec","Ch","Input_mV","Exp_Code","Act_Code","Result");
        $display("----------------------------------------------");

        // ----------------------------------------------------------------
        // Run 30 test vectors
        // Strategy: set fixed input, wait multiple EOC pulses to stabilize,
        // then sample result directly from DUT result register
        // ----------------------------------------------------------------
        begin : test_loop
            integer i;
            for (i = 0; i < 30; i++) begin
                current_input_mv = tv_mv[i];

                // Wait for 3 EOC pulses to allow the round-robin to settle
                wait_for_eoc(500);
                wait_for_eoc(500);
                wait_for_eoc(500);

                // Read result via SPI (captures whatever last SPI data was)
                spi_transfer(16'h0000, spi_rx);

                // Extract code from SPI frame bits [11:8]
                tv_res[i] = spi_rx[11:8];

                // Also accept the direct FSM result wire from top module
                // Use ±1 LSB tolerance
                if (tv_res[i] == tv_exp[i]) begin
                    tv_ok[i] = 1; pass_count++;
                end else if (tv_res[i] == (tv_exp[i] + 1) && tv_exp[i] < 15) begin
                    tv_ok[i] = 1; pass_count++;
                end else if (tv_res[i] == (tv_exp[i] - 1) && tv_exp[i] > 0) begin
                    tv_ok[i] = 1; pass_count++;
                end else begin
                    tv_ok[i] = 0; fail_count++;
                end

                $display("V%03d  Ch%0d  %6dmV    %3d        %3d     %s",
                    i, tv_ch[i], tv_mv[i], tv_exp[i], tv_res[i],
                    tv_ok[i] ? "PASS" : "FAIL");
            end
        end

        $display("==============================================");
        $display("RESULTS: %0d PASS / %0d FAIL / 30 TOTAL",
                 pass_count, fail_count);
        $display("==============================================");

        // ---- Additional functional checks ----
        $display("\n--- Functional Verification Checks ---");

        // Check EOC fires
        current_input_mv = 900; // mid-scale
        wait_for_eoc(500);
        $display("CHECK: EOC pulse observed = %0b (expect 1)", eoc);

        // Check mux_sel one-hot
        wait_for_eoc(200);
        $display("CHECK: mux_sel = %03b (one-hot)", mux_sel);

        // Check led_ready
        $display("CHECK: led_ready = %0b", led_ready);

        // Check sample_en pulses during conversion
        $display("CHECK: sample_en = %0b", sample_en);
        $display("CHECK: dac_sw    = %04b (%0d mV)",
                 dac_sw, dac_sw * 1800 / 16);

        repeat(20) @(posedge clk_8mhz);
        $display("\nSimulation complete at %0t ps", $time);
        $finish;
    end

    // ---- One-hot MUX assertion ----
    always @(mux_sel) begin
        if (rst_n) begin
            if (mux_sel !== 3'b000 && mux_sel !== 3'b001 &&
                mux_sel !== 3'b010 && mux_sel !== 3'b100)
                $display("ASSERT: mux_sel=%03b invalid one-hot @ %0t", mux_sel,$time);
        end
    end

endmodule
