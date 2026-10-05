# POPANE archive provenance bridge: R1 ↔ checksummed archive

Issue:
POPANE-R1 (run 37257239830) downloaded Study 6 from the public stable URL but did not record the raw ZIP SHA256 at that time. The later provenance run 37270877344 recorded the currently served archive as:
- size: 2,872,865,432 bytes
- SHA256: a5db8dd9b57fb1cd1ad799b635f4e59c9edaeb8481285a9e1fbef3522e998140
- ZIP entries: 1,497

Strictly, a later checksum alone cannot prove that the server bytes were unchanged between R1 and provenance capture.

Empirical bridge:
POPANE-R6 (run 37270191779) independently re-downloaded the public Study 6 archive, reran the exact R1 extraction and held-person × held-segment model fitting, and reports MAE as a consistency metric. The resulting R6 MAEs match the preserved R1 values to full stored precision:

1 s:
- naive 0.12484766822408812
- Ridge physiology 0.16256715839283628
- HGB physiology 0.180226002768008

11 s:
- naive 0.3005024802585197
- Ridge physiology 0.37803143374964404
- HGB physiology 0.4042720671812217

21 s:
- naive 0.4383545149007306
- Ridge physiology 0.5420644150249383
- HGB physiology 0.5785603356681063

31 s:
- naive 0.5534943690214389
- Ridge physiology 0.6796457980092181
- HGB physiology 0.7259958087536483

R6 also reproduces the R1 QC shape:
- 1,122 files seen
- 1,115 usable
- 8,919 feature rows
- 186 usable participants
- 18 eligible segments
- 7 peripheral_missing rejections

Interpretation:
This exact aggregate reproduction strongly supports that the archive used by the later checksummed run is the same effective dataset version used for R1, even though a raw R1-time SHA256 was not captured.

Claim boundary:
Do not state that the R1 raw ZIP hash was contemporaneously recorded. State instead that a later checksum was preserved and an independent rerun from the then-current archive exactly reproduced R1's QC and primary MAEs.
