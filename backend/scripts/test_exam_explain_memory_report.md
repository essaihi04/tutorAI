# Diagnostic — mode examen > « Aide au tableau » > questions de suivi

_Généré le 2026-05-01 19:11:25_


## Hypothèse
En mode `explain` (ExamPractice > « Aide au tableau »), le backend injecte la question dans le PREMIER message utilisateur (opening) mais ne remplit JAMAIS `self.current_exam_view`. Résultat : le bloc `[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ]` n'est PAS ajouté au prompt système sur les tours 2, 3, 4… Le LLM n'a plus que `conversation_history` comme mémoire et peut perdre la question étudiée.


## Expérience
On rejoue 4 tours (1 opening + 3 questions de suivi) contre le vrai LLM DeepSeek sur une question SVT Q2 (pollution par nitrates), dans 2 scénarios :
- **A — prod actuelle** : bloc exam non injecté sur les tours de suivi
- **B — avec fix** : bloc exam injecté à CHAQUE tour (mirroir de la proposition de fix)

On mesure :
- `prompt_contains_question` : l'énoncé est-il dans le prompt système ?
- `references_question_correctly` : la réponse du LLM cite-t-elle ≥ 2 termes-clés de la question (nitrate, eutrophisation, …) ?
- `loss_signals` : la réponse contient-elle une formule de perte de contexte (`quelle question`, `peux-tu me redonner l'énoncé`, …) ?


## Résultats

| Scénario | Prompt contient question | Réponses qui citent ≥2 termes-clés | Réponses avec perte de contexte |
|---|---|---|---|
| **A — prod actuelle** (sans fix) | 4/4 | 4/4 | 0/4 |
| **B — avec fix** (current_exam_view injecté) | 4/4 | 4/4 | 0/4 |

---

## Scénario A — PROD ACTUELLE (sans fix)


### T1 — opening explain

**Message utilisateur :** `L'élève a répondu à une question d'examen et veut comprendre EN PROFONDEUR ses points forts et ses erreurs.

Question (open, 4 pts) : Question 2 : En se basant sur les documents 1 et 2, expliquer l'im`

- `prompt_contains_question` = **True** (prompt_length=60292)
- `references_question_correctly` = **True** (citations nitrate/eutrophisation/phytoplancton/…)
- ✅ pas de signal de perte de contexte

**Réponse LLM (1973 chars, 9.3s) :**
```
واخا خويا، دابا غادي نحللوا الـ réponse ديالك كلمة بكلمة. شوف، جبتي الفكرة العامة بلي "السمك كيموت والطحالب كتنمو" ولكن هادشي ناقصو بزاف ديال التفاصيل العلمية لي كتطلب السؤال. السؤال طلب منك "expliquer l'impact" و"préciser les mécanismes biogéochimiques". أنت ماجبتيش لا مصطلح eutrophisation ولا كيفاش كتستهلك البكتيريا l'oxygène. هاد الشي لي خلاك تجيب غير 0.5 من 4.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Analyse de ta réponse (0.5/4)","lines":[{"type":"title","icon":"🧪","content":"Correction détaillée — Question 2 (4 pts)"},{"type":"subtitle","content":"📖 Ta réponse","color":"blue"},{"type":"box","content":"« La pollution tue les poissons et les algues poussent. »","color":"blue"},{"type":"subtitle","content":"⚠️ Ce qui manque","color":"orange"},{"type":"text","content":"1. Aucun terme scientifique (eutrophisation, phytoplancton, O2 dissous)"},{"type":"text","content":"2. Mécanisme biogéochimique absent (nitrates → prolifération → décomposition → asphyxie)"},{"type":"text","content":"3. Pas de lien explicite entre les 2 documents (NO3- → biomasse → O2)"},{"type":"subtitle","content":"🔑 Correction officielle (4/4)","color":"green"},{"type":"step","content":"Étape 1 : Les nitrates (NO3-) enrichissent le lac → prolifération du phytoplancton = EUTROPHISATION","label":"1","color":"green"},{"type":"step","content":"Étape 2 : La décomposition de cette biomasse par les bactéries consomme l'oxygène dissous","label":"2","color":"green"},{"type":"step","content":"Étape 3 : Résultat = asphyxie des poissons → chute de la biodiversité aquatique","label":"3","color":"green"},{"type":"box","content":"💡 Astuce BAC : Utilise TOUJOURS les mots-clés du programme : eutrophisation, phytoplancton, O2 dissous, respiration bactérienne","color":"purple"}]}}]}</ui>

شفت الفرق؟ دابا غادي نعطيك سؤال باش نتأكد بلي فهمتي الطريقة الصحيحة. واش تقدر تقولي ليا شنو هو المصطلح العلمي لي كيوصف هاد الظاهرة ديال زيادة الطحالب بسباب النترات؟
```

