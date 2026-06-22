# 🤖 ML-Enhanced Clash Prevention System

## Overview

The timetable system now includes intelligent machine learning features for clash prevention and smart recommendations. This module uses scikit-learn to predict scheduling conflicts before they occur and provides actionable recommendations.

## Features

### 1. **Clash Risk Prediction** 🎯
Predicts the likelihood of scheduling conflicts using machine learning.

```python
from services.clash_service import ClashService

# Get clash risk for a proposed scheduling
risk = ClashService.predict_clash_risk(
    faculty_id=1,
    division_id=2,
    subject_id=3,
    time_slot_id=1,
    day='Monday',
    room_number='101'
)

# Returns:
# {
#     'risk_score': 0.35,           # 0-1, lower is better
#     'risk_level': 'low',          # 'low', 'medium', 'high'
#     'confidence': 0.92            # Model confidence (0-1)
# }
```

### 2. **Smart Time Slot Recommendations** ⏰
Get intelligent suggestions for alternative time slots with low clash risk.

```python
recommendations = ClashService.get_smart_slot_recommendations(
    faculty_id=1,
    division_id=2,
    subject_id=3,
    preferred_day='Monday',
    exclude_slot_id=None
)

# Returns:
# [
#     {
#         'slot_id': 5,
#         'time_range': '09:00 - 10:00',
#         'day': 'Monday',
#         'clash_risk': 0.15,
#         'status': 'available'
#     },
#     ...
# ]
```

### 3. **Faculty Recommendations** 👥
Get recommendations for the best faculty to teach a subject based on:
- Subject expertise
- Availability
- Current workload
- Teaching preferences

```python
faculty_list = ClashService.recommend_best_faculty(
    subject_id=3,
    division_id=2,
    preferred_day='Monday',
    preferred_time_slot_id=1
)

# Returns:
# [
#     {
#         'faculty_id': 5,
#         'faculty_name': 'Dr. John Doe',
#         'subject_match': 1.0,         # Can teach this subject
#         'availability_score': 1.0,    # Available at this time
#         'overall_score': 0.95,        # Composite score
#         'can_teach_subject': True,
#         'current_workload': 12
#     },
#     ...
# ]
```

### 4. **Timetable Quality Evaluation** 📊
Evaluate the overall quality and feasibility of a complete timetable.

```python
timetable_entries = [
    {
        'faculty_id': 1,
        'division_id': 2,
        'subject_id': 3,
        'time_slot_id': 1,
        'day': 'Monday',
        'room_number': '101'
    },
    # ... more entries
]

quality = ClashService.evaluate_timetable_quality(timetable_entries)

# Returns:
# {
#     'quality_score': 0.87,
#     'issues': [],
#     'recommendations': ['Consider alternative faculty assignments'],
#     'feasibility': 'high'
# }
```

### 5. **Clash Risk Summary** 📈
Get overall statistics on clash risks across the timetable.

```python
summary = ClashService.get_clash_risk_summary(division_id=None)

# Returns:
# {
#     'average_risk_score': 0.32,
#     'high_risk_entries': 2,
#     'medium_risk_entries': 8,
#     'low_risk_entries': 45,
#     'total_entries': 55,
#     'risk_distribution': {
#         'high': 2,
#         'medium': 8,
#         'low': 45
#     }
# }
```

## How It Works

### ML Model Training
The system automatically trains a Random Forest classifier on your historical timetable data:

```python
# Train model (call periodically, e.g., weekly)
success = ClashService.train_clash_prediction_model()
```

**Training Data:**
- Faculty ID
- Division ID
- Subject ID
- Time Slot ID
- Day of week
- Room number

**Output:**
- Clash probability (0-1)

### Risk Scoring Algorithm

1. **Faculty Availability Check** - Hard constraint check
2. **Subject Expertise Match** - Soft constraint
3. **Time Slot Overlap Analysis** - Pattern matching
4. **Workload Distribution** - Balancing factor
5. **Historical Patterns** - ML model prediction

### Model Persistence
Trained models are automatically saved to `ml_models/clash_predictor_model.pkl` and reloaded on startup.

## Integration in Flask Routes

### Example: Add to Timetable Creation

```python
@app.route('/api/create_timetable_entry', methods=['POST'])
def create_timetable_entry():
    data = request.json
    
    # Check basic conflicts
    is_valid, clashes = ClashService.validate_and_detect_clashes(
        data['faculty_id'],
        data['division_id'],
        data['room_number'],
        data['day'],
        data['time_slot_id']
    )
    
    if not is_valid:
        return jsonify({
            'success': False,
            'message': 'Conflicts detected',
            'clashes': clashes
        }), 400
    
    # Get ML risk prediction
    risk = ClashService.predict_clash_risk(
        data['faculty_id'],
        data['division_id'],
        data['subject_id'],
        data['time_slot_id'],
        data['day'],
        data['room_number']
    )
    
    # Warn if high risk
    if risk['risk_level'] == 'high':
        # Get recommendations
        recommendations = ClashService.get_smart_slot_recommendations(
            data['faculty_id'],
            data['division_id'],
            data['subject_id'],
            data['day']
        )
        
        return jsonify({
            'success': False,
            'message': 'High clash risk detected',
            'risk': risk,
            'recommendations': recommendations,
            'allow_override': True
        })
    
    # Create the entry
    # ... rest of the logic
```

## Best Practices

1. **Train Regularly**: Retrain the model weekly or when adding 50+ new entries
2. **Monitor Risks**: Use `get_clash_risk_summary()` to track timetable health
3. **Act on Recommendations**: Use smart slot recommendations to resolve conflicts
4. **Faculty Matching**: Always use `recommend_best_faculty()` for new assignments
5. **Quality Checks**: Evaluate timetable quality before finalizing

## Configuration

### Tuning ML Model Sensitivity

Edit `services/ml_clash_predictor.py` to adjust:

```python
# Risk thresholds
LOW_RISK_THRESHOLD = 0.3        # < 30% = low risk
MEDIUM_RISK_THRESHOLD = 0.7     # 30-70% = medium risk
HIGH_RISK_THRESHOLD = 0.7       # > 70% = high risk

# Model parameters
n_estimators=100                 # Number of trees
max_depth=10                     # Tree depth
```

## Performance Notes

- **Training time**: ~1-5 seconds (depending on data size)
- **Prediction time**: <50ms per prediction
- **Memory usage**: ~10-50MB
- **Model size**: ~100-500KB

## Troubleshooting

### Model not learning well
- **Solution**: Ensure at least 50+ timetable entries before training

### Predictions seem random
- **Solution**: Retrain model after adding new data

### High memory usage
- **Solution**: Reduce `n_estimators` in Random Forest configuration

## Future Enhancements

- [ ] Deep learning models (Neural Networks)
- [ ] Genetic algorithm-based optimization
- [ ] Constraint solver integration
- [ ] Real-time model updates
- [ ] Web UI for clash analysis dashboard
