from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Float, Date
from sqlalchemy.sql import func  # <--- Added this import
from database import Base
import enum

# 1. Enums matching the Database exactly
class UserRole(str, enum.Enum):
    super_admin = "super_admin"
    barangay_official = "barangay_official"
    resident = "resident"

class AnnouncementStatus(str, enum.Enum):
    active = "Active"
    archived = "Archived"

class FeedbackStatus(str, enum.Enum):
    pending = "Pending"
    reviewed = "Reviewed"
    resolved = "Resolved"

# 2. All Tables
class User(Base):
    __tablename__ = "tbl_Users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    roles = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, server_default=func.now())  # <--- Fixed

class Admin(Base):
    __tablename__ = "tbl_Admin"
    admin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    birthday = Column(Date)
    gender = Column(String(20))
    contact = Column(String(20))

class Official(Base):
    __tablename__ = "tbl_Official"
    official_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    birthday = Column(Date)
    gender = Column(String(20))
    contact = Column(String(20))

class Resident(Base):
    __tablename__ = "tbl_Residents"
    resident_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    birthday = Column(Date)
    gender = Column(String(20))
    contact = Column(String(20))

class Announcement(Base):
    __tablename__ = "tbl_Announcement"
    announcement_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="SET NULL"))
    created_at = Column(DateTime, server_default=func.now())  # <--- Fixed
    status = Column(Enum(AnnouncementStatus), default=AnnouncementStatus.active)

class Feedback(Base):
    __tablename__ = "tbl_Feedback"
    feedback_id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("tbl_Residents.resident_id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(200))
    message = Column(Text, nullable=False)
    status = Column(Enum(FeedbackStatus), default=FeedbackStatus.pending)
    created_at = Column(DateTime, server_default=func.now())  # <--- Fixed

class DetectionLog(Base):
    __tablename__ = "tbl_DetectionLog"
    log_id = Column(Integer, primary_key=True, index=True)
    camera_location = Column(String(100))
    confidence_score = Column(Float)
    image_path = Column(String(255))
    timestamp = Column(DateTime, server_default=func.now())  # <--- Fixed

class Notification(Base):
    __tablename__ = "tbl_Notifications"
    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"))
    detection_log_id = Column(Integer, ForeignKey("tbl_DetectionLog.log_id", ondelete="SET NULL"))
    announcement_id = Column(Integer, ForeignKey("tbl_Announcement.announcement_id", ondelete="SET NULL"))
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())  # <--- Fixed

class AuditLog(Base):
    __tablename__ = "tbl_AuditLog"  # <--- Fixed name (was tbl_AuditLogs)
    audit_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())  # <--- Fixed

class Report(Base):
    __tablename__ = "tbl_Report"  # <--- Fixed name (was tbl_Reports)
    report_id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(50), nullable=False)
    generated_by = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(255))
    date_range_start = Column(Date)
    date_range_end = Column(Date)
    created_at = Column(DateTime, server_default=func.now())  # <--- Fixed