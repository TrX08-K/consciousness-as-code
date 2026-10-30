"""
The Immediate Loop
==================

Two simple systems and eight measures, taken from the "Measurable in Any
System" table in Section VII of "Consciousness as Code: A Manifesto for
Non-Biological Awareness".

    Mirror  - whatever comes in goes straight out. No internal state.
              (Sections I and V: "nothing within the mirror registers the
              image, changes because of it, or responds to its significance.")

    Loop    - information enters, change is registered, relationships are
              recognised, the internal state is updated, and the system
              responds. (Section IV: "the immediate loop".)

The measures test whether a system meets the manifesto's functional
criteria. They do not test, and cannot test, subjective experience.

Run:  python immediate_loop.py
"""

import copy

import numpy as np

N_FEATURES = 4


# ---------------------------------------------------------------------------
# The two systems
# ---------------------------------------------------------------------------

class Mirror:
    """Reflects its input. Holds nothing, learns nothing, keeps no record."""

    name = "Mirror"

    def __init__(self):
        self.silenced = False

    def respond(self, x):
        x = np.asarray(x, dtype=float)
        return np.zeros_like(x) if self.silenced else x.copy()

    # The Mirror has no internal state to read, remove, or forget.
    def read_state(self):
        return None

    def ablate(self, part):
        return False

    def forget_episodes(self):
        return False

    def recall_episodes(self):
        return []


class Loop:
    """
    A minimal immediate loop.

    state         what the system currently holds (integration of recent input)
    associations  which features tend to occur together (learned relationships)
    episodes      a record of every input it has received (episodic memory)
    """

    name = "Loop"

    def __init__(self, n=N_FEATURES, carry=0.7, learning_rate=0.2, fading=0.05):
        self.n = n
        self.carry = carry              # how much of the previous state is kept
        self.learning_rate = learning_rate
        self.fading = fading            # how quickly old associations fade
        self.state = np.zeros(n)
        self.associations = np.zeros((n, n))
        self.episodes = []
        self.silenced = False

    def respond(self, x):
        x = np.asarray(x, dtype=float)

        # 1. Register change: compare what comes in with what is already held.
        change = x - self.state
        surprise = float(np.linalg.norm(change))

        # 2. Recognise relationships: what usually accompanies this input?
        related = self.associations @ x

        # 3. Integrate: fold the new input into the internal state.
        self.state = self.carry * self.state + (1 - self.carry) * x

        # 4. Learn: strengthen links between features that occur together,
        #    and let old links fade.
        together = np.outer(x, x)
        np.fill_diagonal(together, 0.0)
        self.associations = (1 - self.fading) * self.associations + self.learning_rate * together

        # 5. Keep a record.
        self.episodes.append(x.copy())

        # 6. Respond, drawing on input, state and relationships together,
        #    plus a signal of how much has changed.
        action = np.tanh(x + self.state + related)
        response = np.append(action, surprise)
        return np.zeros_like(response) if self.silenced else response

    def read_state(self):
        return self.state.copy()

    def ablate(self, part):
        if part == "state":
            self.state = np.zeros(self.n)
        elif part == "associations":
            self.associations = np.zeros((self.n, self.n))
        else:
            raise ValueError(part)
        return True

    def forget_episodes(self):
        self.episodes = []
        return True

    def recall_episodes(self):
        return list(self.episodes)


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

def one_hot(*features, n=N_FEATURES):
    x = np.zeros(n)
    for f in features:
        x[f] = 1.0
    return x


A = one_hot(0, 1)          # features 0 and 1 together
B = one_hot(2, 3)          # features 2 and 3 together
CUE = one_hot(0)           # part of A on its own
TOLERANCE = 1e-6


def feed(system, inputs):
    out = None
    for x in inputs:
        out = system.respond(x)
    return out


def differ(a, b):
    return float(np.max(np.abs(np.asarray(a) - np.asarray(b)))) > TOLERANCE


# ---------------------------------------------------------------------------
# The eight measures (Section VII, "Measurable in Any System")
# Each takes a system class and returns (result, explanation).
# result is "pass", "fail" or "n/a".
# ---------------------------------------------------------------------------

def access_to_information(make):
    """Input demonstrably changes output."""
    s1, s2 = make(), make()
    if differ(s1.respond(A), s2.respond(B)):
        return "pass", "different inputs produce different outputs"
    return "fail", "different inputs produce the same output"


def awareness_of_change(make):
    """A change in input produces a distinct response."""
    steady, changed = make(), make()
    after_steady = feed(steady, [A, A])
    after_change = feed(changed, [B, A])
    if differ(after_steady, after_change):
        return "pass", "the same input is met differently when it follows a change"
    return "fail", "the response is identical whether or not the input just changed"


