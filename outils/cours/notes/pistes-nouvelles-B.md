# Pistes nouvelles (passe B) : Ondes mécaniques progressives

*2026-11-07. Matière : `extraits_B.md` (phrases repérées par les marqueurs « image / analogie » et « méthode / astuce »), et pour chaque piste retenue, relecture du passage dans `transcripts/<videoId>.ar-orig.txt`. Comparaison faite avec `experience_profs.json` (ondes_mecaniques) et la note `experience-profs-ondes-synthese.md`. Rien n'a été modifié dans le dépôt.*

## 0. Avertissement : les noms de profs sont faux dans extraits_B.md

Le script `analyse2.py` (dictionnaire `PROFS`) associe les vidéos aux mauvais profs. La table de la note de synthèse est la bonne ; vérification faite sur des passages connus (règle de signe de Laksabi « pas efficace dans tous les cas », national 2018 chez Chargui, μ et longueur de la bosse chez Taousse, robinet chez Adrar).

| Étiquette dans extraits_B | Vidéo | Vrai prof |
|---|---|---|
| TOP | 00vbZrDiky0 | **Driss DOTCOM** |
| Chargui | 27FyalYEXhg | **Taousse** |
| Noureddine | GW-FyuY-rpA | Noureddine (en classe), juste |
| Noureddine live | W9XwPFD0sMU | **Laksabi** |
| Driss | XLQdN4C9L5g | **AdrarPhysic** |
| Taousse | YCzE0EZvsC8 | **TOP (cours)** |
| AdrarPhysic | iCQNAgZZors | **bacfacile** |
| Laksabi | lyiJmLP67Dk | **Chargui** |
| BacFacile | vG-rfo1TLAA | **TOP (série)** |

Ci-dessous, les **vrais** noms sont utilisés ; l'horodatage est celui de la vidéo.

**Bilan honnête.** Sur environ 450 lignes, à peu près les deux tiers sont du bruit : transcription illisible (surtout Noureddine en classe), publicité, mots « ديما » ou « بحال » sans contenu. Aucune image de stade, domino ou file d'attente n'apparaît. Les pistes vraiment nouvelles sont une quinzaine ; les autres affinent des entrées existantes.

---

## 1. Analogies et images du quotidien

| # | Piste | Source | Citation (telle quelle) | Nouveau / affine | Programme | Physique |
|---|---|---|---|---|---|---|
| A1 | **Voyage en voiture pour y_M(t) = y_S(t − τ)** : partir de S à 8 h, arriver en M à « 8 h + durée du trajet » ; arrivé en M à 8 h, parti de S à « 8 h − durée du trajet ». Donne le signe sans règle mécanique. | Driss 30:00-31:00 | « تحركات مع الثمانية ناقص مدة الرحلة, هادي هي اللي صحيحة » | **Nouveau** (analogies_validees). Répond au piège « signe ± appliqué par une règle apprise ». | Au programme | Juste : le retard est une durée de trajet ; l'élongation se transporte sans changer de forme. |
| A2 | Variante de l'horloge : remonter le temps en soustrayant des heures (« enlever quatre heures pour revenir »). | TOP cours 24:30 | « نقص من واحد اربع ساعه ولا شي حاجه باش نرجع كنا في الاول » | Affine A1 (transcription en partie illisible) | Au programme | Juste |
| A3 | **Autoroute Casa → Rabat** : même distance, l'un roule à 120 km/h et l'autre à 50 ; le plus rapide arrive le premier, la durée la plus courte va avec la plus grande vitesse. Sert au cas « même distance L dans l'eau et dans l'air ». | Laksabi 201:00 et 203:30 | « أنا فاش مشيت للرباط في 45 دقيقة صاحبي مشى في ساعة ونص » | **Nouveau** (analogie pour cas_types.deux_milieux) | Au programme | Juste |
| A4 | **Piscine** : un haut-parleur dans l'eau, l'air au-dessus, deux récepteurs ; qui détecte le premier ? Celui de l'eau. | Laksabi 199:00-200:30 | « بحال البيسين البيسين الماء ديالو ... فوق من الماء راه كاين ليغ » | **Nouveau** (mise en situation pour deux_milieux) | Au programme | Juste |
| A5 | **« Salam alaykoum » qui part à 340 m/s** ; en classe, le premier et le dernier rang l'entendent « en même temps », le décalage existe mais n'est pas perçu. | Laksabi 115:00-116:00 | « تخيل معايا هذا السلام عليكم خارجة بواحد السرعة ديال 340 مترو في الثانية » | **Nouveau** (image du retard du son) | Au programme | Juste. Ordre de grandeur : 10 m / 340 m/s ≈ 30 ms. Ajouter « vers 20 °C ». |
| A6 | **Le mur des voisins** : on entend la rue ou les voisins à travers le mur, donc le son traverse les solides. Sous l'eau, à la piscine ou à la mer, on entend aussi. | Laksabi 152:30-153:00 ; Adrar 8:00 | « شو بينك وبين جيرانك هو الحائط ... الصوت كيخترق ذاك الحائط » | **Nouveau** (analogies_validees ; s'oppose à l'entrée a_ne_pas_dire « un solide n'est pas élastique ») | Au programme | Image juste. **À corriger** : Laksabi enchaîne aussitôt sur « le problème, c'est la densité ». Garder l'image, jamais l'explication. |
| A7 | **« Molécule frappe molécule »** : la perturbation passe de proche en proche jusqu'à l'oreille. | Laksabi 154:30-155:00 | « وحدة كتضرب وحدة. جزيئة كتضرب جزيئة » | Nouveau, **à compléter** | Au programme | Image incomplète : seule, elle laisse croire que la molécule voyage jusqu'à l'oreille. Il faut ajouter « chacune pousse sa voisine et revient à sa place ». |
| A8 | **Membrane du haut-parleur** qui pousse puis tire l'air : compressions qui se transmettent jusqu'à l'oreille, onde longitudinale. | TOP cours 6:00-6:30 ; Driss 10:00 | « واحد الغشاء هنا يتحرك ... تضغط واحد شويه الهواء » | Nouveau (image du son longitudinal) | Au programme | Juste, à condition de dire aussi « dilatations » quand la membrane recule. |
| A9 | **Une personne suspendue dans un grand ressort** : à l'arrivée de l'onde, elle se sent aller et venir le long de l'axe. Montre la perturbation longitudinale vue de l'intérieur. | Driss 9:30 | « واحد الشخص مثلا معلق مثلا في واحد النابض كبير ... غيحس براسو مشا وجا » | **Nouveau** | Au programme | Juste. Driss ajoute ensuite que le ressort est « toujours » longitudinal (10:00) : c'est le piège déjà listé, et un 2ᵉ prof le commet. |
| A10 | Le ressort, c'est « la spirale du cahier » ou le ressort d'amortisseur de voiture ou de moto. | Driss 9:00 | « النابض داير بحال السلك ديال الدفتر » | Nouveau (vocabulaire concret) | Au programme | Juste |
| A11 | **La main comme une bosse** qui avance : les doigts à l'avant montent, l'arrière descend. Version gestuelle de la coupe de la bosse au sommet. | Driss 24:00-24:30 | « هذه اليد ديالي مثلا تخيلها عبارة على موجة » | Affine cas_types.etat_vibratoire | Au programme | Juste pour une bosse « vers le haut » qui avance vers la droite. Le tuteur doit préciser le sens de propagation. |
| A12 | **Le tableau vu comme une surface d'eau** pour une onde à 2 dimensions ; corde et ressort à 1 dimension ; son à 3 dimensions (« quand tu parles, ça part dans toutes les directions »). | Driss 14:00-14:30, 23:30 ; TOP cours 4:00 | « إلا تخيلتي مثلا هذه السبورة أخوتي عبارة مثلا على واحد السطح ديال الماء » | Nouveau : `dimensions` n'a ni exemple ni analogie dans le JSON | Au programme (notion « une, deux ou trois dimensions ») | Juste |
| A13 | **« Cinq quoi ? »** : « apporte-moi cinq élastiques », cinq paquets ou cinq mètres ? Un nombre sans unité n'a pas de sens. | Driss 21:30 | « واش خمسة د الباكيات ديال اللاستيك؟ ولا خمسة مترو ديال اللاستيك؟ » | Affine pieges « résultat sans unité » | Au programme (méthode) | Juste |
| A14 | **« الكعيبيبة »** (la petite bosse) pour la perturbation, opposée à la corde entière quand on calcule μ. | Taousse 35:00 | « هادي المسافة اللي قطعتها الكعيبيبة والكعيبيبة هي الموجة » | Affine piège « μ = m/L avec L la bosse » (mot darija utile) | Formule de la célérité hors programme à retenir ; exploitation au programme si elle est donnée | Juste |
| A15 | **Tsunami** : v = √(g·h), donc l'onde ralentit à l'approche de la côte, quand la profondeur diminue. Exercice cité comme « posé en 2014 ». | Chargui 51:30-52:00 | « قد ما كن قربوا الشط ديال البحر قد ما سرعه الانتشار كتن قص » | **Nouveau** (exemple concret du facteur « profondeur de l'eau ») | Au programme si la formule est donnée (perimetre.json : « profondeur de l'eau » est un facteur) ; ne jamais la faire apprendre | Juste qualitativement. La valeur « 250 km/h » qu'il donne pour le large est douteuse : avec h = 4 000 m, √(g·h) ≈ 200 m/s ≈ 700 km/h. **À ne pas reprendre.** La date du national 2014 est aussi à vérifier. |

