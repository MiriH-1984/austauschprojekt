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

        return si

    def imp_susa_vj(self):
        sivj = pd.read_csv(
            r"G:\Documents\arbeit\python\austauschprojekt\Textdateien\SuSa_VJ_" + str(self.mdt) + "_" + str(
                self.jahr_vj) + "_kopie.csv",
            delimiter=";", encoding='cp850')
        sivj.fillna(0, inplace=True)
        sivj.set_index('Konto', inplace=True)

        return sivj


class SusaSumme:
    def susa_summe_o_EB(self, susa):
        counter = 1
        summe = 0

        while counter <= self:
            summe = summe + susa["MVZ Monat " + str(counter) + " (mit Soll/Haben-Kz)"]
            counter = counter + 1

        susa["Saldo ohne EB"] = summe

    def susa_summe_m_EB(self, susa):
        counter = 1
        summe = 0

        while counter <= self:
            summe = summe + susa["MVZ Monat " + str(counter) + " (mit Soll/Haben-Kz)"]
            counter = counter + 1

        susa["Saldo mit EB"] = susa["EB-Wert (mit Soll/Haben-Kz)"] + summe
        susa["Saldo mit EB"] = np.round(susa["Saldo mit EB"], 2)


mandant = Mandant(10044, 2018)

sik = Imp.imp_susa(mandant)

sikvj = Imp.imp_susa_vj(mandant)

# SummenderZeilenbildenundjeneueSpaltefürSaldoohne/mitEBhinzufügen
SusaSumme.susa_summe_o_EB(5, susa=sik)
SusaSumme.susa_summe_m_EB(5, susa=sik)
SusaSumme.susa_summe_o_EB(5, susa=sikvj)
SusaSumme.susa_summe_m_EB(5, susa=sikvj)

sik
"""
def einlesen():
    with open(r"Textdateien/bwa_schema.csv") as file:
        for line in file:
            data = line.strip().split(";")
            if data[0] == "1020":
                bereich = pd.DataFrame({})
                von = int(data[1])
                bis = int(data[2])
"""