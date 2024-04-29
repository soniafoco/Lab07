import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        if self._mese == 0:
            self._view.create_alert("Non hai inserito alcun mese!")
            return
        medie_umidita = self._model.get_umidita_media(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è:"))
        for citta in medie_umidita.keys():
            self._view.lst_result.controls.append(ft.Text("%s: %.4f" % (citta, medie_umidita[citta])))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)
        print(self._mese)

    def handle_calcola_sequenza(self, e):
        if self._mese == 0:
            self._view.create_alert("Non hai inserito alcun mese!")
            return
        sequenza = self._model.calcola_percorso(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {sequenza[1]} ed è:"))
        for situazione in sequenza[0]:
            self._view.lst_result.controls.append(ft.Text(f"[{situazione.localita}-{str(situazione.data)}] Umidità = {situazione.umidita}"))
        self._view.update_page()

