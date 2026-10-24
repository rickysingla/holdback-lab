# holdback-lab

A small simulation of a long-term holdback experiment, and why short readouts mislead.

## Problem

Product teams often read an experiment at 2 weeks and ship on that number. But new features frequently get a novelty bump: users click the new thing because it is new, not because it is better. The 2-week estimate then mixes the novelty effect with the true effect, and the launch decision is made on a number the product will never actually deliver.

## Approach

`holdback_sim.py` simulates two arms over 26 weeks:

- Control converts at a flat 10%.
- Treatment has a true effect of +0.4 points, plus a +1.2 point novelty bump for the first 2 weeks.
- Weekly rates include binomial sampling noise at realistic traffic (20k users/day/arm).

It then prints the estimated effect at weeks 2, 6, 13, and 26, plus the minimum detectable effect (MDE) at 2 vs 26 weeks.

## What the code shows

- The week-2 readout overstates the effect by roughly the size of the novelty bump.
- The estimate converges to the true effect only because the holdback keeps running.
- Longer runs also shrink the MDE, so the holdback buys both honesty and precision.

The point is not the simulation itself — it is the discipline: decide the readout horizon before you launch, and keep a holdback when the cost of being wrong is high.

## Run

```bash
python3 holdback_sim.py
```

Standard library only. All data is simulated; no real experiment data is used.
