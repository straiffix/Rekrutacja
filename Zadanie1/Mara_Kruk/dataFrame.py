import csv
from operator import itemgetter
from statistics import mean, median, stdev
from matplotlib import pyplot as plt

class DataFrame:

    # Klasa DataFrama jest zrobiona z listy list: lista frame składa się z list row.
    # Jeśli jest podany plik csv, klasa tworzy tablicę z tego pliku, ale nie sprawdza poprawność danych w pliku. Zakładamy, że poprawny plik zawiera w pierwszym wierszu nazwy kolumn, oddzielonych przycinkiem
    # Jeśli nie podajemy pliku, klasa tworzy pustą tablicę

    def __init__(self, file=None):
        self.frame = list()
        self.rows_num = 0
        self.column_num = 0
        if file is not None:
            reader = csv.reader(open(file, encoding="UTF-8"))
            header_row = next(reader)
            self.column_num = len(header_row)
            self.frame.append(header_row)
            self.rows_num += 1
            for row in reader:
                self.frame.append(row)
                self.rows_num += 1

    # Podajemy nazwę kolumny, nie jej numer. Dla nowej kolumny wszystkie komórki uzupelniamy wartością None
    def add_new_column(self, column_id):
        if self.frame == []:
            self.rows_num += 1
            self.frame.append(list())
            self.frame[0].append(column_id)
            self.column_num += 1
        else:
            self.frame[0].append(column_id)
            self.column_num += 1
            for row in self.frame[1:]:
                row.append(None)

    # Jeśli nie podajemy listy, to tworzy się nowy wiersz z wartościami None
    def add_new_row(self, row = None):
        if row is None:
            new_row = list()
            for column in range(self.column_num):
                new_row.append(None)
            self.frame.append(new_row)
            self.rows_num += 1
        else:
            if len(row) == len(self.frame[0]):
                self.frame.append(row)
                self.rows_num += 1
            elif len(row) < len(self.frame[0]):
                row_len = len(row)
                for i in range(row_len, len(self.frame[0])):
                    row.append(None)
                self.frame.append(row)
                self.rows_num +=1

    # Zamiana wartości w tablice. Podajemy numer wiersza(licząc od 1, bo 0 jest wiersz z nazwami kolumn) oraz nazwę kolumny
    def insert(self, data, column_id, row):
        for column in range(self.column_num):
            if self.frame[0][column] == column_id:
                del self.frame[row][column]
                self.frame[row].insert(column, data)

    def delete_column(self, column_id):
        for column in range(self.column_num):
            if self.frame[0][column] == column_id:
                self.frame[0].remove(column_id)
                for row in range(1, self.rows_num):
                    del self.frame[row][column]
                self.column_num -= 1

    def delete_row(self, row):
        if row != 0: # Bo nie możemy usunąć wiersz z nazwami kolumn
            del self.frame[row]
            self.rows_num -= 1

    #Funkcja zwraca tuple z wartościami. Liczy dobrze dla poprawnych wartości.
    def count_statistics(self, column_id):
        stat = list()
        for column in range(self.column_num):
            if self.frame[0][column] == column_id:
                for row in range(1, self.rows_num):
                    if self.frame[row][column] is not None:
                        if self.frame[row][column].isdigit():
                            stat.append(int(self.frame[row][column]))
                maximum = max(stat)
                minimum = min(stat)
                average = mean(stat)
                med = median(stat)
                std = stdev(stat)
                print("For column ", str(column_id), " max = ", maximum, ' min = ', minimum, ' average = ', average, ' median = ', med, ' standard deviation = ', std)
                return (maximum, minimum, average, med, std)

    #Sortowanie według wybranej kolumny
    def sort(self, column_id):
        for column in range(self.column_num):
            if self.frame[0][column] == column_id:
                header_row = self.frame[0]
                sorts = sorted(self.frame[1:], key=itemgetter(column))
                new_frame = list()
                new_frame.append(header_row)
                new_frame.extend(sorts)
                self.frame = new_frame


    def print(self):
        for row in self.frame:
            print(row)

    def make_list(self, column_id):
        new_list = list()
        for column in range(self.column_num):
            if self.frame[0][column] == column_id:
                for row in range(1, self.rows_num):
                    new_list.append(self.frame[row][column])
        return new_list


    #Dodatkowa funkcja: robi wykres na podstawie dwuch wybranych kolumn, wymaga matplotlib
    def mkplt(self, column_x, column_y, color='red'):
        fig = plt.figure(dpi=64, figsize=(10, 6))
        x = self.make_list(column_x)
        y = self.make_list(column_y)
        plt.plot(x, y, c=color)
        plt.xlabel(column_x, fontsize=16)
        plt.ylabel(column_y, fontsize=16)
        plt.tick_params(axis='both', which='major', labelsize=16)
        plt.show()


ex = DataFrame()
ex.add_new_column("Day")
ex.add_new_column("Temperature")
ex.add_new_row([1, 24])
ex.add_new_row([2, 25])
ex.add_new_row([3, 20])
ex.add_new_row([4, 23])
ex.add_new_row([5, 19])
ex.print()
ex.sort('Temperature')
ex.print()
ex.delete_column("Temperature")
ex.delete_row(3)
ex.print()

ex2 = DataFrame('random.csv')
ex2.print()
ex2.count_statistics('Max TemperatureF')
ex2.mkplt('AKDT', 'Max TemperatureF')