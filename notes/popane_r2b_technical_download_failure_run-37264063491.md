# POPANE-R2b technical download failure audit — run 37264063491

Scientific status: NO OUTCOME COMPUTED.

The import-only correction was present, but the dataset download terminated at approximately 87% with curl exit code 18: transfer closed with 372159128 bytes remaining. The analysis step was skipped and no aggregate artifact existed.

This is a network/transfer failure only. No scientific protocol or analysis rule changes.

R2 scientific protocol remains: 5e8f8038f06fb96b216b93a6ddc81371e748eb24
Corrected analysis remains: dd18e3b7b4d04997fb70c0fe61e2be428bef73c8

Permitted correction for R2c: replace the single-shot download command with deterministic resumable range retries and verify the expected archive byte size (2872865432) before analysis.

This failure contains no scientific evidence.
