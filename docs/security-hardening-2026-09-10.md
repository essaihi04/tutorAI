# Sécurisation de Moalim — 10 septembre 2026

Ce document décrit les corrections de code et leur déploiement. Il ne constitue pas une garantie d'absence d'intrusion. Aucun secret n'est reproduit ici.

## Périmètre et décision du propriétaire

Application `moalim.online`, serveur `87.106.1.128`. Le propriétaire a demandé de préserver Ferdaous. Le 10 septembre, il a demandé de laisser Supabase de côté en attendant une migration vers une installation open source : aucune modification supplémentaire de Supabase n'est autorisée dans cette intervention.

## Actions déjà appliquées

- Les trois comptes aléatoires signalés ont été désactivés et bannis, sans suppression. Ferdaous reste actif. La dernière vérification avant la mise à l'écart de Supabase comptait 25 comptes, dont 22 actifs. Les autres comptes n'ont pas été supprimés.
- Les routes d'extraction et d'administration exigent désormais un jeton administrateur. L'inscription directe de l'application est fermée ; les demandes d'inscription restent soumises à validation.
- Les comptes désactivés ou expirés sont refusés par les contrôles d'accès, y compris sur les messages des séances de tutorat déjà ouvertes. Le renouvellement des jetons conserve l'identité de l'élève.
- Les jetons administrateur durent une heure, avec des vérifications de signature, d'émetteur, de destinataire et de rôle. Les valeurs de configuration triviales sont refusées.
- Les requêtes HTTP et les messages vocaux ont des limites de taille et de fréquence. Les adresses transmises par les clients ne permettent plus de contourner la limitation locale.
- Les accès aux fichiers sont limités aux répertoires attendus. Les fichiers internes et brouillons JSON ne sont plus servis par les routes de médias.
- Le rendu des formules, tableaux, SVG et cartes mentales a été sécurisé. Les simulations intégrées sont isolées de l'origine de l'application.
- Les dépendances vulnérables identifiées ont été mises à jour, dont la bibliothèque PDF et les bibliothèques Python. Les clés présentes dans la documentation ont été retirées des fichiers de travail ; cela ne révoque pas les clés ni leur présence dans l'historique Git.
- Nginx applique les limitations de requêtes, les protections des en-têtes et le refus des fichiers cachés. La journalisation des URL de tutorat contenant un jeton est désactivée.
- Le service fonctionne sous le compte système dédié `moalim`, sans privilèges root, avec le système de fichiers principalement en lecture seule et des répertoires d'écriture explicitement délimités.
- Fail2ban bloque les tentatives SSH répétées. Les délais et tentatives d'authentification ont été réduits. L'authentification SSH par mot de passe reste disponible.
- Les mises à jour de sécurité du système ont été installées. Le nouveau noyau est `5.14.0-687.42.1.el9_8.x86_64`. Le redémarrage a été autorisé et sa vérification est en cours.

## Validation et limites

- 84 tests ciblés passent dans l'espace de travail, avec un test de contenu de cours préexistant exclu. Ce test concernait une durée d'activité, sans lien avec les protections.
- Les 56 tests de sécurité passent dans l'environnement Linux préparé sur le serveur.
- Les 24 contrôles d'expressions mathématiques et six contrôles du rendu des libellés, tableaux et liens passent.
- Les audits npm, Python local, dépendances déclarées et environnement Python Linux préparé ne signalent plus de vulnérabilité connue au moment du contrôle.
- La version actuelle de travail compile. Pour la production, les correctifs ont été appliqués séparément à la version réellement déployée, `1ad2e3495c0cfe1a64a1522851a6b0a2193fbd02`, afin de ne pas publier les modifications de cours en préparation.
- Le contrôle TypeScript de cette ancienne version conserve exactement ses 23 diagnostics préexistants ; la compilation de production Vite réussit. Les correctifs de sécurité n'en ajoutent pas.
- Une instance privée a validé l'authentification administrateur et le fonctionnement sous les restrictions système avant le déploiement.
- Après déploiement, la page d'accueil et ses cinq fichiers d'entrée répondent correctement. Les routes administrateur et extraction refusent les visiteurs anonymes. Un problème de permissions des fichiers statiques a été détecté puis corrigé pendant le contrôle de déploiement.
- La vérification visuelle interactive dans un navigateur reste limitée par l'indisponibilité de l'outil de contrôle du navigateur. La version locale de Node utilisée pour la compilation est 22.12 ; certaines dépendances demandent 22.13 ou plus pour un environnement officiellement pris en charge.

## Points restant ouverts

1. **Supabase, reporté par le propriétaire :** des lectures anonymes ont été constatées sur `students`, `student_profiles` et `token_usage`. L'inscription directe Supabase avec confirmation automatique était également activée. Le verrouillage de l'application ne ferme pas ces accès directs. Le script `database/migrations/20260909_close_public_data_access.sql` est préparé mais n'a pas été exécuté.
2. **Clés Supabase, reportées :** une clé privilégiée utilisée par l'application a été retrouvée dans la documentation versionnée. Elle doit être remplacée et rendue inutilisable. Une migration de l'hébergement seule ne suffit pas si l'ancien projet et ses accès restent actifs.
3. **Clé DeepSeek :** une clé configurée a également été retrouvée dans la documentation. Son contrôle de validité, autorisé par le propriétaire, est en cours ; son retrait des fichiers ne constitue pas une révocation chez le fournisseur.
4. **Investigation d'incident :** les journaux confirment de nombreuses tentatives SSH échouées. Les connexions réussies récentes correspondent aux adresses observées dans les sessions du propriétaire et de cet audit. Les traces disponibles ne permettent pas d'affirmer qu'aucune intrusion ni copie de données n'a eu lieu.

## Exploitation et retour arrière

Les sauvegardes et journaux de l'intervention sont conservés sur le serveur dans `/root/moalim-security-20260910`, accessible à root. La sauvegarde précédant le déploiement contient le code, les fichiers de l'interface concernés, la configuration Nginx et l'unité systemd. Les anciens noyaux ont été conservés.

Le code de production reste dans `/root/moalim/backend`. Les données restent dans son répertoire `data`. Les fichiers de l'interface restent dans `/var/www/moalim`. Les caches de modèles utilisés par le compte dédié sont dans `/var/cache/moalim`.

Avant tout retour arrière, examiner les modifications de base et de clés intervenues depuis cette sauvegarde : restaurer une ancienne configuration peut rétablir une vulnérabilité. Aucun changement de cours en préparation n'a été inclus dans le paquet de sécurité.

Les copies temporaires de connexion utilisées sur le poste Windows seront effacées à la fin de l'intervention.

## Références

- [Supabase : sécurisation de l'API](https://supabase.com/docs/guides/api/securing-your-api)
- [Supabase : remplacement d'une clé exposée](https://supabase.com/docs/guides/getting-started/api-keys)
- [Nginx : héritage des en-têtes de réponse](https://nginx.org/en/docs/http/ngx_http_headers_module.html)
- [Avis de sécurité du lecteur PDF](https://github.com/mozilla/pdf.js/security/advisories/GHSA-hq66-cqwq-w95j)
