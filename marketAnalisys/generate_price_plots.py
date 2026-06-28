import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
from datetime import datetime

# ── Output directories ──────────────────────────────────────────────────────
BASE = r"C:\Users\thega\Desktop\tesi-triennale"
DATA_DIR = os.path.join(BASE, "marketAnalisys")
PLOT_DIR = os.path.join(BASE, "tesi", "plots")

# ── Significant events per coin ─────────────────────────────────────────────
EVENTS = {
    "BTC": [
        ("2017-08-24", "SegWit\nattivato"),
        ("2017-12-17", "ATH\n$19K"),
        ("2020-05-11", "3° Halving"),
        ("2021-11-10", "ATH\n$69K"),
        ("2022-11-11", "Crollo\nFTX"),
        ("2024-01-10", "ETF\napprovato"),
        ("2024-04-19", "4° Halving"),
    ],
    "ETH": [
        ("2018-01-13", "ATH\n$1.4K"),
        ("2020-07-01", "DeFi\nSummer"),
        ("2021-11-09", "ATH\n$4.9K"),
        ("2022-09-15", "The Merge\n(PoS)"),
        ("2022-11-11", "Crollo\nFTX"),
    ],
    "LTC": [
        ("2017-05-10", "SegWit\nLTC"),
        ("2017-12-19", "ATH\n$375"),
        ("2019-08-05", "3° Halving"),
        ("2022-11-11", "Crollo\nFTX"),
        ("2023-08-02", "4° Halving"),
    ],
    "DOGE": [
        ("2021-02-08", "Tweet\nMusk"),
        ("2021-05-08", "ATH\n$0.73"),
        ("2022-11-11", "Crollo\nFTX"),
        ("2023-04-03", "Twitter\n→ X"),
        ("2024-11-05", "Elezioni\nUSA"),
    ],
}

COIN_LABELS = {
    "BTC":  ("Bitcoin (BTC)",  "#F7931A", "bitcoin"),
    "ETH":  ("Ethereum (ETH)", "#627EEA", "ethereum"),
    "LTC":  ("Litecoin (LTC)", "#BFBBBB", "litecoin"),
    "DOGE": ("Dogecoin (DOGE)","#C2A633", "dogecoin"),
}

# ── Analysis window ─────────────────────────────────────────────────────────
START = "2017-01-01"
END   = "2026-06-30"

for coin, (label, color, folder) in COIN_LABELS.items():
    csv_path = os.path.join(DATA_DIR, f"{coin}_All_graph_coinmarketcap.csv")
    df = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df["timestamp"] = pd.to_datetime(df["timestamp"].str.strip('"'))
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df[(df["timestamp"] >= START) & (df["timestamp"] <= END)].dropna(subset=["price"])

    fig, ax = plt.subplots(figsize=(10, 4.5))

    ax.plot(df["timestamp"], df["price"], color=color, linewidth=1.6, zorder=3)
    ax.fill_between(df["timestamp"], df["price"], alpha=0.08, color=color, zorder=2)

    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, _: f"${x:,.0f}" if x >= 1 else f"${x:.4f}"
    ))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[7]))

    ax.set_xlim(pd.Timestamp(START), pd.Timestamp(END))
    ax.set_xlabel("Anno", fontsize=11)
    ax.set_ylabel("Prezzo (USD, scala log)", fontsize=11)
    ax.set_title(f"Andamento storico del prezzo — {label}", fontsize=13, fontweight="bold")
    ax.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.grid(True, which="minor", linestyle=":", linewidth=0.3, alpha=0.3)

    # ── Vertical event lines ──────────────────────────────────────────────
    ymin, ymax = df["price"].min(), df["price"].max()
    events = EVENTS[coin]
    for i, (date_str, label_txt) in enumerate(events):
        dt = pd.Timestamp(date_str)
        if dt < pd.Timestamp(START) or dt > pd.Timestamp(END):
            continue
        ax.axvline(dt, color="#333333", linewidth=0.9, linestyle="--", alpha=0.7, zorder=4)
        # Alternate label height to avoid overlap
        y_frac = 0.82 if i % 2 == 0 else 0.60
        ax.text(
            dt, ymin * (ymax / ymin) ** y_frac,
            label_txt,
            fontsize=7.5, ha="center", va="bottom",
            color="#222222",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.75),
            zorder=5,
        )

    fig.tight_layout()

    out_path = os.path.join(PLOT_DIR, folder, "price_history.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Salvato: {out_path}")

print("Tutti i grafici generati.")
