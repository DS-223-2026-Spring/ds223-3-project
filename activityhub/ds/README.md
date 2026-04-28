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
1. `prepare_survey.py` - pivot survey into (features, style_bucket) rows
2. `augment_training.py` - 2x augmentation with 10% attribute noise
3. `train_model.py` - train LR + RF, compare, save winner by top-3 accuracy

## Metrics
- **Top-3 accuracy**
- Top-1 accuracy
- Per-class precision / recall / F1
- Held-out test set (20%, stratified)

## Limitations
- Augmentation introduces synthetic variation but not new information
- The model recommends style buckets, not individual classes - the final
  class ranking combines bucket probability with business filters (budget,
  district) in `shared/recommend.py`
