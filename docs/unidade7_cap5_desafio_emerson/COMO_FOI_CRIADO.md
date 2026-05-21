# Como foi criado o Relatório do Emerson — ThermalSensorChip v1.0

## Visão Geral

O relatório técnico `relatorio_thermal.pdf` documenta o design completo do
**ThermalSensorChip v1.0**, um sensor de temperatura PTAT em processo CMOS 0,18 µm,
desenvolvido por Emerson Paes de Souza Borges para a disciplina PADIS (Unidade 7,
Capítulo 5). O trabalho foi produzido inteiramente com ferramentas open-source e
Python, seguindo as normas ABNT (NBR 14724).

---

## Arquivos produzidos

| Arquivo | Tipo | Propósito |
|---|---|---|
| `thermal_sensor.cir` | SPICE netlist | Circuito elétrico completo do chip |
| `gerar_figuras_thermal.py` | Python | Diagrama de arquitetura, curvas V_BE e simulação PTAT |
| `gerar_esquematicos_thermal.py` | Python | Esquemáticos elétricos (PTAT, BJT, chip completo) |
| `gerar_layout_fisico_thermal.py` | Python | Layout físico (célula BJT e die completo) |
| `relatorio_thermal.tex` | LaTeX | Documento final do relatório |
| `relatorio_thermal.pdf` | PDF | Saída compilada para entrega |

---

## Passo 1 — Netlist SPICE (`thermal_sensor.cir`)

O primeiro artefato criado foi a descrição elétrica do chip em formato SPICE.

**O que o netlist define:**

- Tensão de alimentação: `VDD = 1,8 V`
- Espelho de corrente PMOS com três transistores:
  - `M1` (W/L = 10 µm / 0,5 µm) — diodo-conectado, define `I_REF = 10 µA`
  - `M2` (10/0,5) — cópia do espelho, alimenta `Q1`
  - `M3` (80/0,5, 8×) — cópia 8× do espelho, alimenta o array `Q2`
- Par de BJTs NPN de substrato:
  - `Q1` — BJT de referência (diodo-conectado)
  - `Q2_1` a `Q2_8` — array de 8 BJTs paralelos (emulando razão de área N=8)
- Rede resistiva PTAT:
  - `R1 = 5 kΩ` (poly) — define condição de polarização
  - `R2 = 20 kΩ` (poly) — amplifica a tensão PTAT (ganho R2/R1 = 4×)
- Modelo BJT inline: `NPN_SUB` com `IS=1e-18`, `BF=100`, `VA=50`, `EG=1.12`

**Análises SPICE configuradas:**

```spice
.temp 27
.op                      * ponto de operação
.dc TEMP -40 125 5       * varredura de temperatura
.probe V(n1) V(n2) V(delta) V(vbias)
```

**Resultado esperado:**  
`V(delta)` ≈ 252 mV @ −40 °C e ≈ 594 mV @ 125 °C → sensibilidade ≈ 2,07 mV/°C.

---

## Passo 2 — Figuras de análise (`gerar_figuras_thermal.py`)

Gerou **5 figuras PNG** (150 dpi, P&B) com `matplotlib` + `numpy`.

### Bibliotecas usadas

```python
import numpy as np
import matplotlib
matplotlib.use('Agg')          # renderização sem display (headless)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
```

### Figura 1 — Diagrama de arquitetura (`fig_arquitetura_thermal.png`)

Diagrama de blocos do sistema com 4 estágios:

```
Sensor BJT → Espelho PMOS → Rede PTAT → V_PTAT saída
```

Cada bloco desenhado com `FancyBboxPatch`; setas com `ax.annotate(..., arrowprops=...)`.

### Figura 2 — Curvas V_BE e ΔV_BE (`fig_char_vbe.png`)

Modelo analítico implementado em NumPy:

```python
T_K = T + 273.15
VBE = VBG - (VBG - VBE0) * (T_K / T0_K) + k * T_K * np.log(T_K / T0_K)
DVBE = k * T_K * np.log(N) * 1000   # N = 8 BJTs em paralelo
```

Dois subplots lado a lado (V_BE linear decrescente, ΔV_BE linear crescente com
hachura de preenchimento via `ax.fill_between`).

### Figura 3 — Simulação PTAT pré vs. pós-layout (`fig_sim_ptat.png`)

