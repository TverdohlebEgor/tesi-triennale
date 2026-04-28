# Analisi Strutturale del Lightning Network

**Tesi triennale di Egor Tverdohleb**

Questo repository contiene il lavoro per la mia tesi triennale, incentrata sullo studio strutturale del **Lightning Network**. 
Ho fatto riferimento al lavoro del collega Samoggia e, similmente al suo approccio, ho estratto i dati dal repository originale di cui questo progetto è un fork. I risultati finali includono la generazione di grafici sull'evoluzione temporale della rete (come il coefficiente di clustering) utilizzando **Matplotlib** su dati strutturati tramite **igraph**.

## Come utilizzare il codice

Come sempre per i progetti Python, si consiglia fortemente l'uso di un virtual environment per la gestione delle dipendenze

**1. Creazione e attivazione del Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
**2. Installazione delle dipendenze**
```bash
pip3 install -r requirements.txt
```

## Download dei Dati

È possibile scaricare i dump della rete presi dal repository originale. Una volta scaricati, i file compressi vanno posizionati all'interno della cartella `data/gossip/`.

| Filename / Link | SHA256 Checksum | Messages |
| :--- | :--- | :--- |
| [gossip-20201014.gsp.bz2](https://storage.googleapis.com/lnresearch/gossip-20201014.gsp.bz2) | `8c507298d2d2e7f5577ae9484986fc05630ef0bd2b59da39a60b674fd743713c` | |
| [gossip-20201102.gsp.bz2](https://storage.googleapis.com/lnresearch/gossip-20201102.gsp.bz2) | `e6628e77907406288f476d5c86f02fb310474c430eb980e0232a520c98d390aa` | |
| [gossip-20201203.gsp.bz2](https://storage.googleapis.com/lnresearch/gossip-20201203.gsp.bz2) | `fa323aae6b1c4d3d659abab8ec42cbbe81dded2ed7b3c526d3bf85f03d7b93cc` | |
| [gossip-20210104.gsp.bz2](https://storage.googleapis.com/lnresearch/gossip-20210104.gsp.bz2) | `992199372dfb5cb1fa5e305c5ef4f2604f591798d522fc0576dc8de32315c79b` | |
| [gossip-20210908.gsp.bz2](https://storage.googleapis.com/lnresearch/gossip-20210908.gsp.bz2) | `0ba0b31c12c4aec7f1255866acef485e239d54dedde99f4905cf869ec57804c1` | |
| [gossip-20220823.gsp.bz2](https://storage.googleapis.com/lnresearch/gossip-20220823.gsp.bz2) | `cb260b0d7d3633db3b267256e43b974d1ecbcd403ab559a80f5e80744578777d` | |
| [gossip-20230924.gsp.bz2](https://storage.googleapis.com/lnresearch/gossip-20230924.gsp.bz2) | `b6298fea4dd468e9f6857ab844993363143515b18f9e8c8278f33c601c058e78` | 35'984'848 |

## Estrazione dei file .graphml
I dati scaricati sono versioni compresse dei messaggi del protocollo gossip utilizzati dalla Lightning Network, i quali contengono informazioni dettagliate sullo scambio di dati e sugli annunci all'interno della rete.
Per ricostruire la topologia della rete, è stato utilizzato lo script lntopo/timemachine.py (presente nella repository sorgente dei dati), che permette di simulare la crescita della rete a partire dai messaggi di gossip fino a uno specifico momento storico.
Originariamente, lo script applicava un meccanismo di pruning per eliminare i canali considerati troppo datati. Tuttavia, poiché questa funzione generava criticità nella ricostruzione di snapshot relativi a date meno recenti, ho modificato il codice per consentire la disattivazione del pruning tramite un apposito flag. Grazie a questa modifica, i file .graphml ottenuti rappresentano l'intera topologia della rete senza perdite di dati.
Il processo è automatizzato nel file convert.sh. Di seguito la sintassi utilizzata per invocare la timemachine
```python3
    python3 -m lntopo timemachine restore [INPUT] [TIMESTAMP] --fmt graphml --no-pruning > [OUTPUT]
```

## Esecuzione

**1. Estrazione dei Grafi** Tramite lo script bash `converter.sh` è possibile processare i dump e generare i file `.graphml` (il formato standard per grafi supportato nativamente da igraph).  
I file estratti verranno salvati automaticamente nella cartella `data/graphml/`.

```bash
cd data
./converter.sh
```

**2. Generazione dell'Analisi** Infine, eseguendo lo script Python principale, il sistema elaborerà i grafi `.graphml` e creerà un plot con Matplotlib che mostra l'evoluzione del coefficiente di clustering nel tempo.

```bash
python3 main.py
```

Il risultato è presente nella cartella plots
