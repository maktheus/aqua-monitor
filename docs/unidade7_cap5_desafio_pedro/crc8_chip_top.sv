// =============================================================================
// crc8_chip_top.sv -- Top-level CRCChip v1.0
// Unidade 7 | Capitulo 5 | PADIS
// Autor : Pedro Victor dos Santos Oliveira
// Prof. : Thiago Brito
// =============================================================================

module crc8_chip_top (
    input  logic [7:0] data_in,     // byte de entrada
    input  logic [7:0] crc_in,      // CRC acumulado anterior
    output logic [7:0] crc_out,     // CRC resultante
    output logic       zero_flag    // indica CRC == 0x00
);

    crc8 u_crc8 (
        .data_in (data_in),
        .crc_in  (crc_in),
        .crc_out (crc_out)
    );

    assign zero_flag = (crc_out == 8'h00);

endmodule
