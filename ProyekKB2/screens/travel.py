from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import numpy as np
from numpy import inf
import copy


class Data:
    def __init__(self) -> None:
        self.asal = None
        self.destinasi = None
        self.bestperformance = None  # harga terbaik
        self.rute = None
        self.bestperformanceArray = None
        self.pheromone = None
        self.kota_asal = None
        self.kota_destinasi = None
        self.bestSolution = None
        self.rincianHarga = ""


data = Data()


class Travel(MDScreen):

    def __init__(self, **kw):
        Builder.load_file("kv/travel.kv")
        super().__init__(**kw)

    def convert_city(self, kota):
        if kota == 'Surabaya':
            return 0
        elif kota == 'Medan':
            return 1
        elif kota == 'Padang':
            return 2
        elif kota == 'Batam':
            return 3
        elif kota == 'Palembang':
            return 4
        elif kota == 'Jakarta':
            return 5
        elif kota == 'Yogyakarta':
            return 6
        elif kota == 'Bali':
            return 7
        elif kota == 'Bima':
            return 8
        elif kota == 'Kupang':
            return 9
        elif kota == 'Pontianak':
            return 10
        elif kota == 'Banjarmasin':
            return 11
        elif kota == 'Palangkaraya':
            return 12
        elif kota == 'Balikpapan':
            return 13
        elif kota == 'Tarakan':
            return 14
        elif kota == 'Palu':
            return 15
        elif kota == 'Manado':
            return 16
        elif kota == 'Makassar':
            return 17
        elif kota == 'Jayapura':
            return 18
        elif kota == 'Merauke':
            return 19
        else:
            return None

    def createObj(self):
        if self.ids.spinner_opt1.text != 'Select A City' and self.ids.spinner_opt2.text != 'Select A City':
            self.generate()
        # return self

    def generate(self):
        # Implementasi Solusi
        def findRouteAllAnt(rute, pheromone, visibility):
            rute = np.zeros((m, n))
            rute[:, 0] = asal  # set posisi awal dari bandara mana
            temp_visibility = np.array(visibility)
            for i in range(m):  # untuk seluruh semut yang ada
                rute = findRoute(rute, i, temp_visibility, pheromone)
            return rute

        def findRoute(rute, antNumber, temp_visibilty, pheromone):
            i = copy.copy(antNumber)  # semut keberapa
            p_feature = np.power(pheromone, alpha)  # pangkat
            v_feature = np.power(temp_visibilty, beta)  # pangkat
            combine_feature = np.multiply(p_feature, v_feature)  # perkalian array
            sampai = False
            for j in range(n - 1):  # untuk setiap bandara yang ada
                if sampai is False:
                    cur_loc = int(rute[i, j])  # lokasi semut sekarang
                    # mengecek lokasi awal inputan benar atau tidak
                    combine_feature[:, cur_loc] = 0  # membuat seluruh visibilty dari seluruh bandara yang dikunjungi
                    # 0 agar tidak dikunjungi
                    locom_feature = combine_feature[cur_loc, :]  # ambil satu baris dari kota ini
                    total = np.sum(locom_feature)  # menjumlah seluruh feature
                    probs = locom_feature / total  # propabilitas jika dijumlah seluruhnya adalah 1
                    cum_prob = np.cumsum(probs)  # propabilitas cumulative
                    r = np.random.random_sample()  # bilangan random [0,1]
                    city = np.nonzero(cum_prob > r)[0][
                        0]  # mencari rute selanjutnya dengan kemungkinan bilangan lebih besar dari r yang pertama
                    rute[i, j + 1] = city
                    if city == destinasi:
                        sampai = True
                else:
                    rute[i, j + 1] = -1
            rute.astype(int)
            # print("Rute : ", rute)
            return rute

        def totalHargaTour(tour):  # pada rute tempuh sebuah semut
            harga = 0  # inisialisasi awal 0
            # print("Tour : ", tour)
            tour = np.array(tour)  # create array berupa tour atau semut
            tour = tour.astype(int)  # Akibat perubahan type data
            for i in range(0, len(tour) - 1):  # panjang tour -1 0-6 jika bandara = 7
                if tour[i + 1] != -1:
                    harga = harga + d[tour[i]][tour[i + 1]]  # total harga dari kota awal menuju kota tujuan
            return harga

        def evaluate(ants):  # evaluasi seluruh semut
            evaluateArray = np.zeros(m)  # declare array sebanyak semut
            for i in range(m):  # loop sebanyak semut
                evaluateArray[i] = totalHargaTour(ants[i])  # total harga yang ditempuh dimasukkan kedalam evaluasi
            return evaluateArray

        # update pheromone
        def updatePheromone(pheromone, rute, evaluasi):
            for i in range(m):  # sebanyak semut
                for j in range(n - 1):  # semua rute
                    dt = 1 / evaluasi[i]  # 1 dibagi evaluasi dari hasil evaluasi semut i semakin sering makan pheromone akan makin meningkat
                    # print("Rute : ", rute)
                    if rute[i, j + 1] != -1:
                        pheromone[int(rute[i, j]), int(rute[i, j + 1])] = pheromone[int(rute[i, j]), int(rute[i, j + 1])] + dt
                    else:
                        pheromone[int(rute[i, j]), int(rute[i, j + 1])] = pheromone[int(rute[i, j]), int(rute[i, j + 1])]
                    return pheromone  # tapi karena ada random sample maka masih ada kemungkinan jalur lain yang dipilih

        # Program Utama
        def performanceRecord(evaluasi, rute, bestPerformance, solutionArray, performanceArray, bestperformanceArray,bestSolution):
            currentPerformance = min(evaluasi)  # minimal dari evaluasi yang dicari
            currentSolution = rute[np.argmin(evaluasi)]  # array rute dari solusi hasil evaluasi paling minimum
            if currentPerformance < bestPerformance:  # jika performa saat ini lebih baik dari performa terbaik
                bestPerformance = copy.copy(currentPerformance)  # deep copy data performa saat ini ke performa terbaik
                bestSolution = currentSolution
            solutionArray.append(currentSolution)
            performanceArray.append(currentPerformance)
            bestperformanceArray.append(bestPerformance)
            return solutionArray, performanceArray, bestperformanceArray, bestPerformance, bestSolution

        # Inisialisasi
            # 0 = Surabaya              5 = Jakarta                 10 = Pontianak              15 = Palu
            # 1 = Medan                 6 = Yogyakarta              11 = Banjarmasin            16 = Manado
            # 2 = Padang                7 = Bali                    12 = Palangkaraya           17 = Makasar
            # 3 = Batam                 8 = Bima                    13 = Balikpapan             18 = Jayapura
            # 4 = Palembang             9 = Kupang                  14 = Tarakan                19 = Merauke

                    # 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19
        d = np.array([[0, 23, 18, 26, 14, 10, 15, 7, 18, 17, 18, 11, 28, 15, 19, 17, 21, 10, 35, 38],  # 0
                      [27, 0, 29, 10, 25, 17, 27, 31, 41, 41, 27, 29, 33, 31, 43, 36, 39, 29, 58, 81],  # 1
                      [20, 18, 0, 10, 18, 11, 21, 26, 36, 33, 23, 25, 29, 27, 38, 31, 36, 23, 52, 75],  # 2
                      [23, 9, 26, 0, 22, 14, 22, 27, 38, 36, 20, 25, 31, 31, 40, 34, 39, 26, 54, 61],  # 3
                      [14, 22, 19, 21, 0, 7, 15, 20, 31, 30, 18, 20, 24, 23, 36, 26, 32, 19, 47, 70],  # 4
                      [8, 12, 10, 11, 7, 0, 8, 11, 19, 19, 10, 10, 18, 9, 24, 14, 19, 9, 34, 47],  # 5
                      [8, 14, 15, 16, 13, 8, 0, 9, 21, 25, 14, 14, 17, 11, 27, 22, 23, 12, 33, 40],  # 6
                      [6, 19, 17, 18, 15, 12, 8, 0, 15, 15, 17, 13, 18, 12, 24, 19, 21, 8, 29, 42],  # 7
                      [15, 31, 28, 30, 25, 18, 26, 30, 0, 36, 27, 29, 30, 29, 40, 36, 58, 25, 48, 52],  # 8
                      [15, 30, 29, 25, 27, 17, 26, 20, 35, 0, 20, 17, 30, 20, 33, 31, 32, 19, 48, 60],  # 9
                      [12, 20, 17, 21, 15, 8, 15, 17, 30, 27, 0, 17, 19, 20, 65, 30, 33, 20, 40, 48],  # 10
                      [7, 20, 20, 18, 16, 10, 15, 14, 30, 19, 17, 0, 34, 17, 26, 28, 29, 16, 41, 50],  # 11
                      [13, 20, 23, 25, 24, 10, 18, 18, 38, 28, 23, 35, 0, 18, 40, 31, 42, 20, 42, 50],  # 12
                      [15, 30, 28, 31, 23, 17, 23, 21, 33, 32, 27, 25, 34, 0, 24, 22, 23, 10, 35, 69],  # 13
                      [31, 42, 44, 37, 42, 32, 30, 46, 27, 49, 47, 34, 55, 18, 0, 58, 39, 26, 52, 55],  # 14
                      [22, 33, 30, 44, 26, 18, 40, 32, 42, 41, 29, 31, 36, 19, 26, 0, 21, 9, 34, 81],  # 15
                      [21, 41, 37, 48, 35, 27, 51, 28, 31, 38, 35, 32, 43, 25, 30, 27, 0, 15, 23, 36],  # 16
                      [1, 25, 20, 21, 22, 11, 14, 13, 18, 27, 22, 21, 23, 9, 15, 9, 11, 0, 23, 29],  # 17
                      [45, 57, 54, 59, 53, 41, 56, 41, 59, 71, 50, 60, 56, 37, 44, 40, 23, 29, 0, 11],  # 18
                      [33, 55, 49, 52, 57, 36, 40, 38, 81, 53, 50, 38, 55, 32, 43, 36, 32, 25, 1, 0], ])  # 19

        iteration = 100
        n_ants = 22
        n_bandara = len(d)

        sampai = False

        m = n_ants
        n = n_bandara
        e = .2  # rate evaporasi, digunakan utk menghilangkan pheromone
        alpha = 1  # pheromone factor
        beta = 1  # visibillity factor

        visibility = 1 / d
        visibility[visibility == inf] = 0  # menjadikan nilai yang infinite menjadi 0
        pheromone = .1 * np.ones((n, n))
        rute = np.zeros((m, n))  # menjadikan seluruh rute array kosong sebesar banyak bandara = 0
        bestperformance = inf  # harga terbaik
        solutionarray = []  # rute - rute yang pernah dilewati
        performanceArray = []  # simpan harga harga dari rute yang ada
        bestperformanceArray = []  # hasil dari harga yang terbaik
        bestSolution = []  # hasil rute terbaik

        kota_asal = self.ids.spinner_opt1.text
        kota_destinasi = self.ids.spinner_opt2.text
        asal = self.convert_city(kota_asal)
        destinasi = self.convert_city(kota_destinasi)

        for ite in range(iteration):
            rute = findRouteAllAnt(rute, pheromone, visibility)
            evaluasi = evaluate(rute)
            pheromone = updatePheromone(pheromone, rute, evaluasi)
            pheromone = (1 - e) * pheromone

            # hasil solusi
            solutionarray, performanceArray, bestperformanceArray, bestperformance, bestSolution = performanceRecord(
                evaluasi, rute, bestperformance, solutionarray, performanceArray, bestperformanceArray, bestSolution)

        data.asal = asal
        data.destinasi = destinasi
        data.bestperformance = bestperformance
        data.bestperformanceArray = bestperformanceArray
        data.rute = rute
        data.pheromone = pheromone
        data.kota_asal = kota_asal
        data.kota_destinasi = kota_destinasi
        data.bestSolution = bestSolution

        print()
        print("Hasil akhir ----------------------------------------------------------")
        print("Harga terbaik: ", bestperformance)
        print("Rute terbaik: ", bestSolution)
        # print("Route: ")
        # print(rute)
        # print("Performance Array: ")
        # print(performanceArray)
        # print("Pheromone: ")
        # print(pheromone)
        for i in range(len(bestSolution)-1):
            x = int(bestSolution[i])
            y = int(bestSolution[i+1])
            # print(d[x][y]*100000)
            if y != -1:
                if i == 0:
                    data.rincianHarga = "Rp. {:,}".format(d[x][y]*100000)
                else:
                    data.rincianHarga += " + " + "Rp. {:,}".format(d[x][y]*100000)
        print(data.rincianHarga)
        print("Asal: ", asal)
        print("Destinasi: ", destinasi)
