import streamlit as st
import matplotlib.pyplot as plt
import school_info as inf
import csv

#====================СЦЕНАРІЙ 1.ВІДОБРАЖЕННЯ ОСНОВНОЇ ІНФОРМАЦІЇ ПРО ШКОЛУ====================
#створюємо головний заголовок сторінки з сірою лінією-розділювачем
st.header("Статистична інформація школи", text_alignment = "center", divider = "gray") 

#функція для відображення статистичних даних школи у Streamlit
def show_statistics(school):
    #виводимо загальну кількість учнів, викликаючи метод об'єкта школи
    st.write(f'<b>Загальна кількість учнів у школі:</b> {school.get_number_of_students()}', unsafe_allow_html=True)
    #виводимо заголовок для гендерного співвідношення
    st.write(f'<b> Відсоткове свіввідношення хлопців та дівчат:</b>', unsafe_allow_html=True)
    #отримуємо відсотки хлопців та дівчат
    boys, girls = school.gender_statistics()
    #виводимо відсоток хлопців та дівчат у вигляді елемента списку
    st.write(f'<li><b>Хлопців:</b>  {boys:.2f} %</li>', unsafe_allow_html=True )
    st.write(f'<li><b>Дівчат:</b>  {girls:.2f}%</li>', unsafe_allow_html=True)

    #виводимо середню кількість учнів на клас у школі
    st.write(f'<b>Середня кількість учнів у класах:</b> {school.student_average()}', unsafe_allow_html=True)

    #отримуємо об'єкти класів із найбільшою та найменшою кількістю учнів
    maximum, minimum = school.min_max_students()
    #виводимо інформацію про клас із найбільшою та найменшою кількістю учнів
    st.write(f'<b>Максимальна кількість студентів:</b> {maximum.student_count()} у класі {maximum.class_name()}', unsafe_allow_html=True)
    st.write(f'<b>Мімнімальна кількість студентів:</b> {minimum.student_count()} у класі {minimum.class_name()}', unsafe_allow_html=True)

#завантажуємо дані школи з файлів та передаємо їх у функцію для відображення на сторінці
show_statistics(inf.load_school())

#=======================ПОБУДОВА СТОВПЧИКОВИХ ГРАФІКІВ=============
#функція для створення графіків
def grafics(school):
    #створюємо словник для зберігання загальної кількості учнів по паралелях
    parallel_data = {}

    #створюємо словник для зберігання загальної кількості учнів по вертикалях
    vertical_data = {}
    
    for school_class in school.get_classes: #перебираємо всі класи в школі
        parallel = school_class.paralel 
        vertical = school_class.vertical 

        if parallel not in parallel_data: #якщо паралелі ще немає в словнику, створюємо ключ для паралелі зі значенням 0
            parallel_data[parallel] = 0 
        parallel_data[parallel] += school_class.student_count() #додаємо кількість учнів поточного класу до загальної суми цієї паралелі

        if vertical not in vertical_data: #якщо вертикалі ще немає в словнику, створюємо ключ для поточної вертикалі з порожнім списком
            vertical_data[vertical] = []  
        vertical_data[vertical].append(school_class.student_count())  #додаємо кількість учнів поточного класу до списку відповідної вертикалі
        
    fig, ax = plt.subplots() #створюємо фігуру та осі для графіка
    ax.set_facecolor('lightblue') #встановлюємо світло-блакитний фоновий колір
    ax.patch.set_alpha(0.2) #роби фон напівпрозорим
    #створюємо стовпчикову діаграму, у якій вісь х - паралелі, вісь у - загальна кількість учнів
    ax.bar(list(parallel_data.keys()), list(parallel_data.values()), facecolor = "#457b9d", alpha = 0.8)
    plt.xticks(list(parallel_data.keys())) #відображення всіх міток на осі х
    ax.set_title("Розподіл учнів по паралелях", c="#1d3557")  #заголовок графіка
    ax.set_xlabel("Паралель", c="#1d3557") #підпис горизонтальної осі
    ax.set_ylabel("Кількість учнів", c="#1d3557")  #підпис вертикальної осі
    
    st.pyplot(fig) #виводимо графік
    plt.close(fig) #закриваємо фігуру 

    st.divider()

    #створюємо порожній словник для зберігання середньої кількості учнів по кожній вертикалі
    average_vertical = {}

    #обчислення середньої кількості учнів у кожній вертикалі
    for vertical, counts in vertical_data.items(): 
        average_vertical[vertical] = sum(counts) / len(counts)

    #cтворюємо стовпчикову діаграму у якій вісь х - літера класу, вісь у - середня кількість учнів на вертикаль
    fig, ax = plt.subplots()
    ax.set_facecolor('lightblue')
    ax.patch.set_alpha(0.2)
    ax.bar(list(vertical_data.keys()), list(average_vertical.values()), facecolor = "#457b9d", alpha = 0.8)
    plt.xticks(list(vertical_data.keys())) 
    ax.set_xlabel("Вертикаль", c = "#1d3557")
    ax.set_ylabel("Середня кількість учнів", c = "#1d3557")
    ax.set_title("Розподіл середньої кількості учнів по вертикалях", c = "#1d3557")

    st.pyplot(fig)
    plt.close(fig)

    st.divider()

