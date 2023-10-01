class Vacancy:
    def __init__(self, name, salary, description, emploer, sourse, id):
        self.name = name
        self.salary = salary
        self.description = description
        self.emploer = emploer
        self.sourse = sourse
        self.id = id

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.salary}, {self.description}, {self.emploer}, {self.salary},{self.id})'

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass