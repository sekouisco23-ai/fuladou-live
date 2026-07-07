# 🎵 Fuladou Live – Plateforme intelligente de réservation d'artistes

## 📖 Présentation

Fuladou Live est une plateforme numérique conçue pour simplifier et moderniser la réservation d'artistes pour tous types d'événements (mariages, baptêmes, concerts, cérémonies, événements culturels, etc.).

Le projet automatise l'ensemble du processus de réservation, depuis la demande du client jusqu'à la génération d'une affiche personnalisée après validation de la réservation.

L'objectif est d'offrir une solution simple, rapide et professionnelle aux artistes tout en améliorant l'expérience des organisateurs d'événements.

---

# 🚀 Fonctionnalités principales

- Création de réservations en ligne
- Vérification automatique des disponibilités
- Gestion des statuts (En attente, Confirmée, Refusée)
- Refus automatique des demandes en conflit sur une même date
- Génération automatique d'affiches promotionnelles
- Interface utilisateur moderne développée avec Lovable
- API Backend développée avec Flask
- Stockage des réservations
- Notification automatique de l'artiste
- Architecture évolutive permettant l'intégration future de services SMS, WhatsApp et paiements en ligne

---

# 🛠️ Technologies utilisées

## Frontend
- Lovable

## Backend
- Python
- Flask

## Traitement d'image
- Pillow

## Stockage
- JSON
- (Migration prévue vers SQLite ou PostgreSQL)

## API
- REST API

---

# ⚙️ Fonctionnement

Le fonctionnement de la plateforme est entièrement automatisé :

1. Le client effectue une demande de réservation.
2. Les informations sont transmises au backend Flask.
3. La disponibilité de la date est vérifiée.
4. La réservation est enregistrée avec le statut **En attente**.
5. Une notification est envoyée à l'artiste.
6. Après validation, la réservation passe au statut **Confirmée**.
7. Les éventuelles réservations concurrentes sur la même date sont automatiquement refusées.
8. Une affiche personnalisée est générée automatiquement.

# 🎯 Impact

Fuladou Live est né d'un constat simple : dans le Fouladou, et plus largement dans la région de Kolda, la gestion des réservations d'artistes repose encore majoritairement sur des appels téléphoniques, des messages WhatsApp et des échanges informels. Cette organisation entraîne fréquemment des conflits de dates, des pertes d'informations, des annulations de dernière minute et une charge administrative importante pour les artistes.

En proposant une plateforme numérique centralisée, Fuladou Live ambitionne de moderniser cette organisation en offrant un processus de réservation simple, transparent et automatisé.

Au-delà de l'aspect technique, le projet répond à plusieurs enjeux locaux :

- Faciliter l'accès aux artistes du Fouladou pour les particuliers, les associations, les collectivités et les organisateurs d'événements.
- Réduire les erreurs de planification grâce à une gestion intelligente des disponibilités.
- Valoriser le professionnalisme des artistes en automatisant les confirmations, les notifications et la création de supports de communication.
- Renforcer la visibilité des talents culturels de Kolda grâce à une présence numérique moderne.
- Encourager la transformation numérique du secteur culturel local en mettant les technologies au service des acteurs de terrain.

L'automatisation des tâches administratives permet aux artistes de consacrer davantage de temps à la création, aux répétitions et aux performances, tout en améliorant la qualité du service offert aux clients.

À terme, cette plateforme pourra être adaptée à d'autres domaines (animateurs, photographes, vidéastes, groupes folkloriques, humoristes, conférenciers, etc.), faisant de Fuladou Live un véritable écosystème numérique dédié aux métiers de l'événementiel.

---

# 🌍 Vision

Le Fouladou possède une richesse culturelle exceptionnelle portée par des artistes, des musiciens et des groupes traditionnels qui participent activement au rayonnement de la région de Kolda. Pourtant, ces talents disposent encore de peu d'outils numériques adaptés à leurs besoins quotidiens.

Fuladou Live s'inscrit dans une démarche d'innovation locale : utiliser l'intelligence artificielle, le développement logiciel et l'automatisation pour résoudre des problématiques concrètes rencontrées par les acteurs culturels.

L'ambition est de construire une plateforme capable d'accompagner la professionnalisation des artistes, de renforcer leur visibilité et de faciliter leur mise en relation avec les organisateurs d'événements, tout en contribuant à la transformation numérique du secteur culturel.

À long terme, Fuladou Live aspire à devenir une référence au Sénégal, puis en Afrique de l'Ouest, en proposant une solution moderne, évolutive et accessible qui valorise les talents locaux et participe au développement de l'économie culturelle régionale.

# 👨‍💻 Auteur

Développé par **Sékou Diamanka**

Étudiant en Intelligence Artificielle et passionné par le développement de solutions numériques à fort impact social.

---

## 🌍 Vision

Fuladou Live ambitionne de devenir une plateforme de référence pour la gestion numérique des réservations artistiques en Afrique, en proposant une solution innovante, accessible et évolutive qui rapproche les artistes de leur public tout en modernisant l'organisation des événements culturels.
