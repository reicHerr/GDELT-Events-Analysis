import os
import logging
from typing import Optional
from google.cloud import bigquery
from google.api_core import exceptions
from google.oauth2 import service_account
from functions.setup_authentication import setup_authentication

# Configuration du logging pour suivre les événements et erreurs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    )
logger = logging.getLogger(__name__)

def initialize_bigquery_client(
    project_id: str,
    credentials_path: Optional[str] = None,
    env_var: Optional[str] = None,
    auto_close: bool = False,
    ) -> bigquery.Client:
    """
    Initialise un client BigQuery pour le projet spécifié.

    Args:
        project_id (str): L'identifiant du projet Google Cloud.
        credentials_path (Optional[str]): Chemin vers le fichier JSON du compte de service.
        env_var (Optional[str]): Nom de la variable d'environnement à définir pour l'authentification.
        auto_close (bool): Si True, ferme le client en cas d'erreur. Si False, l'appelant doit le fermer.

    Returns:
        bigquery.Client: Une instance du client BigQuery.

    Raises:
        ValueError: Si project_id est vide ou invalide.
        FileNotFoundError: Si credentials_path est spécifié mais introuvable (via setup_authentication).
        PermissionError: Si le fichier de clé n'est pas lisible.
        RuntimeError: En cas d'erreur inattendue lors de l'initialisation.
    """
    # Validation de l'identifiant du projet
    if not project_id or not isinstance(project_id, str):
        logger.error("L'identifiant du projet doit être une chaîne non vide")
        raise ValueError("L'identifiant du projet doit être une chaîne non vide")

    client = None
    try:
        client_params = {"project": project_id, "location": "US"}
        if credentials_path:
            # Valider et configurer via setup_authentication
            setup_authentication(credentials_path, env_var)
            if not os.access(credentials_path, os.R_OK):
                logger.error("Fichier de clé %s non lisible", credentials_path)
                raise PermissionError(f"Fichier de clé {credentials_path} non lisible")
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            client_params["credentials"] = credentials
            logger.info("Utilisation des identifiants depuis %s", credentials_path)
        else:
            logger.info("Aucun identifiant explicite, utilisation des Application Default Credentials")

        # Initialisation du client
        client = bigquery.Client(**client_params)
        logger.info("Client BigQuery initialisé pour le projet %s", project_id)
        return client

    except exceptions.NotFound as e:
        logger.error("Projet %s introuvable ou accès refusé : %s", project_id, e)
        raise RuntimeError(f"Projet {project_id} introuvable ou accès refusé") from e
    except exceptions.Forbidden as e:
        logger.error("Erreur d'authentification pour %s : %s", project_id, e)
        raise RuntimeError("Erreur d'authentification, vérifiez vos identifiants") from e
    except exceptions.GoogleAPIError as e:
        logger.error("Erreur API BigQuery pour %s : %s", project_id, e)
        raise RuntimeError(f"Erreur API BigQuery : {e}") from e
    except Exception as e:
        logger.error("Erreur inattendue lors de l'initialisation pour %s : %s", project_id, e)
        raise RuntimeError(f"Échec de l'initialisation du client BigQuery : {e}") from e
    finally:
        if auto_close and client is not None and isinstance(client, bigquery.Client):
            try:
                client.close()
                logger.debug("Client BigQuery fermé automatiquement")
            except Exception as e:
                logger.warning("Erreur lors de la fermeture du client : %s", e)
