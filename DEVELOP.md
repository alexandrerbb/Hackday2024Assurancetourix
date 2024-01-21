# Developpement

```bash
uvicorn insurance.main:app --reload

cd frontend && npm run dev
```

## Note sur les références cycliques.

L'emploi de references cycliques dans le code peut poser problème à plusieurs endroits :

- **Au niveau de l'ORM** : Il y a un problèmes avec les foreign keys cycliques lors de la génération
  des tables avec _Tortoise_. voir
  [cette issue](https://github.com/tortoise/tortoise-orm/issues/379).

- **Au niveau du SGBD.**

### Fix local pour Tortoise

Suffisant pour travailler avec SQLite.

Modifier le fichier `tortoise\backends\base\schema_generator.py`.

```python
try:
    next_table_for_create = next(
        t
        for t in tables_to_create
        # if t["references"].issubset(created_tables | {t["table"]}) # <<< Commenter cette ligne (435)
    )
except StopIteration:
    raise ConfigurationError("Can't create schema due to cyclic fk references")
```