Dois traços lineares:
- **Pré-layout**: 252 → 594 mV (sensibilidade ≈ 2,07 mV/°C)
- **Pós-layout**: degradação de 2% na inclinação + offset de 3 mV

Área entre as curvas preenchida com `fill_between` (hachura cinza) para realçar o
desvio introduzido por efeitos parasitários do layout.

### Figura 4 — Layout físico simplificado (`fig_layout_thermal.png`)

Mapa de camadas do die (30 µm × 40 µm) usando `Rectangle` com hachuras distintas por
tipo de camada:

| Hachura | Camada |
|---|---|
| `------` | N-Well |
| `....` | Ativo (PMOS) |
| `////` | Poly (gates/resistores) |
| `\\\\` | BJT NPN substrato |
| sólido escuro | Trilhas Metal-2 |

### Figura 5 — Painel LVS e DRC (`fig_lvs_drc.png`)

Dois painéis de texto (fonte monospace) simulando saída de ferramenta EDA:

```
LVS REPORT — 0 ERRORS, 0 WARNINGS
  5 instâncias MOSFET correspondidas
  2 pares BJT correspondidos
  2 resistores poly correspondidos
  STATUS: APROVADO

DRC REPORT — 0 VIOLAÇÕES
  Espaçamento mínimo: OK
  Largura mínima: OK
  ...
  STATUS: APROVADO
```

---

## Passo 3 — Esquemáticos elétricos (`gerar_esquematicos_thermal.py`)

Gerou **3 esquemáticos PNG** desenhando símbolos de componentes manualmente via
primitivas matplotlib (linhas, círculos, setas).

### Funções de componentes implementadas

```python
def draw_pmos(ax, cx, cy, scale, label)   # Símbolo MOSFET PMOS com bolha na gate
def draw_npn(ax, cx, cy, scale, label)    # Símbolo BJT NPN com seta no emissor
def draw_resistor(ax, x1, y1, x2, y2)    # Zigzag para resistor (vertical ou horizontal)
def draw_gnd(ax, x, y)                   # Símbolo GND com 3 linhas decrescentes
def draw_vdd(ax, x, y, label)            # Símbolo VDD com linha horizontal espessa
```

### Esquemático 1 — Célula PTAT completa (`fig_schem_ptat_cell.png`)

- Espelho PMOS: M1 (diodo-conectado) + M2 (cópia 1×) + M3 (cópia 8×)
- BJTs: Q1 (referência) + Q2×8 (array)
- Rede R1/R2 com nó de saída V_PTAT
- Equações renderizadas com LaTeX inline do matplotlib:
  ```python
  r'$\Delta V_{BE} = V_T\ln(N)$'
  r'$V_{PTAT} = \frac{R_2}{R_1}\Delta V_{BE}$'
  ```

### Esquemático 2 — Princípio do sensor BJT (`fig_schem_bjt_sensor.png`)

- Símbolo NPN grande com anotações B/C/E
- Tabela V_BE vs. temperatura desenhada linha a linha com `FancyBboxPatch`
- Equações físicas do modelo de Gummel-Poon

### Esquemático 3 — Visão completa do chip (`fig_schem_chip_full.png`)

- Borda do die com todos os blocos internos (espelho, BJTs, resistores)
- Pads de I/O (VDD, GND, V_PTAT OUT)
- Caixa de especificações com todos os parâmetros do chip

---

## Passo 4 — Layout físico detalhado (`gerar_layout_fisico_thermal.py`)

Gerou **2 figuras de layout** com `matplotlib.patches.Rectangle` e hachuras.

### Figura 1 — Zoom célula BJT Q1 vs. Q2×8 (`fig_layout_bjt_cell.png`)

Desenho em escala da célula unitária BJT com todas as camadas de processo:
- N-Well, P-Base, P+ Emitter, N+ Collector ring
- Contatos de metal representados como quadrados pretos 0,4 µm × 0,4 µm
- Array Q2×8 com padrão **ABBA common-centroid** (reduz mismatch por gradiente
  térmico):

```python
abba_label = ['A', 'B', 'B', 'A'][row]   # padrão de disposição das células
```

- Guard rings tracejados ao redor de cada bloco BJT

### Figura 2 — Die completo (`fig_layout_die_full.png`)

