import re
from abc import ABC
import requests as requests


class ApiGetService(ABC):
    employers = {"Lesta Games": '856498', "Яндекс": '1740', "АВТОВАЗ": '193400', "ПАО Ростелеком": '2748',
                 "Лаборатория Касперского": '1057', "ПАО Газпром автоматизация": '903111', "Авито": '84585',
                 "VK": '15478', "Ozon": '2180', "Контур": '41862'}

    def __init__(self):
        pass

    def get_service(self):
        pass


class GetEmployer(ApiGetService):
    """
    Класс для подключения по АПИ к hh.ru. Реализованы два метода.
    Первый подключается к сайту и получает данные о работодателе по id.
    Второй парсит полученные данные и записывает в массив.
    """
    url = "https://api.hh.ru/employers/"

    def __init__(self, name):
        self.name_employer = name
        self.id_employer = ApiGetService.employers.get(self.name_employer)
        self.url = GetEmployer.url + self.id_employer

    def get_service_employer(self):
        """
        Отправляет Get запрос к сайту hh.ru с поиском о работодателе по его id.
        :return: Данные о вакансиях в формате Json.
        """
        data_employer = requests.get(self.url)
        return data_employer.json()
        # ['items']

    def cleanhtml(self, strint):
        CLEANR = re.compile('<.*&>')
        cleantext = re.sub(CLEANR, '', strint)
        return cleantext

    def info_employer_data(self):
        """
        Проходит в цикле по полученным данным, парсит и записывает в словарь необходимые данные о работодателе.
        :return: Массив работодателей с нужными атрибутами
        """

        data = self.get_service_employer()
        description = self.cleanhtml(data['description']).replace(u'\xa0', '').replace(u'<p><strong>', '').replace(
            u'</strong>', '').replace(u'</p>', '').replace(u'<ul>', '').replace(u'<li>', '').replace(u'</li>',
                                                                                                     '').replace(u'<p>',
                                                                                                                 '').replace(
            u'<strong>', '').replace(u'</ul>', '').replace(u'<h3>', '').replace(u'</h3>', '').replace(u'<br /> ',
                                                                                                      '').replace(
            u'<br />', '').replace(
            u'<br /><br />', '').replace(u'<em>', '').replace(u'</em>', '').replace(u'<ol>', '').replace(u'</ol>',
                                                                                                         '').replace(
            u'<u>', '').replace(u'</u>', '')
        my_dict_info_employer = {'employer_id': data['id'], 'employer_title': data['name'],
                                 'description': description,
                                 'employer_site_url': data['site_url'], 'employer_url_hh': data['alternate_url'],
                                 'open_vacancies': data['open_vacancies']}

        return my_dict_info_employer


class GetEmployerVacancies(ApiGetService):
    """
    Класс для подключения по АПИ к hh.ru. Реализованы два метода один возвращает данные о вакансиях в формате Json.
    Второй метод возвращает массив вакансий с необходимыми полями.
    "https://api.hh.ru/vacancies?employer_id=3177"
    """
    url = "https://api.hh.ru/vacancies?"

    def __init__(self, name: str):
        self.name_employer = name
        self.id_employer = ApiGetService.employers.get(self.name_employer)

    def get_service_vacancies(self):
        """
        Отправляет Get запрос к сайту hh.ru с поиском вакансии по id Работодателя.
        :return: данные о вакансиях в формате Json.
        """
        vacancies_employer = requests.get(GetEmployerVacancies.url, params={'employer_id': f'{self.id_employer}',
                                                                            'per_page': 100})
        return vacancies_employer.json()['items']

    def info_vacancies_employer_data(self):
        """
        Проходит в цикле по каждой вакансии и записывает в словарь необходимые данные о вакансии.
        :return: Массив вакансий с нужными атрибутами
        """
        data_vacancies = []
        for data in self.get_service_vacancies():
            if data['salary'] == None:
                salary_currency = 'value not set'
                salary_from = 0
                salary_to = 0
            else:
                salary_currency = data['salary']['currency']
                if data['salary']['from'] == None:
                    salary_from = 0
                else:
                    salary_from = int(data['salary']['from'])

                if data['salary']['to'] == None:
                    salary_to = 0
                else:
                    salary_to = int(data['salary']['to'])

            salary = salary_from if salary_to < salary_from else salary_to

            my_dict_vacancies = {'vacancy_id': data['id'], 'employer_id': data['employer']['id'],
                                 'vacancy_title': data['name'],
                                 'vacancy_url': data['alternate_url'],
                                 'salary_currency': salary_currency, 'salary_from': salary_from,
                                 'salary_to': salary_to, 'salary': salary, 'employment': data['employment']['name'],
                                 'experience': data['experience']['name'],
                                 'requirement_vacancy': data['snippet']['requirement'],
                                 'responsibility_vacancy': data['snippet']['responsibility'],
                                 'city_id': data['area']['id'], 'city_name': data['area']['name']}
            data_vacancies.append(my_dict_vacancies)
        return data_vacancies
