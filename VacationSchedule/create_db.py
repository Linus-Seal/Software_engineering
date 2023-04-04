# -*- coding: cp1251 -*-
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_data(conn, create_table_sql, data):
    try:
        c = conn.cursor()
        c.execute(create_table_sql, data)
        conn.commit()
    except Error as e:
        print(e)

def main():
    database = "VacationSchedule.db"
    sql_create_department_table = """ CREATE TABLE IF NOT EXISTS department (
                                                id integer PRIMARY KEY,
                                                departmentName text
                                            ); """
    sql_create_position_table = """ CREATE TABLE IF NOT EXISTS position (
                                                    id integer PRIMARY KEY,
                                                    positionName text
                                                ); """
    sql_create_typeVacation_table = """ CREATE TABLE IF NOT EXISTS typeVacation (
                                                        id integer PRIMARY KEY,
                                                        typeVacation text
                                                    ); """
    sql_create_employees_table = """ CREATE TABLE IF NOT EXISTS employees (
                                            id integer PRIMARY KEY,
                                            surname text,
                                            name text,
                                            patronymic text,
                                            personnelNumber text,
                                            id_position integer,
                                            id_department integer,
                                            FOREIGN KEY(id_position) REFERENCES position(id),
                                            FOREIGN KEY(id_department) REFERENCES department(id)
                                        ); """

    sql_create_schedule_table = """ CREATE TABLE IF NOT EXISTS schedule (
                                                        id integer PRIMARY KEY,
                                                        numberCalendar integer,
                                                        datePlanning datetime,
                                                        dateFact datetime,
                                                        dateTransfer datetime,
                                                        note text
                                                    ); """
    sql_create_employeesSchedule_table = """ CREATE TABLE IF NOT EXISTS employeesSchedule (
                                                            id integer PRIMARY KEY,
                                                            id_employees integer,
                                                            id_schedule integer,
                                                            FOREIGN KEY(id_employees) REFERENCES employees(id),
                                                            FOREIGN KEY(id_schedule) REFERENCES schedule(id)
                                                        ); """
    sql_create_vacationSchedule_table = """ CREATE TABLE IF NOT EXISTS vacationSchedule (
                                                                id integer PRIMARY KEY,
                                                                id_vacation integer,
                                                                id_schedule integer,
                                                                FOREIGN KEY(id_vacation) REFERENCES typeVacation(id),
                                                                FOREIGN KEY(id_schedule) REFERENCES schedule(id)
                                                            ); """
    data_department = (1, "Отдел разработки")
    data_position = (1, "Программист")
    data_employees = (1, "Иванов", "Иван", "Иванович", "111333", 1, 1)
    data_schedule = (1, 12, "30.01.2022", "30.01.2022", "", "база")
    data_typeVacation = (1, "Ежегодный (основной) оплачиваемый отпуск")
    data_employeesSchedule = (1, 1, 1)
    data_vacationSchedule = (1, 1, 1)

    query_department = 'INSERT INTO department VALUES(?, ?)'
    query_position = 'INSERT INTO position VALUES(?, ?)'
    query_employees = 'INSERT INTO employees VALUES(?, ?, ?, ?, ?, ?, ?)'
    query_schedule = 'INSERT INTO schedule VALUES(?, ?, ?, ?, ?, ?)'
    query_typeVacation = 'INSERT INTO typeVacation VALUES(?, ?)'
    query_employeesSchedule = 'INSERT INTO employeesSchedule VALUES(?, ?, ?)'
    query_vacationSchedule = 'INSERT INTO vacationSchedule VALUES(?, ?, ?)'

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_department_table)
        create_table(conn, sql_create_position_table)
        create_table(conn, sql_create_typeVacation_table)
        create_table(conn, sql_create_employees_table)
        create_table(conn, sql_create_schedule_table)
        create_table(conn, sql_create_employeesSchedule_table)
        create_table(conn, sql_create_vacationSchedule_table)
        add_data(conn, query_department, data_department)
        add_data(conn, query_position, data_position)
        add_data(conn, query_employees, data_employees)
        add_data(conn, query_schedule, data_schedule)
        add_data(conn, query_typeVacation, data_typeVacation)
        add_data(conn, query_employeesSchedule, data_employeesSchedule)
        add_data(conn, query_vacationSchedule, data_vacationSchedule)
    else:
        print("Error: can't connect to database")

if __name__ == '__main__':
    main()