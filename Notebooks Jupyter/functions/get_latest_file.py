import os
import glob
from typing import Optional

def get_latest_file_by_keyword(
    keyword: str, 
    directory: str, 
    extension: str
    ) -> Optional[str]:
    """
    Recherche le fichier le plus récent dans un dossier contenant un mot-clé et une extension donnée.

    Args:
        keyword (str): Mot-clé à chercher dans les noms de fichiers.
        directory (str): Dossier dans lequel chercher les fichiers.
        extension (str): Extension de fichier à filtrer (ex: '.csv', '.json').

    Returns:
        Optional[str]: Chemin du fichier le plus récent, ou None si aucun fichier trouvé.

    Raises:
        ValueError: Si le mot-clé ou l'extension est invalide.
        NotADirectoryError: Si le dossier n’existe pas.
        PermissionError: Si le dossier n’est pas accessible.
    """
    # Vérification des paramètres
    if not keyword or not isinstance(keyword, str):
        raise ValueError("Le mot-clé doit être une chaîne non vide.")

    if not extension or not extension.startswith("."):
        raise ValueError("L'extension doit commencer par un point (ex: '.csv', '.json').")

    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Le dossier spécifié n'existe pas : {directory}")

    if not os.access(directory, os.R_OK):
        raise PermissionError(f"Dossier non lisible : {directory}")

    # Recherche du fichier dans le dossier indiqué
    pattern = os.path.join(directory, f"*{keyword}*{extension}")
    matching_files = glob.glob(pattern)

    if not matching_files:
        print(f" Aucun fichier trouvé contenant '{keyword}' avec l'extension '{extension}' dans {directory}")
        return None  
    
    # Recuperation du fichier le plus récent
    latest_file = max(matching_files, key=os.path.getmtime)
    print(f" Fichier le plus récent trouvé dans {directory} pour '{keyword}' : {os.path.basename(latest_file)}")
    return os.path.basename(latest_file)
