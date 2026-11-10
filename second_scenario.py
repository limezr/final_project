import csv
#Cценарій 2
class Worker:
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

    @property
    def full_name(self) -> str:
        return f"{self.__surname} {self.__first_name} {self.__father_name}"


class Headmaster(Worker):
    def __init__(
        self,
        surname: str,
        first_name: str,
        father_name: str,
        base_salary: float,
        teaching_experience: int,
        management_experience: int
    ):
        super().__init__(
            surname,
            first_name,
            father_name,
            base_salary
        )
        self.__teaching_experience = teaching_experience
        self.__management_experience = management_experience

    def calculate_salary(self) -> float:
        return (
            self.base_salary * self.__teaching_experience / 50
            + self.__management_experience * 500
        )


class Teacher(Worker):
    def __init__(
        self,
        surname: str,
        first_name: str,
        father_name: str,
        base_salary: float,
        teaching_experience: int
    ):
        super().__init__(
            surname,
            first_name,
            father_name,
            base_salary
        )
        self.__teaching_experience = teaching_experience

    def calculate_salary(self) -> float:
        return self.base_salary * self.__teaching_experience / 30


class Guard(Worker):
    def __init__(
        self,
        surname: str,
        first_name: str,
        father_name: str,
        base_salary: float,
        work_experience: int
    ):
        super().__init__(
            surname,
            first_name,
            father_name,
            base_salary
        )
        self.__work_experience = work_experience

    def calculate_salary(self) -> int:
        return self.base_salary + self.__work_experience * 250
    


        