#=========================Лінійні графіки==============

    birth_data = {}  #створюємо словник для зберігання кількості учнів за роками народження

    for school_class in school.get_classes: #перебираємо всі класи школи
        for student in school_class.get_students: #перебираємо всіх учнів поточного класу
            year = student.get_birth_year #отримуємо рік народження поточного учня

            if year in birth_data:
                birth_data[year] += 1 #якщо рік народження вже є у словнику, збільшуємо кількість учнів цього року на 1
            else:
                birth_data[year] = 1 #якщо року ще немає у словнику, створюємо новий ключ зі значенням 1

    
    years = sorted(birth_data.keys())  #отримуємо відсортований список років народження учнів
    counts = [birth_data[year] for year in years] #створюємо список кількості учнів для кожного року народження

    #побудова лінійного графіку, у якому х - рік народження, у - кількість учнів, які народилися цього року 
    fig, ax = plt.subplots()
    ax.set_facecolor('lightblue')
    ax.patch.set_alpha(0.2) #встановлюємо прозорість фону
    ax.plot(years, counts, c = "#1d3557", marker="o")
    ax.set_xlabel("Рік народження", c = "#1d3557")
    ax.set_ylabel("Кількість учнів", c = "#1d3557")
    ax.set_title("Кількість учнів за роком народження", c = "#1d3557")

    plt.xticks(years)  #встановлюємо позначки на осі х, гарантуючі, що будуть відображені всі роки народження зі списку years
    st.pyplot(fig)
    plt.close(fig)

    st.divider()

    #сортуємо класи спочатку за паралеллю, а потім за вертикаллю
    sorted_classes = sorted(school.get_classes, key=lambda cl: (cl.paralel, cl.vertical))

    classes = [] 
    avg_grades = []

    #обчислення середньої оцінки учнів кожного класу
    for school_class in sorted_classes:
        cl_grades = [] #створюємо порожній список для зберігання середніх оцінок учнів поточного класу
        cl_name = school_class.class_name()
        for student in school_class.get_students: #перебираємо всіх учнів поточного класу
            cl_grades.append(student.get_average_grade) #додаємо середню оцінку поточного учня до списку оцінок класу
        avrg_grade_per_class = sum(cl_grades)/len(cl_grades) #обчислюємо середнє арифметичне середныъ оцінок усіх учнів поточного класу
        avg_grades.append(avrg_grade_per_class) #додаємо обчислену середню оцінку класу до загального списку середніх оцінок класу
        classes.append(cl_name) #додаємо назву поточного класу до списку назв класів

    #будуємо точкову діаграму, в якій x - назви класів, у - середня оцінка учнів у класі
    fig, ax = plt.subplots() 
    ax.set_facecolor('lightblue')
    ax.patch.set_alpha(0.2)
    ax.scatter(classes, avg_grades, c="#1d3557", alpha = 0.8)
    ax.set_xlabel("Класи")
    ax.set_ylabel("Середня оцінка учня")
    ax.set_title("Залежність середньої оцінки від класів")

    #повертаємо підписи на 60 градусів, щоб класи на накладались один на один
    plt.xticks(rotation=60, ha="right")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
                       
grafics(inf.load_school()) #викликаємо функцію grafics, передаючи їй об'єкт школи з модуля info

#=============ПЕРЕВЕДЕННЯ КЛАСІВ=================
if st.button("Перевести всі класи на наступний рік"):
    #створення оновленої школи
    st.session_state.updated_school = inf.load_school()
    #переведення класів
    st.session_state.updated_school.next_year()

#виведення статистики оновлених класів
if "updated_school" in st.session_state:
    st.header("Класи після переведення", text_alignment="center", divider = "grey")
    st.write("\n")
    updated_school = st.session_state.updated_school

    #сортування класів за паралеллю та літерою класу
    classes = sorted(updated_school.get_classes, key=lambda cl: (cl.paralel, cl.vertical))

    #створення двох колонок для відображення класів
    col1, col2 = st.columns(2)

    #розподіл класів між колонками
    half = (len(classes) + 1) // 2

    #виведення першої половини класів у першій колонці
    with col1:
        for school_class in classes[:half]:
            st.write(f"<p style='text-align: center;'><b>Клас {school_class.class_name()}</b> - {school_class.student_count()} учнів</p>", unsafe_allow_html=True)
    
    #виведення другої половини класів у другій колонці
    with col2:
        for school_class in classes[half:]:
            st.write(f"<p style='text-align: center;'><b>Клас {school_class.class_name()}</b> - {school_class.student_count()} учнів</p>", unsafe_allow_html=True)

    #оновлена статистика
    st.header("Оновлена статистична інформація школи", text_alignment="center", divider="gray")
    #виклик функції відображення статистичної інформації оновленої школи
    show_statistics(updated_school)


#====================СЦЕНАРІЙ 2==========
with open("salary.csv", "w", encoding="utf-8", newline="") as f:  #відкриваємо файл salary.csv для запису даних
    info = csv.DictWriter(f, fieldnames=["Посада", "ПІБ", "Базова ставка", "Розрахована зарплата"]) #створюємо об'єкт DictWriter для запису даних у csv файл у вигляді словників із заданими назвами стовпців
    info.writeheader() #записуємо заголовки стовпців у перший рядок файлу

    for worker in inf.load_school().get_workers: #перебираємо всіх працівників школи
        if isinstance(worker, inf.Headmaster): #перевіряємо, чи є поточний працівник об'єктом класу Headmaster
            position = "Директор" #присвоюємо працівнику посаду директора
        elif isinstance(worker, inf.Teacher): #якщо попередня умова не виконалася, перевіряємо, чи є працівник об'єктом класу Teacher
            position = "Вчитель" #присвоюємо працівнику посаду вчителя
        else:
            position = "Охоронець" #присвоюємо працівнику посаду охоронець

        #записуємо інформацію про поточного працівника в окремий рядок csv файлу
        info.writerow({
            "Посада": position,
            "ПІБ": worker.full_name,
            "Базова ставка": worker.base_salary,
            "Розрахована зарплата": round(worker.calculate_salary(), 2)
        })
        #виводимо в консоль повне ім'я працівника, його посаду та розраховану зарплату
        print(f'{worker.full_name} - {position} - {worker.calculate_salary():.2f} грн')