### T2 — question breve de suivi

**Message utilisateur :** `Pourquoi le phytoplancton prolifere ?`

- `prompt_contains_question` = **True** (prompt_length=60292)
- `references_question_correctly` = **True** (citations nitrate/eutrophisation/phytoplancton/…)
- ✅ pas de signal de perte de contexte

**Réponse LLM (1280 chars, 6.4s) :**
```
واخا، سؤال مزيان! دابا غادي نعرفو علاش كاين هاد la prolifération.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Pourquoi le phytoplancton prolifère ?","lines":[{"type":"title","icon":"🌿","content":"Mécanisme de l'eutrophisation"},{"type":"subtitle","content":"🔑 Le moteur : les NITRATES (NO3-)","color":"purple"},{"type":"text","content":"Les nitrates sont des NUTRIMENTS (engrais) pour le phytoplancton (algues microscopiques)."},{"type":"text","content":"Normalement, leur quantité dans le lac est limitée → croissance contrôlée."},{"type":"step","content":"Rejets agricoles (engrais) → augmentation massive des NO3- dans l'eau","label":"1","color":"green"},{"type":"step","content":"Le phytoplancton trouve soudainement une nourriture abondante → il se multiplie rapidement","label":"2","color":"green"},{"type":"step","content":"C'est ce qu'on appelle l'EUTROPHISATION : enrichissement excessif en nutriments","label":"3","color":"green"},{"type":"box","content":"💡 À retenir : Les nitrates = engrais pour les algues. Plus il y a de NO3-, plus le phytoplancton pousse vite !","color":"purple"}]}}]</ui>

هاد الفكرة هي المفتاح. النترات كتعتبر comme un engrais pour les algues. واش عقلتي ليه هاد la prolifération كتسبب نقصان l'oxygène ف le lac؟
```

### T3 — reference implicite a la question

**Message utilisateur :** `Donne-moi un exemple concret de la reponse modele pour cette question.`

- `prompt_contains_question` = **True** (prompt_length=60292)
- `references_question_correctly` = **True** (citations nitrate/eutrophisation/phytoplancton/…)
- ✅ pas de signal de perte de contexte

**Réponse LLM (1536 chars, 7.1s) :**
```
واخا خويا، دابا غادي نعطيك مثال ديال réponse كاملة 4/4 باش تشوف الفرق مع الجواب ديالك.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Réponse modèle 4/4","lines":[{"type":"title","icon":"🧪","content":"Exemple de réponse complète (BAC 2024 Normale)"},{"type":"subtitle","content":"📝 Réponse rédigée","color":"green"},{"type":"box","content":"L'augmentation des nitrates (NO3-) dans le lac, due aux rejets agricoles, stimule la prolifération du phytoplancton : c'est l'eutrophisation. La décomposition de cette biomasse par les bactéries aérobies consomme l'oxygène dissous. Cette chute d'O2 provoque l'asphyxie des poissons et la réduction de la biodiversité aquatique.","color":"green"},{"type":"subtitle","content":"🔑 Mots-clés obligatoires","color":"purple"},{"type":"text","content":"• Nitrates (NO3-)"},{"type":"text","content":"• Prolifération du phytoplancton"},{"type":"text","content":"• Eutrophisation"},{"type":"text","content":"• Décomposition par les bactéries aérobies"},{"type":"text","content":"• Consommation d'oxygène dissous (O2)"},{"type":"text","content":"• Asphyxie des poissons → baisse de biodiversité"},{"type":"subtitle","content":"⚠️ Piège à éviter","color":"orange"},{"type":"note","content":"Ne dis PAS juste « les algues poussent ». Dis « prolifération du phytoplancton = eutrophisation ».","color":"orange"}]}}]</ui>

هاد الجواب فيه 4 éléments essentiels لي كيجيبو النقطة كاملة. شوف الفرق مع جوابك لي كان فيه غير فكرة وحدة. دابا واش تقدر تعاود تحاول تجاوب على السؤال بنفسك؟
```

### T4 — demande de reformulation

**Message utilisateur :** `Peux-tu me reexpliquer autrement, je n'ai pas compris la partie biogeochimique ?`

- `prompt_contains_question` = **True** (prompt_length=60292)
- `references_question_correctly` = **True** (citations nitrate/eutrophisation/phytoplancton/…)
- ✅ pas de signal de perte de contexte

