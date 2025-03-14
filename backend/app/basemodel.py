from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List

# ========================== #
#   STUDENT & FACULTY MODELS #
# ========================== #

class StudentProfile(BaseModel):
    enrollment_no: str
    name: str
    semester: int
    admission_date: date
    passing_date: Optional[date] = None
    mobile_no: str
    email: EmailStr

    class Config:
        from_attributes = True  # ORM mode

class FacultyProfile(BaseModel):
    faculty_id: int
    name: str
    email: EmailStr
    mobile_no: str
    department: str
    joining_date: date
    leaving_date: Optional[date] = None

    class Config:
        from_attributes = True

# ========================== #
#   LECTURE BOOKING MODELS   #
# ========================== #

class LectureBookingRequest(BaseModel):
    lecture_date: date
    start_time: str  # HH:MM:SS format
    end_time: str
    room_id: int
    semester: int
    subject_code: str
    faculty_id: int

class LectureBookingResponse(BaseModel):
    lecture_id: int
    lecture_date: date
    start_time: str
    end_time: str
    room_id: int
    semester: int
    subject_code: str
    faculty_id: int

    class Config:
        from_attributes = True

# ========================== #
#   FINAL STUDENT LIST MODELS #
# ========================== #

# Student record in the attendance list
class StudentAttendanceRecord(BaseModel):
    student_id: str
    name: str
    status: str  # 'Present' or 'Absent'

# Final Student List Response (After manual additions/removals)
class FinalStudentListResponse(BaseModel):
    lecture_id: int
    room_id: int
    students: List[StudentAttendanceRecord]

# Manually Add a Student to Attendance
class ManualAddStudent(BaseModel):
    lecture_id: int
    student_id: str

# Remove a Student from Attendance
class RemoveStudent(BaseModel):
    lecture_id: int
    student_id: str
