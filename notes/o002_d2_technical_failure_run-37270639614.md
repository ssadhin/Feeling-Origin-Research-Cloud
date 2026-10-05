# O002-D2 technical failure audit — run 37270639614

Scientific status: NO OUTCOME COMPUTED.

The script failed immediately after loading the frozen CASE feature rows, before any model fitting or D2 metric result was computed.

Exact error:
ValueError: invalid literal for int() with base 10: 'sub-01'

Cause:
The D2 implementation incorrectly assumed CASE subject identifiers were numeric. The frozen feature rows use string identifiers such as "sub-01".

Correction rule:
The scientific protocol, targets, features, horizons, held-person × held-video evaluation, learners, metrics, bootstrap, and decision rules remain unchanged. The only permitted fix is to preserve subject identifiers as strings throughout prediction collection and crossed-bootstrap bookkeeping.

Original failed run: 37270639614
Protocol: 600a5cd95398d1f023c06a128e9520872a138790
Analysis: dabe1b3076d17da6a30e9877c95e3d9905e692fe
Workflow: fff49cf5a16948ccea01f60a20cb8afbd8e248f8
Trigger: 29345daed82a32c02cd3482e48dcfaa6557b2bb4

This failure contains no scientific evidence.
