import csv
from pathlib import Path
import glob

class Student: #створення класу Student
    #конструктор класу Student
    def __init__(self,
                 name: str,
                 surname: str,
                 father_name: str,
                 birth_year: int,
                 sex: str,
                 average_grade: float):
        self.__name = name 
        self.__surname = surname
        self.__father_name = father_name
        self.__birth_year = birth_year 
        self.__sex = sex 
        self.__average_grade = average_grade 

    #методи для отримання даних студента
    @property
    def get_name(self):
        return self.__name
    @property
    def get_surname(self):
        return self.__surname
    @property
    def get_father_name(self):
        return self.__father_name
    @property
    def get_birth_year(self):
        return self.__birth_year
    @property
    def get_sex(self):
        return self.__sex
    @property
    def get_average_grade(self):
        return self.__average_grade


#створення класу Class
class Class:
    def __init__(self, paralel: int, vertical:str): #конструктор класу Class
        self.paralel = paralel 
        self.vertical = vertical 
        self.__students = [] 

    #метод для отримання даних студента
    @property
    def get_students(self):
        return self.__students

    #метод додавання студентів до списку
    def add_student(self, student: Student):
        self.__students.append(student)

    #метод підрахунку кількості студентів
    def student_count(self) -> int:
        return len(self.__students)

    #метод повернення повного імені класму часли - літера (1-Б)
    def class_name(self) -> str:
        return f"{self.paralel}-{self.vertical}"
    
    #метод переведення класу на наступний навчальний рік, збільшує паралель на 1
    def next_year(self):
            self.paralel += 1

#створення батьківського класу Worker
class Worker:
    #конструктор класу Worker
    def __init__(
        self,
        surname: str,
        first_name: str,
        father_name: str,
        base_salary: float
    ):
        self.__surname = surname
        self.__first_name = first_name
        self.__father_name = father_name
        self.base_salary = base_salary

    #повернення повного імені працівника
    @property
    def full_name(self) -> str:
        return f"{self.__surname} {self.__first_name} {self.__father_name}"
    
#створення дочірнього класу Headmaster
class Headmaster(Worker):
        #конструктор дочірнього класу
        def __init__(
            self,
            surname: str,
            first_name: str,
            father_name: str,
            base_salary: float,
            teaching_experience: int,
            management_experience: int
        ):
            #виклик конструктора батьківського класу Worker
            super().__init__(
                surname,
                first_name,
                father_name,
                base_salary
            )
            #ініціалізація приватних атрибутів дочірнього класу
            self.__teaching_experience = teaching_experience
            self.__management_experience = management_experience

        #метод розрахунку заробітної плати директора
        def calculate_salary(self) -> float:
            return (
                self.base_salary * self.__teaching_experience / 50
                + self.__management_experience * 500
            )
    
#створення дочірнього класу Teacher
class Teacher(Worker):
        #конструктор дочірнього класу
        def __init__(
            self,
            surname: str,
            first_name: str,
            father_name: str,
            base_salary: float,
            teaching_experience: int
        ):
            #виклик конструктора батьківського класу Worker
            super().__init__(
                surname,
                first_name,
                father_name,
                base_salary
            )
            #ініціалізація приватних атрибутів дочірнього класу
            self.__teaching_experience = teaching_experience

        #метод розрахунку заробітної плати вчителя
        def calculate_salary(self) -> float:
            return self.base_salary * self.__teaching_experience / 30
    
#створення дочірнього класу Guard
class Guard(Worker):
    #конструктор дочірнього класу
    def __init__(
        self,
        surname: str,
         first_name: str,
        father_name: str,
        base_salary: float,
        work_experience: int
        ):
        #виклик конструктора батьківського класу Worker
        super().__init__(
            surname,
            first_name,
            father_name,
            base_salary
        )
        #ініціалізація приватних атрибутів дочірнього класу
        self.__work_experience = work_experience

    #метод розрахунку заробітної плати вчителя
    def calculate_salary(self) -> int:
        return self.base_salary + self.__work_experience * 250


