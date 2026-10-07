> Publication link-adapted view; the original report is preserved unchanged in `reports/`.

# Evidence inventory v0

Date: 2026-10-05. All work products reside under the Voynich Project folder. No source evidence was modified. Verification rehashed all 14 current root files and confirmed the original 13 files remain identical to the initial snapshot.

## Files and hashes

| Exact filename | Bytes | SHA-256 |
|---|---:|---|
| `httpsvoynich-nudataRF1b-e.txt` | 367,984 | `9e86f104282e17bd673b7a21150c4a167e1595ae68658db72859db24c2ca455f` |
| `httpsvoynich.nudataGC2a-n.txt` | 320,736 | `69de7c6e36f5f54dad52141c5535601206b6130c1e93592becfbc3eca7e94b22` |
| `httpswww.voynich.nudataZL3b-.txt` | 420,179 | `3012092a1cf91ea2adbf82d56babdfe2be94fd916b2288c040850c957ed25935` |
| `UD_Finnish-TDT-master.zip` | 3,085,884 | `76dadde527f9f505628f7ae99beb68450eaf9980faf7cd06d2ed0dbff35fd628` |
| `UD_Latin-PROIEL-master.zip` | 2,966,356 | `90de877cfa1079031daa55bd7351331b98a385f9859abb06b78203bca940cce1` |
| `UD_Turkish-IMST-master.zip` | 802,821 | `2dd5d4d78db2fa0bd8bbf638a0ddda0e46e6c52bf6cdfcba697b5b29eb328c8b` |
| `voynich-main.zip` | 24,777,070 | `7554794e09bc6eb19b21d785ec0c233fad2710621a29390636186129a95c658f` |
| `Voynich-Manuscript_all_Pages.pdf` | 118,428,581 | `b048d09835c66522cc7a6d93e3edf4693edacc403aa79f738c47a421d840f761` |
| `Voynich-public-main.zip` | 40,804,721 | `bcf312324cd914d6cd7badd277a691e405b317411cb198ce93ef643299716b28` |
| `Voynich_Decipher_Test_2nd_Chat.txt` | 91,442 | `9b304082f3bc9ce9d2b94efa6674a72c29512a833677c66fd982acf90a263378` |
| `Voynich_Decipher_test_Chat.txt` | 26,797 | `aae036e8cfd927dd4d48b9d2d067dfd319fcbccad0fa8a6e13da4835ed6439ac` |
| `Voynich_Decipher_test_Chat_More_Chat.txt` | 124,038 | `e3c39a31e5409d064d40e6cfb68542e5eebea7ca007ed8ac3a0f004509e6c09f` |
| `VOYNICH_GROUND_UP_HANDOFF.md` | 25,257 | `1a03a07aad4450bbb94aeb10b924361c55b5e7d22e0382ed20612cafbea034ea` |
| `VOYNICH_TEST_LEDGER.md` | 31,392 | `4573693919bf17305f43f5ab7cf4b59af7afdcd84943ac5f0a35c191f4b94da1` |

Machine-readable records: `../data/source/evidence_manifest.csv`. The thirteen-file inventory recorded before the test ledger arrived is retained as `evidence_manifest_initial.csv`. The ZL filename actually present ends in `ZL3b-.txt`; the handoff/ledger's `ZL3b-(1).txt` is not a second local file.

## Evidence roles and provenance

- `Voynich-Manuscript_all_Pages.pdf`: primary local visual evidence. Its embedded Yale catalogue sheet gives title "Cipher manuscript", Beinecke MS 408, and Yale catalogue URL `https://collections.library.yale.edu/catalog/2002046`. PDF creation metadata and embedded generation text date this export to 2026-08-17. This is file provenance, not a new external-source verification or historical dating conclusion.
- ZL3b, RF1b, and GC2a: comparison transcriptions identified by the handoff/ledger. Contents have not been used for the initial visual segmentation. Exact upstream versions and transcription dependence are pending review.
- Three UD ZIPs: natural-language comparison corpora, retained compressed. Archive names and internal roots identify Finnish TDT, Turkish IMST, and Latin PROIEL. Exact upstream commits are not verified.
- `voynich-main.zip`: 344 archive entries. Its root README describes a statistical/generative project derived from dbourdeau/cyphersolver. Strong claims in that README have not been endorsed, audited, or reproduced here.
- `Voynich-public-main.zip`: 1,857 archive entries. Its root README describes a multiscale structural/generative research project with unresolved semantics. It contains third-party code and reports; its connection to the Yoshida work named in the chat remains to be verified from attribution/provenance files.
- Three saved chat files, handoff, and test ledger: provenance/instructions. The handoff, second chat, and test ledger were read fully. The two older chat files were inventoried but not yet read in full. Reported numerical results remain reported until a reproducible rerun exists.

All five ZIPs have been listed without extracting or executing their code: 2,231 entries including directory entries; each UD archive has ten entries. `archive_members.csv` preserves names, uncompressed/compressed sizes, and CRC32. CRC32 is not an independent cryptographic member hash; SHA-256 identifies each whole archive.

## PDF readability, mapping, and image resolution

The PDF is unencrypted, version 1.4, with 214 letter-sized pages (612 × 792 points), no outlines, and numeric PDF page labels. Its structure, caption text, and all page image descriptors were read successfully. This is structural readability, not visual verification of every manuscript page.

Each page contains one directly embedded image. Page 1 is a catalogue sheet with a 120 × 120 image. The other 213 image views, including covers, have a longest edge of 2,000 pixels. Tall views are up to 2,000 pixels high; wide unfolded views are up to 2,000 pixels wide and can have substantially fewer vertical pixels. The PDF canvas size does not determine the original manuscript scale or a trustworthy manuscript DPI.

`page_folio_map.csv` gives one-based PDF page, zero-based index, exact embedded caption, Yale image ID, canvas dimensions, and rotation for every page. Example: PDF page 4 → caption `1r`, Yale image ID `1006076`; page 127 → `69v and 70r`. Repeated/combined captions and multi-panel imagery require a separate panel mapping. Caption extraction is complete; physical-panel mapping is not.

`pdf_image_inventory.csv` gives embedded pixel dimensions, filters, color spaces, and component depth. Twelve selected views have been decoded at native size into PNG and saved with their native extracted image data. Verification compared every exported sample PNG's RGB pixels with a fresh PDF image decode: all twelve match. Their hashes and coordinate frames are in `sample_manifest.csv`.

## Visual quality and limitations

Six discovery views were visually inspected on a contact sheet; a native-size text crop from B_001 was also inspected. Recurring broad shapes and whitespace can be examined. Fine joins, touching strokes, and stroke order can be unresolved at this source resolution, particularly for small writing and foldouts. Enlarging a PNG cannot recover absent detail.

No loose higher-resolution Yale scans were found at the project root. Archives include other illustrations/PDFs; these have not all been inspected for primary manuscript scan content. Do not infer that no better local or online source exists. Any later higher-resolution acquisition must be separately hashed and registered, with a mapping to the present views.

No local AGENTS.md was found. The folder is not currently a Git repository. Source files remain at the root; derived output is isolated in `voynich-groundup/`. `runtime_manifest.json` records the bundled Python and library versions used. Schema verification: JSON parses; local schema references and scaffold keys checked; full validator unavailable. No downloads, source modifications, OCR assignments, corpus assays, crosswalks, or decipherment were performed.

## Next gate

Review the neutral schema and the twelve-view proposal. Annotate the six discovery views with competing boundaries, then freeze candidate segmentation and provenance before mapping it to transcriptions. The ledger's ordinal token-rank endpoint must be reproduced explicitly; measured pixel position is a separate endpoint. Dependence-aware uncertainty and null design remain required, not already satisfied.
