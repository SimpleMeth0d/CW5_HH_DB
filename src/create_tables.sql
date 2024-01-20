CREATE DATABASE coursework;

CREATE TABLE companies (
	company_id int PRIMARY KEY,
	name_company varchar(300)
);
CREATE TABLE job (
	job_id int PRIMARY KEY,
	company_id int REFERENCES companies(company_id),
	job_title varchar(300),
	salary_from int,
	salary_to int,
	link_vacancy varchar(500)
);

SELECT* FROM companies INNER JOIN job USING(company_id)

SELECT AVG(salary_from) as salary_avg_from FROM job

SELECT * FROM job WHERE salary_to > (SELECT AVG(salary_to) FROM job)

SELECT * FROM job WHERE job_title = '{self.keyword}'

SELECT companies.name_company, COUNT(job.job_id)
FROM companies
LEFT JOIN job ON companies.company_id = job.company_id
GROUP BY companies.name_company