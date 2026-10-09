---
published: true
title: "Gaze as Evidence for Common Grounding: A Cross-Corpus Analysis of MapTask and MUNDEX"
arxiv_id: "2609.18011"
url: "https://arxiv.org/abs/2609.18011"
authors: ["Nan Li", "Albert Gatt", "Massimo Poesio"]
---
published: true

# Gaze as Evidence for Common Grounding: A Cross-Corpus Analysis of MapTask and MUNDEX

[KO version](../ko/sources/papers/Gaze_as_Evidence_for_Common_Grounding.md)

## Abstract

In collaborative tasks with asymmetric information, participants coordinate their understanding through interaction. We ask whether gaze provides evidence about grounding across two such tasks. Working from discrete behavioral annotations, we map HCRC MapTask (Anderson et al., 1991) and MUNDEX (Türk et al., 2023) into a shared partner/task/away vocabulary and compute gaze features around task-relevant dialogue units. In both corpora, aligned reference interpretations (MapTask) and UND (understood) judgments (MUNDEX) are associated with more task-directed gaze and with less partner-directed gaze, lower gaze entropy, and fewer gaze transitions. The associations are clearest for the participant leading the task: in giver-produced references, and in explainer judgments, which also co-vary with the explainee's gaze. In same-speaker MapTask reference chains, the speaker's gaze entropy is lower at the mention where a previously non-aligned referent becomes aligned. The best gaze feature groups improve modestly over controls under grouped cross-validation: temporal features in MapTask and raw proportions in MUNDEX. Because effects are small and several weaken when recurring participants rather than dialogues are the unit of inference, we treat gaze as one contributing cue to grounding, to be interpreted alongside task and dialogue context.

## Background & Problem Setup

When participants hold different private information, mutual understanding (common ground) cannot be assumed — it must be built through interaction (Clark and Wilkes-Gibbs 1986; Clark and Brennan 1991). Gaze is an observable cue: people look at task materials, at each other, or away while giving instructions and checking understanding. Many corpora annotate gaze from video as discrete categories rather than eye-tracking coordinates, but ontologies are corpus-specific, blocking cross-task comparison.

The paper studies two asymmetric face-to-face tasks. HCRC MapTask: a giver guides a follower along a route using maps with deliberately different landmarks; perspectivist labels record each participant's interpretation separately, so a reference is aligned only when speaker and addressee resolve to the same landmark. MUNDEX: an explainer teaches a board game in German to an explainee; afterwards both retrospectively judge the explainee's understanding on UND / PART_UND / NON_UND / MISUND scales. Prior within-corpus work linked partner-directed gaze to difficulty (Boyle et al. 1994; Nakano et al. 2003; Murat and Vogel 2026) and listener gaze entropy to self-reported understanding (Wang et al. 2026). The open question is whether gaze-grounding associations converge across distinct tasks and grounding measures, and whether they carry predictive signal beyond controls.

## Methodology

**Shared representation.** Both gaze ontologies are mapped to partner/task/away: MapTask up/down/off become partner/task/away; MUNDEX EX/EE/TABLE/AWAY map analogously. (The up-to-partner mapping is literal only in the eye-contact condition.) Non-positive-duration events are discarded and within-participant overlaps resolved. MapTask windows span a reference expression plus 1.5 s post-context to catch the addressee's reaction; MUNDEX windows span the understanding annotation ± 2 s. Windows with either participant below 30% gaze coverage are dropped, leaving 5,144 MapTask reference windows (3,807 aligned, 1,261 pending, 76 misunderstood; 46 dialogues, 31 eye-contact / 15 no-eye-contact) and 807 MUNDEX windows (360 UND, 199 PART_UND, 151 NON_UND, 97 MISUND; 26 interactions, 9 explainers; EX 458 / EE 349 annotations pooled with one row per annotation).

**Feature groups.** From the shared vocabulary: raw proportions (per-participant time on each target plus mutual gaze, 7–8 features); structured (adds coverage, transition count, duration-weighted Shannon entropy, 13–14 features); temporal dynamics (run counts, durations, switch rate, latency, first/last/dominant indicators, 21 per participant); transition bigrams (ordered pairs such as task→partner, 6 per participant); coordination (joint states sampled ~10 Hz: mutual task/partner gaze, alignment, complementarity, joint entropy, coupling, 6 joint features); derived ratios (partner/task ratio, engagement, task dominance, asymmetries, 9 features).

**Analyses.** Binary contrasts (aligned vs. non-aligned; annotator-judged UND vs. non-UND) with Mann–Whitney U and rank-biserial `r`, stratified by role and eye-contact condition, plus cluster-robust logistic GEE with Benjamini–Hochberg correction; inference units varied (dialogue vs. recurring-participant groups). A within-speaker reference-chain analysis compares speaker gaze at the last non-aligned mention vs. the resolving aligned mention (189 pairs, 45 dialogues). Prediction uses logistic regression with standardized features and balanced weights under grouped cross-validation (10-fold grouped-by-dialogue MapTask; 5-fold grouped-by-explainer MUNDEX), ablating feature groups against controls-only (condition + speaker role; annotator role).