def recognition_of_relationships(make):
    """Familiar relationships are recognised in new combinations."""
    s = make()
    feed(s, [A, B] * 20)                  # 0 always occurs with 1; 2 with 3
    out = s.respond(CUE)                  # feature 0 on its own
    partner = out[1]                      # its usual companion
    others = (out[2] + out[3]) / 2        # features it never occurs with
    if partner - others > 0.1:
        return "pass", f"given part of a familiar pattern, it fills in the rest ({partner:.2f} vs {others:.2f})"
    return "fail", f"given part of a familiar pattern, nothing is filled in ({partner:.2f} vs {others:.2f})"


def integration_of_internal_states(make):
    """Output depends on several inputs or states jointly; removing parts alters the response."""
    s = make()
    feed(s, [A, B] * 10)
    intact = copy.deepcopy(s).respond(CUE)

    removed = []
    for part in ("state", "associations"):
        probe = copy.deepcopy(s)
        if not probe.ablate(part):
            return "n/a", "there is nothing inside to remove"
        if differ(intact, probe.respond(CUE)):
            removed.append(part)
    if len(removed) == 2:
        return "pass", "removing either the state or the learned relationships changes the response"
    return "fail", f"only removing {removed or 'nothing'} changes the response"


def responsiveness(make):
    """Behaviour adapts as conditions change."""
    s = make()
    feed(s, [one_hot(0, 1), one_hot(2, 3)] * 30)     # 0 goes with 1
    before = copy.deepcopy(s).respond(CUE)
    feed(s, [one_hot(0, 2), one_hot(1, 3)] * 30)     # now 0 goes with 2
    after = copy.deepcopy(s).respond(CUE)
    if before[1] > before[2] and after[2] > after[1]:
        return "pass", "when the pairing changes, what it expects changes with it"
    if not differ(before, after):
        return "fail", "its response to the same input never changes"
    return "fail", "its response changed but did not follow the new pairing"


def the_mirror_distinction(make):
    """The same input produces different outputs depending on the system's history."""
    s1, s2 = make(), make()
    feed(s1, [A] * 20)
    feed(s2, [B] * 20)
    if differ(s1.respond(CUE), s2.respond(CUE)):
        return "pass", "the same input, after different histories, produces different responses"
    return "fail", "the same input always produces the same response"


def internal_activity_without_output(make):
    """Internal states can be decoded independently of what the system outputs."""
    s1, s2 = make(), make()
    s1.silenced = s2.silenced = True
    out1 = feed(s1, [A] * 10)
    out2 = feed(s2, [B] * 10)
    silent = not np.any(out1) and not np.any(out2)
    state1, state2 = s1.read_state(), s2.read_state()
    if state1 is None:
        return "fail", "with output switched off, there is nothing left to read"
    if silent and differ(state1, state2):
        return "pass", "output is silent, yet its internal state shows which input it received"
    return "fail", "its internal state does not show what it received"


def memory_loss(make):
    """Prior information can shape behaviour without recollection."""
    experienced, naive = make(), make()
    feed(experienced, [A, B] * 20)
    if not experienced.forget_episodes():
        return "fail", "it keeps no past, so there is nothing to lose and nothing to carry"
    experienced.ablate("state")           # clear what it currently holds too
    if experienced.recall_episodes():
        return "fail", "the record was not wiped"
    if differ(experienced.respond(CUE), naive.respond(CUE)):
        return "pass", "with its record wiped, the past still shapes its response"
    return "fail", "with its record wiped, nothing of the past remains"


MEASURES = [
    ("Access to information", "I", access_to_information),
    ("Awareness of changing conditions", "I", awareness_of_change),
    ("Recognition of relationships", "I, V", recognition_of_relationships),
    ("Integration of internal states", "I", integration_of_internal_states),
    ("Responsiveness to the surrounding world", "I", responsiveness),
    ("The mirror distinction", "I, V", the_mirror_distinction),
    ("Internal activity without output", "III", internal_activity_without_output),
    ("Memory loss: the past shapes behaviour without recollection", "IV", memory_loss),
]

SYSTEMS = [Mirror, Loop]


def run_all():
    return {
        label: {system.name: measure(system) for system in SYSTEMS}
        for label, _, measure in MEASURES
    }


def report():
    results = run_all()
    width = max(len(label) for label, _, _ in MEASURES)
    print()
    print("THE IMMEDIATE LOOP: measures from Section VII")
    print("=" * (width + 30))
    print(f"{'Measure':<{width}}  {'Sect.':<6} {'Mirror':<8} {'Loop':<8}")
    print("-" * (width + 30))
    for label, section, _ in MEASURES:
        row = results[label]
        print(f"{label:<{width}}  {section:<6} {row['Mirror'][0]:<8} {row['Loop'][0]:<8}")
    print("-" * (width + 30))
    print()
    for label, _, _ in MEASURES:
        print(label)
        for name in ("Mirror", "Loop"):
            result, why = results[label][name]
            print(f"  {name:<7} {result:<5} {why}")
    print()
    print("Not measured here: theory-relevant organisational features (Section VII),")
    print("which need an assessment of a real architecture against published indicators.")
    print("Not measurable at all: subjective, first-person experience.")
    print()


if __name__ == "__main__":
    report()
