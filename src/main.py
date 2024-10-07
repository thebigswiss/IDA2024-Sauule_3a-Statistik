import pandas


class Umfrage:
    _stichprobe_liste: pandas.DataFrame

    def __init__(self, path_to_data: str):
        self._stichprobe_liste = pandas.read_csv(path_to_data)

    def print_to_cmd(self):
        print(self._stichprobe_liste.to_string())

    def _drop_colum(self, colum: str):
        """
        Removes the specified colum by the name
        """
        del self._stichprobe_liste[colum]

    def clean_data(self):
        """
        Cleans the Data from trash
        """
        self._drop_colum('Zeitstempel')

    def alter_arithmetisches_mittel(self) -> int:
        """
        Berechung des Arithmetischen Mittel vom Alter
        aller Merklmalsträger in der Stichprobe.
        """
        merkmal: str = "Alter"
        return self._stichprobe_liste[merkmal].mean()

    def alter_median(self) -> int:
        """
        Berechung des Medians vom Alter
        aller Merklmalsträger in der Stichprobe.
        """
        merkmal: str = "Alter"
        return self._stichprobe_liste[merkmal].median()

    def print_status_des_kontos(self):
        merkmal: str = "Status"
        print(self._stichprobe_liste[merkmal].value_counts())


def main():
    PATH_TO_DATA = "../urliste/"
    ida_2024: Umfrage = Umfrage(PATH_TO_DATA + "urliste.csv")
    ida_2024.clean_data()
    #ida_2024.print_to_cmd()
    #TODO: PATH_TO_EXPORT = "../export/"
    print("Arithmetisches Mittel des Alters: " + str(ida_2024.alter_arithmetisches_mittel()))
    print("Medial des Alters: " + str(ida_2024.alter_median()))
    ida_2024.print_status_des_kontos()


if __name__ == "__main__":
    main()
