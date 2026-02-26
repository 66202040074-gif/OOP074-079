from datetime import datetime
from enum import Enum

class Gender(Enum):
    """ระบุเพศ"""
    MALE = "male"
    FEMALE = "female"

class Activity(Enum):
    """ระดับการออกแบบ"""
    SEDENTARY = 1.2  # นั่งประจำ
    LIGHTLY_ACTIVE = 1.375  # ออกกำลังน้อย
    MODERATELY_ACTIVE = 1.55  # ออกกำลังปานกลาง
    VERY_ACTIVE = 1.725  # ออกกำลังมาก
    EXTREMELY_ACTIVE = 1.9  # ออกกำลังหนัก

class Person:
    """คลาสแทนคนเดียว"""
    
    def __init__(self, name, age, weight_kg, height_cm, gender):
        """
        สร้างอ็อบเจกต์คน
        
        Args:
            name (str): ชื่อ
            age (int): อายุ (ปี)
            weight_kg (float): น้ำหนัก (กิโลกรัม)
            height_cm (float): ส่วนสูง (เซนติเมตร)
            gender (Gender): เพศ
        """
        self.name = name
        self.age = age
        self.weight_kg = weight_kg
        self.height_cm = height_cm
        self.gender = gender
        self.created_date = datetime.now()
    
    def get_bmi(self):
        """คำนวณ BMI"""
        height_m = self.height_cm / 100
        bmi = self.weight_kg / (height_m ** 2)
        return round(bmi, 2)
    
    def get_bmi_category(self):
        """ตรวจสอบหมวดหมู่ BMI"""
        bmi = self.get_bmi()
        
        if bmi < 18.5:
            return "ต่ำกว่าเกณฑ์" 
        elif 18.5 <= bmi < 25:
            return "น้ำหนักปกติ"
        elif 25 <= bmi < 30:
            return "ท้องอ้วน"
        else:
            return "อ้วนมาก"
    
    def get_info(self):
        """ส่งข้อมูลของบุคคล"""
        return {
            "name": self.name,
            "age": self.age,
            "weight_kg": self.weight_kg,
            "height_cm": self.height_cm,
            "gender": self.gender.value,
            "bmi": self.get_bmi(),
            "bmi_category": self.get_bmi_category()
        }

class CalorieCalculator:
    """คลาสสำหรับคำนวณแคลอรี่"""
    
    # ตารางแคลอรี่ของกิจกรรมต่างๆ (แคลอรี่/นาที)
    ACTIVITIES = {
        "เดิน (ช้า)": 3,
        "เดิน (ปกติ)": 4,
        "เดิน (เร็ว)": 5,
        "วิ่ง": 8,
        "ว่ายน้ำ": 7,
        "ปั่นจักรยาน": 6,
        "โยคะ": 3,
        "เต้น": 5,
        "กีฬา (ทั่วไป)": 6,
        "เล่นเกม": 1.5,
        "นั่งทำงาน": 1,
        "นอน": 1
    }
    
    def __init__(self, person):
        """
        สร้าง CalorieCalculator
        
        Args:
            person (Person): อ็อบเจกต์ Person
        """
        self.person = person
    
    def calculate_tdee(self, activity_level):
        """
        คำนวณแคลอรี่ที่ใช้ในแต่ละวัน (TDEE - Total Daily Energy Expenditure)
        
        Args:
            activity_level (Activity): ระดับการออกกำลัง
        
        Returns:
            float: แคลอรี่ที่ใช้ต่อวัน
        """
        bmr = self.calculate_bmr()
        tdee = bmr * activity_level.value
        return round(tdee, 2)
    
    def calculate_bmr(self):
        """
        คำนวณ BMR (Basal Metabolic Rate) โดยใช้สูตร Mifflin-St Jeor
        
        Returns:
            float: แคลอรี่ต่อวัน
        """
        weight = self.person.weight_kg
        height = self.person.height_cm
        age = self.person.age
        
        if self.person.gender == Gender.MALE:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
        return round(bmr, 2)
    
    def calculate_activity_calories(self, activity_name, minutes):
        """
        คำนวณแคลอรี่ที่ใช้ในกิจกรรม
        
        Args:
            activity_name (str): ชื่อกิจกรรม
            minutes (int): ระยะเวลา (นาที)
        
        Returns:
            dict: ข้อมูลแคลอรี่ที่ใช้
        """
        if activity_name not in self.ACTIVITIES:
            return {"error": f"ไม่พบกิจกรรม: {activity_name}"}
        
        calories_per_minute = self.ACTIVITIES[activity_name]
        total_calories = calories_per_minute * minutes
        
        return {
            "activity": activity_name,
            "duration_minutes": minutes,
            "calories_burned": round(total_calories, 2)
        }
    
    def get_all_activities(self):
        """ส่งรายชื่อกิจกรรมทั้งหมด"""
        return self.ACTIVITIES
    
    def get_calorie_info(self, activity_level):
        """
        ส่งข้อมูลแคลอรี่อย่างละเอียด
        
        Args:
            activity_level (Activity): ระดับการออกกำลัง
        
        Returns:
            dict: ข้อมูลแคลอรี่ทั้งหมด
        """
        return {
            "person": self.person.get_info(),
            "bmr": self.calculate_bmr(),
            "activity_level": activity_level.name,
            "tdee": self.calculate_tdee(activity_level),
            "daily_goal": {
                "lose_weight": round(self.calculate_tdee(activity_level) - 500, 2),
                "maintain": round(self.calculate_tdee(activity_level), 2),
                "gain_weight": round(self.calculate_tdee(activity_level) + 500, 2)
            }
        }

class CalorieTracker:
    """กอบเก็บบันทึกการออกแบบ"""
    
    def __init__(self):
        self.logs = []
    
    def add_activity(self, activity_data):
        """เพิ่มบันทึกกิจกรรม"""
        log_entry = {
            "timestamp": datetime.now(),
            "activity": activity_data
        }
        self.logs.append(log_entry)
    
    def get_total_calories(self):
        """รวมแคลอรี่ทั้งหมด"""
        total = sum(log["activity"]["calories_burned"] for log in self.logs)
        return round(total, 2)
    
    def get_activity_logs(self):
        """ส่งบันทึกกิจกรรมทั้งหมด"""
        return self.logs
    
    def clear_logs(self):
        """ลบบันทึกทั้งหมด"""
        self.logs = []

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # สร้างอ็อบเจกต์ Person
    person = Person("สมชาย", 30, 75, 175, Gender.MALE)
    
    # สร้าง CalorieCalculator
    calc = CalorieCalculator(person)
    
    # แสดงข้อมูลบุคคล
    print("=== ข้อมูลบุคคล ===")
    print(person.get_info())
    
    # คำนวณแคลอรี่
    print("\n=== การคำนวณแคลอรี่ ===")
    print(f"BMR: {calc.calculate_bmr()} แคลอรี่/วัน")
    print(f"TDEE (ปานกลาง): {calc.calculate_tdee(Activity.MODERATELY_ACTIVE)} แคลอรี่/วัน")
    
    # ตัวอย่างกิจกรรม
    print("\n=== แคลอรี่จากกิจกรรม ===")
    activity = calc.calculate_activity_calories("วิ่ง", 30)
    print(activity)
    
    # บันทึกกิจกรรม
    tracker = CalorieTracker()
    tracker.add_activity(activity)
    print(f"\nแคลอรี่ทั้งหมด: {tracker.get_total_calories()}")
