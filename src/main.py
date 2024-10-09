import pandas
import matplotlib.pyplot as plt

PATH_TO_DATA = "../urliste/"
PATH_TO_EXPORT = "../export/"


class Umfrage:
    _stichprobe_liste: pandas.DataFrame

    def __init__(self, path_to_data: str) -> None:
        self._stichprobe_liste = pandas.read_csv(path_to_data)

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

    def std_abweichung(self, merkmal: str) -> int:
        return self._stichprobe_liste[merkmal].std()

    def kennzahlen(self, merkmal: str) -> list[str]:
        werte: list[str] = []

        werte.append("\nArt. Mittel: " +
                     str(self._stichprobe_liste[merkmal].mean()))
        werte.append("\nMedian: " +
                     str(self._stichprobe_liste[merkmal].median()))
        werte.append(
            "\nModus: " + str(self._stichprobe_liste[merkmal].mode().values))
        werte.append(
            "\nQ1: " + str(self._stichprobe_liste[merkmal].quantile(.25)))
        werte.append(
            "\nQ3: " + str(self._stichprobe_liste[merkmal].quantile(.75)))
        werte.append("\nStd: " + str(self._stichprobe_liste[merkmal].std()))
        werte.append("\nVarianz: " +
                     str(self._stichprobe_liste[merkmal].var()))
        return werte

    def status_der_konten(self) -> pandas.Series:
        merkmal: str = "Status"
        return self._stichprobe_liste[merkmal].value_counts()

    def alter_der_konten(self) -> pandas.Series:
        merkmal: str = "Eroeffnung"
        bins = pandas.IntervalIndex.from_tuples([(17.5,25.5),(25.5,35.5),(35.5,55.5),(55.5,64.5),(64.5,99)])
        return pandas.cut(self._stichprobe_liste[merkmal], bins).value_counts()


def export_to_file(file_path: str, file_content: str | list[str]) -> None:
    try:
        with open(file_path, "w") as export_file:
            export_file.write(file_content)
    except TypeError:
        with open(file_path, "w") as export_file:
            export_file.writelines(file_content)


def export_to_graph(file_path: str, graph_content):
    raise NotImplementedError


def export_to_bar(file_path: str, data: pandas.Series) -> None:
    # TODO: plot beautifier
    plt.bar(data.index.astype(str), data.values)
    plt.savefig(fname=file_path, format='svg')
    plt.close()


def export_to_boxplot(file_path: str, data: pandas.Series) -> None:
    plt.boxplot(data.values)
    plt.savefig(fname=file_path, format='svg')
    plt.close()


def exports_alter(ida_2024: Umfrage) -> None:
    export_to_file(PATH_TO_EXPORT + "alter_values.txt",
                   ida_2024.kennzahlen("Alter"))
    export_to_boxplot(PATH_TO_EXPORT + "alter-boxplot.svg",
                      ida_2024._stichprobe_liste["Alter"])


def export_alter_konto(ida_2024: Umfrage) -> None:
    export_to_bar(PATH_TO_EXPORT + "konto-alter_values.svg", ida_2024.alter_der_konten())
    print(ida_2024.alter_der_konten())
    export_to_file(PATH_TO_EXPORT + "konto-alter_values.txt",
                   ida_2024.kennzahlen("Eroeffnung"))


def exports_konto_status(ida_2024: Umfrage) -> None:
    export_to_file(PATH_TO_EXPORT + "status_konten.txt",
                   ida_2024.status_der_konten().to_string())
    export_to_bar(PATH_TO_EXPORT + "status_konten.svg",
                  ida_2024.status_der_konten())


def main():
    # Globale Pfade

    # Instanziert die Klasse und bereinigt die Daten
    ida_2024: Umfrage = Umfrage(PATH_TO_DATA + "urliste.csv")
    ida_2024.clean_data()
    # Exportiert die Daten in externe Files für das verwenden in der Dokumenation.
    exports_konto_status(ida_2024)
    exports_alter(ida_2024)
    export_alter_konto(ida_2024)


if __name__ == "__main__":
    main()
