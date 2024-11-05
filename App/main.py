import customtkinter as ctk
from Home_page_V4 import HomePage
from Team_summary_page_V4 import TeamSummaryPage
from Players_details_page_V4 import PlayerDetailPage
from Raw_data_page_V4 import RawDataPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurations de la fenêtre principale
        self.title("CS2 Stats Aggregator")
        self.geometry("1600x900")
        self.grid_rowconfigure(1, weight=1)  # Ligne 0 pour le header, 1 pour le contenu
        self.grid_columnconfigure(0, weight=1)

        # Création des headers mais sans les afficher directement
        self.home_header = self.create_home_header()
        self.default_header = self.create_default_header()

        # Initialisation des pages
        self.home_page = HomePage(self)
        self.team_summary_page = TeamSummaryPage(self)
        self.players_details_page = PlayerDetailPage(self)
        self.raw_data_page = RawDataPage(self)

        # Dictionnaire des pages pour simplifier la navigation
        self.pages = {
            "home": self.home_page,
            "team_summary": self.team_summary_page,
            "players_details": self.players_details_page,
            "raw_data": self.raw_data_page
        }
        

        # Placement des pages dans le conteneur
        for page in self.pages.values():
            page.grid(row=1, column=0, sticky="nsew")  # Les pages sont placées sous le header

        self.analysis_results = None 


        # Afficher uniquement la page d'accueil au démarrage
        self.show_page("home")

    def set_analysis_results(self, results):
        self.analysis_results = results
        # Appelle les méthodes de mise à jour pour chaque page avec les nouveaux résultats
        self.team_summary_page.update_data(self.analysis_results)
        # self.players_details_page.update_data(self.analysis_results)
        # self.raw_data_page.update_data(self.analysis_results)

    def create_home_header(self):
        #### Header ####
        frame_header = ctk.CTkFrame(self)
        frame_header.grid(row=0, column=0, sticky="nwe")
        frame_header.grid_columnconfigure(0, weight=1)
        frame_header.grid_rowconfigure(0, weight=1)
        frame_header.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(frame_header, text='CS2 STATS AGGREGATOR', font=("Stratum2 Bd", 50), text_color=('#fbac18'))
        title.grid(row=0, column=0, sticky="new", padx=20, pady=(15, 5))

        button_frame = ctk.CTkFrame(frame_header, fg_color="transparent")
        button_frame.grid(row=1, column=0, sticky="n", padx=20, pady=20)

        ### Navigation buttons in button_frame ###
        button_team_summary = ctk.CTkButton(master=button_frame, text='Team Season Summary', font=('Stratum2 Bd', 20),command=lambda: self.show_page("team_summary"))
        button_team_summary.grid(row=1, column=0, padx=20)

        button_player_details = ctk.CTkButton(master=button_frame, text='Players Detailed Performances', font=('Stratum2 Bd', 20),command=lambda: self.show_page("players_details"))
        button_player_details.grid(row=1, column=1, padx=20)

        button_raw_data = ctk.CTkButton(master=button_frame, text='Raw Data', font=('Stratum2 Bd', 20),command=lambda: self.show_page("raw_data"))
        button_raw_data.grid(row=1, column=2, padx=20)

        return frame_header

    def create_default_header(self):
        frame_header = ctk.CTkFrame(self)
        frame_header.grid(row=0, column=0, sticky="nwe")

        # Configurer les colonnes du frame_header
        frame_header.grid_columnconfigure(0, weight=1)
        frame_header.grid_columnconfigure(1, weight=1)

        # Titre aligné à gauche
        title = ctk.CTkLabel(master=frame_header, text='CS2 STATS AGGREGATOR', font=("Stratum2 Bd", 50), text_color=('#fbac18'))
        title.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        # Frame des boutons aligné à droite
        button_frame = ctk.CTkFrame(master=frame_header, fg_color="transparent")
        button_frame.grid(row=0, column=1, sticky="e", padx=20, pady=15)

        # Boutons de navigation
        button_home = ctk.CTkButton(master=button_frame, text='Home', font=('Stratum2 Bd', 20), command=lambda: self.show_page("home"))
        button_home.grid(row=1, column=0, padx=20)

        button_team_summary = ctk.CTkButton(master=button_frame, text='Team Season Summary', font=('Stratum2 Bd', 20), command=lambda: self.show_page("team_summary"))
        button_team_summary.grid(row=1, column=1, padx=20)

        button_player_details = ctk.CTkButton(master=button_frame, text='Players Detailed Performances', font=('Stratum2 Bd', 20), command=lambda: self.show_page("players_details"))
        button_player_details.grid(row=1, column=2, padx=20)

        button_raw_data = ctk.CTkButton(master=button_frame, text='Raw Data', font=('Stratum2 Bd', 20), command=lambda: self.show_page("raw_data"))
        button_raw_data.grid(row=1, column=3, padx=20)

        return frame_header

    def show_page(self, page_name):
        # Cache toutes les pages
        for page in self.pages.values():
            page.grid_remove()

        # Affiche le header correspondant
        if page_name == "home":
            self.default_header.grid_remove()
            self.home_header.grid(row=0, column=0, sticky="nwe")
        else:
            self.home_header.grid_remove()
            self.default_header.grid(row=0, column=0, sticky="nwe")

        # Affiche la page sélectionnée
        self.pages[page_name].grid(row=1, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
