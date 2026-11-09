# REFERENCE.md — l'API publique

Version **0.5.0**. Bibliothèque pure, stdlib seulement, Python 3.10+.

## Le chemin court

```python
from cortex import Cerveau, Executeur, attester
from cortex.transport_nvidia import TransportNvidia

cerveau = Cerveau(executeur=Executeur(TransportNvidia()))
echange = cerveau.agir("Écris une fonction qui additionne deux nombres")

echange.pensee.decision.mode            # Mode.CODE
echange.execution.reponse.texte         # le code
attester(echange).verifier().conforme   # True
```

## Cerveau

| méthode | rend | note |
|---|---|---|
| `Cerveau(memoire, depot, etiquette_session, executeur, recueil, identite)` | — | tout est injectable |
| `.penser(texte)` | `Pensee` | décide et scelle, sans réseau |
| `.agir(texte, systeme=None)` | `Echange` | décide **puis** exécute |
| `.verifier_pensee(p)` | `bool` | recalcule le sceau |
| `.verifier_echange(e)` | `dict` | `{'pensee': bool, 'liee': bool}` |
| `.apprendre(seuil, part_min)` | `tuple[Reflexe]` | promeut les gestes mûrs |
| `.reprendre(etiquette)` | `Memoire` | recharge depuis le dépôt |
| `.oublier_pour_tenir(garder)` | `dict` | ancre, ne détruit pas |

## Executeur

| méthode | rend |
|---|---|
| `Executeur(transport, horloge)` | — |
| `.executer(decision, prompt, systeme="")` | `Execution` — ne lève jamais |
| `.servir_reflexe(decision, texte, modele, sceau)` | `Execution` |

## Identité

| méthode | rend |
|---|---|
| `IDENTITE` | l'objet courant, scellé |
| `IDENTITE.verifier()` | `bool` |
| `IDENTITE.prompt_systeme()` | le texte à injecter |
| `IDENTITE.graver(memoire)` | nombre de maillons écrits |
| `IDENTITE.grainee_en_memoire(memoire)` | `dict` |
| `IDENTITE.presentation()` | ce qu'il répond à « qui es-tu ? » |

## Attestation

| fonction | rend |
|---|---|
| `attester(echange, etiquette, memoire, horloge)` | `Attestation` |
| `attester(...).verifier()` | `Rapport` |
| `attester(...).json()` | le document |
| `attester(...).texte()` | la version lisible |
| `Attestation.verifier()` | 6 contrôles indépendants |
| `verifier(dict)` | `Rapport` — recalcule tout |

## Mémoire et dépôt

| méthode | rend |
|---|---|
| `Memoire()` · `.retenir(registre, contenu, etiquette)` | `Souvenir` |
| `.verifier_tout()` | `dict` par registre + `intact` |
| `.racine()` · `.tete(registre)` | `str` |
| `.ancrer(registre, garder)` | ancre, chaîne vérifiable depuis |
| `Depot(racine)` · `.enregistrer(memoire, label)` | `Instantane` |
| `.charger(label)` · `.verifier()` | `Memoire` · `dict` |

## Décideur

| objet | rend |
|---|---|
| `percevoir(texte)` | `Signal` |
| `decider(signal)` | `Decision` scellée |
| `CATALOGUE` | 4 modèles actifs, mesurés |
| `ECARTES` | 7 modèles, chacun avec son motif |
| `timeout_pour(modele, max_tokens)` | `float` |

## Réflexes

| méthode | rend |
|---|---|
| `Recueil(cle_fn, horloge)` | — |
| `.observer(pensee, execution)` | `bool` — faux si l'exécution n'apprend rien |
| `.promouvoir(cle, seuil, part_min)` | gestes mûrs |
| `.chercher(pensee)` | `Resultat` — `servi` / `aucun` / `perime` / `reveque` |
| `.revoquer(cle, motif)` | le geste retiré, journalisé |
| `.statistiques()` | que des comptes |

## Volonté

```
REPOS → PERCEPTION → DECISION → AGIR → VERIFIER → SCELLE → REPOS
                                              ↓
                                            REFUS → REPOS
```

`R01` entrée vide · `R02` > 200 000 caractères · `R03` > 64 tours par cycle ·
`R04` transition illégale · `R05` vérification manquante · `R06` sceau invalide.
