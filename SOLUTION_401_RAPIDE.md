# 🔴 Solution Rapide - Erreur 401

## Le Problème
Votre token JWT est **expiré** ou **invalide**.

## ✅ Solution en 3 Étapes

### Étape 1: Déconnexion
1. Allez sur le **Dashboard** (http://localhost:5173/dashboard)
2. Cliquez sur le bouton **"Déconnexion"** en haut à droite

### Étape 2: Reconnexion
1. Vous serez redirigé vers la page **Login**
2. Entrez vos identifiants:
   - Email: `votre_email@example.com`
   - Mot de passe: `votre_mot_de_passe`
3. Cliquez sur **"Se connecter"**

### Étape 3: Test
1. Retournez au **Dashboard**
2. Cliquez sur **SVT**
3. Cliquez sur **Chapitre 1**
4. Cliquez sur **"Démarrer la session"**
5. ✅ **Ça devrait fonctionner maintenant !**

---

## 🔍 Vérification Rapide

### Dans le Navigateur (DevTools - F12)

**Console:**
```javascript
// Vérifier le token actuel
localStorage.getItem('token')

// Si vous voulez forcer la déconnexion:
localStorage.removeItem('token')
localStorage.removeItem('student')
// Puis rechargez la page (F5)
```

---

## 🎯 Pourquoi Cette Erreur ?

Les tokens JWT Supabase ont une **durée de vie limitée** (généralement 1 heure).

**Scénarios courants:**
- ✅ Vous êtes resté connecté longtemps sans activité
- ✅ Le backend a redémarré (nouveau secret)
- ✅ Vous avez modifié le code d'authentification

**Solution permanente:** Refresh token automatique (à implémenter plus tard)

---

## 📝 Alternative: Supprimer le Token Manuellement

Si le bouton de déconnexion ne fonctionne pas:

1. **F12** (DevTools)
2. **Application** (ou **Storage**)
3. **Local Storage** → `http://localhost:5173`
4. Supprimez les clés:
   - `token`
   - `student`
5. **Rechargez la page** (F5)
6. Vous serez redirigé vers Login
7. Reconnectez-vous

---

## ✅ Checklist Avant de Tester

- [ ] Backend est démarré (`python -m uvicorn app.main:app --reload`)
- [ ] Frontend est démarré (`npm run dev`)
- [ ] Vous êtes **déconnecté** puis **reconnecté**
- [ ] Le script SQL SVT est exécuté dans Supabase
- [ ] Les matières sont visibles sur le Dashboard

---

## 🚀 Après la Reconnexion

Vous aurez un **nouveau token valide** et pourrez:
- ✅ Accéder au profil (`/sessions/profile`)
- ✅ Voir les matières (`/content/subjects`)
- ✅ Démarrer des sessions (`/sessions/start`)
- ✅ Utiliser toutes les fonctionnalités

---

## 💡 Astuce

Pour éviter ce problème à l'avenir:
- Reconnectez-vous régulièrement
- Ne laissez pas l'onglet ouvert trop longtemps
- Utilisez le mode développement avec refresh automatique (à venir)

**C'est tout ! Déconnectez-vous et reconnectez-vous maintenant.** 🔐
