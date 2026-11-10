import streamlit as st
import matplotlib.pyplot as plt
import first_scenario as scen

#====================ВІДОБРАЖЕННЯ ОСНОВНОЇ ІНФОРМАЦІЇ ПРО ШКОЛУ====================
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
show_statistics(scen.load_school())

#=======================ПОБУДОВА ГРАФІКІВ=============

#функція для створення графіків
def grafics(school):
    #створюємо словник для зберігання загальної кількості учнів по паралелях
    parallel_data = {}

    #створюємо словник для зберігання загальної кількості учнів по вертикалях
    vertical_data = {}
    
    for school_class in school.get_classes: #перебираємо всі класи в школі
        parallel = school_class.paralel #отримуємо номер паралелі поточного класу
        vertical = school_class.vertical

        if parallel not in parallel_data: #якщо паралелі ще немає в словнику, визначаємо її з нульовим значенням
            parallel_data[parallel] = 0 #створюємо ключ для поточної паралелі зі значенням 0
        parallel_data[parallel] += school_class.student_count() #додаємо кількість учнів поточного класу до загальної суми цієї паралелі

        if vertical not in vertical_data: #якщо вертикалі ще немає в словнику, визначаємо її з нульовим значенням
            vertical_data[vertical] = []  #створюємо ключ для поточної вертикалі з порожнім списком
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
    plt.close(fig) #закриваємо фігуру для звільнення оперативної пам'яті

    #створюємо порожній словник для зберігання середньої кількості учнів по кожній вертикалі
    average_vertical = {}

    for vertical, counts in vertical_data.items(): #перебираємо елементи словника, отримуючи назву вертикалі та список кількості учнів у її класах
        average_vertical[vertical] = sum(counts) / len(counts)

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

#=========================Лінійні графіки==============
    birth_data = {}

    for school_class in school.get_classes:
        for student in school_class.get_students:
            year = student.get_birth_year

            if year in birth_data:
                birth_data[year] += 1 
            else:
                birth_data[year] = 1

    if birth_data:
        years = sorted(birth_data.keys())
        counts = [birth_data[year] for year in years]

        fig, ax = plt.subplots()
        ax.set_facecolor('lightblue')
        ax.patch.set_alpha(0.2)
        ax.plot(years, counts, c = "#1d3557", marker="o")
        ax.set_xlabel("Рік народження", c = "#1d3557")
        ax.set_ylabel("Кількість учнів", c = "#1d3557")
        ax.set_title("Кількість учнів за роком народження", c = "#1d3557")

        plt.xticks(years)
        st.pyplot(fig)
        plt.close(fig)


    sorted_classes = sorted(school.get_classes, key=lambda cl: (cl.paralel, cl.vertical))

    classes = []
    avg_grades = []
    for school_class in sorted_classes:
        cl_grades = []
        cl_name = school_class.class_name()
        for student in school_class.get_students:
            cl_grades.append(student.get_average_grade)
        avrg_grade_per_class = sum(cl_grades)/len(cl_grades)
        avg_grades.append(avrg_grade_per_class)
        classes.append(cl_name)

    if classes:
        fig, ax = plt.subplots() 
        ax.set_facecolor('lightblue')
        ax.patch.set_alpha(0.2)
        ax.scatter(classes, avg_grades, c="#1d3557", alpha = 0.8)
        ax.set_xlabel("Класи")
        ax.set_ylabel("Середня оцінка учня")
        ax.set_title("Залежність середньої оцінки від класів")

         # Повертаємо підписи на 60 градусів, щоб вони не накладалися
        plt.xticks(rotation=60, ha="right")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
                       
grafics(scen.load_school())


#=============ПЕРЕВЕДЕННЯ КЛАСІВ=================
if st.button("Перевести всі класи на наступний рік"):
    #Створення оновленої школи
    st.session_state.updated_school = scen.load_school()
    #Переведення класів
    st.session_state.updated_school.next_year()

#Виведення статистики оновлених класів
if "updated_school" in st.session_state:
    st.header("Класи після переведення", text_alignment="center", divider="gray")

    updated_school = st.session_state.updated_school

    #Виведення оновленого списку класів
    for school_class in sorted(updated_school.get_classes, key=lambda cl: (cl.paralel, cl.vertical)):
        st.write(f"<b>Клас {school_class.class_name()}</b> — {school_class.student_count()} учнів",unsafe_allow_html=True)
    #Оновлена статистика
    st.header("Оновлена статистична інформація школи", text_alignment="center", divider="gray")
    show_statistics(updated_school)


#====================СЦЕНАРІЙ ДВА==========
with open("salary.csv", "w", encoding="utf-8", newline="") as f:
    info = csv.DictWriter(f, fieldnames=["Посада", "ПІБ", "Базова ставка", "Розрахована зарплата"])
    info.writeheader()

    for worker in scen.load_school().get_workers:
        if isinstance(worker, scen.Headmaster):
            position = "Директор"
        elif isinstance(worker, scen.Teacher):
            position = "Вчитель"
        else:
            position = "Охоронець"

        info.writerow({
            "Посада": position,
            "ПІБ": worker.full_name,
            "Базова ставка": worker.base_salary,
            "Розрахована зарплата": round(worker.calculate_salary(), 2)
        })

        print(f'{worker.full_name} - {position} - {worker.calculate_salary():.2f} грн')







