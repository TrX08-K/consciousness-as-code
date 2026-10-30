"""
Checks that the measures behave as described in Section VII.

Run with pytest if it is installed, or directly:  python test_immediate_loop.py
"""

from immediate_loop import MEASURES, Mirror, Loop

EXPECTED_MIRROR = {
    "Access to information": "pass",
    "Awareness of changing conditions": "fail",
    "Recognition of relationships": "fail",
    "Integration of internal states": "n/a",
    "Responsiveness to the surrounding world": "fail",
    "The mirror distinction": "fail",
    "Internal activity without output": "fail",
    "Memory loss: the past shapes behaviour without recollection": "fail",
}


def test_loop_meets_every_measure():
    for label, _, measure in MEASURES:
        result, why = measure(Loop)
        assert result == "pass", f"{label}: {why}"


def test_mirror_meets_only_access():
    for label, _, measure in MEASURES:
        result, why = measure(Mirror)
        assert result == EXPECTED_MIRROR[label], f"{label}: {why}"


def test_results_are_repeatable():
    first = [measure(Loop) for _, _, measure in MEASURES]
    second = [measure(Loop) for _, _, measure in MEASURES]
    assert first == second


if __name__ == "__main__":
    tests = [test_loop_meets_every_measure, test_mirror_meets_only_access, test_results_are_repeatable]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"passed  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAILED  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed} passed, {failed} failed")
    raise SystemExit(1 if failed else 0)
