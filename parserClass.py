'''импорт библиотек'''
from bs4 import BeautifulSoup
import requests
import csv

'''класс парсера'''
class Parser():
    '''конструктор'''
    def __init__(self, group, fileName):
        self.group = group
        self.fileName = fileName

    '''выбор действия с группой товаров'''
    def ToDo(self):
        choiseDo = input('Выберите, что требуется сделать:\n'
                       '1-запись данных в файл\n'
                       '2-вывод информации в консоль\n')
        if choiseDo == '1':
            self.Parsing()
        elif choiseDo == '2':
            self.InfoGroup()
        else:
            print('команда выбрана неверно')
            self.ToDo()

    '''парсинг даннных'''
    def Parsing(self):
        '''ссылка на сайт'''
        url = f'https://webscraper.io/test-sites/e-commerce/allinone/{self.group}'
        '''открытие ссылки'''
        res = requests.get(url)
        '''парсинг'''
        soup = BeautifulSoup(res.text,'html.parser')
        '''выбор получаемой информации'''
        models = soup.find_all('a', class_='title')
        description = soup.find_all('p', class_='description')
        prices = soup.find_all('h4', class_='pull-right price')
        '''сохранение данных в .csv файл'''
        '''имя файла зависит от группы товаров'''
        with open(f'{self.fileName}.csv', 'w', encoding='utf-8') as file:
            file.write(f'Модель;Описание;Цена\n')
            for m, d, p in zip(models, description, prices):
                file.write(f"{m['title']};{d.get_text()};{p.get_text()}\n")

    '''вывод информации о группе товаров в консоль'''
    def InfoGroup(self):
        '''сперва парсим сайт'''
        self.Parsing()
        '''считываем данные из файла соответствующей группы товаров'''
        with open(f'{self.fileName}.csv', 'r', encoding='utf-8') as file:
            print(file.readline())
            '''Создаем объект reader, указываем символ-разделитель ";"'''
            file_reader = csv.reader(file, delimiter=";")
            '''Счетчик для подсчета количества строк и вывода заголовков столбцов'''
            count = 0
            '''Считывание данных из CSV файла'''
            for row in file_reader:
                if count == 0:
                    '''Вывод строки, содержащей заголовки для столбцов'''
                    print(f'Файл содержит столбцы: {", ".join(row)}')
                else:
                    '''Вывод строк'''
                    print(f'Модель:{row[0]}\nОписание\n{row[1]}\nЦена:{row[2]}\n\n')
                count += 1
            print(f'Всего в файле {count} строк.')

'''основное меню'''
def Menu():
    choise = input('Выберите группу интересующих товаров:\n'
                   '1-телефоны\n'
                   '2-планшеты\n'
                   '3-ноутбуки\n')
    '''устанавливаем адрес страницы с группой товаров'''
    if choise == '1':
        groupCh = 'phones/touch'
    elif choise == '2':
        groupCh = 'computers/tablets'
    elif choise == '3':
        groupCh = 'computers/laptops'
    else:
        '''если выбрана несуществующая группа, то перезапускаем выбор'''
        print('группа выбрана неверно')
        Menu()
    '''выбор названия группы товаров как названия файла'''
    filename = groupCh.split('/')
    '''создание класса с группой товаров и вызов метода с выбором действий для получаемой информации'''
    Parser(groupCh, filename[1]).ToDo()
Menu()