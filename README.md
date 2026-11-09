# RATISS CORTEX — dépôt de passation

Tu tiens le cerveau. Ce dossier te dit **comment le faire router, décider et
parler** sans lire son code source.

- **Qui parle** → [`IDENTITE.md`](IDENTITE.md)
- **D'où il vient** → [`HISTOIRE.md`](HISTOIRE.md)
- **Les modèles à appeler** → [`MODELES.md`](MODELES.md) ← identifiants exacts
- **L'API complète** → [`api/REFERENCE.md`](api/REFERENCE.md)
- **La procédure, pas à pas** → [`AGENT.md`](AGENT.md)
- **Son identité scellée** → [`memoire/identite.json`](memoire/identite.json)

> ⚠️ **L'algorithme de décision n'est pas dans ce dépôt.** Il est remis
> séparément, avec la clé. Ce dépôt dit *quoi* appeler, pas *comment choisir*.

## En trente secondes

```
demande ─▶ SENS ─▶ CORTEX ─▶ RÉFLEXE ? ─▶ EXÉCUTEUR ─▶ MÉMOIRE ─▶ ATTESTATION
            │        │          │
       mesure la   choisit    geste appris
         forme     la voie    (zéro réseau)
```

Le cerveau **décide** : mode, modèle, budget, timeout. Le LLM **exécute**.
Ce n'est pas une nuance de vocabulaire — c'est la seule façon d'empêcher un
modèle d'écrire un verdict.

## Les trois chiffres à retenir

| | |
|---|---|
| **148** | tests, zéro réseau, 0,5 s |
| **7** | modèles écartés, chacun avec son motif écrit |
| **4** | modes de décision, 7 règles publiques et ordonnées |

## Ce que ce dépôt n'est pas

Pas de serveur, pas de REST, pas de PWA, pas de frontend. Une bibliothèque.
Pas de score de sécurité, pas de score de confiance, pas de « certification ».
Pas de clé privée : le sceau prouve l'intégrité, **pas l'identité de l'émetteur**.

## Vérifier sans nous croire

```bash
python3 verifier_attestation.py une-attestation.json
```

Un fichier, zéro dépendance, zéro import de cortex. Il recalcule quatre sceaux
et une liaison. Code de retour 0 = conforme, 1 = falsifié, 2 = illisible.

---

*le cerveau décide, le LLM n'est qu'un outil qu'il appelle*

*Sceau de l'identité : `e85cf175afd3dd261de7eca41a283a4abda08d2cd27dbf45ba5d5b61d549b2d6`*
