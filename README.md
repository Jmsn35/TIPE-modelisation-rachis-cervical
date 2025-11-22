# Simulation d'Impact et Analyse des Commotions Cérébrales

## Description

Ce projet de recherche (TIPE) propose une modélisation biomécanique du rachis cervical et du crâne pour analyser les mécanismes des commotions cérébrales lors d'impacts latéraux. L'objectif est de mieux comprendre les risques associés aux chocs dans les sports de contact (boxe, rugby, équitation) afin d'améliorer la prévention.

## Objectifs

- Modéliser le comportement dynamique de la tête et du rachis cervical lors d'un impact latéral
- Analyser les trajectoires, vitesses et accélérations selon différents points d'impact
- Comparer les résultats de simulation avec des données expérimentales et des études biomécaniques publiées
- Identifier les seuils critiques d'accélération pouvant provoquer des commotions cérébrales

## 🛠️ Technologies Utilisées

- **Python** : Langage de programmation principal
- **Pygame** : Visualisation en temps réel de la simulation
- **Pymunk** : Moteur physique 2D pour la simulation de la dynamique des corps rigides et des collisions

## Modélisation Biomécanique

### Composants du modèle

**Crâne**
- Masse : 5 kg
- Dimensions : 25 cm × 15 cm
- Modélisé comme un solide indéformable

**Vertèbres cervicales (C1-C7)**
- Masse unitaire : 50 g
- Liaisons pivot avec contraintes angulaires
- Débattement : 20° (crâne-C1, C1-C2) et 40° (C2-C7)

**Muscles cervicaux**
- Modélisés par des ressorts amortis
- Raideur : 5000 N/m
- Amortissement : 100 N·s/m
- Muscles simulés : sternocléidomastoïdiens, trapèze, splenius, scalènes

**Impact (poing)**
- Masse : 15 kg
- Vitesse : 10 m/s
- Rayon : 4 cm

## Résultats Clés

### Points d'impact testés
1. **Haut de la tête** : Accélérations maximales extrêmes
2. **Milieu de la tête** : Accélérations élevées
3. **Bas de la tête (menton)** : Comportement dynamique distinct

### Comparaison avec données réelles
- Les accélérations simulées atteignent environ **600-700 m/s²**
- Cohérence avec les données de boxe olympique : **58g ± 13g** (≈ 568 m/s²)
- Validation du modèle par rapport aux seuils critiques de commotion cérébrale

## Méthodologie

1. **Simplifications assumées** : Mouvement d'inclinaison latérale uniquement, liaisons pivot entre vertèbres
2. **Paramètres physiques réalistes** : Masses, dimensions et propriétés mécaniques basées sur des données anatomiques
3. **Échelle de simulation** : 1 cm = 10 pixels, avec conversion appropriée des unités physiques
4. **Validation expérimentale** : Modèle physique construit et testé avec un système de pendule

## Applications Potentielles

- Conception d'équipements de protection améliorés (casques)
- Évaluation des risques dans les sports de contact
- Développement de protocoles de prévention des commotions
- Sensibilisation aux mécanismes des traumatismes crâniens

## Utilisation

```bash
# Cloner le repository
git clone https://github.com/[votre-username]/cervical-impact-simulation.git

# Installer les dépendances
pip install pygame pymunk

# Lancer la simulation
python main.py
```

## 📝 Structure du Projet

```
├── main.py                 # Programme principal de simulation
├── models/
│   ├── vertebrae.py       # Modèle des vertèbres cervicales
│   ├── skull.py           # Modèle du crâne
│   ├── muscles.py         # Modèle des muscles (ressorts)
│   └── impact.py          # Modèle de l'impact (poing)
├── simulation/
│   ├── physics_engine.py  # Configuration du moteur physique
│   └── visualization.py   # Interface de visualisation
├── data/
│   └── experimental_data/ # Données expérimentales
└── results/
    └── analysis/          # Résultats et graphiques
```

## Références

- Walilko TJ, Viano DC, Bir CA. *Biomechanics of the head for Olympic boxer punches to the face*
- Données anatomiques sur le rachis cervical et la biomécanique musculaire
- Documentation Pymunk et Pygame

## Auteur

**Jameson Prat** - TIPE 51161

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