#створення класу School
class School:
    #конструктор класу School
    def __init__(self, name: str):
        self.name = name #ім'я школи
        self.__classes = [] #список класів школи
        self.__workers = [] #список працівників школи

    #метод для отримання даних студента
    @property
    def get_classes(self):
        return self.__classes

    #метод для отримання даних про працівників
    @property
    def get_workers(self):
        return self.__workers

    #метод додавання класів до списку
    def add_class(self, cl: Class):
        self.__classes.append(cl)

    #метод додавання працівників до школи
    def add_worker(self, worker: Worker):
        self.__workers.append(worker)

    #метод отримання кількості студентів у класі
    def get_number_of_students(self) -> int:
        count = 0 #визначення змінної для підрахунку студентів у школі
        for cl in self.__classes: #перебираємо всі класи в списку класів школи
            count += cl.student_count() #додаємо кількість учнів поточного класу до загальної суми
        return count #повертаємо загальну кількість учнів

    def gender_statistics(self) -> tuple[float, float]:
        boys = 0 #визначення змінної для підрахунку хлопців
        girls = 0 #визначення змінної для підрахунку дівчат

        for school_class in self.__classes: #перебираємо класи в школі
            for student in school_class.get_students: #перебираємо студентів у класі
                #перевіряємо стать учня + переводимо рядок у нижній регістр
                if student.get_sex.lower() in ["ч", "хлопець", "чоловіча"]:
                    boys += 1 #збільшуємо лічильник хлопців на 1
                elif student.get_sex.lower() in ["ж", "дівчина", "жіноча"]:
                    girls += 1 #збільшуємо лічильник дівчат на 1
        
        total = self.get_number_of_students() #підраховуємо загальну кількість хлопців та дівчат
        if total > 0: #перевіряємл чи є учні в класах
            boys_percentage = boys / total * 100 #обчислюємо відсоток хлопців у школі
            girls_percentage = girls / total * 100 #обчислюємо відсоток дівчат у школі
            
            return (boys_percentage, girls_percentage) #повертаємо кортеж із відсотками
        else:
           return 0.0, 0.0 #повертаємо нульові значення, якщо учнів немає або дані відсутні

    #метод, що повертає cередню кількість учнів у класі 
    def student_average(self):
        #ділимо загальну кількість учнів на кількість класів
        return int(self.get_number_of_students() / (len(self.__classes))) #перетворюємо результат на ціле число та повертаємо його

    #метод, що знаходить класи з найбільшою та найменшою кількістю учнів
    def min_max_students(self) -> tuple [int, int]:
        #знаходимо об'єкт класу з максимальним та мінімальним значенням учнів за допомогою анонімної функції,
        #яка повертає кількість студентів у класі
        max_class = max(self.__classes, key=lambda cl: cl.student_count())
        min_class = min(self.__classes, key=lambda cl: cl.student_count())
        
        return (max_class, min_class) #повертає кортеж з максимальним на мініма
    
    #метод для переведення класів
    def next_year(self):
            new_classes = [] #створюємо пустий список, який буде заповнюватися новими класами
            for school_class in self.__classes: #перебираємо класи у списку класів
                #11 клас випускається, тому пропускаємо його
                if school_class.paralel == 11:
                    continue
                school_class.next_year() #застосовуємо метод, який додає 1 до значення паралелі
                new_classes.append(school_class) #заповнюэмо список
            self.__classes = new_classes #змінюємо список класів на новий 



#метод для завантаження інформації про школу та повертає об'єкт класу School
def load_school() -> School:
    filenames = Path('classes').glob('*.csv') #знаходимо всі CSV-файли в папці classes та завантажуємо їх у список
    #створення школи об'єкту класа School
    school = School("My School")
    for file in filenames: #перебираємо вайли в списку
        name_part = file.stem  #повертає файл без розширення .csv
        paralel, vertical = name_part.split('-') #повертає список список типу ['1', 'A'], використовуючи "-" як індикатор для розділення
        current_class = Class(int(paralel), vertical) #створюємо екземпляр класу та передаємо як аргументи значення паралелі та вертикалі зі списку 

        with open(file, 'r', encoding='utf-8', newline ='') as f: #відкриваємо файл для читання даних учнів
            reader = csv.reader(f, delimiter=';') #створюємо зчитувач CSV із розділювачем у вигляді крапки з комою
            next(reader) #пропускаємо заголовок таблиці

            for row in reader: #перебиhаємо рядки в зчитувачі
                #розпаковуємо дані поточного рядка CSV на окремі змінні для учня
                name, surname, father_name, birth_year, sex, average_grade = row 
                #створюємо екземпляр класу студент та передаємо йому змінні з рядка 
                student = Student(name, surname, father_name, int(birth_year), sex, float(average_grade))
                current_class.add_student(student) #додаємо створеного учня до списку учнів поточного класу
            #додаємо повністю сформований клас до школи
            school.add_class(current_class)
    #створюємо список працівників школи
    workers = [
        Headmaster("Гриненко", "Марина", "Олександрівна", 15000, 25, 5),
        Teacher("Коваленко", "Марія", "Петрівна",12000, 15),
        Teacher("Шевченко", "Андрій", "Олегович", 12000, 10),
        Teacher("Мельник", "Наталія", "Сергіївна",12000, 20),
        Guard("Бондар", "Василь", "Миколайович",11000, 12)
    ]
    #додаємо працівників до школи
    for worker in workers:
        school.add_worker(worker)

    return school #повертає готовий об'єкт класу School






    


       