-- Create Database if it doesn't exist
CREATE DATABASE IF NOT EXISTS barangay_system_db;
USE barangay_system_db;

-- 1. TABLE: tbl_Users (Central Authentication)
-- Ref: Section 3.3.4 (Table 3.6) & Section 3.1.4
CREATE TABLE tbl_Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Will store bcrypt hash
    roles ENUM('Super Admin', 'Barangay Official', 'Resident') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABLE: tbl_Admin
-- Ref: Section 3.3.4 (Table 3.6)
CREATE TABLE tbl_Admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    birthday DATE,
    gender VARCHAR(20),
    contact VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 3. TABLE: tbl_Official
-- Ref: Section 3.3.4 (Table 3.6)
CREATE TABLE tbl_Official (
    official_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    birthday DATE,
    gender VARCHAR(20),
    contact VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 4. TABLE: tbl_Residents
-- Ref: Section 3.3.4 (Table 3.6) & Functional Requirement FR2 (Includes Address)
CREATE TABLE tbl_Residents (
    resident_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL, -- Required per FR2
    birthday DATE,
    gender VARCHAR(20),
    contact VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 5. TABLE: tbl_Announcement
-- Ref: Section 3.3.4 & Module 5 (Announcement Management)
CREATE TABLE tbl_Announcement (
    announcement_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    created_by INT, -- Links to Official or Admin ID
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Active', 'Archived') DEFAULT 'Active',
    FOREIGN KEY (created_by) REFERENCES tbl_Users(user_id) ON DELETE SET NULL
);

-- 6. TABLE: tbl_Feedback
-- Ref: Section 3.3.4 & Module 7 (Resident Feedback Collector)
CREATE TABLE tbl_Feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    resident_id INT NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    status ENUM('Pending', 'Reviewed', 'Resolved') DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resident_id) REFERENCES tbl_Residents(resident_id) ON DELETE CASCADE
);

-- 7. TABLE: tbl_DetectionLog
-- Ref: Section 3.3.4 & Module 2 (Vision-Trak AI Detector)
-- Stores the machine learning output metadata
CREATE TABLE tbl_DetectionLog (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    camera_location VARCHAR(100), -- To identify which camera/RPi sent this
    confidence_score FLOAT, -- e.g., 0.90
    image_path VARCHAR(255), -- Reference to saved evidence image
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 8. TABLE: tbl_Notifications
-- Ref: Section 3.3.4 & Module 4 (Notification Broadcast Service)
-- Links detection events or announcements to user alerts
CREATE TABLE tbl_Notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT, -- If specific user, or NULL for broadcast
    detection_log_id INT, -- Link to garbage truck event
    announcement_id INT, -- Link to announcement event
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (detection_log_id) REFERENCES tbl_DetectionLog(log_id) ON DELETE SET NULL,
    FOREIGN KEY (announcement_id) REFERENCES tbl_Announcement(announcement_id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 9. TABLE: tbl_AuditLogs
-- Ref: Section 3.3.4 & NFR13 (Audit Trail)
-- Immutable logging for accountability
CREATE TABLE tbl_AuditLogs (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(100) NOT NULL, -- e.g., "Add User", "Delete Announcement"
    description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 10. TABLE: tbl_Reports
-- Ref: Section 3.3.4 & Module 12 (Report Generation Engine)
CREATE TABLE tbl_Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(50) NOT NULL, -- e.g., "Activity Summary", "Detection Frequency"
    generated_by INT NOT NULL,
    file_path VARCHAR(255), -- Path to generated PDF/CSV
    date_range_start DATE,
    date_range_end DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (generated_by) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);