**Réponse LLM (1442 chars, 7.6s) :**
```
واخا خويا، باش تفهمها بسهولة، خلينا نشبهوها بحاجة من حياتك اليومية. تصور عندك حوض ديال السمك فداركم، وكل يوم كتزيد فيه شويا ديال الأكل (السميد). فالأول، السمك كياكل وهادشي مزيان. ولكن إلا زدتي بزاف ديال الأكل، راه الأكل الزايد كيطيح للتحت ويبدأ يتعفن. هاد التعفن كيستهلك l'oxygène الموجود فالماء، ونتيجة لذلك السمك كيموت مختنق.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Mécanisme biogéochimique simplifié","lines":[{"type":"title","icon":"🧪","content":"Le cycle nitrates → O2 → biodiversité"},{"type":"subtitle","content":"🔑 Les 3 étapes clés","color":"purple"},{"type":"step","content":"NITRATES (NO3-) = nourriture pour le phytoplancton (algues microscopiques)","label":"1","color":"green"},{"type":"step","content":"Phytoplancton se multiplie → EUTROPHISATION (excès d'algues)","label":"2","color":"green"},{"type":"step","content":"Les algues mortes sont décomposées par les BACTÉRIES AÉROBIES (qui respirent l'O2)","label":"3","color":"orange"},{"type":"step","content":"Les bactéries consomment tout l'O2 dissous → ASPHYXIE des poissons","label":"4","color":"red"},{"type":"box","content":"💡 Résumé : Nitrates → algues → bactéries mangent les algues mortes → bactéries respirent l'O2 → plus d'O2 pour les poissons","color":"purple"}]}}]</ui>

هاد "biogéochimique" كتعني بلي هاد الظاهرة فيها تفاعل بين عناصر حية (phytoplancton, bactéries, poissons) وعناصر غير حية (nitrates, oxygène). واش واضح دابا؟
```

---

## Scénario B — AVEC FIX


### T1 — opening explain

**Message utilisateur :** `L'élève a répondu à une question d'examen et veut comprendre EN PROFONDEUR ses points forts et ses erreurs.

Question (open, 4 pts) : Question 2 : En se basant sur les documents 1 et 2, expliquer l'im`

- `prompt_contains_question` = **True** (prompt_length=61406)
- `references_question_correctly` = **True** (citations nitrate/eutrophisation/phytoplancton/…)
- ✅ pas de signal de perte de contexte

**Réponse LLM (2118 chars, 10.6s) :**
```
واخا خويا، دابا غادي نحللّو هاد الجواب ديالك. شوف، عندك 0.5 من 4، علاش؟ الجواب ديالك فيه الفكرة العامة "السمك كيموت والطحالب كتنمو" ولكن مازال ناقص بزاف. السؤال طلب منك "تشرح الآليات البيوجيوكيميائية" يعني شنو كاين فالدوكومونات وشنو كايدير النترات بالضبط. هادشي لي غادي نركزو عليه دابا.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Analyse de la réponse — Question 2 (4 pts)","lines":[{"type":"illustration","icon":"💧","content":"Lac Oum Er-Rbia — Eutrophisation par nitrates"},{"type":"subtitle","content":"📖 Ta réponse : « La pollution tue les poissons et les algues poussent. »","color":"blue"},{"type":"text","content":"Note : 0.5/4 — Idée générale présente mais mécanisme absent."},{"type":"subtitle","content":"🔑 Ce qu'il fallait dire (correction officielle)","color":"purple"},{"type":"box","content":"1. Nitrates → prolifération du phytoplancton (eutrophisation)\n2. Décomposition de la biomasse → consommation de O₂ dissous par les bactéries\n3. Asphyxie des poissons → chute de la biodiversité","color":"purple"},{"type":"subtitle","content":"⚠️ Erreurs / Oublis dans ta réponse","color":"orange"},{"type":"note","content":"❌ Tu n'as pas cité le mot-clé « eutrophisation »\n❌ Tu n'as pas mentionné la consommation d'oxygène dissous par les bactéries\n❌ Tu n'as pas expliqué le lien entre nitrates et prolifération du phytoplancton\n❌ Tu n'as pas utilisé les documents (graphiques) pour appuyer ta réponse","color":"orange"},{"type":"subtitle","content":"💡 Astuce BAC","color":"purple"},{"type":"note","content":"Pour une question à 4 pts, il faut au moins 3-4 étapes claires : cause → mécanisme → conséquence → conclusion. Utilise les mots-clés du programme : eutrophisation, oxygène dissous, respiration bactérienne, asphyxie.","color":"purple"},{"type":"subtitle","content":"📝 À retenir absolument","color":"green"},{"type":"box","content":"Nitrates (NO₃⁻) → Eutrophisation → Prolifération phytoplancton → Décomposition bactérienne → Consommation O₂ → A
…[tronqué]
```

