# AI Compute: Semiconductor Supply Chain and the Bottleneck Cascade

## Definitive Nucleosynthesis Entry

---

### Provenance

| Field | Value |
|---|---|
| Fusion date | 2026-03-01 |
| Source 00271 | Korean social media post: 8-stage sequential bottleneck timeline (CPU→GPU→HBM→CoWoS→Power→Photonics→1nm→Data), 2020–2030+ |
| Source 01476 | CNBC: NVIDIA vs Google/Amazon custom ASICs, inference demand growing faster than training, three-category chip taxonomy |
| Source 01888/01890 | CNBC interview: ASML High NA EUV ($400M/machine, only 5 shipped), TI $60B megaproject (7 fabs), Apple vertical integration |
| Source 02002 | Intel 18A node at Arizona fab, U.S. government 10% stake, no major external customers yet |
| Source 03394 | DRAM shortage causing price surges, manufacturers shifting from low-margin to HBM/GDDR |
| Fusion type | Nucleosynthesis — five sources fused into unified treatment of the AI compute supply chain |

---

## 1. The Bottleneck Cascade

The defining characteristic of the AI compute supply chain is that bottlenecks do not resolve — they cascade. When one constraint is solved, the system immediately saturates the next layer. Source 00271 maps this as an 8-stage sequential timeline running from 2020 through the 2030s.

The cascade matters for investment and strategy because tracking where the current bottleneck sits reveals where value will concentrate next. "Track the walls to find the golden key" — when HBM supply eases, the constraint immediately slides to packaging or power.

---

## 2. Stage-by-Stage Analysis

### Stage 1: CPU → GPU Transition (2020–2022) — RESOLVED

CPUs are serial processors. GPUs have thousands of parallel cores. The switch from CPU to GPU training delivered 10x–100x speedups. NVIDIA locked the ecosystem in through CUDA, its proprietary software layer. By 2022, the GPU transition was complete and the bottleneck shifted upstream.

### Stage 2: Memory Wall / GDDR → HBM (2022–2024)

GPU compute outpaced memory fetch speeds. HBM (High Bandwidth Memory) — an 8-stack vertical architecture — replaced single-lane GDDR as mandatory for scaling model size. The transition is complete, but the memory wall persists as models continue to grow.

### Stage 3: HBM Supply Shortage (2024–2026, current most severe)

A single AI GPU requires 80GB–200GB of HBM. HBM prices surged 70%–100%. Three suppliers control all production: SK Hynix, Samsung, Micron. All three are struggling to keep pace with demand. NVIDIA Blackwell production was delayed. As of early 2026, chips are sold out. NVIDIA Rubin (late 2026) already faces HBM4 supply anxiety. Supply expected to ease slightly in H2 2026 as capacity expands.

Source 03394 confirms the downstream effect: the DRAM shortage is currently causing significant price increases across consumer hardware (RAM, SSDs, flash memory). Manufacturers are structurally shifting production away from lower-margin products toward high-margin HBM/GDDR — a permanent reorientation of the memory business.

**Adjacent technologies addressing the memory wall:**
- **PIM (Processor-In-Memory)**: Compute embedded inside memory to reduce data travel
- **CXL (Compute Express Link)**: External memory expansion via a standard connection interface
- **Hybrid Bonding**: Direct chip stacking eliminating wires, enabling hundreds of thousands of I/O points

### Stage 4: Advanced Packaging — CoWoS (2025–Mid 2026)

HBM must be placed directly next to the GPU on a silicon interposer. TSMC's CoWoS (Chip-on-Wafer-on-Substrate) packaging holds 90% of the advanced packaging market. NVIDIA, AMD, and Google all faced delayed shipments due to CoWoS bottlenecks. Tight supply in H1 2026; relief expected in H2 2026 from TSMC capacity expansion.

### Stage 5: The Power Wall (2025–2027)

A single modern GPU draws 700W–1000W+. AI data center demand could exceed 100GW by 2026. Grid saturation is already visible — Northern Virginia is cited as a major hurdle. This is the stage where AI infrastructure intersects with energy policy and real estate (see data center entry for full treatment).

### Stage 6: Interconnect and Photonics (2026–2028)

Traditional copper wires hit distance, heat, and bandwidth limits at tens of thousands of GPUs. The solution is CPO (Co-Packaged Optics) — replacing copper with fiber-optic interconnects. The era of CPO is beginning as of 2026.

### Stage 7: 1nm Wall / Miniaturization Limits (2027–2030+)

Below 2nm, quantum effects cause leakage and defects. ASML EUV yield is struggling. Solutions shift from shrinking transistors to architectural innovation: chiplets (stitching smaller chips), backside power delivery (TSMC and Intel targeting 2026), and CFET (Complementary FET) structures.

### Stage 8: Data and Latency Wall (2030s)

High-quality human-generated training data is running out. Speed-of-light latency becomes the bottleneck in massive distributed training. Responses: synthetic data (AI-generated training data) and Mixture of Experts (MoE) for selective model activation.

---

## 3. The ASML Chokepoint

ASML's High NA EUV lithography machine represents the single most concentrated chokepoint in the entire supply chain. Each machine took a decade to develop, costs $400 million, and is the size of a double-decker bus. Only 5 High NA machines have been shipped globally as of late 2025. High NA is the latest generation of Extreme Ultraviolet Lithography — the only technology capable of etching nanoscopic blueprints for advanced chips at Intel, TSMC, and Samsung fabs.

The dependency is near-absolute: without High NA machines, advanced chips for NVIDIA, Apple, and AMD cannot be manufactured at leading-edge nodes.

---

## 4. The ASIC Proliferation

Source 01476 identifies a structural shift: demand for AI inference is growing faster than demand for AI training. This drives interest in smaller, cheaper, purpose-built chips (ASICs) rather than general-purpose GPUs.

The hyperscalers are responding by designing their own silicon:
- **Google**: Pioneered custom AI chips with TPU
- **Amazon**: Custom Trainium/Inferentia chips
- **Meta, Microsoft**: In-house ASIC programs
- **OpenAI**: Partnership with Broadcom for custom silicon

This creates a three-category AI chip taxonomy: GPUs (general compute, NVIDIA dominance) / ASICs (custom cloud AI, hyperscaler-designed) / on-device chips (edge AI, Apple and Qualcomm). NVIDIA's strategic position is being eroded from the ASIC side as its largest customers become competitors on inference workloads.

---

## 5. U.S. Semiconductor Repatriation

Two parallel efforts to reshore advanced chip manufacturing to the United States:

**Intel 18A**: Intel is in high-volume production of its 18A node at a new Arizona fabrication plant, explicitly targeting competition with TSMC. The U.S. government has taken a 10% stake in Intel alongside billions in funding from NVIDIA and SoftBank. However, no major external customers are currently using the 18A node — Intel faces significant challenges regaining foundry customer trust after past delays and missteps.

**Texas Instruments**: Constructing a $60 billion megaproject — 7 new fabs in Utah and Texas — for customers including NVIDIA and Ford. Apple plans to manufacture critical foundation semiconductors at TI's U.S. facilities, part of its broader vertical integration strategy eliminating reliance on Broadcom and Qualcomm. Apple's chip announcements include the A19 Pro SoC (neural accelerators for AI), N1 (first Apple iPhone networking chip), and C1X (second-generation iPhone modem).

---

*This entry is the definitive treatment of the AI compute semiconductor supply chain as of 2026-03-01. All distinct reasoning paths from sources 00271, 01476, 01888/01890, 02002, and 03394 are carried forward. Subsequent discoveries should be fused into this entry, not appended alongside it.*
