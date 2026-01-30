-- Create Database
CREATE DATABASE IF NOT EXISTS barangay_system_db;
USE barangay_system_db;

-- 1. Users Table
CREATE TABLE tbl_Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    roles ENUM('super_admin', 'barangay_official', 'resident') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Admin Table
CREATE TABLE tbl_Admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    birthday DATE,
    gender VARCHAR(20),
    contact VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 3. Official Table
CREATE TABLE tbl_Official (
    official_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    birthday DATE,
    gender VARCHAR(20),
    contact VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE
);

-- 4. Residents Table
CREATE TABLE tbl_Residents (
    resident_id INT PRIMARY KEY AUTO_INCREMENT,
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

-- 5. Announcement Table
CREATE TABLE tbl_Announcement (
    announcement_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Active', 'Archived') DEFAULT 'Active',
    FOREIGN KEY (created_by) REFERENCES tbl_Users(user_id) ON DELETE SET NULL
);

-- 6. Feedback Table
CREATE TABLE tbl_Feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    resident_id INT NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    status ENUM('Pending', 'Reviewed', 'Resolved') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resident_id) REFERENCES tbl_Residents(resident_id) ON DELETE CASCADE
);

-- 7. Detection Log Table
CREATE TABLE tbl_DetectionLog (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    camera_location VARCHAR(100),
    confidence_score FLOAT,
    image_path VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Notifications Table
CREATE TABLE tbl_Notifications (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    detection_log_id INT,
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (detection_log_id) REFERENCES tbl_DetectionLog(log_id) ON DELETE SET NULL
);

-- 9. Audit Log Table
CREATE TABLE tbl_AuditLog (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_Users(user_id) ON DELETE SET NULL
);

-- 10. Report Table
CREATE TABLE tbl_Report (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES tbl_Users(user_id) ON DELETE SET NULL
);

-- Insert Test Data
INSERT INTO tbl_Users (username, password, roles) VALUES
('admin', 'admin123', 'super_admin'),
('official1', 'official123', 'barangay_official'),
('resident1', 'resident123', 'resident');

INSERT INTO tbl_Admin (user_id, first_name, last_name, gender, contact) VALUES
(1, 'John', 'Doe', 'Male', '09123456789');

INSERT INTO tbl_Official (user_id, first_name, last_name, gender, contact) VALUES
(2, 'Jane', 'Smith', 'Female', '09987654321');

INSERT INTO tbl_Residents (user_id, first_name, last_name, address, gender, contact) VALUES
(3, 'Maria', 'Garcia', '123 Main St', 'Female', '09555555555');