# Formalisation du Problème d'Optimisation d'Infrastructure IA

## 1. Contexte Général
L'application d'IA est structurée comme un pipeline de 4 micro-services :
1. **Pre-processing**
2. **Model Worker**
3. **Parameter Server**
4. **Evaluator**



## 2. Modélisation Mathématique

### Variables de décision
Pour chaque micro-service $i \in \{1, 2, 3, 4\}$ et chaque type de VM $j \in \{1, \dots, 17\}$ :
* $r_i \in \mathbb{N}$ : Nombre de réplicas (instances) du service $i$.
* $y_j \in \mathbb{N}$ : Nombre de VMs de type $j$ utilisées.
* $x_{ij} \in \mathbb{N}$ : Nombre d’instances du service $i$ placées sur les VMs de type $j$.

### Paramètres
* $\lambda(t)$ : Demande en requêtes par seconde (RPS) à l'instant $t$.
* $\mu_i$ : Capacité de traitement unitaire d'un réplica du service $i$ (RPS).
* $cpu_i, ram_i$ : Ressources requises par une instance du service $i$.
* $CPU_j, RAM_j$ : Capacité totale de la VM de type $j$.
* $C_j$ : Coût horaire de la VM de type $j$.
* $Stock_j$ : Nombre maximal de VMs disponibles pour le type $j$.

---

## 3. Contraintes

### 3.1. Stabilité et Capacité
Chaque étape du pipeline doit absorber le flux entrant pour éviter la saturation.

* **Niveau 1 (Statique) :**
  $$r_i \cdot \mu_i \ge \lambda_{max} \quad \forall i$$

* **Niveau 2 (Robuste) :**
  $$r_i \cdot \mu_i \ge \lambda(t) \quad \text{pour une proportion donnée des } t$$

### 3.2. Cohérence du placement
Le déploiement physique doit correspondre au nombre de réplicas décidés :
$$\sum_{j} x_{ij} = r_i \quad \forall i$$

### 3.3. Limites des Ressources Physiques (Bin Packing)
Pour chaque VM, la somme des ressources consommées ne doit pas excéder sa capacité :
* **CPU :** $\sum_{i} x_{ij} \cdot cpu_i \le y_j \cdot CPU_j \quad \forall j$
* **RAM :** $\sum_{i} x_{ij} \cdot ram_i \le y_j \cdot RAM_j \quad \forall j$

### 3.4. Disponibilité infrastructurelle
$$0 \le y_j \le Stock_j \quad \forall j$$

---

## 4. Fonctions Objectifs

### Niveaux 1 & 2 : Minimisation du coût
L'objectif est de réduire les dépenses opérationnelles (OPEX) :
$$\min \sum_{j} y_j \cdot C_j$$

### Niveau 3 : Compromis Coût / Performance
En intégrant la latence via l'approximation $T_i(t) \approx \frac{1}{(r_i \cdot \mu_i) - \lambda(t)}$, on cherche à minimiser :
$$\min \quad \alpha \cdot \left(\sum_j y_j C_j\right) + \beta \cdot \overline{T}$$
*Où $\overline{T}$ est la latence moyenne et $\alpha, \beta$ sont les coefficients de pondération.*

---

## 5. Pistes d'Implémentation Algorithmique

### Modèle 1 : Heuristique Gloutonne (Baseline)
* **Étape 1 :** Calcul de $r_i = \lceil \lambda / \mu_i \rceil$.
* **Étape 2 :** Tri des VMs par ratio coût/ressources et placement via *First-Fit*.
* **Justification :** Simple à coder, fournit une solution de référence immédiate.

### Modèle 2 : Recherche Locale (Hill Climbing / Recuit Simulé)
* **Principe :** Partir de la solution gloutonne et explorer des voisins (ajouter/enlever un réplica, changer une VM).
* **Justification :** Permet de sortir des optima locaux et d'améliorer le coût global de l'infrastructure.

### Modèle 3 : Recherche Informée (A*)
* **Principe :** Exploration d'un arbre d'états où chaque nœud est une configuration de réplicas, guidée par une fonction de coût estimée.
* **Justification :** Approche plus rigoureuse mathématiquement pour garantir une qualité de solution supérieure.