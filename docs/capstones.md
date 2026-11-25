# Small projects

Each project begins with inline koans, then the runner exercises the scaffold
in the same learner file. Run a module directly to work on one project. The
fixed checks contain small synthetic datasets so you can follow every row.

| Project | Start here | What to reason through |
| --- | --- | --- |
| **Sensor report** | `python contemplate.py python named_records` | Read CSV into named tuples and summarize by sensor. Distinguish a recorded zero from a blank and identify duplicate observations across a composite key. |
| **Vector path** | `python contemplate.py python special_methods` | Implement the operators for a small vector class. Combine an initial position, a repeated step, and drift, then project the endpoint onto an axis. |
| **Interaction model** | `python contemplate.py deep_learning interactions` | Fit a product feature with batch gradient descent. Work out why linear terms have zero gradient on the balanced sign pairs and test the fitted coefficient at unseen magnitudes. |
| **Classifier evaluation** | `python contemplate.py deep_learning evaluation` | Choose an operating threshold on validation data and measure it on a separate holdout. Explain what would change if you tuned on the holdout. |
| **Read-only model audit** | `python contemplate.py cross_track model_audit` | Compare missed positives by cohort with a mock agent. Require enough positive examples, distinguish undefined rates from zero, and keep tool permissions independent of retrieved notes. |

The audit runs with a deterministic model. For its final integration check,
complete `deep_learning evaluation`, `agents protocol`, and `agents runtime`.
The audit's first two project checks use a small injected counter so you can
work on the cohort calculations independently.

## Checks to do by hand

- For a sensor with readings `0`, missing, and `6`, calculate how many
  observations contribute to its mean. Decide what should happen if the
  same sensor and tick appear twice.
- For a path ending at `(9, 4)`, predict its projection onto `(0, 1)`.
  Trace the order in which Python resolves `2 * vector`.
- Starting the interaction model at zero, compute the gradient for the
  product coefficient over the four balanced sign pairs. Repeat after you
  duplicate every row and compare the two updates.
- Compare a cohort with zero positive labels to a cohort where every positive
  is detected. Decide which one you can include in a comparison of miss rates.
