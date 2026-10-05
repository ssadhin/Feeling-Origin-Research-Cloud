# MRA-001 measurement / construct audit v001

Date: 2026-10-05
Verdict: CONSTRUCT_SCOPE_PASS ONLY IF MANUSCRIPT TARGET IS “FUTURE CONTINUOUS SELF-REPORTED AFFECT,” NOT PSYCHOLOGICAL AFFECTIVE INERTIA OR PHENOMENAL FEELING ITSELF.

## CASE measurement

CASE participants continuously and simultaneously reported valence/arousal while viewing videos using a 2-D joystick interface.
Published method descriptions state that:
- participants were instructed to rate how they themselves felt, not the emotional content of the video;
- joystick x/y positions represent valence/arousal;
- the joystick was sampled at ~20 Hz;
- the physical joystick has a return spring / neutral center and requires ongoing embodied interaction with the rating device.

Consequences:
The report trajectory is a measurement process containing both subjective experience and response-interface dynamics. Very short-lag self-predictability can reflect some combination of:
- genuine persistence of felt affect;
- perceptual/cognitive continuity;
- decision/report inertia;
- motor/joystick dynamics;
- any processing/interpolation in the released annotation stream.

## POPANE Study 6 measurement

POPANE Study 6 continuously measured participant SELF-REPORTED valence during elicitation.
The data descriptor states:
- an electronic rating scale from 1 (extremely negative) to 10 (extremely positive);
- participants were asked to adjust the scale as often as necessary so it always reflected how they felt at the current moment;
- movement right indicated more positive/pleasant feeling; left more negative/unpleasant;
- the rating channel was recorded by the acquisition system at 1 kHz.

Important interpretation:
1 kHz is the acquisition rate of the rating-position signal, not evidence that humans make independent affect judgments 1000 times per second.
Between intentional adjustments, the device position may remain unchanged. Therefore a recent-state carry-forward baseline can exploit both experiential continuity and hold-state/reporting mechanics.

## Why external replication still matters

CASE and POPANE use different datasets, participants, elicitation designs and reporting interfaces, so identical numerical dynamics are not guaranteed.
The persistence-dominance pattern replicating across them is therefore methodologically meaningful.

However, both are continuous response-interface paradigms. The external replication does NOT isolate “true emotional inertia” from continuous-report measurement persistence.

## 2025 affective-inertia measurement warning

Jacobsen, Cloos, Vanpaemel, Ceulemans & Kuppens (2025), PsyArXiv DOI 10.31234/osf.io/5unj7_v1, “No Evidence that Continuous Affect Ratings Offer a Meaningful Measure of Affective Inertia,” reports that continuous affect-profile-derived inertia estimates did not show satisfactory stability and did not robustly add validity beyond momentary assessments in their data.

Their measurement paradigm is not identical to CASE or POPANE, so the paper does not invalidate our forecasting result.
It does strengthen a general warning: high autocorrelation/self-predictability in continuous affect records should not automatically be interpreted as a stable psychological “affective inertia” construct.

## Manuscript terminology rule

Avoid as substantive interpretation:
- “affective inertia explains the result”
- “feelings persist for 31 seconds”
- “emotion itself is autoregressive”
- “we measure the persistence of phenomenology”

Preferred:
- “recent-state persistence in the continuous self-report trajectory”
- “short-horizon self-report persistence”
- “a strong recent-report benchmark”
- “the observed affect-report trajectory is highly self-predictive”

When discussing psychology:
“The persistence benchmark may combine genuine affect dynamics with reporting/interface dynamics; our experiments are designed to test conditional forecasting information, not to decompose those sources.”

## Implication for the paper’s contribution

This caveat actually sharpens the benchmarking contribution.

The paper need not assume that the recent-report baseline is a pure psychological state. A deployed affect-prediction model is still required to beat information already available from the measured history if that history is part of the forecasting setting.

The defensible question is:
Given the recent observed self-report trajectory, do the tested peripheral physiological features add out-of-sample information about the future observed self-report trajectory?

That question is identifiable from the data and survives the measurement caveat.

## Connection to “feelings and emotion” research goal

The study is relevant to feelings because the outcomes are participants’ own valence/arousal reports, not merely stimulus labels.
But it is not a direct measurement of phenomenal feeling independent of reporting behavior.

Paper category:
affective science / psychophysiology / affective-computing methodology and predictive identifiability.

Not justified:
a theory of the origin, ontology, or phenomenal substrate of feelings.

## MRA construct gate

PASS under narrowed construct:
“future continuous self-reported affect.”

FAIL if the manuscript tries to equate report persistence with affective inertia or phenomenality.
