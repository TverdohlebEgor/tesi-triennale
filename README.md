# Analisi Strutturale del Lightning Network

**Tesi triennale di Egor Tverdohleb**

Questo repository contiene il lavoro per la mia tesi triennale, incentrata sullo studio strutturale del **Lightning Network**. In questa fase iniziale, l'obiettivo principale è prendere familiarità con gli strumenti di analisi e i dataset. 

Per fare ciò, ho fatto riferimento al lavoro del collega Samoggia e, similmente al suo approccio, ho estratto i dati dal repository originale di cui questo progetto è un fork. I risultati finali includono la generazione di grafici sull'evoluzione temporale della rete (come il coefficiente di clustering) utilizzando **Matplotlib** su dati strutturati tramite **igraph**.

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
