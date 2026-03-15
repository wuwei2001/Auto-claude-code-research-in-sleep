# Literature Landscape Summary

**Research Direction**: 复杂的生物物理建模 + 多模态 Virtual 单细胞在神经毒理学的应用
**Date**: 2026-03-14

## 1. Virtual Cell Models (虚拟细胞模型)

### 1.1 VCWorld (arXiv 2512.00306)
- White-box biological world model integrating structured biological knowledge with LLMs
- Simulates cellular responses to perturbations with interpretable, stepwise predictions
- State-of-the-art on drug perturbation benchmarks
- **Gap**: Focuses on gene expression perturbation, not biophysical/electrophysiological properties

### 1.2 TwinCell (bioRxiv 2026)
- Large Causal Cell Model (LCCM) integrating single-cell foundation model embeddings with multiomics
- Bridges in vitro experiments to clinical insights
- **Gap**: No electrophysiological modeling component

### 1.3 AI-driven Virtual Cell Models (Nature npj Digital Medicine 2025)
- Review: Multimodal omics data + deep generative models + graph neural networks
- Predictions at subcellular, single-cell, and cell-population levels
- Validated via CRISPR assays and organoid platforms

## 2. Single-Cell Foundation Models (单细胞基础模型)

### 2.1 CAPTAIN (bioRxiv 2025)
- Pretrained on 4M+ cells with concurrent transcriptome + 382 surface protein measurements
- Excels at protein imputation, cell type annotation, batch harmonization

### 2.2 scMomer (bioRxiv 2025)
- Modality-aware pretraining for multi-omics under missing modality conditions
- Strong on drug response and perturbation prediction tasks

### 2.3 Multimodal Benchmarking (bioRxiv 2025)
- Evaluates foundation model representations for cellular perturbation response prediction

## 3. Biophysical Neuron Modeling + ML (生物物理神经元建模 + 机器学习)

### 3.1 Deep Hybrid Modeling for Alzheimer's (2025)
- DeepHM: cGAN + Hodgkin-Huxley conductance-based models
- Maps experimental hippocampal neuron data to HH parameter space
- Identifies disrupted ion channels in disease conditions

### 3.2 BPTT for Hodgkin-Huxley (bioRxiv 2025)
- Backpropagation-through-time training of unrolled HH models
- Auto-recovers Na+, K+, leak conductances from single voltage recordings

### 3.3 ElectroPhysiomeGAN (eLife 2024)
- GAN + RNN generates >170 HH model parameters from membrane potential responses
- Validated on C. elegans neurons; fast inference

## 4. Neurotoxicology Applications (神经毒理学应用)

### 4.1 Time-resolved Multi-omic Analysis (Nature Cell Death & Disease 2026)
- Paclitaxel exposure in iPSC-derived sensory neurons
- Sequential RNA-seq + deep proteome + lipidomics
- Identified neuroinflammation, stress response, metabolic disruption signatures

### 4.2 iPSC-derived Neural Models (Frontiers 2026)
- Combined morphological (neurite outgrowth) + electrophysiological (MEA) endpoints
- Drug neurotoxicity screening with functional readouts

### 4.3 MoltiTox (PMC 2025)
- Multimodal fusion model for molecular toxicity prediction
- Combines molecular structure with biological assay data

## 5. Identified Gaps (关键空白)

| Gap | Description | Opportunity |
|-----|-------------|-------------|
| **G1: Omics → Biophysics Bridge** | No framework translates scRNA-seq/proteomics data into biophysical model (HH) parameters | Build a multimodal translator: omics embeddings → ion channel conductances |
| **G2: Virtual Cell ≠ Virtual Neuron** | VCWorld/TwinCell model gene perturbation, not electrophysiology | Extend virtual cell concept to include biophysical simulation layer |
| **G3: Static Toxicity Assessment** | Current neurotoxicology uses endpoint assays (morphology/MEA), not dynamic simulation | Create temporal prediction models for neurotoxic effects |
| **G4: Single-Cell Resolution Missing** | Biophysical models fit per-cell but ignore cell-to-cell heterogeneity from scRNA-seq | Leverage single-cell foundation models to parameterize cell-type-specific HH models |
| **G5: No Unified Framework** | Separate communities: comp neuro (HH models), single-cell genomics, toxicology | Integrative framework bridging all three |

## 6. Landscape Map

```
Single-Cell Foundation Models          Biophysical Neuron Models
(scGPT, CAPTAIN, scMomer)            (Hodgkin-Huxley, DeepHM)
         ↓                                    ↓
    Cell embeddings                   Ion channel parameters
    Perturbation prediction           Electrophysiology simulation
         ↓                                    ↓
         └──────── [GAP: No Bridge] ──────────┘
                        ↓
              Virtual Cell Models
              (VCWorld, TwinCell)
              [GAP: No electrophysiology]
                        ↓
              Neurotoxicology
              [GAP: Endpoint-only, no simulation]
```

## 7. Key Open Problems

1. **How to map from transcriptomic profiles to biophysical parameters?** (Gene expression → ion channel conductance mapping)
2. **Can single-cell heterogeneity predict differential neurotoxic susceptibility?** (Why some neurons die and others survive)
3. **Can we simulate neurotoxic effects before they happen?** (Predictive virtual neuron model)
4. **How to validate virtual neuron predictions against real electrophysiology?** (MEA/patch-clamp ground truth)
