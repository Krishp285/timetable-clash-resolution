# 🚀 Quick Start Guide - ML-Enhanced Clash Prevention

## ✅ Installation

1. **Install ML Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start Your Application:**
```bash
python app.py
```

## 📊 API Endpoints Reference

### 1. **Predict Clash Risk** 🎯
Predicts if a scheduling combination has high clash risk.

**Endpoint:** `POST /api/ml/predict-clash-risk`

**Request:**
```json
{
  "faculty_id": 1,
  "division_id": 2,
  "subject_id": 3,
  "time_slot_id": 1,
  "day": "Monday",
  "room_number": "101"
}
```

**Response:**
```json
{
  "success": true,
  "risk": {
    "risk_score": 0.35,
    "risk_level": "low",
    "confidence": 0.92
  }
}
```

---

### 2. **Get Slot Recommendations** ⏰
Get alternative time slots sorted by risk.

**Endpoint:** `GET/POST /api/ml/slot-recommendations`

**Query Parameters:**
- `faculty_id` (required)
- `division_id` (required)
- `subject_id` (required)
- `preferred_day` (optional, default: "Monday")

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "slot_id": 5,
      "time_range": "09:00 - 10:00",
      "day": "Monday",
      "clash_risk": 0.15,
      "status": "available"
    }
  ]
}
```

---

### 3. **Recommend Best Faculty** 👥
Get ranked faculty recommendations for a subject.

**Endpoint:** `GET/POST /api/ml/recommend-faculty`

**Query Parameters:**
- `subject_id` (required)
- `division_id` (required)
- `preferred_day` (optional)
- `preferred_time_slot_id` (optional)

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "faculty_id": 5,
      "faculty_name": "Dr. John Doe",
      "subject_match": 1.0,
      "availability_score": 1.0,
      "overall_score": 0.95,
      "can_teach_subject": true,
      "current_workload": 12
    }
  ]
}
```

---

### 4. **Evaluate Timetable Quality** 📊
Analyze overall timetable quality and get recommendations.

**Endpoint:** `POST /api/ml/evaluate-timetable`

**Request (Option 1 - Provide Entries):**
```json
{
  "entries": [
    {
      "faculty_id": 1,
      "division_id": 2,
      "subject_id": 3,
      "time_slot_id": 1,
      "day": "Monday",
      "room_number": "101"
    }
  ]
}
```

**Request (Option 2 - By Division ID):**
```json
{
  "division_id": 2
}
```

**Response:**
```json
{
  "success": true,
  "quality": {
    "quality_score": 0.87,
    "issues": [],
    "recommendations": [],
    "feasibility": "high"
  }
}
```

---

### 5. **Get Clash Risk Summary** 📈
Get risk statistics for your timetable.

**Endpoint:** `GET /api/ml/clash-risk-summary?division_id=2`

**Query Parameters:**
- `division_id` (optional, if omitted: entire timetable)

**Response:**
```json
{
  "success": true,
  "summary": {
    "average_risk_score": 0.32,
    "high_risk_entries": 2,
    "medium_risk_entries": 8,
    "low_risk_entries": 45,
    "total_entries": 55,
    "risk_distribution": {
      "high": 2,
      "medium": 8,
      "low": 45
    }
  }
}
```

---

### 6. **Train ML Model** 🤖
Train/retrain the ML model with current data.

**Endpoint:** `POST /api/ml/train-model`

**Response:**
```json
{
  "success": true,
  "message": "Model trained successfully"
}
```

---

## 🔧 Using ML Features in Your Code

### Python Examples

```python
from services.clash_service import ClashService

# Example 1: Check clash risk
risk = ClashService.predict_clash_risk(
    faculty_id=1,
    division_id=2,
    subject_id=3,
    time_slot_id=1,
    day='Monday',
    room_number='101'
)
print(f"Risk Score: {risk['risk_score']}")
print(f"Risk Level: {risk['risk_level']}")

# Example 2: Get recommendations
recommendations = ClashService.get_smart_slot_recommendations(
    faculty_id=1,
    division_id=2,
    subject_id=3,
    preferred_day='Monday'
)
for rec in recommendations:
    print(f"{rec['day']} {rec['time_range']} - Risk: {rec['clash_risk']}")

# Example 3: Recommend faculty
faculty_list = ClashService.recommend_best_faculty(
    subject_id=3,
    division_id=2,
    preferred_day='Monday',
    preferred_time_slot_id=1
)
for fac in faculty_list:
    print(f"{fac['faculty_name']} - Score: {fac['overall_score']}")
```

---

## 📱 Using ML Features in Web Templates

### JavaScript/HTML Example

```html
<script>
// Predict clash risk
fetch('/api/ml/predict-clash-risk', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        faculty_id: 1,
        division_id: 2,
        subject_id: 3,
        time_slot_id: 1,
        day: 'Monday',
        room_number: '101'
    })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Risk Level:', data.risk.risk_level);
        if (data.risk.risk_level === 'high') {
            alert('Warning: High clash risk detected!');
        }
    }
});

// Get slot recommendations
fetch('/api/ml/slot-recommendations?faculty_id=1&division_id=2&subject_id=3&preferred_day=Monday')
    .then(response => response.json())
    .then(data => {
        data.recommendations.forEach(rec => {
            console.log(`${rec.day} ${rec.time_range}: ${rec.status}`);
        });
    });
</script>
```

---

## 🎯 Best Practices

1. **Train Model Weekly**: Call `/api/ml/train-model` after adding 50+ new entries
2. **Monitor Risk**: Check summary daily to identify problematic entries
3. **Use Recommendations**: Always use smart slot recommendations when adding entries
4. **Evaluate Before Finalizing**: Always call `evaluate-timetable` before finalizing
5. **Handle Errors**: Always wrap API calls in try-catch blocks

---

## ⚙️ Model Configuration

To adjust ML model sensitivity, edit [services/ml_clash_predictor.py](services/ml_clash_predictor.py):

```python
# Risk thresholds (change these to adjust sensitivity)
if clash_probability < 0.3:
    risk_level = 'low'
elif clash_probability < 0.7:
    risk_level = 'medium'
else:
    risk_level = 'high'
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not predicting well | Train the model first: `POST /api/ml/train-model` |
| Low confidence scores | Ensure you have 50+ timetable entries |
| API returns 400 error | Check request parameters match expected types |
| High memory usage | Reduce `n_estimators` in ML config |

---

## 📚 More Information

See [ML_INTEGRATION_GUIDE.md](ML_INTEGRATION_GUIDE.md) for detailed documentation on:
- How ML models work
- Feature extraction
- Model training process
- Advanced configuration
- Performance tuning

---

## 🎓 Summary

Your timetable system now has intelligent ML-powered features:
- ✅ Clash risk prediction
- ✅ Smart slot recommendations
- ✅ Faculty matching
- ✅ Timetable quality evaluation
- ✅ Risk analytics

**Start using these APIs in your timetable creation page to provide better recommendations to admins!**
