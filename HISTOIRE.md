# HISTOIRE.md — d'où il vient

Chaque étape porte un chiffre mesuré, pas une promesse.

## v0.1.0 — le cœur

SENS mesure la forme, CORTEX décide, la MÉMOIRE chaîne, la VOLONTÉ interdit les transitions illégales.

`37 tests`

## v0.2.0 — la mémoire durable

Le DÉPÔT écrit de façon atomique et vérifie trois fois au chargement. Les ancres permettent d'oublier sans perdre la preuve. La consolidation promeut ce qui revient.

`72 tests`

## v0.3.0 — le bras

L'EXÉCUTEUR applique la décision d'un autre. Un transport injectable, zéro réseau implicite, un sceau qui dit quelle décision a été appliquée.

`99 tests`

## v0.4.0 — les gestes et le document

Les RÉFLEXES n'apprennent que des succès stables, et se taisent quand le cerveau change d'avis. L'ATTESTATION sort chaque échange en preuve vérifiable hors ligne, par un fichier qui n'importe rien de moi.

`148 tests`

## v0.5.0 — l'identité et la passation

RATISS a une histoire, une doctrine et une voix, scellées dans sa mémoire et injectées avant chaque réponse : il parle en son nom au lieu de laisser un modèle parler à sa place. Le dépôt de passation sort tout ce qu'un agent doit savoir pour router, sans lire le code.

`182 tests`

---

## Les sept bugs que ce travail a trouvés

Tous réels, tous corrigés, tous verrouillés par un test qui porte leur nom.

| # | bug | conséquence |
|---|---|---|
| 1 | `memoire or Memoire()` | mémoire vide *fausse* ⇒ la mémoire injectée jetée |
| 2 | double `Etat.SCELLE` | `Refus R04` sur toute vérification obligatoire |
| 3 | `SCELLE` sans sortie | **le cerveau ne pensait qu'une fois** |
| 4 | compteur anti-boucle global | 30 pensées ⇒ `R03_boucle_infinie` |
| 5 | `agir()` persistait après coup | **l'exécution perdue au redémarrage** |
| 6 | `REFUS` terminal | **un seul refus tuait le cerveau** |
| 7 | décision scellée sur un résumé | **son sceau ne se recalculait pas** |

Les n° 3, 6 et 7 sont la même famille : *un état sans sortie*. Le n° 7 est
le plus grave — il dormait depuis la v0.1 et rendait toute attestation
impossible. C'est l'attestation qui l'a débusqué : **exiger qu'un document
se recalcule oblige à vérifier que tout le reste le fasse aussi.**
