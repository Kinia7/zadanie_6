SELECT DISTINCT subjects.name
FROM subjects
JOIN grades ON students.id = grades.student_id
JOIN students ON groups.id = students.group_id
WHERE students.name = ?;