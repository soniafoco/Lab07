import copy
from datetime import date
from operator import itemgetter
from database.meteo_dao import MeteoDao
from model.situazione import Situazione

class Model:
    def __init__(self):
        self.soluzioni = []
        self.mese = None

    def get_umidita_media(self, mese):
        situazioni = MeteoDao.get_umidita(mese)
        somme = {"Genova":[], "Milano":[], "Torino": []}
        for situazione in situazioni:
            if situazione.localita == "Genova":
                somme["Genova"].append(situazione.umidita)
            if situazione.localita == "Milano":
                somme["Milano"].append(situazione.umidita)
            if situazione.localita == "Torino":
                somme["Torino"].append(situazione.umidita)

        medie = {"Genova": self.calcola_media(somme["Genova"]), "Milano": self.calcola_media(somme["Milano"]), "Torino": self.calcola_media(somme["Torino"])}
        return medie

    def calcola_media(self, list):
        sum = 0
        for n in list:
            sum += n
        return sum / len(list)

    def get_umidita_giorno(self, citta, giorno):
        return MeteoDao.get_umidita_giorno(self.mese, giorno, citta)

    def calcola_percorso(self, mese):

        self.mese = mese
        self.soluzioni = []
        self._ricorsione([], ["Genova", "Milano", "Torino"], 15)

        soluzioni_sorted = sorted(self.soluzioni, key=itemgetter(1))

        return soluzioni_sorted[0]


    """ 
    Questo crea tutte le possibili combinazioni di citta (3^15):
    
    def _ricorsione(self, parziale, citta, N):

        # condizione terminale
        if N == 0:
            print(parziale)
            self.soluzioni.append(copy.deepcopy(parziale))
            return
        # caso ricorsivo
        else:
            for i in range(len(citta)):
                parziale.append(citta[i])
                self._ricorsione(parziale, citta, N-1)
                parziale.pop()
    """

    def _ricorsione(self, parziale, citta, N):

        # condizione terminale
        if N == 0:
            nuova_soluzione = self.conta_costo(parziale)
            self.soluzioni.append(copy.deepcopy(nuova_soluzione))
            return
        # caso ricorsivo
        else:
            for c in citta:
                parziale.append(c)
                if self.is_valida(parziale, citta):
                    self._ricorsione(parziale, citta, N-1)
                parziale.pop()

    def is_valida(self, soluzione, citta):
        if len(soluzione)>5:
            for c in citta:
                if soluzione.count(c) > 6:
                    return False
        if len(soluzione) == 1:
            return True
        if len(soluzione) == 2:
            if soluzione[0] != soluzione[1]:
                return False
        elif len(soluzione) >= 3:
            count = 1
            for i in range(1, len(soluzione)):
                if soluzione[i] == soluzione[i-1]:
                    count += 1
                else:
                    if count<3:
                        return False
                    count = 1
            return True
        return True


    def conta_costo(self, soluzione):
        nuova_soluzione = []
        costo = 0
        for i in range(0, len(soluzione)):
            if i!=(len(soluzione)-1) and soluzione[i] != soluzione[i+1]:
                costo += 100
            umidita = self.get_umidita_giorno(soluzione[i], i+1)
            nuova_soluzione.append(Situazione(soluzione[i], date(2013,self.mese,i+1), umidita))
            costo += umidita
        return (nuova_soluzione, costo)




