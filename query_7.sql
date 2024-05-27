SELECT students.name, grades.grade, grades.date
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades
