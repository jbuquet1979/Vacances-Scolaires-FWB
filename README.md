# 📅 Vacances Scolaires Fédération Wallonie-Bruxelles - Home Assistant

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/jbuquet1979/HACS-Vacances-Scolaires-FWB)](https://github.com/jbuquet1979/Vacances-Scolaires-FWB/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Composant personnalisé pour Home Assistant permettant d'intégrer automatiquement le calendrier officiel des vacances et congés scolaires de la **Fédération Wallonie-Bruxelles**.

---

## 🚀 Fonctionnalités

* 📅 **Intégration calendrier native** : Création d'une entité `calendar` entièrement compatible avec le tableau de bord et le moteur d'automatisation de Home Assistant.
* 🔄 **Mise à jour automatique** : Interroge dynamiquement l'année en cours et l'année suivante (rafraîchissement toutes les 12 heures).
* ⚙️ **Configuration via UI** : Installation simple via l'interface graphique (*Config Flow*) sans aucune modification du fichier `configuration.yaml`.
* ⚡ **Performance & Sobriété** : Utilise le `DataUpdateCoordinator` natif de Home Assistant sans requêtes superflues.

---

## 📦 Installation

### Option 1 : Via HACS (Recommandé)

1. Ouvrez **HACS** dans Home Assistant.
2. Cliquez sur les **3 petits points** en haut à droite, puis sur **Dépôts personnalisés**.
3. Ajoutez l'URL du dépôt : `[https://github.com/jbuquet1979/Vacances-Scolaires-FWB](https://github.com/jbuquet1979/Vacances-Scolaires-FWB)`
4. Sélectionnez la catégorie **Intégration**.
5. Cliquez sur **Ajouter**, recherchez **Vacances Scolaires FWB** dans HACS, puis cliquez sur **Télécharger**.
6. Redémarrez Home Assistant.

### Option 2 : Installation manuelle

1. Téléchargez le code source de la dernière version depuis la section **Releases**.
2. Copiez le dossier `custom_components/fwb_school_holidays` dans le répertoire `custom_components` de votre serveur Home Assistant.
3. Redémarrez Home Assistant.

---

## ⚙️ Configuration

1. Dans Home Assistant, allez dans **Paramètres** > **Appareils et services**.
2. Cliquez sur **Ajouter une intégration** en bas à droite.
3. Recherchez **Vacances Scolaires FWB**.
4. Validez le formulaire d'installation.

---

## 💡 Exemples d'automatisations

### 1. Activer le mode vacances sur le chauffage

Ajuste la température de consigne ou passe le thermostat en mode confort en journée lors des congés scolaires :

```yaml
alias: "Chauffage - Mode Congés FWB"
description: "Ajuste le chauffage en journée pendant les vacances scolaires"
trigger:
  - platform: state
    entity_id: calendar.vacances_scolaires_fwb
    to: "on"
action:
  - action: climate.set_preset_mode
    target:
      entity_id: climate.thermostat_salon
    data:
      preset_mode: "home"
```

### 2. Conditionner le réveil les jours de classe uniquement

Empêche le réveil automatique ou la routine matinale de se déclencher pendant les vacances scolaires :

```yaml
alias: "Réveil - Jours d'école uniquement"
trigger:
  - platform: time
    at: "06:45:00"
condition:
  - condition: time
    weekday:
      - mon
      - tue
      - wed
      - thu
      - fri
  - condition: state
    entity_id: calendar.vacances_scolaires_fwb
    state: "off"
action:
  - action: light.turn_on
    target:
      entity_id: light.chambre_parents
```

## 🌐 Source de données

Les données sont récupérées directement depuis l'API publique et gratuite [OpenHolidays API](https://openholidaysapi.org/), avec le paramètre de subdivision régionale `BE-WAL` et la langue française (`FR`).

---

## 📄 Licence

Ce projet est distribué sous la licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.