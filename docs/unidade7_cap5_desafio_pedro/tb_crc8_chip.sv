// =============================================================================
// tb_crc8_chip.sv -- Testbench CRCChip v1.0
// Unidade 7 | Capitulo 5 | PADIS
// Autor : Pedro Victor dos Santos Oliveira
// Prof. : Thiago Brito
// =============================================================================
`timescale 1ns/1ps

module tb_crc8_chip;

    logic [7:0] data_in, crc_in, crc_out;
    logic       zero_flag;

    crc8_chip_top dut (
        .data_in  (data_in),
        .crc_in   (crc_in),
        .crc_out  (crc_out),
        .zero_flag(zero_flag)
    );

    integer pass = 0, fail = 0;

    task automatic check;
        input [7:0] din, cin, expected;
        input integer tnum;
        begin
            data_in = din; crc_in = cin;
            #10;
            if (crc_out === expected) begin
                $display("TESTE %0d: data=0x%02X crc_in=0x%02X => 0x%02X  [APROVADO]",
                         tnum, din, cin, crc_out);
                pass = pass + 1;
            end else begin
                $display("TESTE %0d: data=0x%02X crc_in=0x%02X => 0x%02X  [FALHOU] (esperado 0x%02X)",
                         tnum, din, cin, crc_out, expected);
                fail = fail + 1;
            end
        end
    endtask

    initial begin
        $dumpfile("dump_crc8.vcd");
        $dumpvars(0, tb_crc8_chip);

        $display("=== CRCChip v1.0 -- CRC-8/SMBUS (poly=0x07, init=0x00) ===");

        // --- Casos basicos (crc_in = 0x00) ---
        check(8'h00, 8'h00, 8'h00,  1);  // zero in, zero out
        check(8'h01, 8'h00, 8'h07,  2);  // LSB = 1 -> 0x07 (proprio polinomio)
        check(8'h02, 8'h00, 8'h0E,  3);  // deslocamento 1
        check(8'h04, 8'h00, 8'h1C,  4);  // deslocamento 2
        check(8'h07, 8'h00, 8'h15,  5);  // byte == polinomio (0x07)
        check(8'h55, 8'h00, 8'hAC,  6);  // padrao 01010101
        check(8'hAA, 8'h00, 8'h5F,  7);  // padrao 10101010
        check(8'hFF, 8'h00, 8'hF3,  8);  // todos 1s
        check(8'h0F, 8'h00, 8'h2D,  9);  // nibble baixo = 1
        check(8'hF0, 8'h00, 8'hDE, 10);  // nibble alto = 1

        // --- Cadeia de bytes (crc_in != 0x00) ---
        check(8'h02, 8'h07, 8'h1B, 11);  // CRC([0x01,0x02]) = 0x1B
        check(8'h03, 8'h1B, 8'h48, 12);  // CRC([0x01,0x02,0x03]) = 0x48
        check(8'hFF, 8'hF3, 8'h24, 13);  // CRC([0xFF,0xFF]) = 0x24
        check(8'h00, 8'hF3, 8'hD7, 14);  // CRC([0xFF,0x00]) = 0xD7

        // --- Zeros consecutivos ---
        check(8'h00, 8'h00, 8'h00, 15);
        check(8'h00, 8'h00, 8'h00, 16);

        // --- Propriedade de anulacao: CRC(x,x) = 0x00 para alguns x ---
        check(8'hAC, 8'hAC, 8'h00, 17);  // CRC(0xAC, crc_in=0xAC) = 0x00
        check(8'h07, 8'h07, 8'h00, 18);  // CRC(0x07, crc_in=0x07) = 0x00

        // --- Valores ASCII ---
        check(8'h41, 8'h00, 8'hC0, 19);  // 'A'
        check(8'h42, 8'h00, 8'hC9, 20);  // 'B'
        check(8'h43, 8'h00, 8'hCE, 21);  // 'C'
        check(8'h30, 8'h00, 8'h90, 22);  // '0'
        check(8'h39, 8'h00, 8'hAF, 23);  // '9'

        // --- Borda: bits isolados ---
        check(8'h80, 8'h00, 8'h89, 24);  // MSB = 1
        check(8'h40, 8'h00, 8'hC7, 25);  // bit 6 = 1

        // --- Padroes de alta densidade ---
        check(8'hFE, 8'h00, 8'hF4, 26);  // todos 1 exceto LSB
        check(8'h7F, 8'h00, 8'h7A, 27);  // todos 1 exceto MSB

        // --- Cadeia longa ---
        check(8'hC5, 8'h00, 8'h55, 28);  // byte arbitrario
        check(8'h3A, 8'h55, 8'h0A, 29);  // continuacao
        check(8'hF7, 8'h0A, 8'hFD, 30);  // continuacao

        $display("=== Resultado: %0d/30 APROVADOS | %0d FALHOU ===", pass, fail);
        if (fail == 0)
            $display(">>> SIMULACAO: APROVADO <<<");
        else
            $display(">>> SIMULACAO: FALHOU <<<");

        $finish;
    end

endmodule
