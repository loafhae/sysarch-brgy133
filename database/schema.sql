-- Create Database if it doesn't exist
CREATE DATABASE IF NOT EXISTS barangay_system_db;
USE barangay_system_db;

USE barangay_system_db;

-- 1. tbl_Users (Central Authentication)
-- Ref: PDF Table 3.6
CREATE TABLE tbl_Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    roles ENUM('Super Admin', 'Barangay Official', 'Resident') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. tbl_Admin (Super Admin Profiles)
-- Ref: PDF Table 3.6
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

-- 3. tbl_Official (Barangay Official Profiles)
-- Ref: PDF Table 3.6
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

-- 4. tbl_Residents (Resident Profiles)
-- Ref: PDF Table 3.6 & FR2 (Includes Address)
CREATE TABLE tbl_Residents (
    resident_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    birthday DATE,
    gender VARCHAR(20),
    contact VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 5. tbl_Announcement
-- Ref: PDF Table 3.6 & Section 3.1.2
CREATE TABLE tbl_Announcement (
    announcement_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    created_by INT, -- Links to User ID
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Active', 'Archived') DEFAULT 'Active',
    FOREIGN KEY (created_by) REFERENCES tbl_Users(user_id) ON DELETE SET NULL
);

-- 6. tbl_Feedback
-- Ref: PDF Table 3.6
CREATE TABLE tbl_Feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    resident_id INT NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    status ENUM('Pending', 'Reviewed', 'Resolved') DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resident_id) REFERENCES tbl_Residents(resident_id) ON DELETE CASCADE
);

-- 7. tbl_DetectionLog
-- Ref: PDF Table 3.6 & Section 3.3.2
CREATE TABLE tbl_DetectionLog (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    camera_location VARCHAR(100),
    confidence_score FLOAT,
    image_path VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 8. tbl_Notifications
-- Ref: PDF Table 3.6 & Section 3.3.2
CREATE TABLE tbl_Notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT, -- Null for broadcast
    detection_log_id INT,
    announcement_id INT,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (detection_log_id) REFERENCES tbl_DetectionLog(log_id) ON DELETE SET NULL,
    FOREIGN KEY (announcement_id) REFERENCES tbl_Announcement(announcement_id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 9. tbl_AuditLogs
-- Ref: PDF Table 3.6 & NFR13
CREATE TABLE tbl_AuditLogs (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 10. tbl_Reports
-- Ref: PDF Table 3.6
CREATE TABLE tbl_Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(50) NOT NULL,
    generated_by INT NOT NULL,
    file_path VARCHAR(255),
    date_range_start DATE,
    date_range_end DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (generated_by) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);