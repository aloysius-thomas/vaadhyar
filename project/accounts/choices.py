USER_TYPE = (
    ('hod', "HOD"),
    ('teacher', "Teacher"),
    ('student', "Student"),
    ('trainer', "Trainer"),
    ('trainee', "Trainee"),
    ('admin', "Admin")
)
DEPARTMENT_CHOICES = (
    ('tuition', 'Tuition'),
    ('1-4', ' Lower Primary'),
    ('5-7', 'Upper Primary'),
    ('8-10', 'High School'),
    ('+1-science', '+1 Science'),
    ('+2-science', '+2 science'),
    ('+1-commerce', '+1 Commerce'),
    ('+2-commerce', '+2 Commerce'),
    ('b.com/m.com', 'B.com/ M.com'),
    ('civil-engineering', 'Civil Engineering'),
    ('mechanical-engineering', 'Mechanical Engineering'),
    ('electrical&electronics-engineering', 'Electrical&Electronics Engineering'),
    ('computer-science-engineering', 'Computer Science Engineering'),
)

ADMIN_DEPARTMENT_CHOICES = (
    ('tuition', 'Tuition'),
    ('civil-engineering', 'Civil Engineering'),
    ('mechanical-engineering', 'Mechanical Engineering'),
    ('electrical&electronics-engineering', 'Electrical&Electronics Engineering'),
    ('computer-science-engineering', 'Computer Science Engineering'),
)

AVAILABLE_TIME_CHOICES = (
    ('4-5', '4 PM to 5 PM'),
    ('5-6', '5 PM to 6 PM'),
    ('6-7', '6 PM to 7 PM'),
    ('7-8', '7 PM to 8 PM'),
    ('8-9', '8 PM to 9 PM'),
    ('9-10', '9 PM to 10 PM'),
)

GENDER_CHOICE = (
    ('male', 'Male'),
    ('female', 'Female'),
)

TUITION_DEPARTMENTS = ['1-4', '5-7', '8-10', '+1-science', '+2-science', '+1-commerce', '+2-commerce', 'b.com/m.com']
