# Assurancetourix

Challenge WEB / API pour le HackDay 2024.

## Consigne

D'après nos informations, cette plateforme d'assurance est un facade utilisée par des espions
étrangers pour communiquer.

Trouvez des informations sur leur prochaine mission et devenez administrateur de la plateforme.

Les **fichiers** de configuration OpenAPI sont exposées.

<ins>Note (important)</ins>: il ne sera pas nécessaire de fuzz / énumérer / bruteforce le server web.

## Build / Run image

```bash
docker build --tag "insurance" . --no-cache
docker run -p 80:80 insurance
```