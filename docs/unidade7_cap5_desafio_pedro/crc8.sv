// =============================================================================
// crc8.sv -- CRCChip v1.0: Gerador/Verificador CRC-8/SMBUS
// Unidade 7 | Capitulo 5 | PADIS
// Autor : Pedro Victor dos Santos Oliveira
// Prof. : Thiago Brito
// =============================================================================
// Polinomio: G(x) = x^8 + x^2 + x + 1  (0x07 -- CRC-8/SMBUS)
// Arquitetura: 8 estagios combinacionais desdobrados (MSB-first)
//
// Interface:
//   data_in [7:0] -- byte de entrada
//   crc_in  [7:0] -- CRC acumulado anterior (0x00 para primeiro byte)
//   crc_out [7:0] -- CRC atualizado apos processar data_in
//
// Uso em cadeia (multiplos bytes):
//   crc = 8'h00;
//   for each byte b: crc = crc8(b, crc);
// =============================================================================

module crc8 (
    input  logic [7:0] data_in,   // byte a processar
    input  logic [7:0] crc_in,    // CRC acumulado (0x00 no inicio)
    output logic [7:0] crc_out    // CRC resultante
);

    // Estagio i: aplica bit data_in[7-i] sobre o registrador CRC
    // Equacao: s_i+1 = {s_i[6:0], 0} XOR (topbit ? 8'h07 : 8'h00)
    //          topbit = s_i[7] XOR data_in[7-i]
    logic [7:0] s0, s1, s2, s3, s4, s5, s6;

    assign s0 = {crc_in[6:0], 1'b0} ^ ((crc_in[7] ^ data_in[7]) ? 8'h07 : 8'h00);
    assign s1 = {s0[6:0],     1'b0} ^ ((s0[7]     ^ data_in[6]) ? 8'h07 : 8'h00);
    assign s2 = {s1[6:0],     1'b0} ^ ((s1[7]     ^ data_in[5]) ? 8'h07 : 8'h00);
    assign s3 = {s2[6:0],     1'b0} ^ ((s2[7]     ^ data_in[4]) ? 8'h07 : 8'h00);
    assign s4 = {s3[6:0],     1'b0} ^ ((s3[7]     ^ data_in[3]) ? 8'h07 : 8'h00);
    assign s5 = {s4[6:0],     1'b0} ^ ((s4[7]     ^ data_in[2]) ? 8'h07 : 8'h00);
    assign s6 = {s5[6:0],     1'b0} ^ ((s5[7]     ^ data_in[1]) ? 8'h07 : 8'h00);

    assign crc_out = {s6[6:0], 1'b0} ^ ((s6[7] ^ data_in[0]) ? 8'h07 : 8'h00);

endmodule
