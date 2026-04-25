# Changelog - Pilotage IA des Simulations

## Corrections appliquées (dernière session)

### Problème identifié
La simulation `respiration_energie` envoyait bien ses états au backend, mais le backend ne générait pas de guidage vocal car il cherchait uniquement `simulation_id: 'respiration_cellulaire'`.

### Corrections

#### 1. Backend - Support de `respiration_energie` ✅
**Fichier:** `backend/app/websockets/session_handler.py`

- ✅ Ajout du support pour `simulation_id: 'respiration_energie'` en plus de `'respiration_cellulaire'`
- ✅ Adaptation de l'extraction des données d'état pour supporter les deux formats
- ✅ Amélioration des logs pour déboguer facilement
- ✅ Logique de déclenchement du guidage plus réactive (toutes les 2 actions au lieu de 3)
- ✅ Support des actions au format `dict` avec extraction du champ `action`

**Changements clés:**
```python
# Avant
if simulation_id == 'respiration_cellulaire':

# Après
if simulation_id in ['respiration_cellulaire', 'respiration_energie']:
    is_aerobic = state.get('is_aerobic', state.get('oxygen_present'))
    atp = state.get('current_atp', state.get('atp_produced', 0))
    # Support des deux formats
```

#### 2. Logs améliorés ✅
```python
_safe_log(f"[Simulation] ========================================")
_safe_log(f"[Simulation] Update received: {simulation_id}")
_safe_log(f"[Simulation] Actions count: {len(student_actions)}")
_safe_log(f"[Simulation] Latest actions: {student_actions[-3:]}")
_safe_log(f"[Simulation] Progress: {objective_progress * 100:.0f}%")
_safe_log(f"[Simulation] State: {current_state}")
```

#### 3. Déclenchement du guidage plus réactif ✅
```python
# Avant: toutes les 3 actions
if len(actions) % 3 == 0:

# Après: toutes les 2 actions
if num_actions > 0 and num_actions % 2 == 0:
    _safe_log(f"[Simulation Guidance] Triggering: every 2 actions ({num_actions})")
    return True
```

### Ce qui devrait maintenant fonctionner

1. **Guidage vocal automatique** après chaque 2 actions de l'étudiant
2. **Questions de vérification** basées sur les résultats observés
3. **Support complet** pour `simulation_id: 'respiration_energie'`
4. **Logs détaillés** dans la console backend pour déboguer

### Test attendu

Quand l'étudiant manipule la simulation:
1. Action 1 (ex: `start_simulation`) → ✅ IA génère guidage vocal
2. Action 2 (ex: `toggled_o2`) → ✅ IA génère guidage vocal
3. Action 3 → Pas de guidage (sauf si objectif atteint)
4. Action 4 → ✅ IA génère guidage vocal

### Vérification dans les logs backend

Cherchez ces lignes:
```
[Simulation] ========================================
[Simulation] Update received: respiration_energie
[Simulation] Actions count: 2
[Simulation Guidance] Triggering: every 2 actions (2)
[Simulation] Generating AI guidance for: [SIMULATION] L'étudiant manipule...
```

### Prochaines étapes si ça ne fonctionne toujours pas

1. Vérifier les logs backend pour voir si `_handle_simulation_update` est appelé
2. Vérifier si `_should_provide_guidance` retourne `True`
3. Vérifier si le LLM génère bien une réponse
4. Vérifier si l'audio est bien envoyé au frontend

### Commandes de contrôle (optionnel)

Pour tester le pilotage actif de la simulation par l'IA, vous pouvez ajouter dans `_generate_simulation_guidance`:

```python
# Exemple: mettre en évidence un bouton après la première action
if len(actions) == 1:
    await self._send_simulation_control(
        simulation_id,
        'highlight_button',
        {'button': 'without_o2'},
        'Essaie maintenant sans oxygène'
    )
```

## Résumé des fichiers modifiés

- ✅ `backend/app/websockets/session_handler.py` - Support respiration_energie + logs + guidage réactif
- ✅ `frontend/src/pages/LearningSession.tsx` - Relais des commandes IA vers iframe
- ✅ `frontend/public/media/simulations/.../respiration/simulation.html` - Réception commandes IA
- ✅ `SIMULATION_AI_CONTROL_PROTOCOL.md` - Documentation protocole
- ✅ `GUIDE_RAPIDE_SIMULATION_IA.md` - Guide création simulations
- ✅ `TEMPLATE_SIMULATION.html` - Template réutilisable
