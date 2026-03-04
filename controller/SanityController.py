from pathlib import Path

from src import SanityTree, DocxUpdater

class SanityController:
    """
    Handles the logic between the SanityTree, DocxUpdater classes and the GUI.
    """
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.sanity_tree = SanityTree(base_path)
        self.updater = DocxUpdater(Path(self.base_path) / "Sanity")

    def create_sanity_tree(self):
        """
        Creates instance of SanityTree and corresponding folder
        """

        self.sanity_tree.new_master_dir()

    def process_screen_folders(self):
        """
        Mediates the copypasting of Sanity screenshots in the corresponding Master.docx files.
        """
        self.updater.process_folders()

