# KenPire System Map

## Timeline View

Gold Phase:
- triage_scan.py
- triage_scan_output.json
- triage_group_by_date.py
- triage_by_date.json

Refinement Phase:
- swbst_extractor.py
- cow_extractor.py
- swbst_candidates.json
- cow_candidates.json

Decision Phase:
- capsules/refinement/
- refined_stories.json
- backlog_intake.md

Execution Phase:
- (intentionally empty)
- populated only after refinement approval

## Topology View

[Filesystem]
   |
   v
[Gold Recon]
   |
   v
[Date Clustering]
   |
   v
[Refinement Capsule]
   |       \
   |        -> SWBST
   |        -> COW
   v
[Backlog Intake]
   |
   v
[Execution / Runtime]

No arrow skips a layer.