### T2 — question breve de suivi

**Message utilisateur :** `Pourquoi le phytoplancton prolifere ?`

- `prompt_contains_question` = **True** (prompt_length=61406)
- `references_question_correctly` = **True** (citations nitrate/eutrophisation/phytoplancton/…)
- ✅ pas de signal de perte de contexte

**Réponse LLM (1867 chars, 9.5s) :**
```
مزيان، سؤال ديال واحد اللي كايبغي يفهم العمق. علاش الطحالب (phytoplancton) كاتكثر بزاف فهاد الحالة؟ الجواب كاين فالكلمة ديال "eutrophisation" اللي كاتعني "الإثراء الغذائي". النترات (NO3-) هي سماد طبيعي للطحالب. اللي كاين فالدوكومون 1 هو أن التركيز ديال النترات فالبحيرة بدا كايطاح من 2010، ولكن فجأة من 2015 ارتفع بزاف حيتاش الفلاحين زادو فاستعمال الأسمدة. هاد النترات دخلات للبحيرة، وولات كاتغدي الطحالب بزاف، بحال ما كاتسقي نبتة بالسماد. الطحالب كاتنمو بسرعة هائلة، وهادشي هو "prolifération".

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Pourquoi le phytoplancton prolifère ?","lines":[{"type":"illustration","icon":"🌿","content":"Nitrates = engrais pour le phytoplancton"},{"type":"subtitle","content":"🔑 Le mécanisme clé","color":"purple"},{"type":"box","content":"Nitrates (NO₃⁻) → Nutriments essentiels pour le phytoplancton → Croissance explosive (prolifération) = EUTROPHISATION","color":"purple"},{"type":"subtitle","content":"📊 Lien avec les documents","color":"blue"},{"type":"text","content":"Doc 1 : Hausse des nitrates à partir de 2015 (rejets agricoles)"},{"type":"text","content":"Doc 2 : La biomasse de phytoplancton suit la même courbe → corrélation directe"},{"type":"subtitle","content":"💡 Analogie","color":"green"},{"type":"note","content":"C'est comme si tu arrosais une plante avec de l'engrais concentré tous les jours : elle pousse de façon démesurée. Ici, le lac reçoit un excès de nitrates → les algues explosent.","color":"green"},{"type":"subtitle","content":"⚠️ Piège BAC","color":"orange"},{"type":"note","content":"Ne dis pas « les algues poussent à cause de la pollution » — trop vague. Dis : « L'enrichissement en nitrates (eutrophisation) stimule la prolifération du phytoplancton. »","color":"orange"}]}}]}</ui>

هاد الفكرة وضحت ليك؟ واش عارف شنو كايتّبع هاد الزيادة فالطحالب من ناحية الأوكسجين؟
```

### T3 — reference implicite a la question

**Message utilisateur :** `Donne-moi un exemple concret de la reponse modele pour cette question.`

- `prompt_contains_question` = **True** (prompt_length=61406)
- `references_question_correctly` = **True** (citations nitrate/eutrophisation/phytoplancton/…)
- ✅ pas de signal de perte de contexte

**Réponse LLM (1845 chars, 8.7s) :**
```
واخا، دابا غادي نعطيك جواب نموذجي كامل بحال اللي غادي تكتبو فـ BAC باش تجيب 4/4. شوف كيفاش كايتكون من 3 مراحل مترابطة، كل مرحلة فيها كلمة مفتاحية ونتيجة.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Réponse modèle — Question 2 (4/4)","lines":[{"type":"illustration","icon":"💯","content":"Structure gagnante pour le BAC"},{"type":"subtitle","content":"📝 Réponse complète et structurée","color":"blue"},{"type":"box","content":"L'augmentation de la concentration des nitrates (NO₃⁻) dans le lac (Doc 1) provoque une eutrophisation, c'est-à-dire une prolifération massive du phytoplancton (Doc 2). Cette biomasse en excès est décomposée par les bactéries aérobies, ce qui consomme une grande quantité d'oxygène dissous dans l'eau (Doc 2 : chute de O₂). La diminution de l'oxygène dissous entraîne l'asphyxie des poissons et des autres organismes aquatiques, ce qui conduit à une chute de la biodiversité du lac.","color":"purple"},{"type":"subtitle","content":"🔑 Découpage des points","color":"green"},{"type":"table","content":"","headers":["Étape","Mots-clés","Points"],"rows":[["1. Cause","Nitrates → Eutrophisation → Prolifération phytoplancton","1.5 pt"],["2. Mécanisme","Décomposition bactérienne → Consommation O₂ dissous","1.5 pt"],["3. Conséquence","Asphyxie poissons → Chute biodiversité","1 pt"]]},{"type":"subtitle","content":"💡 Astuce BAC","color":"purple"},{"type":"note","content":"Utilise TOUJOURS les mots : eutrophisation, prolifération, décomposition bactérienne, oxygène dissous, asphyxie. Et cite les documents : « Doc 1 montre... », « Doc 2 indique... ».","color":"purple"}]}}]</ui>

هاد الجواب فيه 3 عناصر أساسية: السبب (النترات -> الطحالب)، الآلية (البكتيريا كاتستهلك الأوكسجين)، النتيجة (السمك كيموت والتنوع البيولوجي كاينقص). كل عنصر كايجيب نقطة.

واضح ليك كيفاش غادي تكتب الجواب فـ BAC؟
```

