from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, Float, Boolean, Date
from database import Base
import enum

# --- Enums (Matching SQL ENUM types) ---
class UserRole(str, enum.Enum):
    super_admin = "Super Admin"
    barangay_official = "Barangay Official"
    resident = "Resident"

class AnnouncementStatus(str, enum.Enum):
    active = "Active"
    archived = "Archived"

class FeedbackStatus(str, enum.Enum):
    pending = "Pending"
    reviewed = "Reviewed"
    resolved = "Resolved"

# --- Models ---

class User(Base):
    __tablename__ = "tbl_Users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False) # Stores bcrypt hash
    roles = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")

class Admin(Base):
    __tablename__ = "tbl_Admin"

    admin_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    contact = Column(String(20), nullable=True)

class Official(Base):
    __tablename__ = "tbl_Official"

    official_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    contact = Column(String(20), nullable=True)

class Resident(Base):
    __tablename__ = "tbl_Residents"

    resident_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False) # Required per PDF FR2
    birthday = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    contact = Column(String(20), nullable=True)

class Announcement(Base):
    __tablename__ = "tbl_Announcement"

    announcement_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    status = Column(Enum(AnnouncementStatus), default=AnnouncementStatus.active)

class Feedback(Base):
    __tablename__ = "tbl_Feedback"

    feedback_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resident_id = Column(Integer, ForeignKey("tbl_Residents.resident_id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(200), nullable=True)
    message = Column(Text, nullable=False)
    status = Column(Enum(FeedbackStatus), default=FeedbackStatus.pending)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")

class DetectionLog(Base):
    __tablename__ = "tbl_DetectionLog"

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    camera_location = Column(String(100), nullable=True)
    confidence_score = Column(Float, nullable=True)
    image_path = Column(String(255), nullable=True)
    timestamp = Column(DateTime, server_default="CURRENT_TIMESTAMP")

class Notification(Base):
    __tablename__ = "tbl_Notifications"

    notification_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), nullable=True) # Null for broadcast
    detection_log_id = Column(Integer, ForeignKey("tbl_DetectionLog.log_id", ondelete="SET NULL"), nullable=True)
    announcement_id = Column(Integer, ForeignKey("tbl_Announcement.announcement_id", ondelete="SET NULL"), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")

class AuditLog(Base):
    __tablename__ = "tbl_AuditLogs"

    audit_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    timestamp = Column(DateTime, server_default="CURRENT_TIMESTAMP")

class Report(Base):
    __tablename__ = "tbl_Reports"

    report_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_type = Column(String(50), nullable=False)
    generated_by = Column(Integer, ForeignKey("tbl_Users.user_id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(255), nullable=True)
    date_range_start = Column(Date, nullable=True)
    date_range_end = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")