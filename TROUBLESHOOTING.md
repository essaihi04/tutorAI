# Résolution du problème de connexion à Supabase

## Problème
Erreur `socket.gaierror: [Errno 11001] getaddrinfo failed` lors de la tentative de connexion à la base de données Supabase.

## Cause
Le système Windows ne peut pas résoudre le nom de domaine `db.yzvlmulpqnovduqhhtjf.supabase.co` en raison d'un problème DNS (le serveur retourne uniquement une adresse IPv6 mais Python/asyncpg a du mal à l'utiliser).

## Solutions

### Solution 1: Utiliser PostgreSQL local avec Docker (RECOMMANDÉ)

1. **Démarrer Docker Desktop**
   - Ouvrez Docker Desktop manuellement
   - Attendez qu'il soit complètement démarré

2. **Démarrer les services**
   ```bash
   cd c:/Users/HP/Desktop/ai-tutor-bac
   docker-compose up -d db redis
   ```

3. **Mettre à jour le fichier .env**
   ```bash
   # Dans backend/.env, remplacer les lignes DATABASE_URL par:
   DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ai_tutor_bac
   DATABASE_URL_SYNC=postgresql://postgres:password@localhost:5432/ai_tutor_bac
   ```

4. **Exécuter les migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

5. **Redémarrer le backend**

### Solution 2: Corriger le DNS Windows

1. **Ouvrir le fichier hosts en tant qu'administrateur**
   ```
   notepad C:\Windows\System32\drivers\etc\hosts
   ```

2. **Ajouter une entrée pour Supabase**
   - Vous devez d'abord obtenir l'adresse IPv4 de Supabase
   - Utilisez un service en ligne comme https://www.nslookup.io/ pour résoudre `db.yzvlmulpqnovduqhhtjf.supabase.co`
   - Ajoutez la ligne: `[IP_ADDRESS] db.yzvlmulpqnovduqhhtjf.supabase.co`

3. **Sauvegarder et tester**

### Solution 3: Changer les serveurs DNS

1. **Ouvrir les paramètres réseau**
   - Panneau de configuration → Réseau et Internet → Centre Réseau et partage
   - Cliquez sur votre connexion Wi-Fi
   - Propriétés → Protocole Internet version 4 (TCP/IPv4)

2. **Configurer les DNS Google**
   - DNS préféré: `8.8.8.8`
   - DNS auxiliaire: `8.8.4.4`

3. **Redémarrer la connexion réseau**

### Solution 4: Utiliser un VPN

Si votre FAI bloque ou filtre certains domaines, utilisez un VPN pour contourner ces restrictions.

## Vérification

Après avoir appliqué une solution, testez la connexion:

```bash
cd backend
python test_db_connection.py
```

Vous devriez voir:
```
✓ Connection successful!
✓ PostgreSQL version: ...
✓ Tables found: [...]
```
