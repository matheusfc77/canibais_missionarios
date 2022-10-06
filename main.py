import logging
import time
import threading
import datetime
import pytz


class Cozinheiro:

    def __init__(self):
        self.qtd_porcoes = 5
        self.qtd_encheu_caldeirao = 0
        self._lock = threading.Lock()


    def pegar_porcao(self, name):
        logging.info("Selvagem %s vai pegar porcao", name)
        with self._lock:
            logging.info("Selvagem %s bloqueando caldeirao. Qtd porcoes %i", name, self.qtd_porcoes)
            if self.qtd_porcoes <= 0:
                logging.info("Caldeirao vazio. Acordando cozinheiro")
                self.enche_caldeirao()
                logging.info("Caldeirao cheio novamente")

            local_copy = self.qtd_porcoes
            local_copy -= 1
            time.sleep(1)
            self.qtd_porcoes = local_copy
            logging.info("Selvagem %s liberando caldeirao. Qtd porcoes %i", name, self.qtd_porcoes)
        logging.info("Selvagem %s pegou porcao", name)


    def enche_caldeirao(self):
        logging.info("Cozinheiro esta enchendo o caldeirao")
        time.sleep(5)
        self.qtd_porcoes = 5
        self.qtd_encheu_caldeirao += 1
        logging.info("Cozinheiro encheu o caldeirao")


class Selvagem:

  def __init__(self, name, cozinheiro):
    self.name = name
    self.cozinheiro = cozinheiro
    self.qtd_comeu = 0


  def servir(self):
    logging.info("Selvagem %s vai se servir", self.name)
    self.cozinheiro.pegar_porcao(self.name)
    logging.info("Selvagem %s terminou de se servir", self.name)


  def comer(self):
    logging.info("Selvagem %s esta comendo", self.name)
    time.sleep(3)
    self.qtd_comeu += 1
    logging.info("Selvagem %s finalizou porcao", self.name)

    

def vamos_comer(selvagem):
    start = time.time()
    interval = 0
    while interval < 120:
        logging.info("Inicio selvagem %s", selvagem.name)
        selvagem.servir()
        selvagem.comer()
        logging.info("Fim selvagen %s", selvagem.name)
        done = time.time()
        interval = done - start



if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S.%03d")
    logging.Formatter.formatTime = (
        lambda self, record, datefmt=None: datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat())

    QTD_CANIBAIS = 3
    cozinheiro = Cozinheiro()
    threads = []
    selvagens = []
    for n in range(QTD_CANIBAIS):
        selvagem = Selvagem('S'+str(n), cozinheiro)
        selvagens.append(selvagem)
        t = threading.Thread(target=vamos_comer, args=(selvagem,))
        threads.append(t)
        t.start()

    for n in range(QTD_CANIBAIS):
        threads[n].join()

    results = {
        'qtd_cozinheiro_encheu_caldeirao': cozinheiro.qtd_encheu_caldeirao
    }
    for n in range(QTD_CANIBAIS):
        results['S'+str(n)] = selvagens[n].qtd_comeu

    print(results)
