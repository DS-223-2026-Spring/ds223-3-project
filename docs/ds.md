# Data Science

## Approach

Multi-class classifier predicting style buckets across all 9 categories
spanning yoga, dance, and fitness.

The key design choice: **activity is not a feature**. The model predicts
probabilities across all 9 buckets at once, so a "calm beginner, structured,
stress-relief" user can be recommended Hatha yoga AND Pilates AND Contemporary
ballet, a mix they wouldn't have filtered for themselves.

## Feature schema

| Feature | Type | Encoding |
|---------|------|----------|
| age | numeric | StandardScaler |
| gender | categorical | OneHotEncoder |
| experience_level | categorical | beginner/intermediate/advanced |
| group_preference | categorical | solo/small/large |
| energy_preference | categorical | low/moderate/high |
| structure_preference | categorical | structured/free-form |
| goal | categorical | stress-relief/fitness/social/etc |

Activity (yoga/dance/fitness) is intentionally NOT a feature as the model
recommends across all 9 buckets so users discover styles they wouldn't have
picked themselves.

## Style buckets (9 total)

- **Yoga-Calm** (Hatha, Restorative, Yin)
- **Yoga-Dynamic** (Vinyasa, Power)
- **Yoga-Aerial** (Aerial)
- **Dance-Latin** (Salsa, Bachata)
- **Dance-Urban** (Hip-hop, Jazz funk)
- **Dance-Classical** (Contemporary, Ballet, Armenian folk)
- **Fitness-HighIntensity** (HIIT, CrossFit)
- **Fitness-Strength** (Strength, Functional, TRX)
- **Fitness-Controlled** (Pilates)

## Data composition

| Dataset | Real | Synthetic | Total |
|---------|------|-----------|-------|
| Studios | 17 | 6 | 23 |
| Classes | 63 | 96 | 159 |
| Survey  | 44 | 270 | 314 |

Synthetic respondents are generated from 9 persona templates, each mapping to
one style bucket, with realistic ranges for age, gender, and preferences. Rows
are tagged `data_source='synthetic'` so they can be filtered for evaluation.

## Performance

| Model | Top-1 | Top-3 |
|-------|-------|-------|
| Logistic Regression | 0.541 | 0.905 |
| Random Forest | 0.636 | 0.951 |

Top-3 accuracy is the headline metric because we surface 3 recommendations to
each user. Random Forest is the production model.

`class_weight="balanced"` is used on both models so rare buckets
(e.g. Yoga-Aerial) get learned despite having fewer samples.

## K-means user segmentation

A separate K-means model (k=4) clusters users into marketing personas for the
studio-facing dashboard:

- **Calm Beginner**
- **High-Energy Strength**
- **Social Dancer**
- **Wellness Seeker**

Clustering features: experience_level, group_preference, energy_preference,
structure_preference, goal.

## Limitations

- Synthetic data is template-driven, not behavioral
- Augmentation can leak near-duplicates into the test split; reported top-3
  accuracy is optimistic
- Booking likelihood per segment is currently a placeholder derived from
  cluster size, not actual booking behavior