import pandas
import matplotlib.pyplot as plt
import scipy

PATH_TO_DATA = "../urliste/"
PATH_TO_EXPORT = "../export/"


class Umfrage:
    _stichprobe_liste: pandas.DataFrame

    def __init__(self, path_to_data: str) -> None:
        self._stichprobe_liste = pandas.read_csv(path_to_data, delimiter="	")

    def print_to_cmd(self) -> None:
        print(self._stichprobe_liste.to_string())

    def _drop_colum(self, colum: str) -> None:
        """
        Removes the specified colum by the name
        """
        del self._stichprobe_liste[colum]

    def clean_data(self) -> None:
        """
        Cleans the Data from trash
        """
        self._drop_colum('Zeitstempel')
        self._stichprobe_liste = self._stichprobe_liste.rename(
            {"Bitte geben Sie Ihr Alter in Jahren an" : 'Alter',
             "Besitzen Sie ein Säule 3a-Konto und zahlen ein?": 'Status',
             "In welchem Alter haben Sie zum ersten mal auf Ihr Säule 3a-Konto eingezahlt.":'Eroeffnung',
             "Was möchten Sie mit Ihrem Säule 3a-Konto erreichen?" : 'Motive-Konto',
             "Wie wichtig ist Ihr Säule 3a-Konto für Ihre Altersvorsorge?" : 'Wichtigkeit_Konto',
             "Aus welchen Gründen haben Sie kein Säule 3a-Konto?" : 'Motive_kein_Konto',
             "Wie wahrscheinlich ist es, dass Sie in den nächsten 5 Jahren ein 3a-Konto eröffnen?":'konto_zukunft',
             "Wie wichtig ist die Altersvorsorge für Sie generell?":'Wichtigkeit_Generell'}, axis='columns')
        self._stichprobe_liste['Status'].replace("Ja, ich habe ein 3a-Konto und ich bezahle ein.", "Besitzt ein 3a Konto", inplace=True)
        self._stichprobe_liste['Status'].replace("Nein, ich habe entweder kein Säule 3a-Konto oder ich zahle nicht ein.", "Besitzt kein ein 3a Konto", inplace=True)
        print(self._stichprobe_liste)

    def std_abweichung(self, merkmal: str) -> int:
        return self._stichprobe_liste[merkmal].std()

    def kennzahlen(self, merkmal: str) -> list[str]:
        werte: list[str] = []

        werte.append("\nAth. Mittel: " +
                     str(round(self._stichprobe_liste[merkmal].mean(), 3)))
        werte.append("\nMedian: " +
                     str(self._stichprobe_liste[merkmal].median()))
        werte.append(
            "\nModus: " + str(self._stichprobe_liste[merkmal].mode().values))
        werte.append(
            "\nQ1: " + str(self._stichprobe_liste[merkmal].quantile(.25)))
        werte.append(
            "\nQ3: " + str(self._stichprobe_liste[merkmal].quantile(.75)))
        werte.append("\ns: " + str(round(self._stichprobe_liste[merkmal].std(), 3)))
        werte.append("\nV: " +
                     str(round(self._stichprobe_liste[merkmal].var(),)))
        return werte

    def status_der_konten(self) -> pandas.Series:
        merkmal: str = "Status"
        return self._stichprobe_liste[merkmal].value_counts()

    def alter_der_konten(self) -> pandas.Series:
        merkmal: str = "Eroeffnung"
        bins = pandas.IntervalIndex.from_tuples([(18, 25), (26, 35), (36, 55), (56, 64), (65, 99)], closed="both")
        return pandas.cut(self._stichprobe_liste[merkmal], bins).value_counts(sort=False)

    def ziele_der_konten(self) -> pandas.Series:
        merkmal: str = 'Motive-Konto'
        return self._stichprobe_liste[merkmal].value_counts()

    def regressions_gerade(self, merkmalA: str, merkmalB: str): # öppis komplizierts luäg i doku
        # y = a*x + b
        stichbrobe_liste = self._stichprobe_liste.dropna(subset=[merkmalA, merkmalB])
        a, b, r, _, _ = scipy.stats.linregress(stichbrobe_liste[merkmalA].values, stichbrobe_liste[merkmalB].values)
        return lambda x : (a * x) + b, f"r: {r}"


def export_to_file(file_path: str, file_content: str | list[str]) -> None:
    try:
        with open(file_path, "w") as export_file:
            export_file.write(file_content)
    except TypeError:
        with open(file_path, "w") as export_file:
            export_file.writelines(file_content)

