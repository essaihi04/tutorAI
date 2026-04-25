# Solution: Corriger le DNS Supabase sur Windows

## Problème
Votre système ne peut pas résoudre `db.yzvlmulpqnovduqhhtjf.supabase.co` en raison d'un problème DNS.

## Solution: Modifier le fichier hosts

### Étape 1: Obtenir l'adresse IP de Supabase

Utilisez un service en ligne depuis votre navigateur:
1. Allez sur https://www.nslookup.io/
2. Entrez: `db.yzvlmulpqnovduqhhtjf.supabase.co`
3. Notez l'adresse IPv4 (exemple: `54.xxx.xxx.xxx`)

OU utilisez un autre appareil/téléphone connecté au même réseau:
```bash
nslookup db.yzvlmulpqnovduqhhtjf.supabase.co 8.8.8.8
```

### Étape 2: Modifier le fichier hosts

1. **Ouvrir Notepad en tant qu'administrateur**
   - Clic droit sur "Bloc-notes" → "Exécuter en tant qu'administrateur"

2. **Ouvrir le fichier hosts**
   - Fichier → Ouvrir
   - Naviguez vers: `C:\Windows\System32\drivers\etc`
   - Changez le filtre de "Fichiers texte" à "Tous les fichiers"
   - Ouvrez le fichier `hosts`

3. **Ajouter cette ligne à la fin du fichier**
   ```
   [ADRESSE_IP_OBTENUE]  db.yzvlmulpqnovduqhhtjf.supabase.co
   ```
   
   Exemple (remplacez par la vraie IP):
   ```
   54.123.45.67  db.yzvlmulpqnovduqhhtjf.supabase.co
   ```

4. **Sauvegarder le fichier**

5. **Vider le cache DNS**
   ```powershell
   ipconfig /flushdns
   ```

6. **Tester**
   ```powershell
   ping db.yzvlmulpqnovduqhhtjf.supabase.co
   ```

### Étape 3: Redémarrer le backend

```bash
cd C:\Users\HP\Desktop\ai-tutor-bac\backend
python -m uvicorn app.main:app --reload
```

---

## Solution 2: Changer les serveurs DNS

1. **Ouvrir les Paramètres réseau**
   - Panneau de configuration → Réseau et Internet
   - Centre Réseau et partage
   - Cliquez sur votre connexion Wi-Fi active
   - Cliquez sur "Propriétés"

2. **Configurer DNS Google**
   - Sélectionnez "Protocole Internet version 4 (TCP/IPv4)"
   - Cliquez sur "Propriétés"
   - Sélectionnez "Utiliser l'adresse de serveur DNS suivante"
   - DNS préféré: `8.8.8.8`
   - DNS auxiliaire: `8.8.4.4`
   - Cliquez sur OK

3. **Redémarrer la connexion réseau**
   - Désactivez puis réactivez votre connexion Wi-Fi

4. **Tester**
   ```powershell
   nslookup db.yzvlmulpqnovduqhhtjf.supabase.co
   ```

---

## Solution 3: Utiliser un VPN

Si votre FAI bloque ou filtre les connexions:
1. Installez un VPN (ProtonVPN, Windscribe, etc.)
2. Connectez-vous au VPN
3. Testez la connexion Supabase

---

## Solution 4: Vérifier le projet Supabase

1. Allez sur https://supabase.com/dashboard
2. Sélectionnez votre projet `yzvlmulpqnovduqhhtjf`
3. Vérifiez que le projet est **actif** (pas en pause)
4. Allez dans Settings → Database
5. Vérifiez la chaîne de connexion et le mot de passe

---

## Test après correction

```bash
cd backend
python test_direct_supabase.py
```

Vous devriez voir:
```
✓ Connection successful!
✓ PostgreSQL: ...
✓ Tables: [...]
```
