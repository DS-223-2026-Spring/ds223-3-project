# Data Science

Multi-class classifier predicting style buckets across all 9 categories (yoga, dance, fitness).

## Approach
- Feature input: age, gender, experience, group preference, energy, structure, goal
- Target: 9 style buckets (e.g., Yoga-Calm, Dance-Latin, Fitness-Strength)
- Output: `predict_proba` distribution → top-3 class recommendations

## Performance
| Model | Top-1 | Top-3 |
|-------|-------|-------|
| Logistic Regression | 0.541 | 0.905 |
| Random Forest | 0.636 | 0.951 |

Random Forest selected as production model.
