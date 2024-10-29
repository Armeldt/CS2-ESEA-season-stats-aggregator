import customtkinter as ctk
from Home_page import HomePage
from Team_summary_page import TeamSummaryPage
# from detailed_performance_page import DetailedPerformancePage
# from match_analysis_page import MatchAnalysisPage

ctk.set_appearance_mode('dark')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CS2 Stats Aggregator")
        self.geometry("1600x900")

        # Dictionnaire des pages
        self.pages = {}
        self.create_pages()

        # Affiche la première page
        self.show_page("Home")

    def create_pages(self):
        self.pages["Home"] = HomePage(self)
        self.pages["Team Summary"] = TeamSummaryPage(self)
        # self.pages["Detailed Performance"] = DetailedPerformancePage(self)
        # self.pages["Match Analysis"] = MatchAnalysisPage(self)

        for page in self.pages.values():
            page.pack(fill="both", expand=True)

    def show_page(self, page_name):
        # Cache toutes les pages et affiche seulement celle sélectionnée
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