### T4 — demande de reformulation

**Message utilisateur :** `Peux-tu me reexpliquer autrement, je n'ai pas compris la partie biogeochimique ?`

- `prompt_contains_question` = **True** (prompt_length=61406)
- `references_question_correctly` = **True** (citations nitrate/eutrophisation/phytoplancton/…)
- ✅ pas de signal de perte de contexte

**Réponse LLM (1753 chars, 8.8s) :**
```
آه، هاد الجزء هو اللي معقد شويا. "الآلية البيوجيوكيميائية" كاتعني شنو كايديرو الكائنات الحية (bio) مع المواد الكيماوية (chimique) فالماء. بكل بساطة: الطحالب اللي كبرات بزاف كتموت. البكتيريا كاتجي باش تحلل هاد الطحالب الميتة، ولكن فهاد العملية كاتستهلك الأوكسجين المذاب فالماء. يعني البكتيريا كاتنافس السمك على الأوكسجين، والسمك كايموت بالاختناق.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Le mécanisme biogéochimique simplifié","lines":[{"type":"illustration","icon":"🔄","content":"Cycle : Nitrates → Algues → Bactéries → O₂ → Poissons"},{"type":"subtitle","content":"🔑 Les 3 acteurs du mécanisme","color":"purple"},{"type":"table","content":"","headers":["Acteur","Rôle","Action"],"rows":[["🌿 Phytoplancton","Producteur","Prolifère grâce aux nitrates"],["🦠 Bactéries","Décomposeur","Décompose les algues mortes"],["🐟 Poissons","Consommateur","Meurt par manque d'O₂"]]},{"type":"subtitle","content":"📊 Le cycle expliqué étape par étape","color":"blue"},{"type":"step","content":"1. Nitrates (engrais) → font pousser les algues (phytoplancton)","label":"1"},{"type":"step","content":"2. Les algues meurent → les bactéries les décomposent","label":"2"},{"type":"step","content":"3. Les bactéries utilisent l'oxygène dissous (O₂) pour décomposer","label":"3"},{"type":"step","content":"4. Plus d'O₂ pour les poissons → asphyxie → biodiversité chute","label":"4"},{"type":"subtitle","content":"⚠️ Piège BAC","color":"orange"},{"type":"note","content":"Ne dis pas « la pollution tue les poissons ». Dis : « La décomposition bactérienne consomme l'oxygène dissous, ce qui asphyxie les poissons. »","color":"orange"}]}}]</ui>

واضح هاد المرة؟ واش تقدر تقولي ليا بجملة واحدة شنو كاتعني "الآلية البيوجيوكيميائية" فهاد السياق؟
```

---

## Conclusion & fix recommandé

⚠️ Les deux scénarios ont produit des scores similaires — dans ce corpus de 4 tours, la conversation history suffit au LLM. Mais le bug rapporté en prod survient sur des sessions plus longues ou quand la history est tronquée.


**Fix proposé** (`backend/app/websockets/session_handler.py` `_init_session`, branche `explain`) :
```python
# Après avoir parsé explain_data…
self.current_exam_view = {
    'exam_id': explain_data.get('examId') or '',
    'subject': explain_data.get('subject') or '',
    'exam_title': explain_data.get('examTitle') or '',
    'exercise_name': explain_data.get('parentContent','')[:80],
    'question_number': explain_data.get('questionNumber'),
    'question_total': explain_data.get('questionTotal'),
    'question_content': q_content,
    'question_correction': q_correction,
    'question_points': q_points,
}
```
Ainsi, à chaque tour de suivi, `_process_student_input` injectera le bloc `[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ]` dans le prompt système et le LLM saura toujours de quelle question on parle.
