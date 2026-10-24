"""Simulate a long-term holdback experiment with a novelty effect.

A new feature lifts the metric a lot in weeks 1-2 (novelty / primacy),
then settles to a smaller true effect. A 2-week readout overstates the
impact; the 26-week holdback readout does not.

Pure standard library. Run:  python3 holdback_sim.py
"""

import math
import random
import statistics

random.seed(42)

WEEKS = 26
DAILY_USERS_PER_ARM = 20_000
BASE_RATE = 0.100          # control conversion rate
TRUE_EFFECT = 0.004        # +0.4 pts once the novelty wears off
NOVELTY_EXTRA = 0.012      # extra +1.2 pts during the novelty window
NOVELTY_WEEKS = 2


def simulate() -> tuple[list[float], list[float]]:
    control, treatment = [], []
    for week in range(WEEKS):
        for arm, out in ((False, control), (True, treatment)):
            rate = BASE_RATE
            if arm:
                rate += TRUE_EFFECT + (NOVELTY_EXTRA if week < NOVELTY_WEEKS else 0)
            n = DAILY_USERS_PER_ARM * 7
            out.append(random.binomialvariate(n, rate) / n)
    return control, treatment


def readout(control: list[float], treatment: list[float], upto_week: int) -> float:
    """Estimated absolute effect using data through `upto_week` (inclusive)."""
    c = statistics.mean(control[: upto_week + 1])
    t = statistics.mean(treatment[: upto_week + 1])
    return t - c


def mde(weeks_of_data: int, alpha: float = 0.05, power: float = 0.8) -> float:
    """Rough minimum detectable effect for a two-proportion test."""
    z = 1.96 + 0.84  # alpha=0.05 two-sided, power=0.8
    n = DAILY_USERS_PER_ARM * 7 * weeks_of_data
    p = BASE_RATE
    return z * math.sqrt(2 * p * (1 - p) / n)


def main() -> None:
    control, treatment = simulate()
    print(f"Base rate {BASE_RATE:.1%}, true long-run effect +{TRUE_EFFECT:.1%}, "
          f"novelty adds +{NOVELTY_EXTRA:.1%} for the first {NOVELTY_WEEKS} weeks\n")
    print(f"{'Readout':<14}{'Estimated effect':>18}{'vs true':>10}")
    for label, wk in (("Week 2", 1), ("Week 6", 5), ("Week 13", 12), ("Week 26", 25)):
        est = readout(control, treatment, wk)
        print(f"{label:<14}{est:>+17.2%}{est - TRUE_EFFECT:>+10.2%}")
    print(f"\nMDE at 2 weeks: {mde(2):.2%} | MDE at 26 weeks: {mde(26):.2%}")
    print("Takeaway: the week-2 readout mostly measures novelty. The holdback")
    print("is what tells you the effect you actually keep.")


if __name__ == "__main__":
    main()
