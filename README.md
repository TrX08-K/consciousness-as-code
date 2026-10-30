# consciousness-as-code

Two simple information-processing systems, a mirror and a loop, and eight measures that test the functional capacities defined in the manifesto.

This is the reference code for Section VII ("What Can Be Measured") of *Consciousness as Code: A Manifesto for Non-Biological Awareness*. It tests whether the manifesto's definition can be measured. It does not test whether any system is conscious, and it does not measure subjective experience.

## Files

| File | Contents |
|---|---|
| `immediate_loop.py` | The Mirror (reflects its input, holds no state) and the Loop (registers change, recognises relationships, integrates input into an internal state, learns associations and responds), the eight measures, and a printed report |
| `test_immediate_loop.py` | Automated checks that each system produces the expected result on every measure |

## Requirements

- Python 3
- NumPy
- pytest (optional; the tests also run directly with Python)

## Running the report

```
pip install numpy
python immediate_loop.py
```

This prints each measure with its result for both systems and a one-line explanation.

## Running the tests

```
pip install numpy pytest
pytest test_immediate_loop.py -v
```

Or, without pytest:

```
python test_immediate_loop.py
```

Expected result: **3 passed**.

## What the measures check

| Measure | Manifesto section | Mirror | Loop |
|---|---|---|---|
| Access to information: input changes output | I | pass | pass |
| Awareness of changing conditions: a change in input produces a distinct response | I | fail | pass |
| Recognition of relationships: given part of a familiar pattern, the rest is filled in | I, V | fail | pass |
| Integration of internal states: removing the state or the learned relationships changes the response | I | n/a | pass |
| Responsiveness: when a pairing changes, the expected pairing changes with it | I | fail | pass |
| The mirror distinction: the same input after different histories produces different responses | I, V | fail | pass |
| Internal activity without output: with output silenced, the internal state still shows what was received | III | fail | pass |
| Memory loss: with the record of past inputs wiped, the past still shapes the response | IV | fail | pass |

"n/a" means the Mirror has no internal state to remove.

## What the tests check

| Test | Check |
|---|---|
| `test_loop_meets_every_measure` | The Loop passes all eight measures |
| `test_mirror_meets_only_access` | The Mirror passes only access to information, and the integration measure does not apply to it |
| `test_results_are_repeatable` | Running the measures twice gives identical results |

These are internal consistency checks of the implemented code. They show that the measures behave as described, not that either system is conscious.

## Not implemented

- Theory-relevant organisational features (the final row of the manifesto's "Measurable in Any System" table), which require assessing a real architecture against published indicators
- Testing of real AI models
- Any measure of subjective, first-person experience

The Loop's settings (how much previous state it keeps, how quickly it learns, how quickly old links fade) were chosen for simplicity and are not derived from anything.
