# AI

Machine-learning layer for the SportsAI simulation project.

The initial model is intentionally trained on **synthetic demonstration data**. It exists to show an end-to-end ML workflow without claiming real predictive performance.

## Train

From the repository root:

```bash
python ai/train_model.py
```

Output:

```text
ai/artifacts/sports_model.joblib
```

The training script:

1. Generates synthetic team-performance examples.
2. Builds a scikit-learn pipeline.
3. Trains a multiclass logistic-regression model.
4. Evaluates holdout accuracy.
5. Saves the model artifact.

## Production Direction

A production-quality system would replace synthetic data with licensed, validated historical sports data and would include:

- feature provenance
- train/validation/test separation by time
- calibration testing
- drift monitoring
- reproducible model/version metadata
- data-provider licensing review
