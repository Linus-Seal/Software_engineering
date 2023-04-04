# -*- coding: cp1251 -*-
from tkinter import ttk
from tkinter import *
import sqlite3

query_schedule = "SELECT schedule.id, employees.surname, employees.name, employees.patronymic, typeVacation.typeVacation, schedule.numberCalendar,\
                schedule.datePlanning, schedule.dateFact, schedule.dateTransfer, schedule.note\
                FROM employees, schedule, employeesSchedule, typeVacation, vacationSchedule\
                WHERE (employees.id = employeesSchedule.id_employees AND schedule.id = employeesSchedule.id_schedule\
                AND typeVacation.id = vacationSchedule.id_vacation AND schedule.id = vacationSchedule.id_schedule)"

query_employees = 'SELECT employees.id, employees.surname, employees.name, employees.patronymic, employees.personnelNumber, position.positionName, department.departmentName\
                FROM employees, position, department\
                WHERE (position.id = employees.id_position AND department.id = employees.id_department)'

query_typeVacation = 'SELECT * FROM typeVacation'

query_position = 'SELECT * FROM position'

query_department = 'SELECT * FROM department'

values_schedule = [1, 2, 3, 4, 5, 6, 7, 8, 9]
values_employees = [1, 2, 3, 4, 5, 6]
values_typeVacation = [1]
values_position = [1]
values_department = [1]

last_id = 0

class ZeroStringError(Exception):
   pass