def export_corr_graph_alter(file_path: str, dataX: pandas.Series, dataY: pandas.Series, gerade) -> None:
    filetype: str = 'png'
    figure, axes = plt.subplots()
    axes.plot(dataX.values, dataY.values, label="Test", linewidth=0, marker='s')
    axes.plot(dataX.values, gerade[0](dataX.values))
    axes.set_title("Regressrion Alter zu Eröffnungsalter")
    axes.set_xlabel("Alter")
    axes.set_ylabel("Eröffnung")
    axes.set_xlim([0,70])
    axes.set_ylim([0,70])
    axes.text(s=gerade[1],x=40,y=50)
    plt.savefig(fname=file_path + "." + filetype, format=filetype)
    plt.close()


def export_to_bar(file_path: str, data: pandas.Series) -> None:
    # TODO: plot beautifier
    filetype: str = 'png'
    figure, axes = plt.subplots()
    axes.bar(data.index.astype(str), data.values, label="Test")
    axes.set_ylabel("Anzahl #")
    axes.set_title("Test")
    plt.savefig(fname=file_path + "." + filetype, format=filetype)
    plt.close()


def export_to_horizontal_bar(file_path: str, data: pandas.Series) -> None:
    # TODO: plot beautifier
    filetype: str = 'png'
    figure, axes = plt.subplots(figsize=(10, 8)) # figsize adjusts the width and height of the diagram
    axes.barh(data.index.astype(str), data.values, label="Test")
    axes.set_xlabel("Anzahl #")
    axes.set_title("Test")
    plt.tight_layout() # solves the problem of clipped names
    plt.savefig(fname=file_path + "." + filetype, format=filetype)
    plt.close()


def export_to_boxplot(file_path: str, data: pandas.Series) -> None:
    plt.boxplot(data.values)
    plt.savefig(fname=file_path, format='svg')
    plt.close()

def export_corr(ida_2024: Umfrage) -> None:
    pass


def exports_alter(ida_2024: Umfrage) -> None:
    axes = plt.subplot()
    axes.bar(ida_2024.status_der_konten().index.astype(str), ida_2024.status_der_konten().values, label="Status der Konten")
    axes.set_ylabel("Anzahl [#]")
    axes.set_title("Wie viele haben ein Konto")
    axes.text(s=ida_2024.kennzahlen("Alter")[5], x=2, y=17.5)
    plt.savefig(fname= PATH_TO_EXPORT + "Status_Konten.png", format='png')
    plt.close()
    export_to_boxplot(PATH_TO_EXPORT + "alter-boxplot",
                      ida_2024._stichprobe_liste["Alter"])


def export_alter_konto(ida_2024: Umfrage) -> None:
    axes = plt.subplot()
    axes.bar(ida_2024.alter_der_konten().index.astype(str), ida_2024.alter_der_konten().values, label="Kontoeröffnungsjahr")
    axes.set_ylabel("Anzahl der Konten (#)")
    axes.set_title("Eröffnungsjahr von 3a-Konten")
    axes.set_xlabel("Zeitintervall in Altersjahren [Δj]")
    axes.text(s=ida_2024.kennzahlen("Eroeffnung")[5], x=2, y=6)
    plt.savefig(fname=PATH_TO_EXPORT + "alter_errofnung.svg",format='svg')
    plt.close()

    export_to_file(PATH_TO_EXPORT + "konto-alter_values.txt",
                   ida_2024.kennzahlen("Eroeffnung"))


def exports_konto_status(ida_2024: Umfrage) -> None:
    export_to_file(PATH_TO_EXPORT + "status_konten.txt",
                   ida_2024.status_der_konten().to_string())
    export_to_bar(PATH_TO_EXPORT + "status_konten",
                  ida_2024.status_der_konten())


def exports_konto_ziele(ida_2024: Umfrage) -> None:
    export_to_file(PATH_TO_EXPORT + "ziele_konten.txt",
                   ida_2024.ziele_der_konten().to_string())
    export_to_horizontal_bar(PATH_TO_EXPORT + "ziele_konten",
                   ida_2024.ziele_der_konten())
    


def main():
    # Globale Pfade

    # Instanziert die Klasse und bereinigt die Daten
    ida_2024: Umfrage = Umfrage(PATH_TO_DATA + "urliste.tsv")
    ida_2024.clean_data()
    # Exportiert die Daten in externe Files für das verwenden in der Dokumenation.
    exports_konto_status(ida_2024)
    exports_alter(ida_2024)
    export_alter_konto(ida_2024)
    exports_konto_ziele(ida_2024)
    test = ida_2024.regressions_gerade("Alter","Eroeffnung")
    #print(test(ida_2024._stichprobe_liste["Alter"].values))
    export_corr_graph_alter(PATH_TO_EXPORT + "Test", ida_2024._stichprobe_liste["Alter"], ida_2024._stichprobe_liste["Eroeffnung"], ida_2024.regressions_gerade("Alter","Eroeffnung"))


if __name__ == "__main__":
    main()
