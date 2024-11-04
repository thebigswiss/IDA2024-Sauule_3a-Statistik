import pandas
from mpl_toolkits.axisartist.axislines import AxesZero
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import scipy

PATH_TO_DATA = "../urliste/"
PATH_TO_EXPORT = "../export/"


class Umfrage:
    _stichprobe: pandas.DataFrame

    def __init__(self, path_to_data: str) -> None:
        self._stichprobe = pandas.read_csv(path_to_data, delimiter="	")
        self._clean_data()

    def print_to_cmd(self) -> None:
        print(self._stichprobe.to_string())

    def _clean_data(self) -> None:
        """
        Cleans the Data from trash
        """
        self._stichprobe = self._stichprobe.rename(
            {"Bitte geben Sie Ihr Alter in Jahren an" : 'Alter',
             "Besitzen Sie ein Säule 3a-Konto und zahlen ein?": 'Status',
             "In welchem Alter haben Sie zum ersten mal auf Ihr Säule 3a-Konto eingezahlt.":'Eroeffnung',
             "Was möchten Sie mit Ihrem Säule 3a-Konto erreichen?" : 'Motive-Konto',
             "Wie wichtig ist Ihr Säule 3a-Konto für Ihre Altersvorsorge?" : 'Wichtigkeit_Konto',
             "Aus welchen Gründen haben Sie kein Säule 3a-Konto?" : 'Motive_kein_Konto',
             "Wie wahrscheinlich ist es, dass Sie in den nächsten 5 Jahren ein 3a-Konto eröffnen?":'konto_zukunft',
             "Wie wichtig ist die Altersvorsorge für Sie generell?":'Wichtigkeit_Generell'}, axis='columns')

        self._stichprobe['Status'] = self._stichprobe['Status'].replace("Ja, ich habe ein 3a-Konto und ich bezahle ein.", "Besitzt ein 3a Konto")
        self._stichprobe['Status'] = self._stichprobe['Status'].replace("Nein, ich habe entweder kein Säule 3a-Konto oder ich zahle nicht ein.", "Besitzt kein ein 3a Konto")
        self._stichprobe['Zeitstempel']

    def kennzahlen(self, merkmal: str) -> list[str]:
        """
        Gibt eine Liste aller Intressanten Statistikwerten zurück
        """
        werte: list[str] = []

        werte.append("\nMittel: " +
                     str(round(self._stichprobe[merkmal].mean(), 3)))
        werte.append("\nMedian: " +
                     str(self._stichprobe[merkmal].median()))
        werte.append(
            "\nModus: " + str(self._stichprobe[merkmal].mode().values))
        werte.append(
            "\nQ1: " + str(self._stichprobe[merkmal].quantile(.25)))
        werte.append(
            "\nQ3: " + str(self._stichprobe[merkmal].quantile(.75)))
        werte.append("\ns: " + str(round(self._stichprobe[merkmal].std(), 3)))
        werte.append("\nV: " +
                     str(round(self._stichprobe[merkmal].var(), 3)))
        return werte

    def _status_der_konten(self) -> pandas.Series:
        merkmal: str = "Status"
        return self._stichprobe[merkmal].value_counts()

    def _alter_der_konten(self) -> pandas.Series:
        merkmal: str = "Eroeffnung"
        bins = pandas.IntervalIndex.from_tuples([(0,14),(15, 23), (24, 32), (33, 41), (42, 60), (61, 99)], closed="both")
        return pandas.cut(self._stichprobe[merkmal], bins).value_counts(sort=False)

    def _ziele_der_konten(self) -> pandas.Series:
        merkmal: str = 'Motive-Konto'
        return self._stichprobe[merkmal].value_counts()

    def regressions_gerade(self, merkmalA: str, merkmalB: str):# öppis komplizierts luäg i doku und gloub mir eifach. Aber Funktionales Prog. Check :) Lisp wäri stolz uf mi ;)
        """
        Gibt als Liste die Regressrionsfunktion und der r wert zurück
        """
        # y = a*x + b
        bereinigte_stichbrobe = self._stichprobe.dropna(subset=[merkmalA, merkmalB])
        a, b, r, _, _ = scipy.stats.linregress(bereinigte_stichbrobe[merkmalA].values, bereinigte_stichbrobe[merkmalB].values)
        # [f(x) = a * x + b, r]
        return lambda x : (a * x) + b, f"r: {round(r,3)}"

    def export_to_file(self, file_name: str, file_content: str | list[str]) -> None:
        file_path = PATH_TO_EXPORT + file_name
        try:
            with open(file_path, "w") as export_file:
                export_file.write(file_content)
        except TypeError: # wenn a list is provided
            with open(file_path, "w") as export_file:
                export_file.writelines(file_content)


    def export_alter_zu_wichtikeit_als_korr(self, file_name: str) -> None:
        file_path= PATH_TO_EXPORT + file_name
        xachse = self._stichprobe['Alter'].values
        _, axes = plt.subplots()
        attention = Rectangle((40,1.5),20,2,fill=False,color='red')
        axes.add_patch(attention)
        axes.spines[["left", "bottom"]].set_position(("data", 0))
        axes.spines[["top", "right"]].set_visible(False)
        axes.plot(1, 0, ">k", transform=axes.get_yaxis_transform(), clip_on=False)
        axes.plot(0, 1, "^k", transform=axes.get_xaxis_transform(), clip_on=False)
        axes.plot(xachse, self._stichprobe['Wichtigkeit_Generell'].values, linewidth=0, marker='s')
        axes.set_xlabel("Merkmalsträgeralter")
        axes.set_ylabel("Wichtikeit der Altersvorsorge von 1 bis 5")
        plt.savefig(fname=file_path)
        plt.close()

    def export_alter_zu_eroeffnung_als_korr(self, file_name: str) -> None:
        file_path = PATH_TO_EXPORT + file_name
        gerade = self.regressions_gerade('Alter','Eroeffnung')
        _, axes = plt.subplots()
        axes.spines[["left", "bottom"]].set_position(("data", 0))
        axes.spines[["top", "right"]].set_visible(False)
        axes.plot(1, 0, ">k", transform=axes.get_yaxis_transform(), clip_on=False)
        axes.plot(0, 1, "^k", transform=axes.get_xaxis_transform(), clip_on=False)
        # 1. der X Y Plot mit den Punkten
        axes.plot(self._stichprobe['Alter'].values, self._stichprobe['Eroeffnung'].values, label="Test", linewidth=0, marker='s')
        # 2. Der Regressions Plot
        axes.plot(self._stichprobe['Alter'].values, gerade[0](self._stichprobe['Alter'].values))
        axes.set_xlabel("Merkmalsträgeralter")
        axes.set_ylabel("Merkmalsträgeralter bei der Eröffnung")
        axes.text(s=gerade[1],x=40,y=50)
        plt.savefig(fname=file_path)
        plt.close()


    def export_motive_konten_als_barh(self, file_name: str) -> None:
        file_path = PATH_TO_EXPORT + file_name
        figure, axes = plt.subplots(figsize=(10, 8)) # figsize adjusts the width and height of the diagram
        axes.barh(self._stichprobe['Motive-Konto'].values.astype(str), self._stichprobe['Motive-Konto'].values, label="Test")
        axes.set_xlabel("Anzahl Merkmalsträger")
        plt.tight_layout() # solves the problem of clipped names
        plt.savefig(fname=file_path)
        plt.close()

    def exports_alter_als_bar(self, file_name: str) -> None:
        file_path = PATH_TO_EXPORT + file_name
        _, axes = plt.subplots()
        axes.spines[["left", "bottom"]].set_position(("zero"))
        axes.spines[["top", "right"]].set_visible(False)
        axes.plot(1, 0, ">k", transform=axes.get_yaxis_transform(), clip_on=False)
        axes.plot(0, 1, "^k", transform=axes.get_xaxis_transform(), clip_on=False)
        axes.bar(self._status_der_konten().index.astype(str), self._status_der_konten().values, label="Status der Konten",align="edge")
        axes.set_ylabel("Anzahl Merkmalsträger")
        # Text mit der Standart abweichung
        #axes.set_xmargin(0.2)
        plt.tight_layout() # solves the problem of clipped names
        axes.text(s=self.kennzahlen("Alter")[5], x=2, y=17.5)
        plt.savefig(fname=file_path)
        plt.close()


    def export_eroeffnung_als_bar(self, file_name: str) -> None:
        file_path = PATH_TO_EXPORT + file_name
        axes = plt.subplot()
        axes.spines[["left", "bottom"]].set_position(("data", 0))
        axes.spines[["top", "right"]].set_visible(False)
        axes.plot(1, 0, ">k", transform=axes.get_yaxis_transform(), clip_on=False)
        axes.plot(0, 1, "^k", transform=axes.get_xaxis_transform(), clip_on=False)
        axes.bar(self._alter_der_konten().index.astype(str), self._alter_der_konten().values, label="Kontoeröffnungsjahr",align="center")
        axes.set_ylabel("Anzahl der Konten")
        axes.set_xlabel("Zeitintervall in Altersjahren")
        axes.text(s=self.kennzahlen("Eroeffnung")[5], x=4, y=7)
        plt.savefig(fname=file_path)
        plt.close()

def main():
    # Globale Pfade

    # Instanziert die Klasse und bereinigt die Daten
    #TODO: DingsPLot für Alter

    ida_2024: Umfrage = Umfrage(PATH_TO_DATA + "urliste.tsv")
    ida_2024.export_alter_zu_eroeffnung_als_korr("korr_alter_eroeffnung.png")
    ida_2024.export_eroeffnung_als_bar("eroeffnung_bar.png")
    #ida_2024.export_motive_konten_als_barh("motive_konto.pgf")
    ida_2024.exports_alter_als_bar("Alter_bar.png")
    ida_2024.export_alter_zu_wichtikeit_als_korr("korr_aler_wichtikeit.png")
    ida_2024.export_to_file("Alter_Kennzahlen.txt",ida_2024.kennzahlen('Alter'))
    ida_2024.export_to_file("Eroeffnung_Kennzahlen.txt",ida_2024.kennzahlen('Eroeffnung'))
    ida_2024.export_to_file("Wichtigkeit_Generell_Kennzahlen.txt",ida_2024.kennzahlen('Wichtigkeit_Generell'))

if __name__ == "__main__":
    main()