## Results

- **Directional convergence**: in both corpora the positive class (aligned / UND) shows more task-directed gaze, less partner-directed gaze, lower entropy, and fewer transitions. Largest pooled `|r|`: 0.058 MapTask, 0.181 MUNDEX. All top associations have Mann–Whitney p < 0.001; entropy and transition features also survive dialogue-clustered GEE in MapTask, and explainer task/partner gaze plus explainee entropy/transitions survive participant-clustered GEE in MUNDEX.
- **Role concentration**: clearest for the task leader. Giver-produced references carry six significant features (largest `|r|` 0.086) vs. near-zero for follower-produced (largest 0.043). In MUNDEX all 14 structured features agree in sign across EX judgments and EE self-reports, but only the EX-judgment stratum survives correction, including explainee gaze proportions, entropy, and transitions. Feature×role interactions do not survive correction, so this is a stratum difference, not a tested moderation.
- **Grounding process**: aligned rate rises from 0.30 at first mentions to 0.59 at second and 0.85 at fourth-plus; speaker partner gaze, entropy, and transitions are lower at second than first mentions. Within-speaker, entropy drops at the resolving mention (dz = −0.20, q = 0.044), though the effect does not survive dialogue-level aggregation (q = 0.20) and concentrates in two of six participant-sharing groups. At matched chain positions, only second-mention task gaze survives correction (q = 0.01).
- **Prediction**: modest, partition-sensitive gains. MapTask best is structured+temporal (macro-F1 0.532 vs. 0.472 controls-only, majority 0.425); MUNDEX best is raw proportions (0.564 vs. 0.544 controls-only, majority 0.356). MapTask gains range 0.015–0.070 across 30 reshuffled partitions (mean 0.038); MUNDEX gains are positive in 29/30 but at most 0.027. Eye-contact stratum shows larger `|r|` than pooled data, but the condition interaction is not significant; no-contact stratum has near-zero effects.
- Accepted to the MINT workshop at EMNLP 2026 (oral); 16 pages, 17 tables, 2 figures. Data and code: GMMT labels, MUNDEX Zenodo v0.7, analysis repo https://github.com/chnln/gaze-as-grounding-evidence

## Limitations & Open Questions

- Three gaze categories cannot identify which landmark or object is viewed, and shared names do not imply equivalent interactional functions (a partner glance may check a reference in MapTask but organize topic structure in MUNDEX). The up→partner mapping is literal only with eye contact.
- MUNDEX pools two perspectives (explainer judgments vs. explainee self-reports); 44 of 135 fully retained linked pairs disagree on the binary label, and paired windows need not coincide (median anchor separation 4.36 s).
- Small, recurring-participant samples: 46 MapTask dialogues from 24 participants in six connected groups, 26 MUNDEX interactions from nine explainers (eight with three interactions each). With participants/groups as clusters, no MapTask feature survives correction; coverage filtering drops 17 MapTask and 149 MUNDEX windows unevenly (two explainers account for 139 MUNDEX exclusions).
- Effects are small, inference-unit-sensitive, and prediction gains are partition-dependent; only two asymmetric face-to-face tasks in English and German are tested. Authors treat gaze as one contributing cue to be modeled alongside lexical, dialogue-act, and task-state features, not a standalone grounding detector.

## Relevance to SW Engineers

For teams building meeting assistants, tutoring agents, or human-robot dialogue (including gaze-aware frontends), the practical takeaway is conservative: log a compact partner/task/away gaze stream around task-relevant utterances and use it as an auxiliary feature, not a ground-truth sensor. Expect small, role-conditioned signal — monitor the task leader's task-vs-partner balance, entropy, and transition rate, and fuse with text, dialogue acts, and task state in a grouped-by-speaker evaluation (held-out speakers, not pooled windows) to avoid overstating gains. The shared-vocabulary mapping plus window/feature definitions in the appendices are directly reusable for instrumenting your own video-coded gaze logs and running the same Mann–Whitney + cluster-robust GEE + grouped-CV ablation before shipping any gaze-triggered UX. Extends `concepts/machine-learning/embedding.md`, `concepts/ai-engineering/agent-evaluation.md`, and `concepts/ai-engineering/agent.md`.

## References

- Paper: https://arxiv.org/abs/2609.18011 (HTML: https://arxiv.org/html/2609.18011v1) — HF: https://huggingface.co/papers/2609.18011 — Code: https://github.com/chnln/gaze-as-grounding-evidence
- MapTask (Anderson et al. 1991); MUNDEX (Türk et al. 2023); GMMT perspectivist labels (Li et al. 2026a); grounding (Clark and Wilkes-Gibbs 1986; Clark and Brennan 1991); GEE (Liang and Zeger 1986); BH correction (Benjamini and Hochberg 1995)
