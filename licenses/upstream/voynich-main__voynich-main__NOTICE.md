# Attribution and Third-Party Notices

This project incorporates, adapts, or relies on research, software, and datasets from several open and academic sources.

---

## 1. Upstream Origin & Initial Source

This investigation originated from and builds upon the research framework developed in:
* **Repository:** [https://github.com/dbourdeau/cyphersolver](https://github.com/dbourdeau/cyphersolver)
* **Author:** Daniel Bourdeau (`dbourdeau`)
* **Context:** The initial historical cipher exploration, IVTFF parsing baseline, and early Phase A test battery were first initiated in `dbourdeau/cyphersolver` (specifically commit `f602841`, *Voynich manuscript adjudicated: hoax / cipher / language, six verified analyses, five literature sweeps*, September 2026).
* **Extension:** This repository extends that foundational work into a complete multi-phase investigation (Phases A through E), including adversarial verification suites (`v_a1`–`v_c1`), boundary transition analysis, quire-level Polya urn generative models achieving 37/37 benchmark closure, Shannon channel capacity bounds ($H_{\text{res}} \le 1.784$ bits/token), and multimodal illustration mutual information collapse ($\Delta I = +0.0015$ bits/token).

We gratefully acknowledge Daniel Bourdeau's pioneering work in computational historical cryptanalysis.

---

## 2. Voynich Manuscript Transliterations & Digital Facsimiles

* **Digital Facsimile:**
  - Beinecke Rare Book and Manuscript Library, Yale University.
  - Voynich Manuscript (Beinecke MS 408), c. 1404–1438.
  - Public Domain digital surrogate: [Yale Digital Collections](https://collections.library.yale.edu/catalog/2003431).

* **Intermediate Voynich Transliteration File Format (IVTFF):**
  - Curated and maintained by **René Zandbergen** and **Gabriel Landini** at [voynich.nu/data](https://www.voynich.nu/data/).
  - Includes academic transliterations contributed by:
    - **ZL (ZL3b-n):** René Zandbergen & Gabriel Landini (Extended EVA).
    - **RF (RF1b-er):** Reference transliteration combining GC and ZL.
    - **IT (IT2a-n):** Takeshi Takahashi (Basic EVA), adapted from Jorge Stolfi's interlinear transcription (1999).
    - **GC (GC2a-n / voyn_101):** Claston (v101 alphabet).
    - **CD (CD2a-n):** Prescott Currier & Mary D'Imperio (Currier alphabet).
  - Scribal hand identifications based on paleographical analysis by **Lisa Fagin Davis** (2020).

---

## 3. Comparative Natural Language Corpora

Comparative natural language baseline texts located in `voynich/data/`:
* **Latin:** St. Augustine, *Confessiones* (`la_confessiones.txt`) — Project Gutenberg / Public Domain.
* **Italian:** Dante Alighieri, *La Divina Commedia* (`it_divcom.txt`) — Project Gutenberg / Public Domain.
* **English:** Jane Austen, *Pride and Prejudice* (`en_pride.txt`) — Project Gutenberg / Public Domain.

These works are in the public domain in the United States and most countries.

---

## 4. Academic Literature & References

The empirical benchmarks and methodology reference key scientific findings:
1. **Lisa Fagin Davis** (2020), *"The Five Scribes of the Voynich Manuscript"*, *Manuscript Studies: A Journal of the Schoenberg Institute for Manuscript Studies*, 5(2), 275–309.
2. **M. A. Montemurro & D. H. Zanette** (2013), *"Keywords and Semantic Structure of the Voynich Manuscript"*, *PLoS ONE*, 8(6), e66344.
3. **Torsten Timm & Andreas Schinner** (2020), *"A Simulation of the Voynich Manuscript"*, *Cryptologia*, 44(2), 129–158.
4. **Claire Bowern & Luke Gaskell** (2022), *"The Voynich manuscript does not look like gibberish, but that does not mean it is a cipher"*, *Cryptologia*.
5. **G. Hodgins** (2009), *"Radiocarbon Dating of the Voynich Manuscript"*, University of Arizona AMS Laboratory.
6. **William R. Bennett** (1976), *Introduction to Computer Applications for Non-Science Students*, Prentice-Hall (character conditional entropy).
