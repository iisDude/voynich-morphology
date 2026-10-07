# Upstream provenance and citation audit

Primary contribution creator: Dylan Bedford. Audit scope includes the project handoff/test ledger, original evidence index, frozen reports/code/data, all five supplied ZIP repositories/corpora, code imports/URLs, archive README/license/citation records, and authoritative online preferred citations/source reuse information.

The machine-readable resource register distinguishes used/built upon, compared against, background/prior art and software dependency. Thirty preferred/publication/software references are included in CITATION.cff; thirty-two resources are individually audited. Transitive inherited repositories with unresolved author/license identity are documented without fabricating a CFF author list. No downloaded repository code was executed. Static normalized nontrivial-function comparison found zero exact matches, which does not exclude conceptual influence.

## Archive identity

Exact supplied archive byte hashes and Git ZIP comments are in archive_audit.json. The comments identify these commits:

- Finnish TDT: bfaae13719f249573d940edda6a0d7aa8eec620f.
- Turkish IMST: 0c939115d8277ecfb39e1bbc3f066b1852ab5ddc.
- Latin PROIEL: ae7c7c5bd92e2ab9d2c58cf8184dd72028ca54eb.
- Supplied voynich-main: 0308ff7d48ffe0e07064679f98fae251f383940f; its own canonical repository and named individual authors were not established.
- Keito Yoshida / Voynich-public: 8920f2e506fce4c2c5a1245fb21a312f25655f1b; preferred root CITATION.cff and paper frontmatter used rather than the account name.

The inherited voynich-main NOTICE points to Daniel Bourdeau's cyphersolver at abbreviated f602841. Current authoritative repository root/API has no detected LICENSE/CITATION and license=null. That pointer is not upgraded to a verified full commit, and the inherited archive's MIT claim is not assumed to clear transitive code. Neither repository's code is bundled.

## License/citation findings

Original archive license and citation/NOTICE texts are preserved under licenses/upstream. Latin's LICENSE.txt says CC BY-NC-SA4.0; README metadata says CC BY-NC-SA3.0. Both statements/hash authorities are recorded; no corpus is redistributed or silently relicensed. Finnish is BY-SA4.0; Turkish BY-NC-SA4.0. Their preferred corpus papers are cited, including both Turkish README requests.

Yoshida's original code is Apache2.0, research/documentation/artifacts CC BY4.0, with third-party exclusions. Its archived report was read as prior art, not executed as a dependency or treated as validation of the present work.

Yale institutional policy and manuscript description were verified. Native Yale images remain external; attributed derived crops are retained. voynich.nu's author roadmap explicitly makes the transliteration files available CC0; fonts are separate and excluded. RF is a derived ZL/GC combination, not an independent witness.

Scientific dependencies are audited from installed distribution versions/METADATA/notices, with preferred project citations where available. No wheels/binaries are bundled. Original bundled-library notices remain available. Python's full license/history is preserved. PyMuPDF, PyYAML and cffconvert were not installed or used and are not invented as dependencies.

The inherited Davis2020 reference was inaccurate. Correct publication: *How Many Glyphs and How Many Scribes? Digital Paleography and the Voynich Manuscript*, DOI10.1353/mns.2020.0011. Initial unrelated DOI/ACL lookups were rejected; the correct Turkish2016 paper is C16-1325, and PROIEL's2008 workshop citation is verified from its authors' bibliography. Corrections are sidecar audit facts; original notices/manifests were not rewritten.

## Public package scope

Full Yale scans, raw external UD corpora, private conversations and third-party repository code are excluded. Public historical output statistics and comparison diagnostics remain, with their source-input requirements and negative/not-estimable dispositions. Project licensing applies only to original code/annotations/numerical/documentation contributions. Source imagery and inherited license/citation texts are explicitly excluded from that grant.

All original freeze bytes and hashes are preserved. Transport compression/deduplication is independently verified. The new contribution freeze seals the publication package rather than rewriting earlier scientific freezes. Numerical replay separately blocks original research-input and lab-file access; software dependency code is allowed. No conventional, linguistic, positional or decipherment assay was rerun for publication.
