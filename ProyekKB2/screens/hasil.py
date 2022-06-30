import screens.travel
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

Builder.load_file("kv/hasil.kv")


class Hasil(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def convert_city(self, kota):
        if kota == 0:
            return 'Surabaya'
        elif kota == 1:
            return 'Medan'
        elif kota == 2:
            return 'Padang'
        elif kota == 3:
            return 'Batam'
        elif kota == 4:
            return 'Palembang'
        elif kota == 5:
            return 'Jakarta'
        elif kota == 6:
            return 'Yogyakarta'
        elif kota == 7:
            return 'Bali'
        elif kota == 8:
            return 'Bima'
        elif kota == 9:
            return 'Kupang'
        elif kota == 10:
            return 'Pontianak'
        elif kota == 11:
            return 'Banjarmasin'
        elif kota == 12:
            return 'Palangkaraya'
        elif kota == 13:
            return 'Balikpapan'
        elif kota == 14:
            return 'Tarakan'
        elif kota == 15:
            return 'Palu'
        elif kota == 16:
            return 'Manado'
        elif kota == 17:
            return 'Makassar'
        elif kota == 18:
            return 'Jayapura'
        elif kota == 19:
            return 'Merauke'
        else:
            return None

    def generate(self):
        data = screens.travel.data
        # user belum memilih kota asal dan/atau tujuan
        if data.asal is None or data.destinasi is None:
            self.ids.asal_label.text = "Choose your origin"
            self.ids.destinasi_label.text = "Choose your destination"
            self.ids.harga_label.text = "-"
            self.ids.rute_label.text = "-"
        # kota asal dan tujuan sama
        elif data.asal == data.destinasi:
            self.ids.asal_label.text = "Same Origin & Destination"
            self.ids.destinasi_label.text = "Same Origin & Destination"
            self.ids.harga_label.text = "-"
            self.ids.rute_label.text = "-"
        else:
            asal = data.kota_asal
            self.ids.asal_label.text = data.kota_asal
            self.ids.destinasi_label.text = data.kota_destinasi
            # self.ids.harga_label.text = "Rp. {:,}".format(int(data.bestperformance) * 100000)
            self.ids.harga_label.text = data.rincianHarga + " = Rp. {:,}".format(int(data.bestperformance) * 100000)
            rute_kota = ""
            for i in range(len(data.bestSolution)):
                if self.convert_city(data.bestSolution[i]) is not None:
                    if i == 0:
                        rute_kota += self.convert_city(data.bestSolution[i])
                    else:
                        rute_kota += " -> " + self.convert_city(data.bestSolution[i])
            self.ids.rute_label.text = rute_kota
