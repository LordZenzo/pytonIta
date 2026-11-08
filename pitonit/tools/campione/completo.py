"""Campione con molti costrutti per provare il traduttore py2pit."""
import asyncio
import functools
from dataclasses import dataclass


@dataclass
class Punto:
    x: int = 0
    y: int = 0

    def __add__(self, altro):
        return Punto(self.x + altro.x, self.y + altro.y)


def descrivi(cmd):
    match cmd:
        case "inizia" | "start":
            return "avvio"
        case ["sposta", x, y]:
            return f"sposta {x},{y}"
        case {"tipo": "foto", "nome": nome}:
            return f"foto {nome}"
        case Punto(x=0, y=0):
            return "origine"
        case [primo, *resto] if len(resto) > 1:
            return f"{primo} e altri {len(resto)}"
        case _:
            return "sconosciuto"


type Numeri = list[int]


def shadow(id, type):
    # "id" e "type" sono parametri dell'utente, non i builtin
    return str(id) + "/" + str(type) + "/" + str(len([1, 2]))


def usa_builtin():
    id = 5                      # nasconde il builtin id solo qui
    return id, type(5).__name__


def globale():
    global CONTA
    CONTA = 7
    return CONTA


def esterna():
    totale = 0

    def interna():
        nonlocal totale
        totale += 1
        return totale

    interna()
    return interna()


class Conto:
    lista = []                  # attributo di classe con nome italiano riservato

    def __init__(self, testo, da=None, tipo="x"):
        self.testo = testo
        self.da = da
        self.tipo = tipo

    @property
    def lungo(self):
        return len(self.testo)

    @staticmethod
    def somma(a, b):
        return a + b

    def __repr__(self):
        return f"Conto({self.testo!r}, da={self.da}, tipo={self.tipo})"


@functools.lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def generatore(n):
    for i in range(n):
        yield i * i
    return


async def lento(n):
    await asyncio.sleep(0)
    return n * 2


def principale():
    stampe = []
    stampe.append(descrivi("start"))
    stampe.append(descrivi(["sposta", 1, 2]))
    stampe.append(descrivi({"tipo": "foto", "nome": "a.jpg"}))
    stampe.append(descrivi(Punto()))
    stampe.append(descrivi(["a", "b", "c"]))
    stampe.append(descrivi(42))
    stampe.append(shadow(1, 2))
    stampe.append(usa_builtin())
    stampe.append(globale())
    stampe.append(esterna())
    c = Conto("ciao", da="lui")
    stampe.append((repr(c), c.lungo, Conto.somma(2, 3), Conto.lista))
    stampe.append(list(generatore(4)))
    stampe.append(fib(20))
    stampe.append(asyncio.run(lento(21)))
    stampe.append([n for n in range(10) if n % 2 == 0 and not n == 4])
    stampe.append({k: v for k, v in zip("ab", range(2))})
    stampe.append((lambda q: q if q is not None else 0)(None))
    if (n := len(stampe)) > 3:
        stampe.append(n)
    try:
        int("x")
    except (ValueError, TypeError) as e:
        stampe.append(type(e).__name__)
    finally:
        stampe.append(sorted({3, 1, 2}, reverse=True))
    with open(__file__, encoding="utf-8") as f:
        stampe.append(len(f.read()) > 0)
    assert isinstance(stampe, list), "lista"
    del stampe[0]
    return stampe


if __name__ == "__main__":
    for riga in principale():
        print(riga)
