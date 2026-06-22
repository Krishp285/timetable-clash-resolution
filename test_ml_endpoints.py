#!/usr/bin/env python
"""Test ML API endpoints."""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_clash_risk_prediction():
    """Test clash risk prediction endpoint."""
    print("\n🧪 Testing Clash Risk Prediction...")
    response = requests.post(
        f"{BASE_URL}/api/ml/predict-clash-risk",
        json={
            "faculty_id": 1,
            "division_id": 6,
            "subject_id": 1,
            "time_slot_id": 1,
            "day": "Monday",
            "room_number": "101"
        }
    )
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

def test_slot_recommendations():
    """Test slot recommendations endpoint."""
    print("\n🧪 Testing Slot Recommendations...")
    response = requests.get(
        f"{BASE_URL}/api/ml/slot-recommendations",
        params={
            "faculty_id": 1,
            "division_id": 6,
            "subject_id": 1,
            "preferred_day": "Monday"
        }
    )
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

def test_faculty_recommendations():
    """Test faculty recommendations endpoint."""
    print("\n🧪 Testing Faculty Recommendations...")
    response = requests.get(
        f"{BASE_URL}/api/ml/recommend-faculty",
        params={
            "subject_id": 1,
            "division_id": 6,
            "preferred_day": "Monday",
            "preferred_time_slot_id": 1
        }
    )
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

def test_clash_risk_summary():
    """Test clash risk summary endpoint."""
    print("\n🧪 Testing Clash Risk Summary...")
    response = requests.get(
        f"{BASE_URL}/api/ml/clash-risk-summary",
        params={"division_id": 6}
    )
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

def test_evaluate_timetable():
    """Test timetable quality evaluation."""
    print("\n🧪 Testing Timetable Quality Evaluation...")
    response = requests.post(
        f"{BASE_URL}/api/ml/evaluate-timetable",
        json={
            "division_id": 6
        }
    )
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 ML API ENDPOINT TESTS")
    print("=" * 60)
    
    try:
        test_clash_risk_prediction()
        test_slot_recommendations()
        test_faculty_recommendations()
        test_clash_risk_summary()
        test_evaluate_timetable()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
