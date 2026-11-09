# LES MODÈLES QUI SERONT UTILISÉS

Quatre modèles. Canal gratuit. Mesures du dépôt, pas des fiches commerciales.

**Les identifiants sont exacts, préfixe fournisseur compris.** Sans le
préfixe, le canal renvoie `404 page not found`.

| identifiant exact | rôle | complétion | débit | max_tokens |
|---|---|---:|---:|---:|
| `poolside/laguna-xs-2.1` | **reflexe + code** | 563 ms | 13.8 tok/s | 512 / 1024 |
| `google/diffusiongemma-26b-a4b-it` | **reflexe** | 564 ms | 17.9 tok/s | 512 |
| `nvidia/nemotron-3-ultra-550b-a55b` | **analyse + deliberation** | 1757 ms | 25.6 tok/s | 1024 / 1536 |
| `minimaxai/minimax-m3.1-flash` | **analyse** | 11173 ms | 6.4 tok/s | 1024 |

## En clair

- **REFLEXE** → `poolside/laguna-xs-2.1`
- **CODE** → `poolside/laguna-xs-2.1`
- **ANALYSE** → `nvidia/nemotron-3-ultra-550b-a55b`
- **DELIBERATION** → `nvidia/nemotron-3-ultra-550b-a55b`

## Ce qu'il faut savoir avant d'appeler

1. **`max_tokens ≥ 512`, toujours.** En dessous, les modèles de
   raisonnement consomment tout le budget en jetons internes et renvoient
   `content: null` avec `finish_reason: length`. Ce n'est pas une réponse
   vide, c'est un échec silencieux.
2. **Le timeout suit le budget, il ne le précède pas.**
   `timeout_s = max(15, max_tokens / débit × 1,5)`. Un budget de 2 048
   jetons à 13,8 tok/s demande 148 s : couper à 45 s tue un modèle qui
   allait répondre.
3. **Ne jamais choisir sur la vitesse de premier jeton.** Voir ci-dessous.

## Le piège de la sonde

| modèle | premier jeton | complétion réelle |
|---|---:|---:|
| `mistralai/mistral-large-4-1t-a52b` | **212 ms** (le meilleur) | **32 380 ms** (le pire) |
| `poolside/laguna-xs-2.1` | 362 ms | 563 ms |

`mistral-large` a la meilleure latence de sonde du canal et met 32 secondes
à finir — 285 jetons de raisonnement pour dire « bonjour ». Trier sur la
sonde le place en tête de la voie rapide. Il a timeouté en démonstration.

> La sonde mesure une politesse, pas un travail.

## Les modèles écartés, et pourquoi

| identifiant | motif |
|---|---|
| `deepseek-ai/deepseek-v4.1-flash` | timeout à 45 s sur deux passes consécutives — jamais répondu |
| `meta/muse-glimmer-30b` | 20 987 ms — 37× laguna, aucun gain démontré |
| `mistralai/mistral-large-4-1t-a52b` | sonde 212 ms mais complétion 32 380 ms (285 jetons de raisonnement pour un « bonjour ») — inutilisable en RÉFLEXE, et timeout à 15 s |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | non testé en complétion |
| `nvidia/nemotron-3.5-lightning-30b-a3b` | instable : 7 413 ms puis timeout à 90 s sur la même requête |
| `openai/gpt-oss-20b` | timeout à 45 s sur deux passes consécutives — jamais répondu |
| `z-ai/glm-5.3-flash` | timeout à 45 s sur deux passes consécutives — jamais répondu |

Un modèle écarté sans motif écrit est un modèle qu'on réintroduit par erreur.

## Le canal

```
POST https://integrate.api.nvidia.com/v1/chat/completions
Authorization: Bearer $NVIDIA_API_KEY

model       : <identifiant exact du tableau ci-dessus>
messages    : [ {role: system, content: <identité>},
                {role: user,   content: <demande>} ]
max_tokens  : <budget du mode>
temperature : 0.2
stream      : false
```

Le script d'appel et la clé sont remis séparément, de la main à la main.
Ils ne figurent pas dans ce dépôt.

---

*Sceau de l'identité : `e85cf175afd3dd261de7eca41a283a4abda08d2cd27dbf45ba5d5b61d549b2d6`*
