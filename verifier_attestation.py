#!/usr/bin/env python3
"""VÉRIFICATEUR D'ATTESTATION RATISS — un fichier, zéro dépendance.

Ce script ne connaît pas RATISS. Il n'importe rien du paquet. Il lit un JSON,
recalcule quatre sceaux et une liaison, et affiche le résultat.

    python3 verifier_attestation.py mon-attestation.json
    python3 verifier_attestation.py mon-attestation.json --json

Code de retour : 0 si conforme, 1 sinon, 2 si le fichier est illisible.

Le protocole tient en une ligne : chaque sceau est
    sha256( json.dumps(corps, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False).encode("utf-8") ).hexdigest()
où ``corps`` est l'objet privé de sa clé « sceau ».

Aucune connexion réseau. Aucune installation. Aucune confiance requise.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

FORMAT = "ratiss-attestation/1"


def canonique(objet):
    return json.dumps(
        objet, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sceau_de(corps):
    return hashlib.sha256(canonique(corps)).hexdigest()


def sans_cle(d, cle="sceau"):
    return {k: v for k, v in d.items() if k != cle}


def verifier(attestation):
    """Recalcule tout. Ne croit rien de ce qui est écrit."""
    motifs = []
    controles = {}

    controles["sceau_attestation"] = attestation.get("sceau", "") == sceau_de(
        sans_cle(attestation)
    )
    if not controles["sceau_attestation"]:
        motifs.append("sceau de l'attestation : recalculé différent")

    if attestation.get("format") != FORMAT:
        motifs.append("format inattendu : %r" % (attestation.get("format"),))

    echange = attestation.get("echange") or {}
    pensee = echange.get("pensee") or {}
    decision = pensee.get("decision") or {}
    execution = echange.get("execution") or {}

    if not pensee:
        motifs.append("aucune pensée dans l'attestation")
    if not execution:
        motifs.append("aucune exécution dans l'attestation")

    controles["sceau_pensee"] = bool(pensee) and pensee.get("sceau", "") == sceau_de(
        sans_cle(pensee)
    )
    if pensee and not controles["sceau_pensee"]:
        motifs.append("sceau de la pensée : recalculé différent")

    controles["sceau_decision"] = bool(decision) and decision.get(
        "sceau", ""
    ) == sceau_de(sans_cle(decision))
    if decision and not controles["sceau_decision"]:
        motifs.append("sceau de la décision : recalculé différent")

    controles["sceau_execution"] = bool(execution) and execution.get(
        "sceau", ""
    ) == sceau_de(sans_cle(execution))
    if execution and not controles["sceau_execution"]:
        motifs.append("sceau de l'exécution : recalculé différent")

    liaison = bool(decision.get("sceau")) and (
        execution.get("sceau_decision") == decision.get("sceau")
    )
    controles["liaison"] = liaison
    if not liaison:
        motifs.append(
            "liaison rompue : l'exécution cite une décision qui n'est pas celle-ci"
        )

    controles["coherence_declaree"] = echange.get("coherent") is liaison
    if not controles["coherence_declaree"]:
        motifs.append(
            "cohérence déclarée (%r) contredite par le recalcul (%r)"
            % (echange.get("coherent"), liaison)
        )

    controles["conforme"] = all(controles.values())
    controles["motifs"] = motifs
    return controles


def resume(attestation, controles):
    e = attestation.get("echange") or {}
    p = e.get("pensee") or {}
    d = p.get("decision") or {}
    x = e.get("execution") or {}

    largeur = 62
    lignes = [
        "VÉRIFICATION D'ATTESTATION RATISS",
        "=" * largeur,
        "fichier        %s" % attestation.get("_fichier", "—"),
        "format         %s" % attestation.get("format", "—"),
        "",
        "demande        %s" % (p.get("signal", {}).get("texte", "—")[:80]),
        "mode décidé    %s" % d.get("mode", "—"),
        "modèle         %s" % (d.get("modele", {}) or {}).get("id", "—"),
        "statut bras    %s" % x.get("statut", "—"),
        "",
        "-" * largeur,
    ]
    for cle in (
        "sceau_attestation",
        "sceau_pensee",
        "sceau_decision",
        "sceau_execution",
        "liaison",
        "coherence_declaree",
    ):
        lignes.append("  %-20s %s" % (cle, "OK" if controles[cle] else "ÉCHEC"))

    lignes.append("-" * largeur)
    for motif in controles["motifs"]:
        lignes.append("  ! %s" % motif)

    lignes += [
        "",
        "RÉSULTAT : %s" % ("CONFORME" if controles["conforme"] else "NON CONFORME"),
        "",
        "Ce document prouve l'intégrité et la cohérence interne.",
        "Il ne prouve pas que la réponse est vraie.",
    ]
    return "\n".join(lignes)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    en_json = "--json" in argv

    if not args:
        print(__doc__)
        return 2

    chemin = Path(args[0])
    try:
        attestation = json.loads(chemin.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("fichier introuvable : %s" % chemin, file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print("JSON illisible (%s ligne %d)" % (exc.msg, exc.lineno), file=sys.stderr)
        return 2

    controles = verifier(attestation)

    if en_json:
        print(json.dumps(controles, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        attestation["_fichier"] = str(chemin)
        print(resume(attestation, controles))

    return 0 if controles["conforme"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
