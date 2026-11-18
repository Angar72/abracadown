"""Invia ad Alice, una volta al giorno, un messaggio WhatsApp che la invita a fare gli esercizi.
Un giorno parla Alice, il giorno dopo Giulia (alternati).
Usa il servizio gratuito CallMeBot. Numero e chiave stanno nei Secrets del repository:
  ALICE_PHONE       -> numero di Alice con prefisso, es. +393331234567
  CALLMEBOT_APIKEY  -> chiave ricevuta da CallMeBot sul telefono di Alice
"""
import datetime
import os
import sys
import urllib.parse
import urllib.request

LINK = "https://angar72.github.io/abracadown/gioco-alice/"

ALICE = [
    "Ciao Alice! Sono Alice 🧡 Oggi ci alleniamo insieme con *e* ed *è*? Bastano 5 minuti!",
    "Ehi! Sono Alice 🧡 Ti ricordi il trucco? Se ci sta *era*, allora ci vuole *è*! Vieni a provare 😉",
    "Alice chiama Alice! 🧡 Una partita veloce e poi sei libera. Ci stai?",
    "Ciao campionessa! 🧡 Oggi proviamo a fare 10 su 10? Io ci credo!",
    "Sono Alice 🧡 Ho preparato nuove frasi per te. Facciamo una sfida?",
    "Buongiorno da Alice! 🧡 Un piccolo esercizio al giorno e diventi imbattibile 💪",
    "Alice qui! 🧡 Oggi tocca a te: *e* oppure *è*? Ti aspetto nel gioco!",
]
GIULIA = [
    "Ciao Alice! Sono Giulia 💙 Oggi giochiamo con *a* e *ha*? Ti aspetto!",
    "Sono Giulia 💙 Ricorda: se ci sta *aveva*, allora ci vuole *ha*! Facciamo qualche frase?",
    "Ehi Alice! Giulia qui 💙 Cinque minuti di allenamento e poi relax 😊",
    "Ciao! Sono Giulia 💙 Vediamo se oggi batti il tuo record?",
    "Giulia ti saluta! 💙 Una partita a *a/ha* e diventi bravissima 🌟",
    "Sono Giulia 💙 Ho una sfida per te: tutto mescolato! Ce la fai?",
    "Ciao Alice! 💙 Giulia ti aspetta per l'allenamento di oggi ✨",
]


def main():
    phone = os.environ.get("ALICE_PHONE", "").strip()
    apikey = os.environ.get("CALLMEBOT_APIKEY", "").strip()
    if not phone or not apikey:
        print("Numero o chiave non impostati nei Secrets: nessun messaggio inviato.")
        return 0

    oggi = datetime.date.today()
    n = oggi.toordinal()
    if n % 2 == 0:
        testo = ALICE[(n // 2) % len(ALICE)]
    else:
        testo = GIULIA[(n // 2) % len(GIULIA)]
    testo += f"\n\n👉 Gioca qui: {LINK}"

    url = "https://api.callmebot.com/whatsapp.php?" + urllib.parse.urlencode(
        {"phone": phone, "text": testo, "apikey": apikey}
    )
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            risposta = r.read().decode("utf-8", "replace")
    except Exception as e:  # rete o servizio non raggiungibile
        print("Invio non riuscito:", e)
        return 1
    print("Risposta CallMeBot:", risposta[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
