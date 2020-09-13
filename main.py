import columns as columns
import pandas as pd
import numpy as np


class Mandant:

    def __init__(self, mdt, jahr):
        self.mdt = mdt
        self.jahr = jahr
        self.jahr_vj = self.jahr - 1


class Imp:

    def __init__(self):
        self.jahr = mandant.jahr
        self.mdt = mandant.mdt

    def imp_susa(self):
        si = pd.read_csv(
            r"G:\Documents\arbeit\python\austauschprojekt\Textdateien\SuSa_" + str(self.mdt) + "_" + str(self.jahr) + "_kopie"
                                                                                                              ".csv",
            delimiter=";", encoding='cp850')
        si.fillna(0, inplace=True)
        si.set_index('Konto', inplace=True)
        si.columns = ["bez","eb","m1","m2","m3","m4","m5","m6","m7","m8","m9","m10","m11","m12","saldo","jvz","mdt","wj"]

        return si

    def imp_susa_vj(self):
        sivj = pd.read_csv(
            r"G:\Documents\arbeit\python\austauschprojekt\Textdateien\SuSa_VJ_" + str(self.mdt) + "_" + str(
                self.jahr_vj) + "_kopie.csv",
            delimiter=";", encoding='cp850')
        sivj.fillna(0, inplace=True)
        sivj.set_index('Konto', inplace=True)
        sivj.columns = ["bez", "eb", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "m11", "m12", "saldo",
                      "jvz", "mdt", "wj"]
        return sivj


class SusaSumme:
    def susa_summe_o_EB(self, susa):
        counter = 1
        summe = 0

        while counter <= self:
            summe = summe + susa["m" + str(counter)]
            counter = counter + 1

        susa["Saldo ohne EB"] = summe

    def susa_summe_m_EB(self, susa):
        counter = 1
        summe = 0

        while counter <= self:
            summe = summe + susa["m" + str(counter)]
            counter = counter + 1

        susa["Saldo mit EB"] = susa["eb"] + summe
        susa["Saldo mit EB"] = np.round(susa["Saldo mit EB"], 2)


mandant = Mandant(10044, 2018)

sik = Imp.imp_susa(mandant)

sikvj = Imp.imp_susa_vj(mandant)

# SummenderZeilenbildenundjeneueSpaltefürSaldoohne/mitEBhinzufügen
SusaSumme.susa_summe_o_EB(5,sik)
SusaSumme.susa_summe_m_EB(5,sik)
SusaSumme.susa_summe_o_EB(5,sikvj)
SusaSumme.susa_summe_m_EB(5,sikvj)

bwa_schema = pd.read_csv("Textdateien/bwa_schema.csv", delimiter=";",encoding="utf-8")
bwa_schema.columns = ["BWA", "VON", "BIS"]

# Durchlaufe bwa_schema und ordne BWA den Zeilen zu anhand des Kontos -> wenn nichts gefunden ist es NaN -> Not a Number
for index, row in bwa_schema.iterrows():
    sik.loc[(sik.index <= row['BIS']) & (sik.index >= row['VON']), 'bwa'] = row['BWA']

#Vorjahr
for index, row in bwa_schema.iterrows():
    sikvj.loc[(sikvj.index <= row['BIS']) & (sikvj.index >= row['VON']), 'bwa'] = row['BWA']

sik= sik.dropna()
sikvj= sik.dropna()

sik_bwa = sik.groupby(by = ["bwa"]).sum()
sikvj_bwa = sikvj.groupby(by = ["bwa"]).sum()
sik_bwa = sik_bwa.drop(["eb","m1","m2","m3","m4","m5","m6","m7","m8","m9","m10","m11","m12","saldo","jvz","mdt","wj"], 1)
sikvj_bwa = sikvj_bwa.drop(["eb","m1","m2","m3","m4","m5","m6","m7","m8","m9","m10","m11","m12","saldo","jvz","mdt","wj"], 1)


