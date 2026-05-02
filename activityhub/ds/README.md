# Data Science

## Approach
Multi-class classification over 9 style buckets spanning yoga, dance, and
fitness.

## The key design choice
Users do not pick an activity in the quiz. The model predicts probabilities
across all 9 buckets at once. This means someone who describes themselves as
"calm beginner, structured, stress relief goal" can get recommended Hatha
yoga AND Pilates AND Contemporary ballet, a mix they wouldn't have found
by filtering themselves.

## Feature schema
- Input: age, gender, experience_level, group_preference, energy_preference,
  structure_preference, goal
- Target: style_bucket (9 classes across yoga/dance/fitness)
- Output: predict_proba - probability distribution over all 9 buckets

## Style buckets (9 total)
- Yoga-Calm (Hatha, Restorative, Yin)
- Yoga-Dynamic (Vinyasa, Power)
- Yoga-Aerial (Aerial)
- Dance-Latin (Salsa, Bachata)
- Dance-Urban (Hip-hop, Jazz funk)
- Dance-Classical (Contemporary, Ballet, Armenian folk)
- Fitness-HighIntensity (HIIT, CrossFit)
- Fitness-Strength (Strength training, Functional, TRX)
- Fitness-Controlled (Pilates)

## Data composition

| Dataset | Real | Synthetic | Total |
|---------|------|-----------|-------|
| Studios | 17 (Yerevan studios researched manually) | 6 (synthetic dance studios with realistic Yerevan addresses) | 23 |
| Classes | 63 (real schedules from studio Instagram pages) | 96 (generated from STYLE_ATTRS template) | 159 |
| Survey  | 44 (Google Form respondents) | 356 (augmented via augment_training.py) | 400 |

Synthetic data is marked with `is_synthetic=True` in studios.csv/classes.csv and `data_source='synthetic'` in survey.csv where applicable.

Generation script: `ds/scripts/generate_data.py` (run once to produce CSVs)

## Pipeline

All scripts are repeatable — re-run any time without breaking state.

### End-to-end (preferred)
```bash
python -m ds.scripts.run_pipeline
```
Runs generate → combine → prepare → augment → train. Outputs `ds/models/style_classifier.pkl` and `ds/models/metrics.csv`.

### Individual steps
```bash
python -m ds.scripts.generate_synthetic_survey   # ~270 persona-based rows
python -m ds.scripts.prepare_survey              # combined training_survey.csv
python -m ds.scripts.augment_training            # 1× to 3× rows
python -m ds.scripts.train_model                 # train + save pkl
python -m ds.scripts.segment_users               # K-means to DB segments table
```

## Pipeline outputs (closes #79)

| Output                                   | Format       | Consumed by              |
|------------------------------------------|--------------|--------------------------|
| `ds/models/style_classifier.pkl`         | joblib       | `shared/recommend.py`    |
| `ds/models/metrics.csv`                  | csv          | reporting / docs         |
| Class-bucket predict_proba (live)        | API response | Frontend recommendations |
| Confidence scores (per recommendation)   | API response | Frontend match badges    |
| User personas + sizes                    | DB rows      | Studio dashboard         |

## Synthetic data strategy

We generate synthetic survey rows using **persona templates** rather than just
adding noise to existing rows. Each persona (e.g. "Yoga Calm Seeker") defines
realistic ranges for age, energy, goal, etc., and the script samples ~30 rows
per persona. This gives every style bucket enough samples to train confidently.

| Dataset | Real | Synthetic | Total |
|---------|------|-----------|-------|
| Studios | 17 | 6 | 23 |
| Classes | 63 | 96 | 159 |
| Survey  | 44 | 270 (persona) | 314 |
| Training rows after augmentation | — | — | ~600 |

Synthetic rows are tagged `data_source='synthetic'` so they can be filtered
out for evaluation if needed.

## Feature engineering

| Feature                | Type        | Notes                                 |
|------------------------|-------------|---------------------------------------|
| age                    | numeric     | StandardScaler                        |
| gender                 | categorical | OneHotEncoder                         |
| experience_level       | categorical | beginner/intermediate/advanced        |
| group_preference       | categorical | solo/small/large                      |
| energy_preference      | categorical | low/moderate/high                     |
| structure_preference   | categorical | structured/free-form                  |
| goal                   | categorical | stress-relief/fitness/social/etc      |

Activity choice (yoga/dance/fitness) is intentionally NOT a feature, the model
recommends across all 9 buckets so users discover styles they wouldn't have
picked themselves.

We also use `class_weight="balanced"` on both LogisticRegression and
RandomForestClassifier so rare buckets (e.g. Yoga-Calm) get learned despite
having fewer samples.

## Limitations
- Synthetic data is template-driven, not behavioral — real users may surprise us
- The model recommends style buckets, not individual classes — final ranking
  combines bucket probability with budget/district filters in `shared/recommend.py`
  
## Metrics
- **Top-3 accuracy**
- Top-1 accuracy
- Per-class precision / recall / F1
- Held-out test set (20%, stratified)

