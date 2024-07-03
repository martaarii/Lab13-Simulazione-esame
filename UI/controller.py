import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        anni = self._model.getYears()
        forme = self._model.getShapes()
        for anno in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(anno))
        for forma in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(forma))
        self._view.update_page()

    def handle_graph(self, e):
        if self._view.ddshape.value is None:
            self._view.create_alert("Selezionare una forma")
            return
        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare una anno")
            return
        self._model.buildGraph(self._view.ddshape.value, self._view.ddyear.value)
        num_nodi, num_archi = self._model.get_info()
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {num_nodi}"
                                                      f"Numero archi: {num_archi}"))
        nodi = self._model.nodi
        for n in nodi:
            self._view.txt_result.controls.append(ft.Text(
                f"{n.id} -- Avvistamenti: {self._model.peso(n)}"))
        self._view.update_page()

    def handle_path(self, e):
        # peso percorso cammino massimo
        pesoMax , percorso = self._model.getBestPath()
        self._view.txtOut2.controls.append(ft.Text(f"Peso del cammino massimo: {pesoMax}"))
        for i in range(len(percorso)-1):
            self._view.txtOut2.controls.append(
                ft.Text(f"{percorso[i]} --> {percorso[i+1]} : "
                        f"{self._model.get_distanza(percorso[i].id ,percorso[i+1].id)}"))
        self._view.update_page()