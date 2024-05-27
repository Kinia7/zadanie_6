SELECT DISTINCT subjects.name
FROM subjects
JOIN lecturers ON subjects.lecturer_id = lecturers.id
JOIN grades ON students.id = grades.student_id
JOIN students ON groups.id = students.group_id
WHERE lecturers.name = ? AND students.name = ?;