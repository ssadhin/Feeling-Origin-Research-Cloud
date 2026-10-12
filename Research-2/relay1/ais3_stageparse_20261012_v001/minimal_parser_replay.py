# AIS-3 numeric-name parser bounded reproduction, no provider calls.
# Original method transcribed exactly from pinned AI-Scientist-v2
# commit 96bd51617cfdbb494a9fc283af00fe090edfae48.
import re
from typing import Tuple
class Original:
    def parse_stage_names(self, stage_name: str) -> Tuple[int, str, int, str]:
        """Parse stage name into main stage number, main stage name,
        sub-stage number, and sub-stage name"""
        # Find the two numbers in the current stage name
        numbers = [int(n) for n in re.findall(r"\d+", stage_name)]

        main_stage = numbers[0]
        sub_stage_num = numbers[1]
        # Extract main_stage_name (everything between the two numbers)
        parts = re.split(r"\d+", stage_name)[1:-1]
        main_stage_name = "_".join(p.strip("_") for p in parts if p.strip("_"))
        # Extract sub_stage_name (everything after the second number)
        sub_stage_name = re.split(r"\d+", stage_name)[-1].strip("_")

        return main_stage, main_stage_name, sub_stage_num, sub_stage_name

o=Original()
assert o.parse_stage_names('1_initial_implementation_1_preliminary')==(1,'initial_implementation',1,'preliminary')
assert o.parse_stage_names('1_initial_implementation_1_v2_repair')==(1,'initial_implementation_v',1,'repair')
assert o.parse_stage_names('2_baseline_tuning_3_trial2026_fix')==(2,'baseline_tuning_trial',3,'fix')
assert o.parse_stage_names('2_baseline_v2_tuning_1_first_attempt')[2]==2
try: o.parse_stage_names('nonsense'); raise AssertionError('must fail')
except IndexError: pass
print('5 bounded original parser checks PASS; see full local ZIP for original next-substage propagation')
