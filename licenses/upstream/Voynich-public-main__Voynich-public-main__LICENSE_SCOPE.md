# License scope and citation policy

This repository uses different standard licenses for software and research
materials. A file-specific license notice, when present, takes precedence over
the defaults below.

## Software: Apache License 2.0

Original software source code, tests, command-line utilities, and executable
configuration authored for this repository are licensed under the
[Apache License 2.0](LICENSE). This includes the original code under
`analysis/`, `paper/`, `scripts/`, and `tests/`.

Redistribution must comply with the Apache License, including its license-copy,
change-notice, attribution-notice, and `NOTICE` requirements. The Apache
License does not require an academic citation merely for privately running the
software.

## Research materials: CC BY 4.0

Original research documentation, the technical paper and its released PDF,
original figures and tables, and project-authored result artifacts are licensed
under the [Creative Commons Attribution 4.0 International Public License](LICENSES/CC-BY-4.0.txt).

When sharing or adapting those materials, provide the attribution required by
CC BY 4.0. A reasonable attribution is:

> Keito Yoshida, *Voynich Research: Multiscale
> Structural Constraints and Executable Generative Models*, version 0.1.0,
> 2026, https://github.com/seeton/Voynich-public, CC BY 4.0.

If a publication, report, public presentation, dataset, or software
documentation uses or relies on this repository's original findings, methods,
or released research artifacts, it must cite the repository using
[`CITATION.cff`](CITATION.cff) and must also cite the external sources used by
the relevant analysis. This scholarly citation policy does not add a condition
to Apache-2.0-licensed software or restrict uses that do not require copyright
permission.

## Exclusions and third-party rights

The licenses above apply only to material that this repository's contributors
have authority to license. They do not relicense the Voynich Manuscript,
third-party transcriptions, corpora, publications, images, databases, model
weights, quotations, trademarks, or other third-party material. Source-specific
terms and attribution requirements remain controlling; see
[`THIRD_PARTY.md`](THIRD_PARTY.md) and [`docs/sources.md`](docs/sources.md).

Tracked numeric result artifacts may be covered as original research
artifacts, but source-text fields and reconstructive exact-token arrays copied
from download-only transcription or corpus inputs are not included. The
deterministic publication-safety ledger records the removed fields and the
before/after hashes; it does not relicense the private source payload.

The full standard license texts are stored in [`LICENSE`](LICENSE) and
[`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt). This scope document explains
which license applies; it does not modify either standard license.
