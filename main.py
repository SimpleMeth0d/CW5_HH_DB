from src.config import config
from src.DB_Manager import DBManager
from src.receiving_and_parsing import ApiGetService, GetEmployer, GetEmployerVacancies

params = config()
database_name = 'coursework5'

employers = ["Lesta Games", "Яндекс", "АВТОВАЗ", "ПАО Ростелеком",
             "Лаборатория Касперского", "ПАО Газпром автоматизация", "Авито",
             "VK", "Ozon", "Контур"]

data_employers = []
data_employers_vacancies = []
for employer in employers:
    data_employer = GetEmployer(employer)
    data_employers.append(data_employer.info_employer_data())

    data_employer_vacancies = GetEmployerVacancies(employer)
    data_employers_vacancies.append(data_employer_vacancies.info_vacancies_employer_data())
db = DBManager
db.create_database(database_name, params)
db.save_data_employers_to_database(data_employers, database_name, params)
for data in data_employers_vacancies:
    db.save_data_vacancies_to_database(data, database_name, params)
print(db.get_companies_and_vacancies_count(database_name, params))

print(f'Чтобы получить список вакансий, Введите название компании из списка - {employers[0:]}')
print(db.get_all_vacancies(database_name, params))

print(f'Средняя заработная плата всех вакансий: ')
print(db.get_avg_salary(database_name, params))

print(f'Все вакансии у которых заработная плата больше средней: ')
print(db.get_vacancies_with_higher_salary(database_name, params))

print(f'Введите ключевое слово для поиска необходимой вакансии: ')
print(db.get_vacancies_with_keyword(database_name, params))