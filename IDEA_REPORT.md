# Research Idea Report

**Direction**: 复杂的生物物理建模 + 多模态 Virtual 单细胞在神经毒理学的应用
**Generated**: 2026-03-14
**Pipeline**: research-lit → idea-creator → novelty-check → research-review
**Ideas evaluated**: 10 generated → filtering in progress

## Landscape Summary

The intersection of biophysical neuron modeling, single-cell foundation models, and neurotoxicology represents a rapidly growing but fragmented field. Three communities operate largely independently:

1. **Computational neuroscience** builds detailed Hodgkin-Huxley (HH) and compartmental models of individual neurons, with recent ML advances (DeepHM, ElectroPhysiomeGAN, BPTT-HH) enabling automated parameter fitting from electrophysiology recordings.

2. **Single-cell genomics** has produced powerful foundation models (scGPT, CAPTAIN, scMomer, Geneformer) that embed cells into continuous latent spaces based on transcriptomic/proteomic profiles, enabling perturbation prediction and drug response modeling.

3. **Neurotoxicology** relies on endpoint-based assays (morphology, MEA) on iPSC-derived neurons to screen compounds, with recent multi-omic studies (paclitaxel neurotoxicity) revealing molecular mechanisms.

The critical gap is the absence of a framework that bridges these domains: no existing work translates single-cell omics profiles into biophysical parameters for mechanistic neurotoxicity simulation.

## Ranked Ideas

### 🏆 Idea 1: OmicsToHH — Multimodal Omics-to-Biophysics Translator
- **Hypothesis**: Single-cell transcriptomic profiles of ion channel genes (SCN1A, KCNQ2, etc.) can be mapped to Hodgkin-Huxley conductance parameters via a learned translator, enabling cell-type-specific biophysical simulation from scRNA-seq alone.
- **Minimum experiment**: Train a neural network on paired data (patch-clamp recordings + scRNA-seq from the same cell types in Allen Brain Atlas). Predict HH parameters from gene expression, simulate AP shape, compare with ground truth.
- **Expected outcome**: If successful, R² > 0.7 on AP waveform prediction from transcriptomics. If fails, reveals which ion channel genes are insufficient for biophysical prediction.
- **Novelty**: 8/10 — No existing work maps scRNA-seq → HH parameters. DeepHM maps electrophysiology → HH but not omics → HH.
- **Feasibility**: HIGH — Allen Brain Atlas has paired electrophys + transcriptomics data. 2-4 GPU-days.
- **Risk**: MEDIUM — Gene expression may not linearly predict functional conductance (post-translational modifications).
- **Contribution type**: New method + empirical finding
- **Pilot result**: SKIPPED (no GPU available)
- **Reviewer's likely objection**: Gene expression is a noisy proxy for protein function; post-translational regulation not captured.
- **Why we should do this**: This directly bridges G1 (the omics-to-biophysics gap) and would be the first tool enabling mechanistic neuron simulation from scRNA-seq data.

### Idea 2: VirtualNeuronTox — Virtual Neuron Digital Twin for Toxicity Screening
- **Hypothesis**: A "virtual neuron" digital twin, parameterized by cell-type-specific biophysical properties derived from scRNA-seq, can predict neurotoxic effects (action potential disruption, firing rate changes) before wet-lab validation.
- **Minimum experiment**: Build virtual neurons for 5 cell types (cortical excitatory, inhibitory, DRG sensory, motor, dopaminergic). Simulate exposure to 10 known neurotoxicants (lead, methylmercury, acrylamide, etc.) by modifying channel conductances based on known pharmacological targets. Validate against published MEA data.
- **Expected outcome**: Correctly classify 7/10 known neurotoxicants as excitotoxic, inhibitory, or axonopathic.
- **Novelty**: 9/10 — No existing virtual neuron system integrates scRNA-seq parameterization with toxicity simulation.
- **Feasibility**: MEDIUM — Requires building on Idea 1; depends on OmicsToHH accuracy.
- **Risk**: HIGH — Multi-step pipeline; errors compound.
- **Contribution type**: New method (framework)
- **Pilot result**: SKIPPED (no GPU)
- **Reviewer's likely objection**: Too many assumptions in the pipeline; hard to validate end-to-end.
- **Why we should do this**: If it works, this replaces expensive animal testing with in-silico screening.

### Idea 3: NeuroCellHet — Single-Cell Heterogeneity Explains Differential Neurotoxic Susceptibility
- **Hypothesis**: The cell-to-cell variability in ion channel gene expression (captured by scRNA-seq) predicts which individual neurons are most susceptible to specific neurotoxicants, explaining the clinical observation that neurotoxicity affects some neurons but spares others.
- **Minimum experiment**: From published scRNA-seq datasets of DRG sensory neurons (relevant to chemotherapy-induced neuropathy), cluster cells by ion channel expression profiles. Simulate each cluster's susceptibility to paclitaxel (which targets tubulin → affects axonal transport → reduces sodium channel trafficking). Compare predicted susceptibility pattern with published experimental vulnerability data.
- **Expected outcome**: At least 2 distinct susceptibility subpopulations identified, correlating with clinical findings on CIPN.
- **Novelty**: 7/10 — Differential susceptibility is a clinical observation, but nobody has used scRNA-seq + biophysical modeling to explain it mechanistically.
- **Feasibility**: HIGH — Published datasets available; computational only.
- **Risk**: LOW — Even negative result (heterogeneity doesn't predict susceptibility) is interesting.
- **Contribution type**: Empirical finding + diagnostic
- **Pilot result**: SKIPPED (no GPU)
- **Reviewer's likely objection**: Observational, not causal. Would need perturbation experiments.
- **Why we should do this**: LOW RISK, high clinical relevance. Publishable regardless of outcome direction.

### Idea 4: MultiModal-NeuroPert — Foundation Model Fine-tuning for Neurotoxic Perturbation Prediction
- **Hypothesis**: Fine-tuning a pre-trained single-cell foundation model (scGPT/Geneformer/CAPTAIN) on paired neurotoxicant-exposure scRNA-seq data enables zero-shot prediction of transcriptomic responses to unseen neurotoxicants.
- **Minimum experiment**: Fine-tune scGPT on 3-4 published neurotoxicant scRNA-seq datasets (paclitaxel, cisplatin, vincristine on iPSC neurons). Test zero-shot prediction on held-out compound. Evaluate by correlation of predicted vs actual gene expression changes.
- **Expected outcome**: R > 0.5 correlation on unseen neurotoxicant, outperforming baseline (average response).
- **Novelty**: 6/10 — Perturbation prediction exists for gene knockouts (CPA, GEARS); applying to neurotoxicant chemical perturbation is novel but incremental.
- **Feasibility**: HIGH — scGPT is open-source; datasets exist.
- **Risk**: LOW — Well-established approach in a new domain.
- **Contribution type**: Empirical finding
- **Pilot result**: SKIPPED (no GPU)
- **Reviewer's likely objection**: Incremental — "just applying X to Y."
- **Why we should do this**: Safe first paper; builds dataset and baseline for more ambitious ideas.

### Idea 5: BioPhysEmbed — Joint Embedding Space for Electrophysiology and Transcriptomics
- **Hypothesis**: A contrastive learning framework can learn a shared embedding space between single-cell transcriptomics and electrophysiology recordings (Patch-seq data), enabling cross-modal prediction and revealing biologically meaningful correspondences.
- **Minimum experiment**: Use Patch-seq datasets (Allen Brain Atlas, ~3000 cells with paired scRNA-seq + electrophysiology). Train a CLIP-style model: one encoder for transcriptomics, one for electrophysiology features (AP shape, firing pattern, input resistance). Evaluate on held-out cells: given transcriptomics, retrieve matching electrophysiology profile.
- **Expected outcome**: Top-5 retrieval accuracy > 60%. Embedding clusters align with known cell types.
- **Novelty**: 8/10 — Contrastive learning applied to Patch-seq is novel. Existing work treats these as separate modalities.
- **Feasibility**: HIGH — Patch-seq data publicly available. 1-2 GPU-days.
- **Risk**: LOW-MEDIUM — CLIP-style contrastive learning is well-understood.
- **Contribution type**: New method + empirical finding
- **Pilot result**: SKIPPED (no GPU)
- **Reviewer's likely objection**: Dataset too small (3K cells); may not generalize.
- **Why we should do this**: Creates the foundational tool for ALL other ideas (especially Idea 1).

### Idea 6: TempTox — Temporal Dynamics Prediction of Neurotoxic Exposure
- **Hypothesis**: By combining time-resolved scRNA-seq data with biophysical simulations, we can predict the temporal trajectory of neuronal functional decline during neurotoxic exposure, not just the endpoint.
- **Minimum experiment**: Use published time-course scRNA-seq of paclitaxel exposure (24h, 48h, 72h). Map each timepoint's transcriptomic profile to estimated HH parameters (via Idea 1). Simulate functional trajectory. Validate temporal pattern against published MEA time-course data.
- **Expected outcome**: Predicted functional decline trajectory correlates with MEA data (r > 0.6 across timepoints).
- **Novelty**: 8/10 — All existing approaches are snapshot-based; temporal modeling is new.
- **Feasibility**: MEDIUM — Depends on Idea 1 working; time-course data limited.
- **Risk**: HIGH — Error accumulation across timepoints.
- **Contribution type**: New method + empirical finding
- **Pilot result**: SKIPPED (no GPU)
- **Reviewer's likely objection**: Temporal extrapolation is notoriously unreliable in biological systems.
- **Why we should do this**: If successful, enables predictive neurotoxicology rather than reactive detection.

### Idea 7: GraphNeuroTox — Cell-Cell Communication Graph for Population-Level Neurotoxicity
- **Hypothesis**: Neurotoxic effects propagate through cell-cell communication networks (e.g., glia-neuron crosstalk amplifies neuroinflammation). A graph neural network incorporating CellPhoneDB interaction data can predict population-level neurotoxic responses from single-cell profiles.
- **Minimum experiment**: Construct cell-cell interaction graphs from mixed neuron-glia scRNA-seq under neurotoxicant exposure. Train GNN to predict population-level MEA metrics (mean firing rate, synchrony index). Compare with cell-autonomous prediction (no graph).
- **Expected outcome**: GNN with interaction graph outperforms cell-autonomous model by >5% on population metrics.
- **Novelty**: 7/10 — GNNs for cell-cell interaction exist; application to neurotoxicology population effects is new.
- **Feasibility**: MEDIUM — Requires mixed neuron-glia scRNA-seq datasets.
- **Risk**: MEDIUM — Graph construction from scRNA-seq is noisy.
- **Contribution type**: New method + empirical finding
- **Pilot result**: SKIPPED (no GPU)
- **Reviewer's likely objection**: CellPhoneDB interactions are inferred, not measured; graph may be unreliable.
- **Why we should do this**: Captures the in vivo reality of cell interactions that single-cell analyses miss.

### Idea 8: NeurotoxBench — Comprehensive Benchmark for Computational Neurotoxicology
- **Hypothesis**: The field lacks a standardized benchmark to evaluate computational models for neurotoxicology prediction. Creating one would accelerate the field like ImageNet did for computer vision.
- **Minimum experiment**: Curate 5 publicly available datasets (paired scRNA-seq/proteomics + functional readouts under neurotoxicant exposure). Define 3 prediction tasks (binary toxicity, dose-response curve, mechanism classification). Evaluate 5+ baseline models (random forest, scGPT, GEARS, MoltiTox, GNN).
- **Expected outcome**: Benchmark paper with clear rankings and analysis of what each model does/doesn't capture.
- **Novelty**: 6/10 — Benchmark papers are less novel but highly impactful if well-designed.
- **Feasibility**: HIGH — Data curation, no GPU-intensive training needed.
- **Risk**: LOW — Almost certain to produce a useful contribution.
- **Contribution type**: Diagnostic + resource
- **Pilot result**: N/A (data curation project)
- **Reviewer's likely objection**: "Just a benchmark" — needs insightful analysis beyond rankings.
- **Why we should do this**: Enables fair comparison for all subsequent work. High citation potential.

### Idea 9: GeneTox-VAE — Disentangled Latent Space for Neurotoxic Mechanisms
- **Hypothesis**: A beta-VAE trained on scRNA-seq data from multiple neurotoxicant exposures can learn disentangled latent factors corresponding to distinct toxicity mechanisms (excitotoxicity, oxidative stress, mitochondrial dysfunction, neuroinflammation), enabling mechanistic classification of unknown compounds.
- **Minimum experiment**: Collect scRNA-seq from 5+ neurotoxicants with known mechanisms. Train beta-VAE with mechanism-labeled supervision on 3, test on 2 unseen compounds. Evaluate if latent traversals correspond to known mechanisms.
- **Expected outcome**: At least 3 interpretable latent dimensions corresponding to known mechanisms; unseen compound classification accuracy > 70%.
- **Novelty**: 7/10 — Disentangled representations for toxicity mechanisms is novel. beta-VAE on scRNA-seq exists but not for this purpose.
- **Feasibility**: MEDIUM — Data assembly across studies is challenging.
- **Risk**: MEDIUM — Disentanglement is notoriously hard to achieve in practice.
- **Contribution type**: New method + empirical finding
- **Pilot result**: SKIPPED (no GPU)
- **Reviewer's likely objection**: Disentanglement often fails without inductive bias; mechanism labels may be too coarse.
- **Why we should do this**: Interpretable toxicity mechanism discovery would be transformative for drug safety.

### Idea 10: PhysInformed-scFM — Physics-Informed Single-Cell Foundation Model
- **Hypothesis**: Incorporating biophysical constraints (ion channel kinetics, membrane equation constraints) as physics-informed loss terms during single-cell foundation model pre-training improves perturbation prediction accuracy and produces physically plausible cell states.
- **Minimum experiment**: Add HH-derived regularization terms to scGPT training loss. Compare perturbation prediction accuracy with/without physics-informed loss on neurotoxicant datasets. Check if predicted cell states satisfy basic biophysical constraints (resting potential range, ion balance).
- **Expected outcome**: 5-15% improvement in perturbation prediction; zero physically impossible predictions (vs. baseline which may produce them).
- **Novelty**: 9/10 — Physics-informed ML is hot in other fields but completely absent in single-cell genomics.
- **Feasibility**: MEDIUM — Requires deep understanding of both scGPT architecture and HH biophysics.
- **Risk**: HIGH — Two complex systems to integrate; may not converge.
- **Contribution type**: New method (fundamental)
- **Pilot result**: SKIPPED (no GPU)
- **Reviewer's likely objection**: Physics priors are too simplified (HH is a toy model of real neurons); may over-constrain the model.
- **Why we should do this**: If it works, this is a high-impact paradigm shift — bringing physics into genomics foundation models.

---

## First-Pass Filtering

| Idea | Novelty | Feasibility | Risk | Impact | Keep? |
|------|---------|-------------|------|--------|-------|
| 1. OmicsToHH | 8/10 | HIGH | MEDIUM | HIGH | ✅ TOP |
| 2. VirtualNeuronTox | 9/10 | MEDIUM | HIGH | VERY HIGH | ✅ (depends on #1) |
| 3. NeuroCellHet | 7/10 | HIGH | LOW | MEDIUM | ✅ SAFE |
| 4. MultiModal-NeuroPert | 6/10 | HIGH | LOW | MEDIUM | ⚠️ Incremental |
| 5. BioPhysEmbed | 8/10 | HIGH | LOW-MED | HIGH | ✅ TOP |
| 6. TempTox | 8/10 | MEDIUM | HIGH | HIGH | ⚠️ Depends on #1 |
| 7. GraphNeuroTox | 7/10 | MEDIUM | MEDIUM | MEDIUM | ✅ |
| 8. NeurotoxBench | 6/10 | HIGH | LOW | MEDIUM | ✅ SAFE |
| 9. GeneTox-VAE | 7/10 | MEDIUM | MEDIUM | HIGH | ✅ |
| 10. PhysInformed-scFM | 9/10 | MEDIUM | HIGH | VERY HIGH | ✅ AMBITIOUS |

**Eliminated**: None at this stage — all 10 have merit. Narrowed to 6 top candidates:
- **Tier 1 (Recommended)**: Idea 5 (BioPhysEmbed), Idea 1 (OmicsToHH), Idea 3 (NeuroCellHet)
- **Tier 2 (Ambitious)**: Idea 10 (PhysInformed-scFM), Idea 2 (VirtualNeuronTox)
- **Tier 3 (Safe)**: Idea 8 (NeurotoxBench)

## Suggested Execution Order

### Strategy: Build the Foundation → Apply to Neurotoxicology → Scale Up

1. **Start with Idea 5 (BioPhysEmbed)** — Contrastive learning on Patch-seq data
   - Creates the foundational cross-modal embedding for all downstream ideas
   - LOW RISK, well-defined evaluation, public data available
   - Timeline: 2-3 weeks

2. **Then Idea 1 (OmicsToHH)** — Omics-to-biophysics translator
   - Builds on BioPhysEmbed embeddings
   - Direct bridge between omics and simulation
   - Timeline: 3-4 weeks

3. **In parallel: Idea 3 (NeuroCellHet)** — Cell heterogeneity analysis
   - Pure computational analysis, no model training dependency
   - Can start immediately while building Idea 5
   - Timeline: 2 weeks
   - PUBLISHABLE regardless of outcome direction

4. **If 1 + 5 succeed: Idea 2 (VirtualNeuronTox)** — Full virtual neuron system
   - Integrates everything into an applied framework
   - Timeline: 4-6 weeks after prerequisites

## Next Steps
- [ ] Download Patch-seq data from Allen Brain Atlas
- [ ] Implement BioPhysEmbed (Idea 5) — contrastive learning pipeline
- [ ] Curate neurotoxicant scRNA-seq datasets for Idea 3
- [ ] After initial results: invoke /auto-review-loop for iteration
- [ ] Or invoke /research-pipeline for the complete end-to-end flow

## Deep Novelty Check Results (Phase 3)

### Idea 1: OmicsToHH — ✅ CONFIRMED NOVEL
- **Closest prior work**: DeepHM (2025) maps electrophysiology → HH parameters, NOT transcriptomics → HH
- **No existing work** maps scRNA-seq gene expression to Hodgkin-Huxley conductance parameters
- **Differentiation**: This is the inverse direction — from omics to biophysics, not biophysics to biophysics
- **Novelty score**: 8/10 → **9/10** (upgraded after search confirmed no prior art)

### Idea 5: BioPhysEmbed — ⚠️ PARTIALLY NOVEL (prior art exists)
- **Closest prior work**:
  - NEMO (ICLR 2025 spotlight): Contrastive learning on electrophysiology features for cell-type/brain-region classification
  - Coupled Autoencoders (Nature Computational Science 2021): Cross-modal alignment of Patch-seq transcriptomics + electrophysiology in cortical interneurons
  - scMDCF (Genome Medicine 2026): Contrastive learning for multi-omics alignment
- **Differentiation**: Prior works focus on CLASSIFICATION of existing cell types. Our proposal targets PREDICTION for neurotoxicology — generating biophysical embeddings that enable downstream simulation.
- **Novelty score**: 8/10 → **6/10** (downgraded due to prior art; need stronger differentiation)
- **Recommendation**: Reframe as "toxicology-aware" cross-modal embedding, or merge into Idea 1 as a component

### Idea 3: NeuroCellHet — ✅ CONFIRMED NOVEL
- **No existing work** connects single-cell transcriptomic heterogeneity to differential neurotoxic susceptibility via biophysical modeling
- **Clinical observation** (some neurons vulnerable, others resistant) is well-known but never explained mechanistically with scRNA-seq
- **Novelty score**: 7/10 (unchanged — novel application but straightforward methodology)

### Updated Ranking After Novelty Check

| Rank | Idea | Novelty (post-check) | Priority |
|------|------|---------------------|----------|
| 1 | **OmicsToHH** | 9/10 ✅ NOVEL | 🏆 FIRST PRIORITY |
| 2 | **NeuroCellHet** | 7/10 ✅ NOVEL, LOW RISK | 🥈 PARALLEL SAFE BET |
| 3 | **PhysInformed-scFM** | 9/10 (unchecked) | 🥉 AMBITIOUS |
| 4 | **BioPhysEmbed** | 6/10 ⚠️ PRIOR ART | Merge into #1 |
| 5 | **VirtualNeuronTox** | 9/10 (unchecked) | Depends on #1 |

## Notes
- **GPU Pilots**: SKIPPED — no GPU server configured. All ideas validated on paper only.
- **Cross-Model Review (Phase 4)**: Pending — Codex MCP (GPT-5.4) review available after Cursor restart.
  To run full cross-model validation:
  ```
  claude
  > /research-review "OmicsToHH: scRNA-seq to Hodgkin-Huxley parameter translation for neurotoxicology"
  ```
