import os
import logging
from datetime import datetime
from typing import Optional
import pandas as pd
from google.cloud import bigquery
from google.api_core import exceptions
from functions.initialize_client import initialize_bigquery_client

# Configuration du logging pour tracer les événements et erreurs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Limite maximale de taille des données à exporter (en Go)
MAX_DATA_SIZE_GB = 2  # Taille maximale des données en mémoire (modifiable)
MAX_DATA_SIZE_BYTES = MAX_DATA_SIZE_GB * 1024**3  # Conversion en octets

def extract_table(
    query: str,
    table_name: str,
    output_dir: str,
    client: Optional[bigquery.Client] = None,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
    env_var: Optional[str] = None,
    suffix_timestamp: bool = True,
    export_empty: bool = False,
    maximum_bytes_billed: Optional[int] = None,
    limit_bytes: bool = True,
) -> Optional[str]:
    """
    Exécute une requête BigQuery, récupère les résultats et les exporte en CSV localement.

    Args:
        query (str): Requête SQL à exécuter.
        table_name (str): Nom logique de la table ou du jeu de résultats.
        output_dir (str): Répertoire où enregistrer le fichier CSV.
        client (bigquery.Client, optional): Client BigQuery existant.
        project_id (str, optional): ID du projet GCP (si client non fourni).
        credentials_path (str, optional): Chemin vers un fichier JSON de credentials.
        env_var (str, optional): Nom de la variable d’environnement avec les credentials.
        suffix_timestamp (bool): Ajoute un timestamp au nom du fichier CSV.
        export_empty (bool): Si True, exporte un CSV vide même si aucun résultat.
        maximum_bytes_billed (int, optional): Limite de données scannées (facturation).
        limit_bytes (bool): Si True, limite la taille des données extraites à MAX_DATA_SIZE_GB.

    Returns:
        Optional[str]: Chemin du fichier CSV généré ou None si vide, trop lourd ou erreur.

    Raises:
        ValueError: Si les arguments query, table_name, output_dir ou project_id sont invalides.
        PermissionError: Si le dossier de sortie n’est pas accessible en écriture.
        RuntimeError: En cas d’erreur d’initialisation du client ou d’erreur API BigQuery.
    """
    # Vérification des arguments d’entrée pour éviter les erreurs
    if not query or not isinstance(query, str):
        raise ValueError("La requête SQL doit être une chaîne non vide")
    if not table_name or not isinstance(table_name, str):
        raise ValueError("Le nom de la table doit être une chaîne non vide")
    if not output_dir or not isinstance(output_dir, str):
        raise ValueError("Le dossier de sortie doit être une chaîne non vide")

    # Création du dossier de sortie s’il n’existe pas
    os.makedirs(output_dir, exist_ok=True)
    # Vérification des permissions d’écriture sur le dossier
    if not os.access(output_dir, os.W_OK):
        raise PermissionError(f"Pas de droits d’écriture dans le dossier : {output_dir}")

    # Initialisation du client BigQuery si non fourni
    if client is None:
        if not project_id or not isinstance(project_id, str):
            raise ValueError("L'identifiant du projet est requis si aucun client n'est fourni")
        try:
            # Utilisation de la fonction externe pour initialiser le client
            client = initialize_bigquery_client(
                project_id=project_id,
                credentials_path=credentials_path,
                env_var=env_var,
                auto_close=False
            )
        except Exception as e:
            logger.error("Échec de l'initialisation du client pour %s : %s", table_name, e)
            raise RuntimeError(f"Erreur d'initialisation du client : {e}") from e

    # Log du début de l’extraction
    logger.info("Début de l'extraction pour la table '%s'", table_name)

    # Construction du nom du fichier CSV avec un timestamp optionnel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if suffix_timestamp else ""
    output_file = os.path.join(output_dir, f"{table_name}{'_' + timestamp if timestamp else ''}.csv")

    try:
        # Configuration de la requête avec une limite de facturation optionnelle
        job_config = bigquery.QueryJobConfig()
        if maximum_bytes_billed is not None:
            job_config.maximum_bytes_billed = maximum_bytes_billed
            logger.info("Limite de facturation définie à %d octets", maximum_bytes_billed)

        # Exécution de la requête BigQuery
        query_job = client.query(query, job_config=job_config)
        # Conversion des résultats en DataFrame pandas (sans barre de progression)
        df = query_job.to_dataframe(progress_bar_type=None)

        # Log des octets facturés pour suivi
        bytes_billed = query_job.total_bytes_billed or 0
        logger.info("Octets facturés : %d", bytes_billed)

        # Vérification de la taille mémoire du DataFrame si limit_bytes est activé
        if limit_bytes:
            data_size = df.memory_usage(deep=True).sum()
            if data_size > MAX_DATA_SIZE_BYTES:
                logger.warning(
                    f"La taille des données ({data_size / 1024**3:.2f} Go) dépasse la limite fixée de {MAX_DATA_SIZE_GB} Go. "
                    "Exportation annulée !"
                )
                return None

        # Gestion des résultats vides
        if df.empty:
            logger.warning("La requête pour %s a retourné un résultat vide.", table_name)
            if not export_empty:
                logger.info("Aucun fichier CSV généré (export_empty=False).")
                return None
            logger.info("Un fichier CSV vide sera généré.")

        # Sauvegarde du DataFrame dans un fichier CSV (UTF-8, sans compression)
        df.to_csv(output_file, index=False, encoding="utf-8", compression=None)
        logger.info("Les données ont été exportées dans le fichier : %s", os.path.basename(output_file))
        logger.info("Nombre de lignes dans le fichier : %d", len(df))

        # Retour du chemin du fichier CSV généré
        return output_file

    except exceptions.Forbidden as e:
        # Gestion de l’erreur si maximum_bytes_billed est dépassé
        logger.error("Limite de facturation dépassée pour %s : %s", table_name, e)
        logger.info("Aucun fichier CSV généré en raison de la limite maximum_bytes_billed.")
        return None
    except exceptions.GoogleAPIError as e:
        # Gestion des erreurs API BigQuery génériques
        logger.error("Erreur API BigQuery pour %s : %s", table_name, e)
        raise RuntimeError(f"Erreur API BigQuery : {e}") from e
    except Exception as e:
        # Gestion des erreurs inattendues
        logger.error("Erreur inattendue lors de l'extraction de %s : %s", table_name, e)
        raise RuntimeError(f"Échec de l'extraction pour {table_name} : {e}") from e