# Simulation handler methods for SessionHandler
# Add these methods to session_handler.py

async def _handle_simulation_update(self, message: dict):
    """Handle simulation state updates from frontend."""
    simulation_id = message.get('simulation_id')
    student_actions = message.get('student_actions', [])
    current_state = message.get('current_state', {})
    objective_progress = message.get('objective_progress', 0)
    
    _safe_log(f"[Simulation] Update received: {simulation_id}")
    _safe_log(f"[Simulation] Actions: {student_actions}")
    _safe_log(f"[Simulation] State: {current_state}")
    _safe_log(f"[Simulation] Progress: {objective_progress}")
    
    # Store current state
    self.simulation_state = {
        'id': simulation_id,
        'state': current_state,
        'actions': student_actions,
        'progress': objective_progress
    }
    
    # Add to history
    self.simulation_history.append({
        'timestamp': message.get('timestamp'),
        'actions': student_actions,
        'state': current_state
    })
    
    # Generate AI guidance based on simulation state
    await self._generate_simulation_guidance(simulation_id, current_state, student_actions, objective_progress)

async def _generate_simulation_guidance(self, simulation_id: str, state: dict, actions: list, progress: float):
    """Generate AI guidance based on simulation state."""
    
    # Build context for AI
    simulation_context = self._build_simulation_context(simulation_id, state, actions, progress)
    
    # Determine if AI should intervene
    should_guide = self._should_provide_guidance(actions, progress)
    
    if not should_guide:
        _safe_log(f"[Simulation] No guidance needed yet (progress: {progress})")
        return
    
    # Generate AI response with simulation context
    ctx = self.session_context
    system_prompt = llm_service.build_system_prompt(
        subject=ctx.get("subject", "Physique"),
        language=self._prompt_language(),
        chapter_title=ctx.get("chapter_title", ""),
        lesson_title=ctx.get("lesson_title", ""),
        phase=self.current_phase,
        objective=ctx.get("objective", ""),
        scenario_context=simulation_context,  # Inject simulation context here
        student_name=ctx.get("student_name", "l'étudiant"),
        proficiency=ctx.get("proficiency", "intermédiaire"),
        struggles=ctx.get("struggles", "aucune identifiée"),
        mastered=ctx.get("mastered", "aucun"),
        teaching_mode=ctx.get("teaching_mode", "Socratique"),
    )
    
    # Add simulation observation to conversation
    observation = f"[SIMULATION] L'étudiant manipule la simulation '{simulation_id}'. Actions: {', '.join(actions)}. État actuel: {state}"
    self.conversation_history.append({"role": "user", "content": observation})
    
    try:
        ai_response = await llm_service.chat(
            messages=self.conversation_history,
            system_prompt=system_prompt,
            max_tokens=250,
        )
    except Exception as e:
        _safe_log(f"[Simulation] Error generating guidance: {e}")
        return
    
    self.conversation_history.append({"role": "assistant", "content": ai_response})
    
    # Send AI guidance to frontend
    await self.websocket.send_json({
        "type": "ai_response",
        "text": ai_response
    })
    
    # Generate audio
    import asyncio
    asyncio.create_task(self.generate_and_send_audio_chunks(ai_response))

def _build_simulation_context(self, simulation_id: str, state: dict, actions: list, progress: float) -> str:
    """Build rich context string for AI about simulation state."""
    
    if simulation_id == 'respiration_cellulaire':
        oxygen = state.get('oxygen_present')
        atp = state.get('atp_produced')
        pathway = state.get('pathway')
        
        context = f"""
CONTEXTE SIMULATION ACTIVE:
L'étudiant manipule actuellement la simulation de respiration cellulaire.

Actions effectuées: {', '.join(actions)}
Progression objectif: {int(progress * 100)}%

État actuel de la simulation:
- Oxygène présent: {'Oui' if oxygen else 'Non'}
- ATP produit: {atp}
- Voie métabolique: {pathway}

INSTRUCTIONS PÉDAGOGIQUES:
1. Si l'étudiant n'a testé qu'une condition, encourage-le à tester l'autre pour comparer
2. Pose des questions sur les résultats observés (combien d'ATP? pourquoi cette différence?)
3. Relie les observations à la théorie (mitochondrie, glycolyse, etc.)
4. Guide vers l'objectif: comprendre l'impact de l'O2 sur le rendement énergétique
"""
        return context
    
    return f"L'étudiant manipule la simulation '{simulation_id}'. Actions: {actions}. Progression: {int(progress * 100)}%"

def _should_provide_guidance(self, actions: list, progress: float) -> bool:
    """Determine if AI should provide guidance based on student actions."""
    
    # Provide guidance after first action
    if len(actions) == 1:
        return True
    
    # Provide guidance when student completes objective
    if progress >= 1.0 and len(actions) >= 2:
        return True
    
    # Provide guidance every 3 actions
    if len(actions) % 3 == 0:
        return True
    
    return False
