from sqlalchemy import Column, String, Integer, Date, ForeignKey, Time, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    enrollment_no = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    semester = Column(Integer, CheckConstraint("semester BETWEEN 1 AND 8"))
    admission_date = Column(Date, nullable=False)
    passing_date = Column(Date, default=None)
    mobile_no = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Relationships
    attendance_records = relationship("Attendance", back_populates="student")

class Faculty(Base):
    __tablename__ = "faculty"

    faculty_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    mobile_no = Column(String(15), unique=True, nullable=False)
    joining_date = Column(Date, nullable=False)
    leaving_date = Column(Date, default=None)
    password_hash = Column(String(255), nullable=False)

    # Relationships
    lectures = relationship("DailyLecture", back_populates="faculty")

class Subject(Base):
    __tablename__ = "subjects"

    subject_code = Column(String(20), primary_key=True)
    subject_name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    semester = Column(Integer, CheckConstraint("semester BETWEEN 1 AND 8"), nullable=False)
    credits = Column(Integer, CheckConstraint("credits > 0"), nullable=False)

    # Relationships
    lectures = relationship("DailyLecture", back_populates="subject")

class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(50), unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    camera_ip = Column(String(50), unique=True, nullable=False)

    # Relationships
    lectures = relationship("DailyLecture", back_populates="room")

class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(20), ForeignKey("students.enrollment_no"))
    lecture_id = Column(Integer, ForeignKey("daily_lectures.lecture_id"))

    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    lecture = relationship("DailyLecture", back_populates="attendance_records")

class DailyLecture(Base):
    __tablename__ = "daily_lectures"

    lecture_id = Column(Integer, primary_key=True, autoincrement=True)
    lecture_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    semester = Column(Integer, CheckConstraint("semester BETWEEN 1 AND 8"), nullable=False)
    subject_code = Column(String(20), ForeignKey("subjects.subject_code"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.faculty_id"))

    __table_args__ = (CheckConstraint("end_time > start_time"),)

    # Relationships
    room = relationship("Room", back_populates="lectures")
    subject = relationship("Subject", back_populates="lectures")
    faculty = relationship("Faculty", back_populates="lectures")
    attendance_records = relationship("Attendance", back_populates="lecture")