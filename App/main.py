import customtkinter as ctk
from PIL import Image, ImageOps, ImageDraw
from Home_page import HomePage
from Team_summary_page import TeamSummaryPage, round_corners_top
# from detailed_performance_page import DetailedPerformancePage
# from match_analysis_page import MatchAnalysisPage

ctk.set_appearance_mode('dark')

# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("CS2 Stats Aggregator")
#         self.geometry("1600x900")

#         # Dictionnaire des pages
#         self.pages = {}
#         self.create_pages()

#         # Affiche la première page
#         self.show_page("Home")

#     def create_pages(self):
#         #self.pages["Home"] = HomePage(self)
#         self.pages["Team Summary"] = TeamSummaryPage(self)
#         # self.pages["Detailed Performance"] = DetailedPerformancePage(self)
#         # self.pages["Match Analysis"] = MatchAnalysisPage(self)

#         for page in self.pages.values():
#             page.pack(fill="both", expand=True)

#     def show_page(self, page_name):
#         # Cache toutes les pages et affiche seulement celle sélectionnée
#         for page in self.pages.values():
#             page.pack_forget()
#         self.pages[page_name].pack(fill="both", expand=True)

# if __name__ == "__main__":
#     app = App()
#     app.mainloop()

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CS2 Stats Aggregator")
        self.geometry("1600x900")

        ### Chargement des images de Maps ###
        ancient_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/ancient.png'), 30), size=(200,100))
        mirage_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/mirage.png'), 30), size=(200,100))
        nuke_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/nuke.png'), 30), size=(200,100))
        dust2_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/dust2.jpg'), 30), size=(200,100))
        anubis_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/anubis.png'), 30), size=(200,100))
        vertigo_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/vertigo.png'), 30), size=(200,100))

        
        # Créer un dictionnaire pour stocker les différentes pages
        self.pages = {}
        
        # Ajouter les pages dans le dictionnaire
        self.pages["home"] = HomePage()
        self.pages["team_summary"] = TeamSummaryPage()
        
        # Afficher la page d'accueil au démarrage
        self.show_page("home")
        
    def show_page(self, page_name):
        """Affiche la page souhaitée et cache les autres."""
        for name, page in self.pages.items():
            page.pack_forget()  # Cache toutes les pages
        
        page = self.pages[page_name]
        page.pack(fill="both", expand=True)
        
        # Ajouter des boutons de navigation dans chaque page
        self.add_navigation_buttons(page)
    
    def add_navigation_buttons(self, page):
        """Ajoute les boutons de navigation en haut de chaque page."""
        frame_header = ctk.CTkFrame(page)
        frame_header.pack(side="top", fill="x", pady=(10, 0))

        button_home = ctk.CTkButton(frame_header, text="Home", command=lambda: self.show_page("home"))
        button_home.pack(side="left", padx=(20, 10))

        button_team_summary = ctk.CTkButton(frame_header, text="Team Season Summary", command=lambda: self.show_page("team_summary"))
        button_team_summary.pack(side="left", padx=(10, 10))

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