class Schedule:
    db_name = 'VacationSchedule.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title('������ ��������')
        # �������� ��������� ��� ����� ���� � ��������
        frame = LabelFrame(self.wind, text='������� ����� ������')
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        Label(frame, text='��������� (id): ').grid(row=1, column=0)
        self.employees = Entry(frame)
        self.employees.focus()
        self.employees.grid(row=1, column=1)
        Label(frame, text='��� ������� (id): ').grid(row=2, column=0)
        self.typeVacation = Entry(frame)
        self.typeVacation.grid(row=2, column=1)
        Label(frame, text='���������� ����������� ����: ').grid(row=3, column=0)
        self.numberCalendar = Entry(frame)
        self.numberCalendar.grid(row=3, column=1)
        Label(frame, text='���� ���������������: ').grid(row=4, column=0)
        self.datePlanning = Entry(frame)
        self.datePlanning.grid(row=4, column=1)
        Label(frame, text='���� �����������: ').grid(row=5, column=0)
        self.dateFact = Entry(frame)
        self.dateFact.grid(row=5, column=1)
        Label(frame, text='���� ��������: ').grid(row=6, column=0)
        self.dateTransfer = Entry(frame)
        self.dateTransfer.grid(row=6, column=1)
        Label(frame, text='����������: ').grid(row=7, column=0)
        self.note = Entry(frame)
        self.note.grid(row=7, column=1)
        ttk.Button(frame, text='���������', command=self.add_schedule).grid(row=8, columnspan=2, sticky=W + E)
        self.message = Label(text='', fg='green')
        self.message.grid(row=9, column=0, columnspan=2, sticky=W + E)

        # ������� ��������
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
        self.tree = ttk.Treeview(height=10, columns=columns)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='id', anchor=CENTER)
        self.tree.heading('#1', text='���������', anchor=CENTER)
        self.tree.heading('#2', text='��� �������', anchor=CENTER)
        self.tree.heading('#3', text='���������� ����������� ����', anchor=CENTER)
        self.tree.heading('#4', text='���� ���������������', anchor=CENTER)
        self.tree.heading('#5', text='���� �����������', anchor=CENTER)
        self.tree.heading('#6', text='���� ��������', anchor=CENTER)
        self.tree.heading('#7', text='����������', anchor=CENTER)

        # ������ �������������� �������
        ttk.Button(text='������� ������ �������', command=self.delete_schedule).grid(row=5, columnspan=2, sticky=W + E)
        ttk.Button(text='���� ��������', command=self.open_typeVacation).grid(row=3, column=0, sticky=W + E)
        ttk.Button(text='����������', command=self.open_employees).grid(row=3, column=1, sticky=W + E)

        # ���������� �������
        self.get_table(self.tree, query_schedule, 'schedule', values_schedule)

        # ��������������� ����������
        self.last_id_schedule = last_id

    # ����������� � ������ � ����
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters).fetchall()
            conn.commit()
        return result

    # ���������� ������� ��������
    def get_table(self, tree, query, name_id, values):
        records = tree.get_children()
        for element in records:
            tree.delete(element)
        db_rows = self.run_query(query)
        for row in db_rows:
            if name_id == 'schedule':
                name = row[1] + ' ' + row[2] + ' ' + row[3]
            values_end = []
            for val in values:
                if name_id == 'schedule':
                    if val == 1:
                        add_value = name
                    elif val == 2 or val == 3:
                        continue
                    else: add_value = row[val]
                else: add_value = row[val]
                values_end.append(add_value)
            if name_id != '':
                global last_id
                last_id = row[0]
            tree.insert('', 0, text=row[0], values=values_end)

    # ��������� �����
    def validation(self, nameTable):
        if nameTable == "schedule":
            return self.run_query(f"""SELECT EXISTS(SELECT id FROM employees WHERE id = {self.employees.get() if self.employees.get() != '' else 0})""")[0][0] != 0 and len(self.datePlanning.get()) != 0 and len(self.numberCalendar.get()) != 0
        elif nameTable == "employees":
            return (len(self.surname.get()) != 0 and len(self.name.get()) != 0 and len(self.personnelNumber.get()) != 0
                    and self.run_query(f"""SELECT EXISTS(SELECT id FROM position WHERE id = {self.id_position.get() if self.id_position.get() != '' else 0})""")[0][0] != 0
                    and self.run_query(f"""SELECT EXISTS(SELECT id FROM department WHERE id = {self.id_department.get() if self.id_department.get() != '' else 0})""")[0][0] != 0)

    # ���������� ����� ������ �������
    def add_schedule(self):
        if self.validation("schedule"):
            query = 'INSERT INTO schedule VALUES(?, ?, ?, ?, ?, ?)'
            last_id_schedule = self.last_id_schedule + 1
            parameters = (last_id_schedule, self.numberCalendar.get(), self.datePlanning.get(), self.dateFact.get(), self.dateTransfer.get(), self.note.get())
            self.run_query(query, parameters)
            query = 'INSERT INTO employeesSchedule VALUES(?, ?, ?)'
            parameters = (last_id_schedule, self.employees.get(), last_id_schedule)
            self.run_query(query, parameters)
            query = 'INSERT INTO vacationSchedule VALUES(?, ?, ?)'
            parameters = (last_id_schedule, self.typeVacation.get(), last_id_schedule)
            self.run_query(query, parameters)
            self.message['text'] = '������ ��� ���������� � {} ��������� � �������'.format(self.employees.get())
            #������� ���� �����
            self.employees.delete(0, END)
            self.typeVacation.delete(0, END)
            self.numberCalendar.delete(0, END)
            self.datePlanning.delete(0, END)
            self.dateFact.delete(0, END)
            self.dateTransfer.delete(0, END)
            self.note.delete(0, END)
        else:
            self.message['text'] = '������� ���������� ������'
        self.get_table(self.tree, query_schedule, self.last_id_schedule, values_schedule)

    # ���������� ������ ����������
    def add_employees(self):
        if self.validation("employees"):
            query = 'INSERT INTO employees VALUES(NULL, ?, ?, ?, ?, ?, ?)'
            parameters = (
            self.surname.get(), self.name.get(), self.patronymic.get(), self.personnelNumber.get(),
            self.id_position.get(), self.id_department.get())
            self.run_query(query, parameters)
            self.message['text'] = '��������� {} ��������'.format(self.surname.get())
            self.surname.delete(0, END)
            self.name.delete(0, END)
            self.patronymic.delete(0, END)
            self.personnelNumber.delete(0, END)
            self.id_position.delete(0, END)
            self.id_department.delete(0, END)
        else:
            self.message['text'] = '������� ����������'
        self.get_table(self.treeEmp, query_employees, self.last_id_employees, values_employees)

    # �������� �������
    def delete_schedule(self):
        self.message['text'] = ''
        try:
            if self.tree.item(self.tree.selection())['text'] == "":
                raise ZeroStringError('�������� ������, ������� ����� �������')
        except ZeroStringError as e:
            self.message['text'] = e
            return
        self.message['text'] = ''
        schedule_id = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM schedule WHERE id = ?'
        self.run_query(query, (schedule_id,))
        self.message['text'] = '������ {} ������� �������'.format(schedule_id)
        self.get_table(self.tree, query_schedule, self.last_id_schedule, values_schedule)

    # �������� ����������
    def delete_employees(self):
        self.message['text'] = ''
        try:
            if self.treeEmp.item(self.treeEmp.selection())['text'] == "":
                raise ZeroStringError('�������� ������, ������� ����� �������')
        except ZeroStringError as e:
            self.message['text'] = e
            return
        self.message['text'] = ''
        employees_id = self.treeEmp.item(self.treeEmp.selection())['text']
        query = 'DELETE FROM employees WHERE id = ?'
        self.run_query(query, (employees_id,))
        self.message['text'] = '������ {} ������� �������'.format(employees_id)
        self.get_table(self.treeEmp, query_employees, self.last_id_employees, values_employees)

    # ������� �����������
    def open_employees(self):
        self.edit_employees = Toplevel()
        self.edit_employees.title('����������')

        # ������� ����������
        columns = ("#1", "#2", "#3", "#4", "#5", "#6")
        self.treeEmp = ttk.Treeview(self.edit_employees, height=10, columns=columns)
        self.treeEmp.grid(row=4, column=0, columnspan=2)
        self.treeEmp.heading('#0', text='id', anchor=CENTER)
        self.treeEmp.heading('#1', text='�������', anchor=CENTER)
        self.treeEmp.heading('#2', text='���', anchor=CENTER)
        self.treeEmp.heading('#3', text='��������', anchor=CENTER)
        self.treeEmp.heading('#4', text='��������� �����', anchor=CENTER)
        self.treeEmp.heading('#5', text='���������', anchor=CENTER)
        self.treeEmp.heading('#6', text='�����', anchor=CENTER)

        # �������� ��������� �����������
        frameEmp = LabelFrame(self.edit_employees, text='������� ������ ����������')
        frameEmp.grid(row=0, column=0, columnspan=3, pady=20)
        Label(frameEmp, text='�������: ').grid(row=1, column=0)
        self.surname = Entry(frameEmp)
        self.surname.focus()
        self.surname.grid(row=1, column=1)
        Label(frameEmp, text='���: ').grid(row=2, column=0)
        self.name = Entry(frameEmp)
        self.name.grid(row=2, column=1)
        Label(frameEmp, text='��������: ').grid(row=3, column=0)
        self.patronymic = Entry(frameEmp)
        self.patronymic.grid(row=3, column=1)
        Label(frameEmp, text='��������� �����: ').grid(row=4, column=0)
        self.personnelNumber = Entry(frameEmp)
        self.personnelNumber.grid(row=4, column=1)
        Label(frameEmp, text='��������� (id): ').grid(row=5, column=0)
        self.id_position = Entry(frameEmp)
        self.id_position.grid(row=5, column=1)
        Label(frameEmp, text='����� (id): ').grid(row=6, column=0)
        self.id_department = Entry(frameEmp)
        self.id_department.grid(row=6, column=1)
        ttk.Button(frameEmp, text='���������', command=self.add_employees).grid(row=8, columnspan=2, sticky=W + E)
        self.messageEmp = Label(text='', fg='green')
        self.messageEmp.grid(row=9, column=0, columnspan=2, sticky=W + E)

        # ������ �������������� �������
        ttk.Button(self.edit_employees, text='������� ����������', command=self.delete_employees).grid(row=5, columnspan=2, sticky=W + E)
        ttk.Button(self.edit_employees, text='������ ����������', command=self.open_position).grid(row=3, column=0, sticky=W + E)
        ttk.Button(self.edit_employees, text='������ �������', command=self.open_department).grid(row=3, column=1, sticky=W + E)

        # ��������������� ����������
        self.last_id_employees = 0

        # ���������� �������
        self.get_table(self.treeEmp, query_employees, self.last_id_employees, values_employees)

        self.edit_employees.mainloop()

    # ������� ������������� ��������
    def open_typeVacation(self):
        self.edit_typeVacation = Toplevel()
        self.edit_typeVacation.title('���� ��������')

        # ������� ����� ��������
        columns = ("#1")
        self.treeTV = ttk.Treeview(self.edit_typeVacation, height=10, columns=columns)
        self.treeTV.grid(row=4, column=0, columnspan=2)
        self.treeTV.heading('#0', text='id', anchor=CENTER)
        self.treeTV.heading('#1', text='��� �������', anchor=CENTER)

        # ���������� �������
        self.get_table(self.treeTV, query_typeVacation, '', values_typeVacation)

        self.edit_typeVacation.mainloop()

    # ������� ���������
    def open_position(self):
        self.edit_position = Toplevel()
        self.edit_position.title('���������')

        # ������� ����������
        columns = ("#1")
        self.treePos = ttk.Treeview(self.edit_position, height=10, columns=columns)
        self.treePos.grid(row=4, column=0, columnspan=2)
        self.treePos.heading('#0', text='id', anchor=CENTER)
        self.treePos.heading('#1', text='���������', anchor=CENTER)

        # ���������� �������
        self.get_table(self.treePos, query_position, '', values_position)

        self.edit_position.mainloop()

    # ������� ������
    def open_department(self):
        self.edit_department = Toplevel()
        self.edit_department.title('������')

        # ������� �������
        columns = ("#1")
        self.treeDep = ttk.Treeview(self.edit_department, height=10, columns=columns)
        self.treeDep.grid(row=4, column=0, columnspan=2)
        self.treeDep.heading('#0', text='id', anchor=CENTER)
        self.treeDep.heading('#1', text='�����', anchor=CENTER)

        # ���������� �������
        self.get_table(self.treeDep, query_department, '', values_department)

        self.edit_department.mainloop()

if __name__ == '__main__':
    window = Tk()
    application = Schedule(window)
    window.mainloop()