Images cherchées et **absentes** : stade (ola), domino, file d'attente, slinky au sens propre (seulement « ressort »), pierre dans l'eau (une seule mention, chez Adrar 1:30, sans exploitation).

---

## 2. Méthodes pas à pas et règles pratiques

| # | Piste | Source | Citation | Nouveau / affine | Programme | Physique |
|---|---|---|---|---|---|---|
| M1 | **Dessiner l'aspect à une date t** : d = v·t en m ; reconvertir en cm (×10²) pour l'échelle du schéma ; compter les carreaux depuis S ; placer le front ; recopier la même bosse, même hauteur et même longueur (« monte d'un carreau et demi, descend d'un carreau et demi »). | TOP série 11:30-13:00 ; Driss 29:30 | « طالع حى انا طالع من بعد عندي هابط حتى انا عندي هابط بنفس الطريقه » | **Nouveau** : le dessin de l'aspect n'a pas de méthode dans cas_types, alors que la synthèse le dit fréquent en contrôle | Au programme | Juste. Ajouter : le front est du côté de la propagation, et la forme est conservée (pas d'amortissement dans les exercices). |
| M2 | **Reconnaître l'émetteur et le récepteur sur l'oscillogramme par l'amplitude** : le signal émis est grand, le reçu plus petit, parce que l'onde s'affaiblit en s'éloignant. | Driss 18:30-19:00 | « اللي كنصيفطوه هو اللي كيكون لومبليتيد ديالو كبير واللي كنستقبلوه ... صغير » | **Nouveau** (aide de lecture pour cas_types.oscillogramme) | Au programme (TP célérité) | Juste en pratique. Préciser : l'amplitude baisse, la **célérité ne change pas**. Le critère sûr reste l'ordre d'arrivée. |
| M3 | **Passer de l'aspect y(x) à l'élongation y(t)** : chaque longueur lue sur l'aspect se convertit en durée par Δt = Δx / v (bosse de 4 cm à 5 m/s, 8 ms de montée), puis on dessine. Le début du mouvement est à gauche sur y(t) ; sur l'aspect, le front est du côté de la propagation. | Noureddine 59:30-60:30 ; TOP série 34:00-36:00 | « منين تبغي تقلب على النقطه امتى كتحرك في ليلونغاسيون كنشوفوا من هنا ... اما الا كنت كتكلم على لاسبي هذك حاجه اخرى » | Affine etat_vibratoire et la synthèse B.2 (« retourner l'aspect ») : ajoute le **calcul** de chaque durée | Au programme | Juste |
| M4 | **θ se lit de deux façons** : sur y(t), c'est la largeur de la bosse en temps (2 carreaux × 1 ms = 2 ms), la même pour **tous** les points ; sur l'aspect, c'est θ = longueur de la bosse / v. « Ne prends pas un Δt sur l'aspect. » | TOP série 35:00-36:00 | « كل نقطه غادي تدوز هذا الوقت هذا » / « فا عطاوني لاسبي ماغاديش نخرج ديالطاطي تي من هنا » | Affine etat_vibratoire | Au programme | Juste |
| M5 | **Contrôler un réarrangement algébrique par le calcul** : à mi-chemin, calculer numériquement l'expression avant et après la transformation ; si les deux valeurs sont égales, c'est juste ; sinon, l'erreur est dans l'une des deux. | Noureddine 33:00-34:00 | « لقيت بحالها متاكد منها صحيحه لقيت ماشي بحالها اما خطئ في الاول اما خطئ في الثاني » | **Nouveau** remède au piège « inverser une différence de fractions terme à terme » | Au programme (méthode) | Juste |
| M6 | **Prendre l'inverse renverse l'inégalité** : L/t_eau > L/t_air ⇒ t_eau < t_air. Le milieu le plus rapide met le moins de temps. | Laksabi 204:00-204:30 | « إلا قلبت غيتقلب معاهم الرمز » | Affine deux_milieux et le piège « τ négatif » | Au programme | Juste pour des grandeurs positives |
| M7 | **Raisonner avec des nombres inventés** : « supposons 3 ms dans l'eau, donc 5 ms dans l'air », puis on rapproche un micro et on voit ce qui change. Permet de trancher un QCM qualitatif sans formule. | Laksabi 225:30-226:30 | « غنديرو إفتراض إفتراض سمع إفتراض ... ثلاثة ميلي سكوند » | **Nouveau** (méthode pour le cas geometrie et les QCM) | Au programme | Juste, à condition que les valeurs inventées respectent l'ordre (le plus lent prend plus de temps). |
| M8 | **Photos d'une caméra à cadence connue** : 25 images/s, donc 1/25 s = 40 ms entre deux images. Retard entre l'image n° 2 et l'image n° 8 = 6 × 40 ms = 0,24 s. « Il n'y a ni distance ni vitesse : il faut seulement faire attention. » | Laksabi 55:00-58:00 | « كتضرب 25 تصويرة في الثانية ... أعطيني لو غوطاغ طومبوغيل أونطغ إيماج ويت إي دوز » | **Nouveau** (variante de cas_types.photo : date donnée par un numéro d'image) | Au programme. Laksabi l'attribue au national sans se souvenir de l'année : **à vérifier** | Juste |
| M9 | **Lire « v = 4 000 m/s » en mots** : chaque seconde, le signal parcourt 4 000 m. Donne du sens au nombre avant de le comparer à la valeur repère. | TOP série 19:30 | « تخيل في كل ثانيه ذاك السينيال مشى 4000 متر » | Affine R11 (vérifier l'ordre de grandeur) | Au programme | Juste |
| M10 | **Sens des conversions** : vers l'unité SI, on multiplie par 10⁻ⁿ (cm → m : ×10⁻²) ; pour revenir à l'échelle du schéma, par 10⁺ⁿ (m → cm : ×10²). Laksabi se trompe en direct, puis se corrige à voix haute. | Laksabi 98:30, 174:00 ; TOP série 11:30 | « رجعت بالعكس من الميتغ للسنتيمتر ... غايعطيك 68 سنتيمتر » | Affine insistances « conversions » : le sens retour manque dans le JSON | Au programme | Juste |
| M11 | **Chasser la racine d'une formule donnée** : élever les deux membres au carré (v² = T/μ), puis isoler ; une fraction de fraction a/(b/c) devient a·c/b. Exemple : trouver m quand T, v et L sont donnés. | Taousse 32:30-34:00 ; TOP cours 23:00 | « درنا اوكاري على اليسار وعلى اليمين ... باش نحيدو الغاسين » | Nouveau (geste algébrique) | La formule est hors programme à retenir ; la manipuler quand l'énoncé la donne est au programme | Juste |
| M12 | **Mesurer τ du début au début, ou de la fin à la fin** | Chargui 57:00 | « من بدايه الارسال حتى بدايه الاستقبال ولا ... من نهايه الارسال حتى نهايه الاستقبال » | Déjà dans le JSON (oscillogramme) : rien de nouveau | Au programme | Juste |
| M13 | **Une graduation peut valoir deux carreaux** : « il t'a tracé deux carreaux, pas un ». | Laksabi 107:30-108:30 | « راه جر لك جوج مربعات, ماشي مربع » | Déjà dans la synthèse (B.4) : rien de nouveau | Au programme | Juste |

---

## 3. Exemples chiffrés réutilisables (valeurs vérifiées)

| # | Situation | Valeurs | Résultat | Source | Programme |
|---|---|---|---|---|---|
| N1 | Deux micros, son dans l'air | d = 85 cm ; 5 div × 0,5 ms/div = 2,5 ms | v = 340 m/s | Driss 19:00-20:30 | Au programme |
| N2 | Corde photographiée | SM = 16 cm, t = 40 ms | v = 4 m/s | Driss 25:30 | Au programme |
| N3 | Barre métallique frappée au marteau, deux capteurs | d = 40 cm, τ = 100 µs | v = 4 000 m/s | TOP série 14:00-19:30 | Au programme |
| N4 | Même distance, mais avec deux micros dans l'air | d = 40 cm, v = 340 m/s | τ ≈ 1,2 ms (à comparer à 100 µs dans le métal) | TOP série 16:00-20:30 | Au programme |
| N5 | Élongation y_M(t) | SM = 20 cm, τ = 4 ms ; θ = 2 ms | v = 50 m/s ; L = v·θ = 10 cm | TOP série 33:30-35:30 | Au programme |
| N6 | Retard entre deux points (deux voies) | SM = 20 cm, SN = 50 cm, v = 50 m/s | τ_MN = 0,30/50 = 6 ms ; contrôle : t_N − t_M = 10 − 4 = 6 ms | TOP série 36:00-37:30 | Au programme |
| N7 | Aspect à dessiner | v = 4 m/s, t = 3×10⁻² s | front à 12 cm de S | TOP série 11:30-12:30 | Au programme |
| N8 | Front de la corde | SM = 8 cm, v = 4 m/s, t₀ = 0 | t = 0,02 s | TOP cours 16:00-16:30 | Au programme |
| N9 | Retard entre M et N | MN = 8 cm, v = 2 m/s | τ = 0,04 s | TOP cours 18:30 | Au programme |
| N10 | Formule donnée v = √(T/μ) | T = 45 N, μ = 5 kg/m | v = 3 m/s | TOP série 24:00 | Formule donnée par l'énoncé |
| N11 | Caméra | 25 images/s ; images n° 2 et n° 8 | τ = 0,24 s | Laksabi 55:00-58:00 | Au programme |
| N12 | Retard en classe (à construire, inspiré de A5) | 10 m, 340 m/s | ≈ 29 ms, imperceptible | Laksabi 115:30 (sans chiffres) | Au programme |

Les chiffres de Taousse pour μ (T = 2 N, v = 2 m/s, m = 0,25 kg) sont mal transcrits : L n'est pas lisible. Ne pas les reprendre sans la vidéo.

---

## 4. Formulations darija qui expliquent bien

| # | Formulation | Notion | Source |
|---|---|---|---|
| D1 | « إلى وصلات مع ... إم ... تحركات مع ... ناقص مدة الرحلة » | t − τ | Driss 30:30-31:00 |
| D2 | « كلما كانت الفيتيس كبيرة، كلما غيكون المدة قصيرة » | relation inverse v / durée | Laksabi 201:30 |
| D3 | « ديما ذوك لي بوان اللي جاو في المقدمة ديال لوند كيبداو يصعدوا » | sens du mouvement | Driss 24:30 |
| D4 | « غير ثانية وحدة كتمشي 340 مترو » | sens physique de la célérité | Laksabi 115:00 |
| D5 | « كل نقطه غادي تدوز هذا الوقت هذا » | θ identique pour tous les points | TOP série 35:00 |
| D6 | « هذه ما كتحتاجش أنك تكون قاري الدرس. كتحتاج أنك ترد البال » | lire l'énoncé (cas caméra) | Laksabi 58:00 |
| D7 | « الكعيبيبة هي الموجة » / « لونغوغ ديال الحبل كامل » | bosse ≠ corde entière | Taousse 35:00 |
| D8 | « الموجة كتخرج من هنا قوية ... وكتضعاف » | reconnaître le signal émis (à nuancer : pas la célérité) | Driss 18:30 |

---

## 5. À signaler (erreurs ou approximations nouvelles)

- **Driss 10:00** : « le ressort, c'est **toujours** parallèle » (longitudinal). C'est le même piège que Taousse ; il est donc commis par 2 profs.
- **Driss 19:30-20:00** : 340 m/s « selon la température **et la densité** ». C'est la même famille d'erreur que « plus dense, plus rapide ».
- **Laksabi 90:30** : « plus la fréquence monte, plus on t'entend », et sous 20 Hz, « comme si je parlais dans ma tête ». C'est faux : l'audibilité dépend de la plage 20 Hz – 20 kHz, et au-delà de 20 kHz on n'entend plus rien. L'erreur est voisine de « chuchoter = basse fréquence », déjà listée.
- **Chargui 52:00** : tsunami à 250 km/h au large. La valeur est douteuse (environ 700 km/h pour 4 000 m de fond).
- **Laksabi 154:30** : « molécule frappe molécule », sans le retour à la place. Il faut le compléter (voir A7).

## 6. Bruit écarté

- Noureddine en classe : la plupart des lignes sont illisibles (passage « فاز », citrons et couleurs vers 99:00-105:00). Il s'agit probablement de points en phase, donc du chapitre suivant.
- Laksabi 78:00 : salves ultrasonores « sinusoïdales », chapitre suivant.
- Publicités (Driss 39:30, Chargui 51:00, Taousse 51:00), encouragements, et lignes qui contiennent seulement « ديما », « أول حاجة » ou « بحال بحال ».
