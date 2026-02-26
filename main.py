"""
โปรเจกต์ Calorie Calculator - OOP
เป็นแอปพลิเคชันสำหรับคำนวณแคลอรี่แบบ Object-Oriented Programming
"""

from flask import Flask, render_template, jsonify, request
import os
from bmi import Person, Gender, Activity, CalorieCalculator, CalorieTracker

# สร้าง Flask app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# ตัวแปรทั่วโลก
current_person = None
calorie_calculator = None
tracker = CalorieTracker()

@app.route('/')
def index():
    """หน้าแรก"""
    return render_template('index.html')

@app.route('/api/create-person', methods=['POST'])
def create_person():
    """API: สร้างข้อมูลบุคคล"""
    global current_person, calorie_calculator
    
    try:
        data = request.json
        
        # ตรวจสอบข้อมูล
        if not all([data.get('name'), data.get('age'), data.get('weight'), 
                   data.get('height'), data.get('gender')]):
            return jsonify({'error': 'ข้อมูลไม่ครบถ้วน'}), 400
        
        # สร้างอ็อบเจกต์ Person
        gender = Gender.MALE if data['gender'] == 'male' else Gender.FEMALE
        current_person = Person(
            name=data['name'],
            age=int(data['age']),
            weight_kg=float(data['weight']),
            height_cm=float(data['height']),
            gender=gender
        )
        
        # สร้าง CalorieCalculator
        calorie_calculator = CalorieCalculator(current_person)
        
        # ส่งคืนข้อมูล
        return jsonify({
            'success': True,
            'person': current_person.get_info()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/calculate-calories', methods=['POST'])
def calculate_calories():
    """API: คำนวณแคลอรี่"""
    global calorie_calculator
    
    if not calorie_calculator:
        return jsonify({'error': 'กรุณาสร้างข้อมูลบุคคลก่อน'}), 400
    
    try:
        data = request.json
        activity_level_map = {
            'sedentary': Activity.SEDENTARY,
            'lightly': Activity.LIGHTLY_ACTIVE,
            'moderate': Activity.MODERATELY_ACTIVE,
            'very': Activity.VERY_ACTIVE,
            'extreme': Activity.EXTREMELY_ACTIVE
        }
        
        activity_level = activity_level_map.get(data.get('activity_level'))
        if not activity_level:
            return jsonify({'error': 'ระดับการออกกำลังไม่ถูกต้อง'}), 400
        
        # คำนวณ
        calorie_info = calorie_calculator.get_calorie_info(activity_level)
        
        return jsonify({
            'success': True,
            'data': calorie_info
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/calculate-activity', methods=['POST'])
def calculate_activity():
    """API: คำนวณแคลอรี่จากกิจกรรม"""
    global calorie_calculator
    
    if not calorie_calculator:
        return jsonify({'error': 'กรุณาสร้างข้อมูลบุคคลก่อน'}), 400
    
    try:
        data = request.json
        activity_name = data.get('activity')
        minutes = int(data.get('duration', 0))
        
        if not activity_name or minutes <= 0:
            return jsonify({'error': 'ข้อมูลกิจกรรมไม่ถูกต้อง'}), 400
        
        # คำนวณ
        result = calorie_calculator.calculate_activity_calories(activity_name, minutes)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/add-activity', methods=['POST'])
def add_activity():
    """API: เพิ่มกิจกรรมไปยังบันทึก"""
    global tracker
    
    try:
        data = request.json
        tracker.add_activity(data)
        
        return jsonify({
            'success': True,
            'total_calories': tracker.get_total_calories()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/get-tracker', methods=['GET'])
def get_tracker():
    """API: ดึงบันทึกทั้งหมด"""
    global tracker
    
    logs = []
    for log in tracker.get_activity_logs():
        logs.append({
            'timestamp': log['timestamp'].isoformat(),
            'activity': log['activity']['activity'],
            'duration': log['activity']['duration_minutes'],
            'calories': log['activity']['calories_burned']
        })
    
    return jsonify({
        'success': True,
        'logs': logs,
        'total_calories': tracker.get_total_calories()
    })

@app.route('/api/clear-tracker', methods=['POST'])
def clear_tracker():
    """API: ล้างบันทึก"""
    global tracker
    
    tracker.clear_logs()
    
    return jsonify({
        'success': True,
        'message': 'ล้างบันทึกสำเร็จ'
    })

@app.route('/api/get-activities', methods=['GET'])
def get_activities():
    """API: ดึงรายชื่อกิจกรรม"""
    if not calorie_calculator:
        return jsonify({'error': 'กรุณาสร้างข้อมูลบุคคลก่อน'}), 400
    
    activities = calorie_calculator.get_all_activities()
    return jsonify({
        'success': True,
        'activities': activities
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 Calorie Calculator OOP Application")
    print("=" * 60)
    print("\n▶️  กำลังเริ่มต้น Flask Server...")
    print("📱 เปิดเบราว์เซอร์ที่: http://localhost:5000")
    print("🛑 กด Ctrl+C เพื่อหยุดเซิร์ฟเวอร์\n")
    
    app.run(debug=True, host='localhost', port=5000)
