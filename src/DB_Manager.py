from typing import Any
import psycopg2 as psycopg2


class DBManager:
    """Класс для работы с БД"""

    def create_database(database_name: str, params: dict):
        """ Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях"""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                employer_title VARCHAR (255) NOT NULL,
                description TEXT,
                employer_site_url TEXT,
                employer_url_hh TEXT,
                open_vacancies INTEGER
                )
            """)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_title VARCHAR (255) NOT NULL,
                vacancy_url TEXT,
                salary_currency VARCHAR(25),
                salary_from INTEGER,
                salary_to INTEGER,
                salary INTEGER,
                employment VARCHAR(50),
                experience TEXT,
                requirement_vacancy TEXT,
                responsibility_vacancy TEXT,            
                city_id INTEGER,
                city_name VARCHAR(50)
                )
            """)

        conn.commit()
        conn.close()

    def save_data_employers_to_database(data_employers: list[dict[str, Any]],
                                        database_name: str,
                                        params: dict):
        """Сохранение данных о компаниях в базу данных."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            for employer in data_employers:
                cur.execute("""
                    INSERT INTO employers (employer_id, employer_title, description, employer_site_url, employer_url_hh, open_vacancies)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                            (employer['employer_id'], employer['employer_title'], employer['description'],
                             employer['employer_site_url'], employer['employer_url_hh'], employer['open_vacancies'])
                            )

        conn.commit()
        conn.close()

    def save_data_vacancies_to_database(data_vacancies: list[dict[str, Any]],
                                        database_name: str,
                                        params: dict):
        """Сохранение данных о вакансиях в базу данных."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            for vacancy in data_vacancies:
                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, employer_id, vacancy_title, vacancy_url, salary_currency, salary_from, 
                    salary_to, salary, employment, experience, requirement_vacancy, responsibility_vacancy, city_id, city_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                            (
                                vacancy['vacancy_id'], vacancy['employer_id'], vacancy['vacancy_title'],
                                vacancy['vacancy_url'],
                                vacancy['salary_currency'], vacancy['salary_from'], vacancy['salary_to'],
                                vacancy['salary'], vacancy['employment'],
                                vacancy['experience'], vacancy['requirement_vacancy'],
                                vacancy['responsibility_vacancy'],
                                vacancy['city_id'], vacancy['city_name'])
                            )

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(database_name: str, params: dict):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        conn = psycopg2.connect(dbname=database_name, **params)
        # conn.row_factory = sqlite3.Row
        with conn.cursor() as cur:
            cur.execute("""
            SELECT employers.employer_title, COUNT(vacancies.employer_id) AS count_vacancies
            FROM employers
            INNER JOIN vacancies USING(employer_id)
            WHERE employers.employer_id=vacancies.employer_id
            GROUP BY employers.employer_title
            """)
            rows = cur.fetchall()

        conn.close()
        return rows

    def get_all_vacancies(database_name: str, params: dict):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        employer_title = input()
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT employers.employer_title, vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url
                FROM employers
                INNER JOIN vacancies USING(employer_id)
                WHERE employers.employer_id=vacancies.employer_id AND employers.employer_title='{employer_title}'
                """)
            rows = cur.fetchall()

        conn.close()
        return rows

    def get_avg_salary(database_name: str, params: dict):
        """Получает среднюю зарплату по вакансиям"""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(salary) AS average_salary_all_vacancies
                FROM public.vacancies
                """)
            rows = cur.fetchall()

        conn.close()
        return rows

    def get_vacancies_with_higher_salary(database_name: str, params: dict):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM public.vacancies
                WHERE salary > (
                SELECT AVG(salary)
                FROM public.vacancies)
                """)
            rows = cur.fetchall()

        conn.close()
        return rows

    def get_vacancies_with_keyword(database_name: str, params: dict):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        conn = psycopg2.connect(dbname=database_name, **params)
        keyword = input()
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT *
                FROM vacancies
                WHERE vacancy_title LIKE '%{keyword}%'
                """)
            rows = cur.fetchall()

        conn.close()
        return rows
