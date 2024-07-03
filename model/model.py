import copy
import networkx as nx
from database.DAO import DAO
from geopy import distance

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.nodi = DAO.getAllStates()
        self._grafo.add_nodes_from(self.nodi)
        self._idMap = {}
        self.idMapPeso = {}
        for nodo in self.nodi:
            self._idMap[nodo.id] = nodo
            self.idMapPeso[nodo.id] = 0

        self._costoMigliore = 0
        self._soluzione = []
        self.dista = {}

    def buildGraph(self, forma, anno):
        self._grafo.clear_edges()
        mappaAggiornata = DAO.getPeso(forma, anno)
        for stato in mappaAggiornata:
            self.idMapPeso[stato[0].upper()] = stato[1]
        print(self.idMapPeso)
        self.addEdges(forma, anno)

        print(self.idMapPeso)
        print(mappaAggiornata)

    def addEdges(self, forma, anno):
        self._grafo.clear_edges()
        archi = DAO.getVicini()
        for arco in archi:
            nodo1 = self._idMap[arco[0]]
            if arco[1] != None:
                archi = arco[1].split()
                for idStato in archi:
                    nodo2 = self._idMap[idStato]
                    if not self._grafo.has_edge(nodo1, nodo2):
                        peso = self.idMapPeso[nodo1.id.upper()] + self.idMapPeso[nodo2.id.upper()]
                        self._grafo.add_edge(nodo1, nodo2, weight=peso)

    def getYears(self):
        return DAO.getAllYear()

    def getShapes(self):
        return DAO.getAllShape()

    def peso(self, nodo):
        peso = 0
        for n in self._grafo.neighbors(nodo):
            peso += self._grafo[nodo][n]["weight"]
        return peso

    def get_info(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getBestPath(self):
        self._soluzione = []
        self._costoMigliore = 0
        for nodo in self._grafo.nodes:
            parziale = [nodo]
            self._ricorsione(parziale)
        return self._costoMigliore, self._soluzione

    def _ricorsione(self, parziale):
        if self.distanza(parziale) > self._costoMigliore:
            self._soluzione = copy.deepcopy(parziale)
            self._costoMigliore = self.distanza(parziale)

        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale:
                if len(parziale) >= 2:
                    if self._grafo[parziale[-1]][n]["weight"] > self._grafo[parziale[-1]][parziale[-2]]["weight"]:
                        parziale.append(n)
                        self._ricorsione(parziale)
                        parziale.pop()
                else:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()

    def distanza(self, listaNodi):
        """ trova distanza lat, long """
        distanzaTot = 0
        for i in range(0, len(listaNodi) - 1):
            stato1 = listaNodi[i]
            stato2 = listaNodi[i + 1]
            posizione1 = (stato1.Lat, stato1.Lng)
            posizione2 = (stato2.Lat, stato2.Lng)
            distanza = distance.geodesic(posizione1, posizione2).km
            distanzaTot += distanza
            self.dista[f"{stato1.id}-{stato2.id}"] = distanza
        return distanzaTot

    def get_distanza(self, n1, n2):
        return self.dista[f"{n1}-{n2}"]