Vista top-level do die 30 µm × 40 µm com todos os blocos posicionados:
- Trilha VDD (Metal-2, topo) e GND (Metal-2, base)
- Espelho PMOS + Poly gates (Metal-1 routing)
- Bloco Q1 + Array Q2×8 com guard rings
- Resistores R1 e R2 em Poly
- Pad de saída V_PTAT
- Cotas dimensionais com setas bidirecionais (`arrowstyle='<->'`)

---

## Passo 5 — Documento LaTeX (`relatorio_thermal.tex`)

### Pacotes utilizados

| Pacote | Função |
|---|---|
| `babel` / `inputenc` | Português brasileiro, UTF-8 |
| `geometry` | Margens ABNT (top 3 cm, left 3 cm, right 2 cm, bottom 2 cm) |
| `setspace` + `onehalfspacing` | Espaçamento 1,5 conforme ABNT |
| `tikz` + `pgfplots` | Diagrama de blocos na capa |
| `tcolorbox` | Caixas estilizadas (especificações, resultados) |
| `listings` | Código SPICE com syntax highlight |
| `booktabs` + `longtable` | Tabelas de dados técnicos |
| `amsmath` + `siunitx` | Equações e unidades SI formatadas |
| `fancyhdr` | Cabeçalho/rodapé customizado |
| `hyperref` | Links internos no PDF |

### Estrutura do documento

```
Capa (logos Softex + CI Inovador, diagrama TikZ)
Folha de rosto (ABNT NBR 14724)
Resumo / Abstract
Sumário
1. Introdução e motivação
2. Especificações de projeto
3. Fundamentação teórica (V_BE(T), ΔVBE, célula Widlar)
4. Netlist SPICE (listagem completa com lstlisting)
5. Resultados de simulação (figuras geradas em Python)
6. Layout físico (figuras geradas em Python)
7. Verificação LVS/DRC
8. Conclusão
Referências
```

### Capa — Logotipo CI Inovador em TikZ

Logo gerado inline em LaTeX (sem arquivo externo):

```latex
\node[regular polygon,regular polygon sides=6,draw=black,thick,...] (hex) at (0,0) {};
\draw[thick,line cap=round] (hex.center) -- ++(0.18, 0.18);
\node[font=\bfseries\large\sffamily] at (2.1,0) {CI Inovador};
```

### Ambiente de código SPICE customizado

```latex
\lstdefinelanguage{SPICE}{
  morekeywords={.model,.include,.temp,.op,.dc,.probe,.end,...},
  morecomment=[l]{*},       % comentários começam com *
}
```

---

## Resumo das ferramentas

| Ferramenta | Versão / Observação | Uso |
|---|---|---|
| **Python 3** | stdlib + pip | Execução de todos os scripts |
| **matplotlib** | backend `Agg` (headless) | Todas as figuras (gráficos, layout, esquemáticos) |
| **numpy** | cálculo numérico | Modelos físicos (V_BE, ΔV_BE, PTAT) |
| **SPICE (NGspice)** | netlist `.cir` | Definição e simulação do circuito |
| **LaTeX** | pdflatex | Compilação do relatório em PDF |
| **TikZ** | lib LaTeX | Diagrama de blocos na capa |
| **tcolorbox** | lib LaTeX | Caixas de especificações e resultados |
| **listings** | lib LaTeX | Syntax highlight do código SPICE |

---

## Fluxo completo de produção

```
1. Projetar o circuito
        ↓
2. Escrever o netlist SPICE (thermal_sensor.cir)
        ↓
3. Executar os 3 scripts Python para gerar as 10 figuras PNG
   ├── gerar_figuras_thermal.py       → 5 figuras (arquitetura, curvas, simulação, layout, LVS/DRC)
   ├── gerar_esquematicos_thermal.py  → 3 esquemáticos elétricos
   └── gerar_layout_fisico_thermal.py → 2 figuras de layout físico
        ↓
4. Compilar o LaTeX
   pdflatex relatorio_thermal.tex
   pdflatex relatorio_thermal.tex   (2ª passagem para referências cruzadas)
        ↓
5. Resultado: relatorio_thermal.pdf (entrega final)
```

---

*Documento gerado automaticamente a partir da análise dos artefatos em
`docs/unidade7_cap5_desafio_emerson/`.*
