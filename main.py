rom abc import ABC, abstractmethod
from datetime import datetime


class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self._jaratszam = jaratszam
        self._celallomas = celallomas
        self._jegyar = jegyar

    def get_jaratszam(self):
        return self._jaratszam

    def get_celallomas(self):
        return self._celallomas

    def get_jegyar(self):
        return self._jegyar

    @abstractmethod
    def jarat_tipus(self):
        pass

    def __str__(self):
        return self._jaratszam + " - " + self._celallomas + " - " + str(self._jegyar) + " Ft - " + self.jarat_tipus()


class BelfoldiJarat(Jarat):
    def jarat_tipus(self):
        return "Belföldi járat"


class NemzetkoziJarat(Jarat):
    def jarat_tipus(self):
        return "Nemzetközi járat"


class LegiTarsasag:
    def __init__(self, nev):
        self._nev = nev
        self._jaratok = []

    def get_nev(self):
        return self._nev

    def jarat_hozzaadasa(self, jarat):
        self._jaratok.append(jarat)

    def jaratok_listazasa(self):
        print("\nElérhető járatok:")
        for jarat in self._jaratok:
            print(jarat)

    def jarat_keresese(self, jaratszam):
        for jarat in self._jaratok:
            if jarat.get_jaratszam() == jaratszam:
                return jarat
        return None


class JegyFoglalas:
    def __init__(self, foglalasi_azonosito, utas_nev, jarat, datum):
        self._foglalasi_azonosito = foglalasi_azonosito
        self._utas_nev = utas_nev
        self._jarat = jarat
        self._datum = datum

    def get_foglalasi_azonosito(self):
        return self._foglalasi_azonosito

    def get_utas_nev(self):
        return self._utas_nev

    def get_jarat(self):
        return self._jarat

    def get_datum(self):
        return self._datum

    def __str__(self):
        return (
            "Foglalás azonosító: " + str(self._foglalasi_azonosito) +
            ", Utas: " + self._utas_nev +
            ", Járat: " + self._jarat.get_jaratszam() +
            ", Célállomás: " + self._jarat.get_celallomas() +
            ", Dátum: " + self._datum
        )


class FoglalasiRendszer:
    def __init__(self, legitarsasag):
        self._legitarsasag = legitarsasag
        self._foglalasok = []
        self._kovetkezo_azonosito = 1

    def datum_ervenyes(self, datum):
        try:
            megadott_datum = datetime.strptime(datum, "%Y-%m-%d")
            mai_datum = datetime.now()

            if megadott_datum.date() < mai_datum.date():
                return False

            return True
        except ValueError:
            return False

    def jegy_foglalasa(self, utas_nev, jaratszam, datum):
        jarat = self._legitarsasag.jarat_keresese(jaratszam)

        if jarat is None:
            print("Hiba: Nem létezik ilyen járat.")
            return

        if not self.datum_ervenyes(datum):
            print("Hiba: Érvénytelen dátum. A formátum legyen ÉÉÉÉ-HH-NN, és nem lehet múltbeli dátum.")
            return

        foglalas = JegyFoglalas(self._kovetkezo_azonosito, utas_nev, jarat, datum)
        self._foglalasok.append(foglalas)
        self._kovetkezo_azonosito += 1

        print("Sikeres foglalás!")
        print("A jegy ára:", jarat.get_jegyar(), "Ft")

    def foglalas_lemondasa(self, foglalasi_azonosito):
        for foglalas in self._foglalasok:
            if foglalas.get_foglalasi_azonosito() == foglalasi_azonosito:
                self._foglalasok.remove(foglalas)
                print("A foglalás sikeresen lemondva.")
                return

        print("Hiba: Nincs ilyen foglalási azonosító.")

    def foglalasok_listazasa(self):
        print("\nAktuális foglalások:")

        if len(self._foglalasok) == 0:
            print("Nincs aktuális foglalás.")
        else:
            for foglalas in self._foglalasok:
                print(foglalas)


def adatok_betoltese():
    legitarsasag = LegiTarsasag("Python Airlines")

    jarat1 = BelfoldiJarat("B101", "Budapest", 15000)
    jarat2 = BelfoldiJarat("B202", "Debrecen", 12000)
    jarat3 = BelfoldiJarat("B303","Sarmellek", 13000)
    jarat4 = NemzetkoziJarat("N404", "London", 55000)
    jarat5 = NemzetkoziJarat("N505", "London", 75000)

    legitarsasag.jarat_hozzaadasa(jarat1)
    legitarsasag.jarat_hozzaadasa(jarat2)
    legitarsasag.jarat_hozzaadasa(jarat3)
    legitarsasag.jarat_hozzaadasa(jarat4)
    legitarsasag.jarat_hozzaadasa(jarat5)

    rendszer = FoglalasiRendszer(legitarsasag)

    rendszer.jegy_foglalasa("Sanyi", "B101", "2026-06-10")
    rendszer.jegy_foglalasa("Feri", "B202", "2026-06-12")
    rendszer.jegy_foglalasa("Laci", "N404", "2026-07-01")
    rendszer.jegy_foglalasa("Peti", "B101", "2026-06-15")
    rendszer.jegy_foglalasa("Mirtillke", "B202", "2026-06-20")
    rendszer.jegy_foglalasa("Rozi", "N505", "2026-07-05")

    return legitarsasag, rendszer


def menu():
    legitarsasag, rendszer = adatok_betoltese()

    while True:
        print("\n--- Repülőjegy Foglalási Rendszer ---")
        print("Légitársaság:", legitarsasag.get_nev())
        print("1. Járatok listázása")
        print("2. Jegy foglalása")
        print("3. Foglalás lemondása")
        print("4. Foglalások listázása")
        print("5. Kilépés")

        valasztas = input("Válassz egy menüpontot: ")

        if valasztas == "1":
            legitarsasag.jaratok_listazasa()

        elif valasztas == "2":
            utas_nev = input("Add meg az utas nevét: ")
            jaratszam = input("Add meg a járatszámot: ")
            datum = input("Add meg az utazás dátumát ÉÉÉÉ-HH-NN formátumban: ")

            rendszer.jegy_foglalasa(utas_nev, jaratszam, datum)

        elif valasztas == "3":
            try:
                azonosito = int(input("Add meg a foglalási azonosítót: "))
                rendszer.foglalas_lemondasa(azonosito)
            except ValueError:
                print("Hiba: Az azonosítónak számnak kell lennie.")

        elif valasztas == "4":
            rendszer.foglalasok_listazasa()

        elif valasztas == "5":
            print("Kilépés...")
            break

        else:
            print("Hiba: Nincs ilyen menüpont.")

menu()
