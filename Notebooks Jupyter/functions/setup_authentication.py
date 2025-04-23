import os
import logging
from typing import Optional

# Configuration du logging pour suivre les événements et erreurs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    )
logger = logging.getLogger(__name__)

def setup_authentication(
    key_path: str, 
    env_var: Optional[str] = None
    ) -> None:
    """
    Configure l'authentification Google Cloud en définissant une variable d'environnement.

    Vérifie l'existence du fichier de clé JSON spécifié et configure la variable
    d'environnement pour l'authentification des requêtes API Google (BigQuery, Storage, etc.).
    Si env_var est fourni, la variable d'environnement correspondante est définie.
    Si env_var est None, aucune variable d'environnement n'est modifiée.

    Args:
        key_path (str): Chemin absolu ou relatif vers le fichier de clé JSON du compte de service.
        env_var (Optional[str]): Nom de la variable d'environnement à définir (facultatif).

    Raises:
        ValueError: Si key_path est vide ou invalide.
        FileNotFoundError: Si le fichier de clé spécifié est introuvable.

    """
    # Validation du chemin
    if not key_path or not isinstance(key_path, str):
        logger.error("Le chemin du fichier de clé est vide ou invalide")
        raise ValueError("Le chemin du fichier de clé doit être une chaîne non vide")

    # Normalisation du chemin pour compatibilité multi-plateforme
    key_path = os.path.abspath(key_path)

    # Vérification de l'existence du fichier
    if not os.path.exists(key_path):
        logger.error("Fichier de clé introuvable : %s", key_path)
        raise FileNotFoundError(f"Fichier de clé introuvable : {key_path}")

    # Configuration de la variable d'environnement si spécifiée
    if env_var:
        os.environ[env_var] = key_path
        logger.info("Clé d'authentification chargée dans %s : %s", env_var, key_path)
    else:
        logger.info("Clé d'authentification validée : %s (aucune variable d'environnement définie)", key_path)
