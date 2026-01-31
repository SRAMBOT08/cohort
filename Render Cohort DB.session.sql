-- ========================================
-- COHORT DATABASE DIAGNOSTIC QUERIES
-- ========================================
-- 1. List all tables in the database
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
-- 2. Count records in each table (estimated row counts - fast)
SELECT schemaname,
    relname as tablename,
    n_live_tup as row_count
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;
-- ========================================
-- USER & MENTOR ASSIGNMENT QUERIES
-- ========================================
-- 3. Check all users with their roles
SELECT u.id,
    u.username,
    u.email,
    u.is_active,
    up.role,
    up.floor,
    up.campus,
    up.assigned_mentor_id
FROM auth_user u
    LEFT JOIN profiles_userprofile up ON u.id = up.user_id
ORDER BY up.role,
    u.id;
-- 4. Check mentor-student assignments
SELECT u.id as student_id,
    u.username as student_username,
    u.email as student_email,
    up.role,
    up.floor,
    up.assigned_mentor_id,
    mentor.username as mentor_username,
    mentor.email as mentor_email
FROM auth_user u
    LEFT JOIN profiles_userprofile up ON u.id = up.user_id
    LEFT JOIN auth_user mentor ON up.assigned_mentor_id = mentor.id
WHERE up.role = 'STUDENT'
ORDER BY up.assigned_mentor_id;
-- 5. Check all mentors and their student counts
SELECT m.id as mentor_id,
    m.username as mentor_username,
    m.email as mentor_email,
    mp.role,
    mp.floor,
    COUNT(up.id) as student_count
FROM auth_user m
    JOIN profiles_userprofile mp ON m.id = mp.user_id
    AND mp.role IN ('MENTOR', 'FLOOR_WING', 'ADMIN')
    LEFT JOIN profiles_userprofile up ON up.assigned_mentor_id = m.id
GROUP BY m.id,
    m.username,
    m.email,
    mp.role,
    mp.floor;
-- ========================================
-- SUBMISSION QUERIES
-- ========================================
-- 6. Check SCD LeetCode submissions
SELECT *
FROM scd_leetcodesubmission
ORDER BY id DESC
LIMIT 10;
-- Check CFC Hackathon registrations (4 rows)
SELECT *
FROM cfc_hackathonregistration
ORDER BY id DESC;
-- Check CFC submissions
SELECT *
FROM cfc_internshipsubmission;
SELECT *
FROM cfc_genaiprojectsubmission;
SELECT *
FROM cfc_bmcvideosubmission;
SELECT *
FROM cfc_hackathonsubmission;
-- Check CLT submissions
SELECT *
FROM clt_cltsubmission;
SELECT *
FROM clt_cltfile;
-- Check IIPC submissions
SELECT *
FROM iipc_connectionscreenshot;
SELECT *
FROM iipc_linkedinconnectionverification;
-- Check mentor-student relationships
SELECT u.id as student_id,
    u.username as student_username,
    u.email as student_email,
    up.role,
    up.floor,
    up.assigned_mentor_id,
    mentor.username as mentor_username,
    mentor.email as mentor_email
FROM auth_user u
    LEFT JOIN profiles_userprofile up ON u.id = up.user_id
    LEFT JOIN auth_user mentor ON up.assigned_mentor_id = mentor.id
WHERE up.role = 'STUDENT'
ORDER BY up.assigned_mentor_id;
-- Check all mentors and their student counts
SELECT m.id as mentor_id,
    m.username as mentor_username,
    m.email as mentor_email,
    COUNT(up.id) as student_count
FROM auth_user m
    JOIN profiles_userprofile mp ON m.id = mp.user_id
    AND mp.role = 'MENTOR'
    LEFT JOIN profiles_userprofile up ON up.assigned_mentor_id = m.id
GROUP BY m.id,
    m.username,
    m.email;
-- Check user profiles with roles
SELECT u.id,
    u.username,
    u.email,
    u.is_active,
    up.role,
    up.floor,
    up.campus,
    up.assigned_mentor_id
FROM auth_user u
    LEFT JOIN profiles_userprofile up ON u.id = up.user_id
ORDER BY up.role,
    u.id;