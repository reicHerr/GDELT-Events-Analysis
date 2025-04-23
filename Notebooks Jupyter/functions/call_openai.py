import os
import logging
from typing import Optional
from openai import AzureOpenAI
from openai import APIError, AuthenticationError, RateLimitError, APIConnectionError

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def call_openai_api(
    prompt: str,
    max_tokens: int = 300,
    model: str = "gpt-4o-pionners10",
    api_version: str = "2024-05-01-preview"
) -> Optional[str]:
    """
    Appelle Azure OpenAI pour analyser un prompt (ex. identifier une thématique).

    Args:
        prompt (str): Texte à envoyer à l'API.
        max_tokens (int): Limite de tokens pour la réponse (défaut: 300).
        model (str): Modèle Azure OpenAI à utiliser (défaut: gpt-4o-pionners10).
        api_version (str): Version de l'API Azure OpenAI (défaut: 2024-05-01-preview).

    Returns:
        Optional[str]: Réponse de l'API ou message d'erreur.
    """
    # Validation des paramètres
    if not prompt or not isinstance(prompt, str):
        logger.error("Le prompt est vide ou invalide.")
        return "Erreur : Le prompt est vide ou invalide."
    if not isinstance(max_tokens, int) or max_tokens <= 0 or max_tokens > 4096:  # Limite typique pour GPT-4
        logger.error("max_tokens doit être un entier positif inférieur à 4096.")
        return "Erreur : max_tokens doit être un entier positif inférieur à 4096."

    
    # Charger les variables d'environnement
    api_key = "GJyIapLqFpG0FtWbxOyulHaHTm6Jto0YRN91YCLyiHQ7GTUkuGDMJQQJ99BCAC5T7U2XJ3w3AAABACOGo2Pg"
    azure_endpoint = "https://instancehackatonpionners01.openai.azure.com/"

    if not api_key:
        logger.error("Clé API manquante dans les variables d'environnement.")
        return "Erreur : La clé API est manquante. Configurez AZURE_OPENAI_API_KEY."

    # Validation de l'endpoint
    if not azure_endpoint.startswith("https://"):
        logger.error("L'endpoint Azure doit commencer par 'https://'.")
        return "Erreur : Endpoint Azure invalide."

    # Initialisation du client Azure OpenAI
    try:
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
    except ValueError as e:
        logger.error(f"Erreur d'initialisation du client : {str(e)}")
        return f"Erreur : Initialisation du client impossible ({str(e)})."

    # Appel de l'API
    try:
        logger.info("Appel de l'API Azure OpenAI avec le prompt : %s", prompt[:50])
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        result = response.choices[0].message.content
        logger.info("Réponse reçue : %s", result[:50])  # Log partiel de la réponse
        return result

    except AuthenticationError:
        logger.error("Erreur d'authentification : Vérifiez la clé API.")
        return "Erreur : Clé API invalide ou problème d'authentification."
    except RateLimitError:
        logger.error("Limite de taux dépassée.")
        return "Erreur : Limite de taux dépassée. Réessayez plus tard."
    except APIConnectionError:
        logger.error("Erreur de connexion à l'API.")
        return "Erreur : Impossible de se connecter à l'API Azure OpenAI."
    except APIError as e:
        logger.error(f"Erreur API : {str(e)}")
        return f"Erreur : Problème avec l'API Azure OpenAI ({str(e)})."
    except Exception as e:
        logger.error(f"Erreur inattendue : {str(e)}")
        return f"Erreur inattendue lors de l'appel à l'API : {str(e)}."