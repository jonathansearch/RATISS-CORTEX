# AGENT.md — intégrer RATISS

Tu reçois ce dépôt. **L'algorithme de décision n'y est pas** : il te sera remis
séparément, avec la clé. Ce document te dit ce qui l'entoure.

## Ce que tu reçois ici

| fichier | à quoi il sert |
|---|---|
| `MODELES.md` | **les modèles à appeler**, identifiants exacts et mesures |
| `IDENTITE.md` | qui parle, et le prompt système exact à injecter |
| `HISTOIRE.md` | d'où vient ce cerveau, et les bugs qu'il a corrigés |
| `api/REFERENCE.md` | chaque fonction publique |
| `memoire/identite.json` | l'identité scellée, rechargeable |
| `verifier_attestation.py` | vérifier un document sans nous croire |

## Ce que tu ne reçois pas ici

- **L'algorithme de décision** (mode, modèle, budget, timeout) → remis à part.
- **La clé du canal.** Elle ne circule pas dans un dépôt. Jamais.

## Les quatre choses à ne pas rater

### ① L'identité s'injecte AVANT la demande

Le rôle `system` n'est pas décoratif : c'est ce qui fait que RATISS parle en
son nom au lieu de laisser un modèle répondre à sa place.

```json
{
  "model": "<identifiant exact de MODELES.md>",
  "messages": [
    {"role": "system", "content": "<le prompt de IDENTITE.md, tel quel>"},
    {"role": "user",   "content": "<la demande>"}
  ],
  "max_tokens": 1024,
  "temperature": 0.2,
  "stream": false
}
```

### ② `max_tokens` ne descend jamais sous 512

En dessous, les modèles de raisonnement consomment tout le budget en jetons
internes et renvoient `content: null` avec `finish_reason: length`. Ce n'est
pas une réponse vide : c'est un échec silencieux qui ressemble à une réponse.

### ③ Le timeout suit le budget, il ne le précède pas

```
timeout_s = max(15, max_tokens / débit_tok_s × 1.5)
```

2 048 jetons à 13,8 tok/s demandent 148 secondes. Couper à 45 s tue un modèle
qui allait répondre. Le timeout est un **plafond**, pas une attente : une
réponse courte revient en 563 ms.

### ④ Ne choisis jamais un modèle sur sa vitesse de premier jeton

`mistral-large` : **212 ms** de sonde — la meilleure du canal — et **32 380 ms**
de complétion. Trier là-dessus le place en tête de la voie rapide. Il a
timeouté en démonstration.

> La sonde mesure une politesse, pas un travail.

## Ce que tu dois produire, et dans quel ordre

1. **Décide** — applique l'algorithme reçu, il produit une décision motivée.
2. **Scelle la décision AVANT l'appel.** `sha256` du JSON canonique, clés
   triées, séparateurs compacts, UTF-8 :
   `json.dumps(corps, sort_keys=True, separators=(',',':'), ensure_ascii=False)`.
3. **Appelle** le modèle désigné par la décision, jamais un autre.
4. **Rattache l'exécution à la décision.** L'exécution porte le sceau de la
   décision qu'elle applique. Pas de sceau, pas de preuve.
5. **Atteste.** Quatre sceaux, une liaison, une dette de vérité déclarée.

## Vérifier un document sans nous croire

```bash
python3 verifier_attestation.py mon-attestation.json
```

Un fichier, zéro dépendance, zéro import de cortex. Code de retour : 0 conforme,
1 falsifié, 2 illisible. Il recalcule quatre sceaux et une liaison, hors ligne.

## Ce que tu ne fais jamais

- inventer un chiffre — s'il n'est pas mesuré, écris qu'il ne l'est pas ;
- donner un score de sécurité ou de confiance ;
- écrire « certifié » ;
- prétendre avoir signé ce que tu n'as pas signé ;
- exécuter une commande que tu n'as pas comprise.

---

*le cerveau décide, le LLM n'est qu'un outil qu'il appelle*
