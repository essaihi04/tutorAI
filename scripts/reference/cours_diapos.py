"""Les 41 diapositives du cours de référence SVT « Consommation de la matière organique et flux d'énergie ».

Contrat : docs/reference-svt/ARCHITECTURE.md. Ce fichier est lu par construire_cours.py.

Dans le texte dit (`mx`), une balise posée juste devant un mot devient un geste au moment où la voix dit ce mot :
  <m:moment>        la simulation joue jusqu'à ce moment (`play_until`), <m:moment:1.8> avec une durée ;
  <r:repere>        la baguette se pose sur ce repère ;
  <c:texte>         la carte s'écrit au centre (formule, équation, définition).
Le générateur retire les balises et calcule le `mot` exact (extrait du texte dit).
"""

REF = "/media/simulations/svt/reference_consommation_mo-tableau/"
RAP = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/"

# Étapes de la démarche d'investigation (fil dessiné en haut à droite des pages, ?demarche=1..6)
DEMARCHE = {1: "Problème", 2: "Hypothèse", 3: "Expérience", 4: "Résultats", 5: "Analyse", 6: "Conclusion"}

D = []


def diapo(**k):
    D.append(k)


# ───────────────────────── Séance 1 — bloc 1 : une question et trois rappels ─────────────────────────

diapo(
    id="rf_ouverture_cours", type="situation", ouverture=True,
    titre="Consommation de la matière organique et flux d'énergie",
    lead="Bienvenue : ce qu'on va apprendre, et pourquoi c'est utile au bac.",
    montre="Aucune animation : trois cartes s'écrivent quand la voix les dit.",
    fr="Bienvenue dans un nouveau cours : Consommation de la matière organique, et flux d'énergie. Dans ce cours, "
       "nous allons apprendre comment la cellule tire son énergie du glucose : la respiration, la fermentation, la "
       "glycolyse et la mitochondrie. Au national, ce domaine compte pour vingt-cinq pour cent de la note, et il "
       "revient à chaque examen. Nous allons suivre une molécule de glucose tout au long de son chemin, comme un "
       "voyage. Comment allons-nous travailler ? Tu écoutes bien, tu réponds aux questions au tableau, et quand le "
       "cours s'arrête, tu écris dans ton cahier. Allons-y !",
    mx="مرحبا بيك فدرس جديد: Consommation de la matière organique، et flux d'énergie. فهاد الدرس "
       "<c:On apprend : respiration, fermentation, glycolyse, mitochondrie>غادي نتعلمو كيفاش la cellule كتاخد "
       "l'énergie من le glucose: la respiration، la fermentation، la glycolyse، و la mitochondrie. "
       "<c:Au bac : ce domaine = 25 % de la note>فle national، هاد الجزء عندو vingt-cinq pour cent ديال النقط، "
       "وكيجي ف كل امتحان. وغادي نتبعو واحد la molécule ديال le glucose ف الطريق ديالها كاملة، بحال شي رحلة. "
       "<c:Écouter · répondre au tableau · écrire dans le cahier>كيفاش غادي نخدمو؟ تسمع مزيان، تجاوب على الأسئلة "
       "فالسبورة، وملي يوقف الدرس، تكتب ف الدفتر ديالك. يلا نبداو!",
    bullets=["On apprend : respiration, fermentation, glycolyse, mitochondrie", "Au bac : ce domaine = 25 % de la note",
             "Écouter · répondre au tableau · écrire dans le cahier"],
    cahier="On apprend : respiration, fermentation, glycolyse, mitochondrie.",
)

diapo(
    id="rf_o1_pate", type="situation", demarche=1,
    titre="Pourquoi la pâte à pain gonfle-t-elle ?",
    lead="La levure du boulanger est vivante : elle a besoin d'énergie.",
    page=REF + "pate.html", legende="La pâte à pain et la levure",
    alt="Un bol de pâte à pain, un sachet de levure ; la pâte gonfle, une loupe montre des levures et des bulles",
    montre="La pâte plate dans son bol, le sachet de levure versé, la pâte qui double ; la loupe montre les levures "
           "et les bulles de gaz ; le problème du cours s'écrit.",
    fr="Regarde ce pain avant la cuisson : de la farine et de l'eau, il est encore petit. On lui ajoute la levure, "
       "celle que l'on achète à l'épicerie. On le laisse une heure, et regarde : il a monté, il a grossi ! Pourquoi ? "
       "Si on s'approche beaucoup, on trouve les levures : de très petits êtres vivants, qui rejettent un gaz, et ce "
       "gaz gonfle le pain. Et ce qui est vivant a besoin d'énergie. Voici donc le problème du cours : d'où la "
       "cellule tire-t-elle son énergie. Cette question nous suivra jusqu'à la fin.",
    mx="شوف هاد <m:bol>الخبز قبل ما يدخل للفران: <r:pate>باقي صغير. <m:levure_ajoutee>كنزيدو ليه la levure، "
       "<r:sachet>هاد الخميرة اللي كتشريها من عند مول الحانوت. كنخليوه واحد الساعة، <m:gonfle>وشوف: الخبز طلع "
       "وكبر! علاش؟ <m:zoom>يلا قربنا بزاف، كنلقاو <r:levures>les levures: كائنات حية صغار بزاف، <r:bulles>وكيخرج "
       "منهم un gaz، هو اللي كيطلع الخبز. واللي حي، خاصو l'énergie باش يخدم. <m:question>إذن هادا هو le problème "
       "ديال الدرس: <r:question>منين كتجيب la cellule، l'énergie ديالها. هاد السؤال غادي يبقى معانا حتى للخر.",
    bullets=["La levure fait gonfler la pâte : elle vit, elle rejette un gaz.",
             "Problème : d'où une cellule tire-t-elle son énergie ?"],
    cahier="Problème : d'où une cellule tire-t-elle son énergie ?",
)

diapo(
    id="rf_r1_cellule", type="simulation",
    titre="Rappel : la cellule",
    lead="Une cellule : la membrane, le hyaloplasme, le noyau et des organites.",
    page=RAP + "depart.html?vue=cellule", legende="La cellule",
    alt="Une cellule peinte : membrane, hyaloplasme, noyau, mitochondries ; la même cellule vue comme une petite ville",
    montre="La cellule se dessine partie par partie (membrane plasmique, hyaloplasme, noyau, mitochondries), puis "
           "elle est comparée à une petite ville.",
    fr="Avant de répondre, il faut savoir où tout se passe : dans la cellule, la plus petite partie vivante. Voici "
       "une cellule. Autour, la membrane plasmique. L'intérieur est rempli d'un liquide : le hyaloplasme. Au milieu, "
       "le noyau, qui commande. Et il y a de petits éléments allongés : les mitochondries, qui font partie des "
       "organites. Autrement dit : la cellule est comme une petite ville. Le noyau est le directeur, le hyaloplasme "
       "ce sont les rues, et les mitochondries sont comme de petites usines. Ce que produisent ces usines, nous "
       "allons le découvrir.",
    mx="قبل ما نجاوبو، خاصنا نعرفو فين كيوقع كلشي: <m:d_cellule>ف la cellule، أصغر جزء حي. <r:cellule>شوف هاد "
       "الخلية. <m:d_membrane>داير بيها <r:membrane>la membrane plasmique. <m:d_hyaloplasme>الداخل ديالها عامر ب "
       "واحد السائل: <r:hyaloplasme>le hyaloplasme. <m:d_noyau>ف الوسط <r:noyau>le noyau، هو اللي كيتحكم. "
       "<m:d_mitochondries>وكاينين شي حوايج صغار وطوال: <r:mitochondries>les mitochondries، وهادو من les organites. "
       "بطريقة أخرى: <m:d_ville>الخلية بحال واحد <r:ville>البلاد صغيرة. <m:d_mairie>le noyau هو المدير، "
       "<m:d_rues>le hyaloplasme هو الطرقان، <m:d_usines>و les mitochondries <r:usines>بحال شي معامل صغار. شنو "
       "كينتجو هاد المعامل، هادا اللي غادي نعرفو ف هاد الدرس.",
    bullets=["La cellule est la plus petite partie vivante.", "Hyaloplasme : le liquide de la cellule."],
    cahier="Rappel : la cellule : membrane plasmique, hyaloplasme, noyau, organites (mitochondries).",
)

diapo(
    id="rf_r2_glucose", type="simulation",
    titre="Rappel : le glucose, de l'énergie rangée",
    lead="Le glucose C₆H₁₂O₆ : une matière organique à six carbones, riche en énergie.",
    page=RAP + "depart.html?vue=glucose", legende="Le glucose",
    alt="Du pain, le glucose dans le sang, puis la molécule de glucose : une chaîne de six billes jaunes",
    montre="Le pain (amidon), le glucose dans le sang, la molécule de glucose en chaîne de six billes jaunes, "
           "l'énergie dans ses liaisons, les liaisons qui se cassent.",
    fr="Bien, nous connaissons la cellule. Et la matière organique qu'elle consomme, qu'est-ce que c'est ? Le pain "
       "que tu manges contient de l'amidon. Dans le corps, il est coupé et devient du glucose, qui passe dans le sang "
       "jusqu'aux cellules. Le glucose est une molécule à six carbones : C6H12O6. Nous le dessinerons toujours ainsi : "
       "une chaîne de six billes jaunes. Son énergie se trouve dans les liaisons entre les atomes. Quand la cellule "
       "coupe ces liaisons, l'énergie sort. Autrement dit : le glucose est comme un billet de cent dirhams : une "
       "grande valeur, mais rangée dans un seul billet.",
    mx="مزيان، عرفنا الخلية. و la matière organique اللي كتستهلك، شنو هي؟ <m:g_pain>الخبز اللي كتاكل <r:pain>فيه "
       "l'amidon. <m:g_sang>ف الجسم كيتقسم، ويولي glucose، <r:sang>وكيدوز ف الدم حتى ل les cellules. "
       "<m:g_molecule>le glucose هو une molécule <r:molecule>فيها six carbones: <c:Glucose : C₆H₁₂O₆ (6 carbones)>C "
       "six H douze O six. غادي نرسمو le glucose ديما هكا: سلسلة فيها ستة ديال الكورات. <m:g_liaisons>و l'énergie ديالو "
       "<r:liaisons>كاينة ف les liaisons اللي بين les atomes. <m:g_casser>ملي la cellule كتقسم هاد les liaisons، "
       "l'énergie كتخرج. بطريقة أخرى: <c:Glucose = un billet de 100 dirhams : de l'énergie rangée>le glucose بحال "
       "ورقة ديال مية درهم: فيها قيمة كبيرة، ولكن مجموعة ف ورقة وحدة.",
    bullets=["Glucose : C₆H₁₂O₆, une chaîne de 6 carbones.", "Son énergie est dans ses liaisons."],
    cahier="Rappel : le glucose C₆H₁₂O₆ est une matière organique riche en énergie.",
)

diapo(
    id="rf_r3_levure", type="simulation",
    titre="La levure : une seule cellule",
    lead="Un champignon unicellulaire, qui vit avec ou sans dioxygène.",
    page=REF + "levure.html", legende="La levure au microscope",
    alt="Un microscope, des levures bourgeonnantes, une levure agrandie, un bocal ouvert et un bocal fermé",
    montre="Le microscope et sa lame, le champ de levures avec sa barre d'échelle, une levure agrandie et ses "
           "parties, puis le bocal ouvert (aérobie) et le bocal fermé (anaérobie), les deux mots découpés.",
    fr="Revenons à la levure du pain. Si on la place sous le microscope, on voit beaucoup de petites boules : "
       "chacune est une seule cellule. La levure est donc un champignon unicellulaire : un être vivant fait d'une "
       "seule cellule. Elle contient tout ce que nous avons vu : le noyau, le hyaloplasme et les mitochondries. Et la "
       "levure a une belle particularité : elle travaille dans deux situations. Avec le dioxygène, on dit milieu "
       "aérobie : aéro veut dire l'air. Sans dioxygène, on dit milieu anaérobie : an veut dire sans. Tout "
       "simplement : aérobie, il y a du dioxygène ; anaérobie, il n'y en a pas.",
    mx="نرجعو دابا ل la levure ديال الخبز. <m:microscope>يلا درناها تحت <r:microscope>le microscope، "
       "<m:champ>كنشوفو بزاف ديال الكورات صغار: <r:echelle>كل وحدة هي خلية وحدة. إذن la levure، champignon "
       "unicellulaire: كائن حي فيه خلية وحدة. <m:une_cellule>وفيها كلشي اللي شفنا: <r:noyau>le noyau، "
       "<r:hyaloplasme>le hyaloplasme، <r:mitochondrie>و les mitochondries. و la levure عندها حاجة زوينة: كتخدم ف "
       "جوج ديال الحالات. <m:aerobie>مع le dioxygène، <r:bocal_ouvert>كنقولو milieu aérobie: aéro يعني الهوا. "
       "<m:anaerobie>وبلا dioxygène، <r:bocal_ferme>كنقولو milieu anaérobie: an يعني بلا. يعني ببساطة: aérobie فيه "
       "le dioxygène، و anaérobie ما فيهش.",
    bullets=["Levure : champignon unicellulaire.", "Aérobie : avec dioxygène ; anaérobie : sans dioxygène."],
    cahier="Milieu aérobie : il contient du dioxygène. Milieu anaérobie : il n'en contient pas.",
)

# ───────────────────────── Séance 2 — bloc 2 : la respiration ─────────────────────────

diapo(
    id="rf_a1_montage", type="simulation", demarche=3, comp=["C1"],
    titre="Le montage ExAO",
    lead="L'expérience assistée par ordinateur : chaque élément, et ce qu'il mesure.",
    page=REF + "exao-levures.html?vue=montage&demarche=3", legende="Le montage ExAO",
    alt="Un bioréacteur avec sa suspension de levures, l'agitateur, deux sondes, une seringue, l'interface et l'ordinateur",
    montre="Le montage arrive un élément à la fois : bioréacteur, suspension de levures, agitateur qui tourne, sonde "
           "à dioxygène, sonde à CO₂, seringue de glucose, interface, ordinateur.",
    fr="Pour savoir d'où la levure tire son énergie, il nous faut une expérience. Voici le montage de l'ExAO, "
       "l'expérience assistée par ordinateur. Ce récipient, c'est le bioréacteur. Il contient de l'eau avec les "
       "levures : la suspension de levures. En bas, l'agitateur tourne, pour que les levures restent partout. Voici "
       "la sonde à dioxygène : elle mesure combien il y en a dans l'eau. Et voici la sonde à dioxyde de carbone. En "
       "haut, la seringue, qui contient le glucose. Les sondes sont reliées à l'interface, qui envoie les mesures à "
       "l'ordinateur, où apparaissent les courbes. Donc l'ExAO : une expérience, et c'est l'ordinateur qui mesure.",
    mx="باش نعرفو منين كتجيب la levure l'énergie، خاصنا تجربة. هادا هو <m:bioreacteur>le montage ديال l'ExAO، يعني "
       "l'expérience assistée par ordinateur. <r:bioreacteur>هاد الكاس سميتو le bioréacteur. <m:suspension>فيه الما "
       "مع les levures: <r:suspension>la suspension de levures. <m:agitateur>لتحت <r:agitateur>l'agitateur كيدور، باش "
       "les levures يبقاو ف كل بلاصة. <m:sonde_o2>هادي <r:sonde_o2>la sonde ديال le dioxygène: كتعطينا شحال كاين "
       "منو ف الما. <m:sonde_co2>وهادي <r:sonde_co2>la sonde ديال le dioxyde de carbone. <m:seringue>ومن الفوق "
       "<r:seringue>la seringue، وفيها le glucose. <m:interface>les sondes مربوطة مع <r:interface>l'interface، "
       "<m:ordinateur>وهي كتصيفط les mesures ل <r:ordinateur>l'ordinateur، وفيه كيبانو les courbes. "
       "<m:complet>إذن l'ExAO: تجربة، و l'ordinateur هو اللي كيحسب.",
    bullets=["ExAO : expérience assistée par ordinateur.", "Une sonde par gaz : dioxygène, dioxyde de carbone."],
    cahier="ExAO : des sondes mesurent le dioxygène et le CO₂ ; l'ordinateur trace les courbes.",
)

diapo(
    id="rf_a1_exp1_avant", type="simulation", demarche=3, comp=["C1"],
    titre="Expérience 1 : avant le glucose",
    lead="Hypothèse : si la levure utilise le glucose avec le dioxygène, alors le dioxygène doit baisser.",
    page=REF + "exao-levures.html?vue=exp1&depart=0&demarche=3", legende="Expérience 1 : les axes et les paliers",
    alt="L'écran de l'ordinateur : deux axes, puis deux paliers, le dioxygène à 5,3 mg/L et le CO₂ à 0,16 mmol/L",
    montre="Les axes sont lus (temps en minutes, dioxygène en mg/L, CO₂ en mmol/L), puis les deux paliers se "
           "tracent de 0 à 1,8 min : 5,3 mg/L et 0,16 mmol/L.",
    fr="Cette expérience a une hypothèse : si la levure utilise le glucose avec le dioxygène, alors le dioxygène "
       "doit diminuer dans l'eau. Maintenant l'expérience : avant toute courbe, on lit les axes. En bas, le temps, "
       "en minutes, de zéro à sept. À gauche, en rouge, le dioxygène, en milligrammes par litre. Et sur le deuxième "
       "axe, le dioxyde de carbone, en millimoles par litre. Voici les résultats du début, avant le glucose : le "
       "dioxygène est stable, à cinq virgule trois milligrammes par litre. Et le dioxyde de carbone est stable lui "
       "aussi, à zéro virgule seize millimole par litre. Sans glucose, rien ne change.",
    mx="هاد التجربة عندها hypothèse: يلا كانت la levure كتستعمل le glucose مع le dioxygène، إذن le dioxygène خاصو "
       "ينقص ف الما. دابا l'expérience: قبل أي courbe، <m:axes>كنقراو les axes. <r:axe_temps>لتحت le temps، en "
       "minutes، de zéro à sept. <r:axe_o2>على اليسار، بالأحمر، le dioxygène، en milligrammes par litre. "
       "<r:axe_co2>وف l'axe الثاني، le dioxyde de carbone، en millimoles par litre. <m:avant>وهادو les résultats ديال "
       "البداية، قبل le glucose: <r:courbe_o2>le dioxygène ثابت، ف cinq virgule trois milligrammes par litre. "
       "<r:courbe_co2>و le dioxyde de carbone ثابت حتى هو، ف zéro virgule seize millimole par litre. بلا glucose، ما "
       "كيتبدل والو.",
    bullets=["On lit les axes avant la courbe.", "Avant le glucose : deux paliers."],
    cahier="Avant de lire une courbe : la grandeur et l'unité de chaque axe.",
)

diapo(
    id="rf_a1_exp1_injection", type="simulation", demarche=4, comp=["C1"],
    titre="On injecte le glucose",
    lead="Les résultats : le dioxygène baisse jusqu'à 0, le dioxyde de carbone monte.",
    page=REF + "exao-levures.html?vue=exp1&depart=avant&demarche=4", legende="Expérience 1 : l'injection",
    alt="La seringue est poussée ; la courbe rouge du dioxygène descend jusqu'à zéro, la courbe du CO₂ monte",
    montre="La seringue est poussée à 1,8 min (flèche « injection glucose »). La page s'arrête : question. Puis le "
           "dioxygène descend jusqu'à 0 à 6,8 min pendant que les levures de la cuve absorbent les bulles, et le "
           "CO₂ monte de 0,16 à 0,31 mmol/L.",
    fr="Voici le moment de l'expérience. On pousse la seringue, et le glucose entre dans le bioréacteur. C'est "
       "l'injection, à un virgule huit minute. Rappelle-toi notre hypothèse, et regarde bien la courbe du dioxygène. "
       "Regarde les résultats : le dioxygène diminue, sans s'arrêter, jusqu'à zéro, à six virgule huit minutes. Les "
       "levures ont consommé tout le dioxygène ! Et en même temps, le dioxyde de carbone augmente, et il arrive à "
       "zéro virgule trente et un millimole par litre. Donc notre hypothèse est juste.",
    mx="جات اللحظة ديال التجربة. <m:injection>كندخلو le glucose ب <r:seringue>la seringue ل le bioréacteur. "
       "<r:fleche_injection>هادي l'injection، ف un virgule huit minute. تفكر l'hypothèse ديالنا، وشوف la courbe ديال "
       "le dioxygène مزيان. <m:o2_baisse>شوف les résultats: <r:courbe_o2>le dioxygène كينقص، وبلا ما يوقف، حتى كيوصل "
       "ل zéro، ف six virgule huit minutes. les levures كيستهلكو le dioxygène كامل! <m:co2_monte>وف نفس الوقت، "
       "<r:courbe_co2>le dioxyde de carbone كيطلع، وكيوصل ل zéro virgule trente et un millimole par litre. إذن "
       "l'hypothèse ديالنا صحيحة.",
    obs="rf_a1_exp1_injection",
    bullets=["Injection du glucose à 1,8 min.", "Le dioxygène baisse, le dioxyde de carbone monte."],
    cahier="Après l'injection du glucose, le dioxygène diminue et le CO₂ augmente.",
)

diapo(
    id="rf_a1_exp1_deduire", type="simulation", demarche=5, comp=["C1", "C2"], etoile=True,
    titre="Décrire, puis déduire",
    lead="La méthode du bac : je décris ce que je vois avec les valeurs, puis j'écris « donc ».",
    page=REF + "exao-levures.html?vue=exp1&depart=co2_monte&demarche=5", legende="Décrire, puis déduire",
    alt="Les deux courbes finies ; les phrases de description s'écrivent, puis la conclusion « respiration cellulaire »",
    montre="Les deux phrases de description s'écrivent sous les courbes avec leurs valeurs, puis la déduction : "
           "« respiration cellulaire ».",
    fr="Nous avons vu les résultats, il reste à les écrire comme à l'examen. Maintenant concentre-toi bien, c'est "
       "la méthode du national : on décrit, puis on déduit. D'abord, l'analyse : je dis ce que je vois, avec les "
       "valeurs. Après l'injection du glucose, le dioxygène diminue, de cinq virgule trois à zéro milligramme par "
       "litre. Et le dioxyde de carbone augmente, de zéro virgule seize à zéro virgule trente et un. Ensuite, "
       "j'écris donc : les levures absorbent le dioxygène et rejettent le dioxyde de carbone : c'est la respiration "
       "cellulaire. Autrement dit : la description, ce sont les yeux ; donc, c'est la tête. Je relis : absorption du "
       "dioxygène, et rejet du dioxyde de carbone : c'est la respiration cellulaire.",
    mx="شفنا les résultats، وباقي نكتبوهم بحال ف الامتحان. دابا ركز معايا مزيان، هادي الطريقة ديال le national: "
       "اللول la description، ومن بعد la déduction. <m:decrire>نبداو ب l'analyse: كنقول شنو كنشوف، مع les valeurs. "
       "<r:courbe_o2>Après l'injection du glucose, le dioxygène diminue, de cinq virgule trois, à zéro milligramme "
       "par litre. <r:courbe_co2>Et le dioxyde de carbone augmente, de zéro virgule seize, à zéro virgule trente et "
       "un. <m:deduire>ومن بعد، كنكتب donc: <c:Donc les levures absorbent O₂ et rejettent CO₂ : c'est la respiration "
       "cellulaire>les levures absorbent le dioxygène, et rejettent le dioxyde de carbone: <r:conclusion>c'est la "
       "respiration cellulaire. بطريقة أخرى: la description هي العينين، و donc هو الراس. نعاود نقرا: absorption du "
       "dioxygène, et rejet du dioxyde de carbone: c'est la respiration cellulaire.",
    bullets=["Décrire : « après…, le dioxygène diminue de… à… ».", "Déduire : « donc les levures respirent »."],
    cahier="Méthode : 1) lire les axes 2) décrire avec des valeurs 3) déduire (« donc… »)\n"
           "Absorption de dioxygène et rejet de CO₂ : c'est la respiration cellulaire.",
)

diapo(
    id="rf_a1_equation_respi", type="simulation", demarche=6, comp=["C2"], etoile=True,
    titre="L'équation de la respiration",
    lead="Un glucose et six dioxygènes : six CO₂, six H₂O et beaucoup d'énergie.",
    page=REF + "equation.html?vue=respiration&demarche=6", legende="L'équation de la respiration",
    alt="Le glucose en six billes jaunes, six molécules de dioxygène, puis six CO₂, six H₂O et un éclat d'énergie",
    montre="Le glucose (six billes jaunes), six O₂ qui arrivent comptés un à un, la flèche, six CO₂ qui sortent "
           "(les six carbones partent un par un), six H₂O, l'éclat « beaucoup d'énergie », puis l'équation écrite.",
    fr="Cette respiration cellulaire, peut-on l'écrire par une équation ? Oui, et ouvre bien les yeux sur le "
       "tableau, c'est ici l'important. Nous avons le glucose : six billes, six carbones. Six molécules de dioxygène "
       "entrent. La réaction se fait, et six molécules de dioxyde de carbone sortent : chaque carbone du glucose est "
       "parti dans l'une d'elles. Il sort aussi six molécules d'eau, et beaucoup d'énergie. On écrit : C6H12O6 plus "
       "six O2 donne six CO2 plus six H2O, plus de l'énergie. Autrement dit : le billet de cent dirhams est devenu "
       "entièrement de la petite monnaie. Je relis : glucose plus six O2 donne six CO2 plus six H2O, plus de "
       "l'énergie.",
    mx="هاد la respiration cellulaire، واش نقدرو نكتبوها ب équation؟ إيه، وحل عينيك مزيان على السبورة، هنا كاين "
       "المهم. <m:glucose>عندنا <r:glucose>le glucose: ستة ديال الكورات، six carbones. <m:o2>كيدخلو <r:o2>six "
       "molécules ديال le dioxygène. <m:fleche>كتوقع la réaction، <m:co2>وكيخرجو <r:co2>six molécules ديال le "
       "dioxyde de carbone: كل carbone ديال le glucose خرج ف وحدة. <m:eau>وكيخرجو <r:eau>six molécules ديال l'eau، "
       "<m:energie>ومعاهم <r:energie>بزاف ديال l'énergie. <m:equation>كنكتبو: <c:C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + "
       "énergie>C six H douze O six, plus six O deux, donne six C O deux, plus six H deux O, <r:equation>plus de "
       "l'énergie. بطريقة أخرى: الورقة ديال مية درهم، ولات كلها دراهم صغار. نعاود نقرا: glucose plus six O deux, "
       "donne six C O deux, plus six H deux O, plus de l'énergie.",
    question="rf_a1_equation_respi",
    bullets=["Les six carbones du glucose sortent dans six CO₂.", "Respiration : beaucoup d'énergie."],
    cahier="Formule : C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + énergie",
)

# ───────────────────────── Séance 2 — bloc 3 : la fermentation ─────────────────────────

diapo(
    id="rf_a1_exp2_axes", type="simulation", demarche=3, comp=["C1"],
    titre="Expérience 2 : une cuve sans dioxygène",
    lead="La cuve est fermée, le glucose est déjà là : quatre courbes à suivre.",
    page=REF + "exao-levures.html?vue=exp2&depart=0&demarche=3", legende="Expérience 2 : les axes",
    alt="Un bioréacteur fermé par un bouchon ; à l'écran, quatre courbes au départ : dioxygène, glucose, CO₂, éthanol",
    montre="La cuve fermée par un bouchon ; les axes sont lus (temps en secondes, 60 s = 1 min ; concentrations en "
           "mg/mL à gauche, glucose à droite) ; les quatre valeurs de départ s'affichent.",
    fr="J'ai une nouvelle question pour toi : et s'il n'y a plus de dioxygène, que fera la levure ? Faisons une "
       "deuxième expérience. Cette fois, on a fermé le bioréacteur : l'air n'entre plus. Et le glucose est là dès le "
       "début. Lisons les axes : le temps en secondes, de zéro à sept cents. Rappel : soixante secondes, c'est une "
       "minute. À gauche, les concentrations, en milligrammes par millilitre. Et nous avons quatre courbes. Au "
       "début : le dioxygène à six, le glucose, sur l'axe de droite, à quarante-deux, le dioxyde de carbone à trois, "
       "et une nouvelle molécule, l'éthanol, à zéro. L'éthanol est un alcool, et nous allons bien le suivre.",
    mx="عندي ليك سؤال جديد: ويلا ما بقاش le dioxygène، شنو غادي دير la levure؟ نديرو تجربة ثانية. <r:bouchon>هاد "
       "المرة سدينا le bioréacteur: الهوا ما كيدخلش. و le glucose كاين من اللول. <m:axes>نقراو les axes: le temps "
       "en secondes، de zéro à sept cents. تفكر: soixante secondes هي une minute. على اليسار، les concentrations، en "
       "milligrammes par millilitre. وعندنا quatre courbes. <m:depart_valeurs>ف البداية: <r:courbe_o2>le dioxygène "
       "ف six، <r:courbe_glucose>le glucose، ف l'axe ديال اليمين، ف quarante-deux، <r:courbe_co2>le dioxyde de "
       "carbone ف trois، <r:courbe_ethanol>وواحد la molécule جديدة، l'éthanol، ف zéro. l'éthanol هو un alcool، "
       "وغادي نتبعو la courbe ديالو مزيان.",
    bullets=["Cuve fermée : plus d'air qui entre.", "Quatre courbes : dioxygène, glucose, CO₂, éthanol."],
    cahier="Expérience en cuve fermée : le dioxygène n'est pas renouvelé.",
)

diapo(
    id="rf_a1_exp2_phase1", type="simulation", demarche=4, comp=["C1"],
    titre="Les trois premières minutes",
    lead="Tant qu'il reste du dioxygène, les levures respirent encore.",
    page=REF + "exao-levures.html?vue=exp2&depart=depart_valeurs&demarche=4", legende="Expérience 2 : le début",
    alt="Le dioxygène descend de 6 à 0 en 190 secondes, le glucose baisse vite, le CO₂ monte un peu, pas d'éthanol",
    montre="De 0 à 190 s : le dioxygène descend de 6 à 0, le glucose de 42 à 28, le CO₂ monte un peu, l'éthanol "
           "reste à 0 ; l'instant 190 s (environ 3 min) s'allume.",
    fr="Lançons l'enregistrement, et regardons le début seul. Regarde le dioxygène : il diminue de six à zéro. Le "
       "glucose diminue vite : de quarante-deux à vingt-huit. Le dioxyde de carbone monte un peu, et l'éthanol reste "
       "à zéro. Cela, nous le connaissons : le dioxygène diminue et le dioxyde de carbone augmente, donc les levures "
       "font encore la respiration, avec le peu de dioxygène resté dans l'eau. Mais regarde ici : à cent "
       "quatre-vingt-dix secondes, environ trois minutes, le dioxygène arrive à zéro. Il n'y en a plus du tout.",
    mx="نطلقو l'enregistrement، ونشوفو البداية بوحدها. <m:phase1>شوف <r:courbe_o2>le dioxygène: كينقص de six à "
       "zéro. <r:courbe_glucose>le glucose كينقص بسرعة: de quarante-deux à vingt-huit. <r:courbe_co2>le dioxyde de "
       "carbone كيطلع شوية، <r:courbe_ethanol>و l'éthanol باقي ف zéro. هادشي كنعرفوه: le dioxygène كينقص و le "
       "dioxyde de carbone كيطلع، يعني les levures باقي كيديرو la respiration، ب le dioxygène القليل اللي بقا ف "
       "الما. <m:o2_zero>ولكن شوف هنا: <r:instant_190>ف cent quatre-vingt-dix secondes، يعني environ trois minutes، "
       "le dioxygène وصل ل zéro. ما بقا منو والو.",
    bullets=["0 à 190 s : le dioxygène passe de 6 à 0.", "Pas d'éthanol : c'est encore la respiration."],
    cahier="Tant qu'il reste du dioxygène, les levures respirent.",
)

diapo(
    id="rf_a1_exp2_phase2", type="simulation", demarche=4, comp=["C1", "C2"], etoile=True,
    titre="Plus de dioxygène : et après ?",
    lead="Les levures ne s'arrêtent pas : elles changent de voie.",
    page=REF + "exao-levures.html?vue=exp2&depart=o2_zero&demarche=4", legende="Expérience 2 : après 190 s",
    alt="Après 190 secondes, le CO₂ monte vite, l'éthanol apparaît et monte, le glucose continue de baisser",
    montre="Arrêt à 190 s : question. Puis le CO₂ monte vite, l'éthanol apparaît et monte en ligne droite, le "
           "glucose baisse encore ; à 700 s, CO₂ 44 et éthanol 34 ; la description puis « fermentation alcoolique » "
           "s'écrivent.",
    fr="Il n'y a plus de dioxygène dans le bioréacteur. Arrête-toi un peu ici avec moi, car c'est très important. "
       "Regarde les courbes après cet instant. Les levures ne se sont pas arrêtées : le dioxyde de carbone continue "
       "de monter, et vite. Et regarde cette belle chose : l'éthanol est apparu, et il monte. Et le glucose diminue "
       "encore. À sept cents secondes : le dioxyde de carbone dépasse quarante, et l'éthanol dépasse trente. Donc, "
       "sans dioxygène, les levures utilisent le glucose, rejettent du dioxyde de carbone et produisent de "
       "l'éthanol : c'est la fermentation alcoolique. Tout simplement : sans dioxygène, la levure ne meurt pas, elle "
       "change de chemin. Je relis : sans dioxygène, production d'éthanol et de dioxyde de carbone : c'est la "
       "fermentation alcoolique.",
    mx="ما بقاش le dioxygène ف le bioréacteur. وقف معايا شوية هنا، حيت هادي مهمة بزاف. شوف les courbes من بعد هاد "
       "اللحظة. <m:co2_monte>les levures باقي خدامين: <r:courbe_co2>le dioxyde de carbone باقي كيطلع، وبسرعة. "
       "<m:ethanol_apparait>وشوف هاد الحاجة، زوينة بزاف: <r:courbe_ethanol>l'éthanol بان، وكيطلع. "
       "<m:glucose_continue>ومعاه <r:courbe_glucose>le glucose باقي كينقص. <m:fin>ف sept cents secondes: le dioxyde "
       "de carbone فات quarante، و l'éthanol فات trente. <m:decrire>إذن بلا dioxygène، <c:Sans O₂ : glucose consommé, "
       "CO₂ rejeté, éthanol produit : fermentation alcoolique>les levures كيستعملو le glucose، كيخرج منهم le dioxyde "
       "de carbone، وكينتجو l'éthanol: <m:deduire>c'est la <r:conclusion>fermentation alcoolique. يعني ببساطة: بلا "
       "dioxygène، la levure كتبقى خدامة، ولكن كتبدل الطريق. نعاود نقرا: sans dioxygène, production d'éthanol, et de "
       "dioxyde de carbone: c'est la fermentation alcoolique.",
    obs="rf_a1_exp2_phase2",
    bullets=["Sans dioxygène : le CO₂ monte encore, l'éthanol apparaît.", "C'est la fermentation alcoolique."],
    cahier="Sans dioxygène, les levures consomment du glucose, rejettent du CO₂ et produisent de l'éthanol : "
           "c'est la fermentation alcoolique.",
)

diapo(
    id="rf_a1_equation_ferm", type="simulation", demarche=6, comp=["C2"], etoile=True,
    titre="L'équation de la fermentation",
    lead="Un glucose : deux éthanols, deux CO₂ et peu d'énergie.",
    page=REF + "equation.html?vue=fermentation&demarche=6", legende="L'équation de la fermentation alcoolique",
    alt="Le glucose en six billes, puis deux éthanols de deux billes et deux CO₂ ; un petit éclat d'énergie",
    montre="Le glucose, la flèche, deux éthanols (deux billes chacun), deux CO₂, les six carbones recomptés, le "
           "petit éclat « peu d'énergie », le halo d'énergie resté sur l'éthanol, puis l'équation écrite.",
    fr="Écrivons maintenant l'équation de la fermentation alcoolique. Écoute-moi bien, c'est l'une des choses les "
       "plus importantes de ce cours. Le même glucose, six carbones, mais sans dioxygène. Il donne deux molécules "
       "d'éthanol, chacune à deux carbones, et deux molécules de dioxyde de carbone. Comptons les carbones : quatre "
       "plus deux égale six. Aucun carbone ne manque. Et l'énergie sortie ? Très peu. Pourquoi ? Parce que l'éthanol "
       "contient encore de l'énergie. On écrit : C6H12O6 donne deux C2H5OH plus deux CO2, plus un peu d'énergie. "
       "Autrement dit : du billet de cent dirhams, seule une petite partie est devenue de la monnaie ; le reste est "
       "parti avec l'éthanol. Je relis : glucose donne deux éthanols plus deux CO2, plus un peu d'énergie.",
    mx="نكتبو دابا l'équation ديال la fermentation alcoolique. سمعني مزيان، هادي من أهم الحوايج فهاد الدرس. "
       "<m:glucose>نفس <r:glucose>le glucose، six carbones، <m:fleche>ولكن بلا dioxygène. <m:ethanol>كيعطي "
       "<r:ethanol>deux molécules ديال l'éthanol، كل وحدة فيها deux carbones، <m:co2>ومعاهم <r:co2>deux molécules "
       "ديال le dioxyde de carbone. <m:compte>نحسبو les carbones: quatre plus deux égale six. ما نقص حتى carbone. "
       "<m:energie>و l'énergie اللي خرجات؟ <r:energie>قليلة بزاف. <m:reste>علاش؟ حيت l'éthanol باقي فيه l'énergie. "
       "<m:equation>كنكتبو: <c:C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + énergie (peu)>C six H douze O six, donne deux C deux H "
       "cinq O H, plus deux C O deux, <r:equation>plus un peu d'énergie. بطريقة أخرى: من الورقة ديال مية درهم، غير "
       "شوية اللي ولا دراهم صغار، والباقي مشا مع l'éthanol. نعاود نقرا: glucose donne deux éthanol, plus deux C O "
       "deux, plus un peu d'énergie.",
    question="rf_a1_equation_ferm",
    bullets=["2 × 2 + 2 × 1 = 6 carbones.", "L'éthanol garde de l'énergie : la fermentation en libère peu."],
    cahier="Formule : C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + énergie (peu)",
)

# ───────────────────────── Séance 3 — bloc 4 : où ? ─────────────────────────

diapo(
    id="rf_a2_deux_levures", type="simulation", demarche=4, comp=["C3"],
    titre="Deux levures au microscope",
    lead="Deux levures au microscope électronique : une du milieu aérobie, une du milieu anaérobie.",
    page=REF + "deux-levures.html?demarche=4", legende="Deux levures au microscope électronique",
    alt="Deux coupes de levures côte à côte : à gauche de nombreuses grandes mitochondries, à droite quelques petites",
    montre="La levure du milieu aérobie, puis celle du milieu anaérobie. Arrêt : question. Puis les mitochondries "
           "s'allument une à une et se comptent des deux côtés, et les légendes se posent.",
    fr="La levure reste-t-elle la même, en milieu aérobie et en milieu anaérobie ? Regardons-la avec le microscope "
       "électronique, qui agrandit beaucoup plus que le microscope ordinaire. Voici une levure qui a vécu avec le "
       "dioxygène. Et voici une levure qui a vécu sans dioxygène. Compare-les bien, et prends ton temps. Comptons "
       "les mitochondries : dans la levure du milieu aérobie, elles sont nombreuses et grandes. Et dans la levure du "
       "milieu anaérobie, elles sont rares et petites. Voici les noms : le noyau, le hyaloplasme et les "
       "mitochondries. La différence, ce sont donc les mitochondries.",
    mx="واش la levure كتبقى هي هي، ف milieu aérobie و ف milieu anaérobie؟ نشوفوها ب le microscope électronique، "
       "اللي كيبين الحوايج الصغار بزاف. <m:aerobie>هادي <r:levure_aerobie>levure كانت مع le dioxygène. "
       "<m:anaerobie>وهادي <r:levure_anaerobie>levure كانت بلا dioxygène. قارن بيناتهم مزيان، وخود الوقت ديالك. "
       "<m:mitochondries>نحسبو les mitochondries: <r:mitochondries_aerobie>ف la levure ديال milieu aérobie، بزاف "
       "وكبار. <r:mitochondries_anaerobie>و ف la levure ديال milieu anaérobie، قلال وصغار. <m:legendes>وهادو "
       "الأسماء: le noyau، <r:hyaloplasme>le hyaloplasme، و les mitochondries. إذن الفرق هو les mitochondries.",
    obs="rf_a2_deux_levures",
    bullets=["Milieu aérobie : mitochondries nombreuses et développées.", "Milieu anaérobie : rares et réduites."],
    cahier="Levure en milieu aérobie : mitochondries nombreuses et développées ; en milieu anaérobie : rares et réduites.",
)

diapo(
    id="rf_a2_localisation", type="simulation", demarche=6, comp=["C3"], etoile=True,
    titre="Où se passe chaque réaction ?",
    lead="La respiration a besoin des mitochondries ; la fermentation se fait dans le hyaloplasme.",
    page=REF + "deux-levures.html?depart=legendes&demarche=6", legende="Le lieu de chaque réaction",
    alt="Les deux levures légendées ; la conclusion s'écrit : respiration et mitochondries, fermentation et hyaloplasme",
    montre="Les deux levures légendées restent à l'écran ; la conclusion s'écrit : respiration ↔ mitochondries, "
           "fermentation ↔ hyaloplasme.",
    fr="Nous avons vu la différence : les mitochondries. Qu'en déduit-on ? Laisse tout de côté un instant, et suis "
       "avec moi. En milieu aérobie, la levure fait la respiration, et elle a beaucoup de mitochondries. Donc la "
       "respiration a besoin des mitochondries. En milieu anaérobie, elle fait la fermentation, et les mitochondries "
       "sont rares. Donc la fermentation n'en a pas besoin : elle se passe dans le hyaloplasme. On écrit la "
       "conclusion : la respiration, dans les mitochondries. La fermentation, dans le hyaloplasme. Autrement dit : "
       "la mitochondrie est la centrale électrique de la cellule. Qui veut beaucoup d'énergie a besoin de beaucoup "
       "de centrales. Je relis : la respiration, dans les mitochondries. La fermentation, dans le hyaloplasme.",
    mx="شفنا الفرق: les mitochondries. شنو كنستنتجو منو؟ خلي كلشي على جنب شوية، وتبع معايا. "
       "<r:mitochondries_aerobie>ف milieu aérobie، la levure كدير la respiration، وعندها بزاف ديال les mitochondries. "
       "إذن la respiration كتحتاج les mitochondries. <r:mitochondries_anaerobie>ف milieu anaérobie، كدير la "
       "fermentation، و les mitochondries قلال. إذن la fermentation خدامة بلا بيهم: <r:hyaloplasme>كتوقع ف le "
       "hyaloplasme. <m:conclusion>كنكتبو la conclusion: <c:Respiration : dans les mitochondries · Fermentation : "
       "dans le hyaloplasme>la respiration, dans les mitochondries. <r:conclusion>La fermentation, dans le "
       "hyaloplasme. بطريقة أخرى: la mitochondrie هي la centrale électrique ديال الخلية. اللي بغا l'énergie بزاف، "
       "خاصو بزاف ديال les centrales. نعاود نقرا: la respiration, dans les mitochondries. La fermentation, dans le "
       "hyaloplasme.",
    bullets=["Respiration : mitochondries.", "Fermentation : hyaloplasme."],
    cahier="Donc la respiration a besoin des mitochondries ; la fermentation se fait dans le hyaloplasme.",
)

diapo(
    id="rf_a2_tableau", type="simulation", demarche=6, comp=["C3", "C2"],
    titre="Respiration ou fermentation : le tableau",
    lead="Cinq lignes pour comparer : milieu, gaz, glucose, énergie, lieu.",
    page=REF + "comparer.html?demarche=6", legende="Respiration et fermentation comparées",
    alt="Un tableau à deux colonnes qui se construit ligne par ligne, chaque ligne illustrée d'une vignette animée",
    montre="Le tableau se construit ligne par ligne : chaque ligne est d'abord une vignette animée (le milieu, les "
           "gaz, le glucose, l'énergie, le lieu), puis elle entre dans le tableau.",
    fr="Rassemblons maintenant tout dans un seul tableau, pour comparer d'un coup d'œil. À gauche la respiration, à "
       "droite la fermentation. La première ligne, le milieu : aérobie pour la respiration, anaérobie pour la "
       "fermentation. La deuxième, les gaz : la respiration prend le dioxygène et rejette le dioxyde de carbone ; la "
       "fermentation rejette seulement du dioxyde de carbone. La troisième, le glucose : dans la respiration il est "
       "dégradé entièrement ; dans la fermentation, il en reste l'éthanol. La quatrième, l'énergie : beaucoup dans "
       "la respiration, peu dans la fermentation. Et la cinquième, le lieu : les mitochondries pour la respiration, "
       "le hyaloplasme pour la fermentation. Ce tableau tombe souvent à l'examen.",
    mx="نجمعو دابا كلشي ف tableau واحد، باش تقارن بالعين. <r:colonne_respiration>على اليسار la respiration، "
       "<r:colonne_fermentation>وعلى اليمين la fermentation. <m:milieu>الأولى، <r:ligne_milieu>le milieu: aérobie ل "
       "la respiration، و anaérobie ل la fermentation. <m:gaz>الثانية، <r:ligne_gaz>les gaz: la respiration كتاخد "
       "le dioxygène، وكتخرج le dioxyde de carbone. و la fermentation كتخرج غير le dioxyde de carbone. "
       "<m:glucose>الثالثة، <r:ligne_glucose>le glucose: ف la respiration كيتفكك كامل. و ف la fermentation، كيبقى "
       "منو l'éthanol. <m:energie>الرابعة، <r:ligne_energie>l'énergie: بزاف ف la respiration، وقليلة ف la "
       "fermentation. <m:lieu>والخامسة، <r:ligne_lieu>le lieu: les mitochondries ل la respiration، و le hyaloplasme "
       "ل la fermentation. هاد le tableau كيجي بزاف ف الامتحان.",
    bullets=["Un tableau comparatif : cinq lignes.", "À savoir refaire au bac."],
    cahier="Tableau comparatif : milieu, gaz, glucose, énergie, lieu.",
)

diapo(
    id="rf_a2_definitions", type="simulation", demarche=6, comp=["C2"], etoile=True,
    titre="Les deux définitions",
    lead="Chaque définition se construit par trois questions : quoi ? où ? avec quel résultat ?",
    page=REF + "comparer.html?depart=lieu&demarche=6", legende="Les définitions",
    alt="Sous le tableau comparatif, les deux définitions s'écrivent : oxydation complète, oxydation incomplète",
    montre="Sous le tableau fini, les deux définitions s'écrivent : oxydation complète (respiration), oxydation "
           "incomplète (fermentation).",
    fr="De ce tableau, nous allons tirer deux définitions. Je veux que tu les retiennes toutes les deux, écoute-les "
       "bien. Qu'est-ce que la respiration ? Le glucose est dégradé entièrement : oxydation complète. Où ? En milieu "
       "aérobie, et dans les mitochondries. Et que donne-t-elle ? Beaucoup d'énergie. Donc : la respiration "
       "cellulaire, c'est l'oxydation complète du glucose, en milieu aérobie, avec beaucoup d'énergie. Et la "
       "fermentation ? Les mêmes questions : la fermentation, c'est l'oxydation incomplète du glucose, en milieu "
       "anaérobie, avec peu d'énergie. Et il reste un déchet organique, qui contient encore de l'énergie. Autrement "
       "dit : le billet de cent dirhams, la respiration le change entièrement en monnaie, la fermentation seulement "
       "un peu. Je relis : respiration, oxydation complète. Fermentation, oxydation incomplète.",
    mx="من هاد le tableau، غادي نخرجو جوج ديال التعاريف. بغيتك تحفظهم بجوج، سمع مزيان. شنو هي la respiration؟ "
       "<r:colonne_respiration>le glucose كيتفكك كامل: oxydation complète. فين؟ ف milieu aérobie، و ف les "
       "mitochondries. وشنو كتعطي؟ بزاف ديال l'énergie. <m:definitions>إذن: <c:Respiration cellulaire : oxydation "
       "complète du glucose, en milieu aérobie, dans les mitochondries ; beaucoup d'énergie>la respiration "
       "cellulaire, c'est l'oxydation complète du glucose, en milieu aérobie, avec beaucoup d'énergie. و la "
       "fermentation؟ <r:colonne_fermentation>نفس الأسئلة: <c:Fermentation : oxydation incomplète du glucose, en "
       "milieu anaérobie, dans le hyaloplasme ; peu d'énergie, déchet organique riche en énergie>la fermentation, "
       "c'est l'oxydation incomplète du glucose, en milieu anaérobie, avec peu d'énergie. وكيبقى un déchet "
       "organique، باقي فيه l'énergie. بطريقة أخرى: <r:ligne_energie>الورقة ديال مية درهم، la respiration كتردها كلها دراهم صغار، و "
       "la fermentation غير شوية. نعاود نقرا: respiration, oxydation complète. Fermentation, oxydation incomplète.",
    question="rf_a2_definitions",
    bullets=["Respiration : oxydation complète du glucose.", "Fermentation : oxydation incomplète du glucose."],
    cahier="Définition : la respiration cellulaire est l'oxydation complète du glucose, en milieu aérobie, dans les "
           "mitochondries ; elle libère beaucoup d'énergie.\n"
           "Définition : la fermentation est l'oxydation incomplète du glucose, en milieu anaérobie, dans le "
           "hyaloplasme ; elle libère peu d'énergie et laisse un déchet organique riche en énergie.",
)

# ───────────────────────── Séance 3 — bloc 5 : que devient le glucose ? ─────────────────────────

diapo(
    id="rf_a3_marquage", type="simulation", demarche=3, comp=["C4"],
    titre="Suivre le glucose à la trace",
    lead="Un glucose marqué au carbone 14 : on sait toujours où il est, et ce qu'il est devenu.",
    page=REF + "marquage.html?demarche=3", legende="Le glucose marqué",
    alt="Un glucose dont un carbone clignote, un compteur de radioactivité, puis deux cultures de levures",
    montre="Un glucose dont un carbone clignote (la balise) et le compteur de radioactivité ; puis les deux "
           "cultures : sans dioxygène et avec dioxygène.",
    fr="Il reste une question : quand le glucose entre dans la levure, que devient-il, et où va-t-il ? Pour le "
       "suivre, il existe une belle méthode. On utilise du glucose marqué : l'un de ses carbones est radioactif, "
       "c'est-à-dire qu'il envoie un signal, et on peut le retrouver partout où il va. Comme si tu mettais un GPS "
       "sur une voiture : où qu'elle aille, tu connais sa place. Et même si le glucose change et devient une autre "
       "molécule, le carbone marqué reste dedans. On fait deux expériences : des levures avec du glucose marqué, "
       "une fois sans dioxygène, une fois avec. Puis on cherche : le signal est-il dehors, dans le hyaloplasme, ou "
       "dans la mitochondrie.",
    mx="باقي واحد السؤال: le glucose ملي كيدخل ل la levure، شنو كيولي، وفين كيمشي؟ باش نتبعو الطريق ديالو، كاينة واحد "
       "الطريقة زوينة. <m:principe>كنستعملو <r:glucose>glucose marqué: واحد le carbone ديالو radioactif، يعني "
       "كيعطي الإشارة، وكنقدرو نلقاوه فين ما مشا. بحال يلا درتي G P S ل شي طوموبيل: فين ما مشات، كتعرف البلاصة "
       "ديالها. <r:glucose>وحتى يلا le glucose تبدل وولا molécule أخرى، le carbone marqué كيبقى فيها. <m:deux_cultures>وكنديرو "
       "جوج ديال التجارب: <r:dehors>les levures مع glucose marqué، مرة بلا dioxygène، ومرة مع le dioxygène. ومن "
       "بعد كنشوفو: واش الإشارة برا، <r:hyaloplasme>ف le hyaloplasme، <r:mitochondrie>ولا ف la mitochondrie.",
    bullets=["Marquage au ¹⁴C : un carbone radioactif, qu'on peut suivre.", "Deux cultures : sans et avec dioxygène."],
    cahier="Le marquage au ¹⁴C permet de suivre le glucose et ce qu'il devient.",
)

diapo(
    id="rf_a3_glycolyse", type="simulation", demarche=4, comp=["C4"], etoile=True,
    titre="Le début est le même : la glycolyse",
    lead="Dans les deux milieux, le glucose devient de l'acide pyruvique dans le hyaloplasme.",
    page=REF + "marquage.html?depart=deux_cultures&demarche=4", legende="T0, T1, T2 : la glycolyse",
    alt="Dans les deux cultures, le glucose marqué entre dans la levure puis se coupe en deux chaînes de trois billes",
    montre="T0 : le glucose marqué est dehors. T1 : il entre dans le hyaloplasme. T2 : la chaîne de six se coupe "
           "en deux chaînes de trois, l'acide pyruvique, des deux côtés. Le mot glyco·lyse s'écrit.",
    fr="Suivons maintenant le glucose marqué dans le temps. C'est le cœur du cours, suis avec moi pas à pas. Au "
       "début, le glucose est hors de la levure, dans les deux expériences. Ensuite, le glucose est entré dans le "
       "hyaloplasme. Puis, regarde : il n'y a plus de glucose ! À sa place apparaît l'acide pyruvique : la chaîne de "
       "six s'est coupée en deux chaînes de trois. Et cela s'est passé dans le hyaloplasme, avec dioxygène et sans "
       "dioxygène. Cette étape s'appelle la glycolyse : glyco veut dire le sucre, et lyse veut dire couper. "
       "Autrement dit : le billet de cent dirhams a été coupé en deux. Je relis : la glycolyse, c'est la dégradation "
       "du glucose en deux acides pyruviques, dans le hyaloplasme.",
    mx="نتبعو دابا le glucose marqué مع الوقت. هادي هي القلب ديال الدرس، تبع معايا خطوة بخطوة. <m:t0>ف البداية، "
       "<r:dehors>le glucose برا la levure، ف جوج ديال التجارب. <m:t1>من بعد، <r:glucose>le glucose دخل ل le "
       "hyaloplasme. <m:t2>ومن بعد، شوف: le glucose ما بقاش! <r:pyruvate>بان ف البلاصة ديالو l'acide pyruvique: "
       "السلسلة ديال ستة، تقسمات على جوج ديال السلاسل ديال ثلاثة. وهادشي وقع <r:hyaloplasme>ف le hyaloplasme، مع "
       "le dioxygène وبلا dioxygène. <m:glycolyse>هاد المرحلة سميتها <c:Glycolyse : glucose → 2 acides pyruviques, "
       "dans le hyaloplasme, avec ou sans O₂>la glycolyse: glyco يعني السكر، و lyse يعني القسمة. بطريقة أخرى: "
       "الورقة ديال مية درهم، تقسمات على جوج. نعاود نقرا: la glycolyse, c'est la dégradation du glucose, en deux "
       "acides pyruviques, dans le hyaloplasme.",
    bullets=["Glycolyse : glucose → 2 acides pyruviques.", "Dans le hyaloplasme, avec ou sans dioxygène."],
    cahier="Définition : la glycolyse est la dégradation du glucose en deux acides pyruviques, dans le hyaloplasme ; "
           "elle est commune à la respiration et à la fermentation.",
)

diapo(
    id="rf_a3_sans_o2", type="simulation", demarche=4, comp=["C4"],
    titre="Sans dioxygène : éthanol et CO₂",
    lead="Sans dioxygène, l'acide pyruvique reste dans le hyaloplasme.",
    page=REF + "marquage.html?depart=glycolyse&demarche=4", legende="T3 à T5, sans dioxygène",
    alt="Dans la culture sans dioxygène, l'acide pyruvique devient éthanol et CO₂, qui sortent de la levure",
    montre="Culture sans dioxygène. T3 : dans le hyaloplasme, l'acide pyruvique baisse, l'éthanol et le CO₂ "
           "apparaissent. T4 : ils commencent à sortir. T5 : tout est dehors.",
    fr="Nous sommes arrivés à l'acide pyruvique. À partir d'ici, le chemin se sépare en deux. Commençons par les "
       "levures sans dioxygène. Regarde dans le hyaloplasme : l'acide pyruvique diminue, et l'éthanol apparaît, avec "
       "le dioxyde de carbone. Ensuite, l'éthanol et le dioxyde de carbone commencent à sortir de la levure. Et à "
       "la fin, tout est dehors : l'éthanol et le dioxyde de carbone. Tu l'as reconnue ? C'est la fermentation "
       "alcoolique de la deuxième expérience. Donc, sans dioxygène, l'acide pyruvique reste dans le hyaloplasme, et "
       "devient éthanol et dioxyde de carbone. Et rien n'est entré dans la mitochondrie.",
    mx="وصلنا ل l'acide pyruvique. ومن هنا، الطريق كتفرق على جوج. نبداو ب les levures اللي بلا dioxygène. "
       "<m:t3_sans>شوف <r:hyaloplasme>ف le hyaloplasme: <r:pyruvate>l'acide pyruvique كينقص، <r:ethanol>وكيبان "
       "l'éthanol، <r:co2>مع le dioxyde de carbone. <m:t4_sans>من بعد، l'éthanol و le dioxyde de carbone كيبداو "
       "يخرجو من la levure. <m:t5_sans>وف اللخر، <r:dehors>كلشي ولا برا: l'éthanol و le dioxyde de carbone. "
       "عرفتيها؟ هادي هي la fermentation alcoolique اللي شفنا ف التجربة الثانية. إذن بلا dioxygène، <r:hyaloplasme>l'acide "
       "pyruvique كيبقى ف le hyaloplasme، وكيولي éthanol و dioxyde de carbone. و la mitochondrie ما دخل ليها والو.",
    bullets=["Sans dioxygène : acide pyruvique → éthanol + CO₂.", "Tout se passe dans le hyaloplasme."],
    cahier="Sans dioxygène : l'acide pyruvique reste dans le hyaloplasme et donne éthanol + CO₂.",
)

diapo(
    id="rf_a3_avec_o2", type="simulation", demarche=4, comp=["C4"], etoile=True,
    titre="Avec dioxygène : la mitochondrie",
    lead="Avec dioxygène, l'acide pyruvique prend un autre chemin.",
    page=REF + "marquage.html?depart=t5_sans&demarche=4", legende="T3 à T5, avec dioxygène",
    alt="Dans la culture avec dioxygène, l'acide pyruvique entre dans la mitochondrie ; il en sort du CO₂",
    montre="Culture avec dioxygène. Arrêt avant T3 : question. T3 : l'acide pyruvique entre dans la mitochondrie "
           "(acides du cycle de Krebs + CO₂). T4, T5 : seul le CO₂ sort. Puis les « + » volent dans le tableau du "
           "document.",
    fr="Et avec le dioxygène, où ira l'acide pyruvique ? Voici le moment important, regarde avec moi. Nous avons "
       "le même acide pyruvique dans le hyaloplasme, mais cette fois le dioxygène est là. Regarde : l'acide "
       "pyruvique est entré dans la mitochondrie ! Là, il devient d'autres acides, appelés les acides du cycle de "
       "Krebs, et il en sort du dioxyde de carbone. Ensuite, le dioxyde de carbone augmente, et à la fin tout est "
       "sorti : seulement du dioxyde de carbone. Il ne reste aucune molécule organique. Tous ces résultats sont dans "
       "un tableau, comme à l'examen. Donc, avec le dioxygène, l'acide pyruvique entre dans la mitochondrie, et il "
       "est dégradé en dioxyde de carbone. Autrement dit : la mitochondrie est la centrale : elle dégrade l'acide "
       "pyruvique jusqu'au bout. Je relis : avec dioxygène, l'acide pyruvique entre dans la mitochondrie.",
    mx="ومع le dioxygène، فين غادي يمشي l'acide pyruvique؟ دابا جات اللحظة المهمة، شوف معايا. عندنا نفس l'acide "
       "pyruvique ف le hyaloplasme، ولكن هاد المرة le dioxygène كاين. <m:t3_avec>شوف: <r:mitochondrie>l'acide "
       "pyruvique دخل ل la mitochondrie! <r:krebs>وتما كيولي des acides أخرى، سميتهم les acides du cycle de "
       "Krebs، <r:co2>وكيخرج منو le dioxyde de carbone. <m:t4_avec>من بعد، le dioxyde de carbone كيتزاد، "
       "<m:t5_avec>وف اللخر <r:dehors>كلشي خرج: غير le dioxyde de carbone. ما بقات حتى molécule organique. "
       "<m:tableau>وهاد النتائج كاملين كاينين ف tableau، بحال ف الامتحان. إذن <c:Avec O₂ : l'acide pyruvique entre "
       "dans la mitochondrie, où il est dégradé en CO₂>avec le dioxygène, l'acide pyruvique entre dans la "
       "mitochondrie, et il est dégradé en dioxyde de carbone. بطريقة أخرى: la mitochondrie هي la centrale: فيها "
       "l'acide pyruvique كيتفكك كامل. نعاود نقرا: avec dioxygène, l'acide pyruvique entre dans la mitochondrie.",
    obs="rf_a3_avec_o2",
    bullets=["Avec dioxygène : l'acide pyruvique entre dans la mitochondrie.", "Il y est dégradé en CO₂."],
    cahier="Avec dioxygène : l'acide pyruvique entre dans la mitochondrie, où il est dégradé en CO₂.",
)

diapo(
    id="rf_a3_voyage1", type="simulation", demarche=6, comp=["C4"],
    titre="La carte du voyage du glucose",
    lead="Le schéma bilan de l'activité 1 : un départ, un carrefour, deux routes.",
    page=REF + "voyage.html?etape=1&demarche=6", legende="La carte du voyage (étape 1)",
    alt="Une carte : le glucose entre dans la cellule, la glycolyse donne l'acide pyruvique, puis deux routes",
    montre="La carte se construit flèche par flèche : le glucose entre, la glycolyse dans le hyaloplasme, l'acide "
           "pyruvique, puis les deux routes : avec dioxygène vers la mitochondrie, sans dioxygène vers l'éthanol.",
    fr="Dessinons le voyage du glucose en entier, sur une seule carte. Le glucose part de l'extérieur, et il entre "
       "dans la cellule. Dans le hyaloplasme, la glycolyse : il est coupé en deux acides pyruviques. Rappelle-toi : "
       "cela se passe avec et sans dioxygène. Ensuite, deux routes. Avec le dioxygène : l'acide pyruvique entre "
       "dans la mitochondrie, et il sort du dioxyde de carbone. C'est la respiration. Et sans dioxygène : il reste "
       "dans le hyaloplasme, et donne l'éthanol et le dioxyde de carbone. C'est la fermentation. L'acide pyruvique "
       "est donc au carrefour, et c'est le dioxygène qui fixe la route. Cette carte, nous la compléterons avec le "
       "cours.",
    mx="يلا نرسمو الرحلة ديال le glucose كاملة ف carte وحدة. <m:entree>كيبدا <r:glucose>le glucose من برا، وكيدخل ل "
       "la cellule. <m:glycolyse>ف le hyaloplasme، <r:glycolyse>la glycolyse: <m:pyruvate>كيتقسم على <r:pyruvate>deux "
       "acides pyruviques. تفكر: هادي كتوقع مع le dioxygène وبلا dioxygène. ومن بعد جوج ديال الطرق. <m:avec_o2>مع "
       "le dioxygène: <r:mitochondrie>l'acide pyruvique كيدخل ل la mitochondrie، وكيخرج le dioxyde de carbone. هادي "
       "la respiration. <m:sans_o2>وبلا dioxygène: كيبقى ف le hyaloplasme، <r:ethanol>وكيعطي l'éthanol و le dioxyde "
       "de carbone. هادي la fermentation. يعني l'acide pyruvique واقف فين كتفرق الطريق، و le dioxygène هو اللي "
       "كيحدد الطريق. هاد la carte غادي نكملوها مع الدرس.",
    question="rf_a3_voyage1",
    bullets=["Glycolyse commune, puis deux routes.", "Le dioxygène décide de la route de l'acide pyruvique."],
    cahier="Bilan : glucose → glycolyse → acide pyruvique ; avec O₂ : mitochondrie ; sans O₂ : éthanol + CO₂.",
)

# ───────────────────────── Séance 4 — bloc 6 : deux rappels ─────────────────────────

diapo(
    id="rf_g0_atp", type="simulation", comp=["C5"],
    titre="Rappel : l'ATP, la monnaie de la cellule",
    lead="Le glucose est un billet ; la cellule paie avec de la monnaie : l'ATP.",
    page=RAP + "atp.html?depart=0&rappel=1", legende="L'ATP",
    alt="La molécule d'ATP et ses trois phosphates ; un phosphate se détache, de l'énergie sort ; puis l'ATP se reforme",
    montre="L'ATP et ses trois phosphates ; une liaison se rompt, l'énergie sort, il reste ADP et Pi (hydrolyse "
           "écrite) ; puis l'énergie revient, le phosphate se rattache (phosphorylation écrite).",
    fr="Avant d'entrer dans la glycolyse, il faut connaître l'ATP. Rappelle-toi : le glucose est un billet de cent "
       "dirhams, et tu ne peux pas payer une petite chose avec. La cellule paie avec la petite monnaie : l'ATP. "
       "Regarde cette molécule : elle a trois phosphates. Quand un phosphate se détache, de l'énergie sort, et la "
       "cellule travaille avec. Il reste l'ADP, et le phosphate qu'on écrit Pi. On écrit : ATP plus eau donne ADP "
       "plus phosphate, plus de l'énergie. Et à l'inverse : si de l'énergie arrive, le phosphate revient sur l'ADP, "
       "et on a de nouveau l'ATP. On écrit : ADP plus phosphate plus énergie donne ATP. Donc : l'ATP utilisé devient "
       "ADP, et l'ADP rechargé redevient ATP.",
    mx="قبل ما ندخلو ل la glycolyse من الداخل، خاصنا نتعرفو على l'ATP. تفكر: le glucose هو ورقة ديال مية درهم، وما "
       "تقدرش تخلص بيها حاجة صغيرة. la cellule كتخلص ب الدراهم الصغار: l'ATP. <m:atp_entier>شوف هاد la molécule: "
       "<r:phosphates>فيها trois phosphates. <m:liaison_rompue>ملي كيتحيد واحد le phosphate، "
       "<m:energie_liberee:1.8>كتخرج l'énergie، <r:travail>وبيها كتخدم la cellule. <m:adp_pi>وكيبقى l'ADP، "
       "<r:phosphate_libre>و le phosphate اللي كنكتبوه Pi. <m:hydrolyse>كنكتبو: <r:ecrit_hydrolyse>A T P plus eau, "
       "donne A D P plus phosphate, plus de l'énergie. <m:recharge:2.2>وبالعكس: يلا جات l'énergie، <m:atp_reforme>le "
       "phosphate كيرجع ل l'ADP، <r:atp>وكيولي l'ATP من جديد. <m:phosphorylation>كنكتبو: <r:ecrit_phosphorylation>A "
       "D P plus phosphate plus énergie, donne A T P. يعني: l'ATP اللي تخدم كيولي ADP، و l'ADP ملي كيولي عامر كيرجع ATP.",
    bullets=["ATP + H₂O → ADP + Pi + énergie", "ADP + Pi + énergie → ATP"],
    cahier="Rappel : ATP + H₂O → ADP + Pi + énergie ; ADP + Pi + énergie → ATP.",
)

diapo(
    id="rf_g0_taxi", type="simulation", comp=["C5"],
    titre="Rappel : le transporteur d'hydrogène",
    lead="NAD⁺ est un taxi vide ; chargé de deux hydrogènes, il devient NADH,H⁺ : il est réduit.",
    page=RAP + "taxi.html?depart=0", legende="Le transporteur d'hydrogène",
    alt="Deux hydrogènes arrachés à une molécule organique ; un taxi NAD⁺ arrive vide et repart chargé, NADH,H⁺",
    montre="Une molécule organique perd deux hydrogènes ; le transporteur NAD⁺ (taxi vide) arrive, les prend et "
           "devient NADH,H⁺ (taxi chargé) ; l'équation s'écrit.",
    fr="Après l'ATP, il nous reste un élément : le transporteur d'hydrogène. Regarde cette molécule organique. La "
       "cellule lui enlève deux hydrogènes. Qui va les prendre ? Un transporteur arrive, il s'appelle NAD plus : "
       "comme un taxi vide. Il prend les deux hydrogènes, et il est plein : maintenant il s'appelle NADH,H plus. "
       "Chaque hydrogène, c'est un proton et un électron, donc deux protons et deux électrons. On écrit : NAD plus, "
       "plus deux protons, plus deux électrons, donne NADH,H plus. Et le taxi plein, on dit qu'il est réduit. Tout "
       "simplement : NAD plus, taxi vide ; NADH,H plus, taxi plein, réduit.",
    mx="ومن بعد l'ATP، باقي لينا عنصر واحد: le transporteur d'hydrogène. <m:molecule>شوف هاد <r:molecule>la molécule "
       "organique. <m:deux_h_arraches:1.6>la cellule كتحيد منها <r:hydrogenes>deux hydrogènes. شكون غادي ياخدهم؟ "
       "<m:taxi_vide_arrive:1.8>جا واحد le transporteur، <r:taxi>سميتو N A D plus: بحال طاكسي خاوي. "
       "<m:taxi_charge:1.6>هز deux hydrogènes، وولا عامر: دابا سميتو N A D H, H plus. <m:deux_h_egal>كل hydrogène "
       "فيه proton و électron، <r:ecrit_2h>يعني deux protons و deux électrons. <m:reduit>كنكتبو: <r:equation>N A D "
       "plus, plus deux protons, plus deux électrons, donne N A D H, H plus. والطاكسي العامر كنقولو عليه réduit. "
       "يعني ببساطة: N A D plus طاكسي خاوي، والآخر طاكسي عامر، réduit.",
    question="rf_g0_taxi",
    bullets=["NAD⁺ + 2 H⁺ + 2 e⁻ → NADH,H⁺", "NADH,H⁺ : le transporteur réduit (chargé)."],
    cahier="Rappel : NAD⁺ + 2 H⁺ + 2 e⁻ → NADH,H⁺ (transporteur d'hydrogène réduit).",
)

# ───────────────────────── Séance 4 — bloc 7 : la glycolyse ─────────────────────────

diapo(
    id="rf_g1_activation", type="simulation", demarche=5, comp=["C5"],
    titre="Phase 1 : activer le glucose",
    lead="La glycolyse commence par une dépense : deux ATP.",
    page=REF + "glycolyse-phases.html?demarche=5", legende="Glycolyse, phase 1 : l'activation",
    alt="Le glucose entre ; deux pièces ATP sont payées, deux phosphates s'accrochent : le fructose diphosphate",
    montre="Le glucose entre dans la bande « activation » ; une pièce ATP est payée, un phosphate s'accroche, puis "
           "une deuxième : le fructose diphosphate (P-C6-P).",
    fr="Maintenant que nous avons l'ATP et le taxi, nous pouvons ouvrir la glycolyse et voir ce qu'il y a dedans. "
       "Elle a trois phases. Le glucose entre, six carbones. La première phase s'appelle l'activation. Regarde : la "
       "cellule donne un ATP, et son phosphate s'attache au glucose. Puis elle donne un deuxième ATP, et un deuxième "
       "phosphate s'attache. Donc deux ATP ont été utilisés. Nous avons maintenant le fructose diphosphate : six "
       "carbones et deux phosphates. C'est beau, non ? La cellule veut de l'énergie, et elle commence par en donner ! "
       "Comme quand il faut payer à la porte pour entrer : tu donnes deux ATP maintenant, et tu gagneras plus "
       "ensuite.",
    mx="دابا عندنا l'ATP والطاكسي، ونقدرو نحلو la glycolyse ونشوفو شنو كاين لداخل. فيها trois phases. "
       "<m:glucose_entre>كيدخل <r:glucose>le glucose، six carbones. <r:phase1>la phase الأولى سميتها l'activation. "
       "<m:atp1>شوف: la cellule كتعطي un ATP، و le phosphate ديالو كيبقى لاصق ف le glucose. <m:atp2>ومن بعد كتعطي "
       "un deuxième ATP، وكيتزاد un deuxième phosphate. <r:atp_payes>إذن deux ATP مشاو. <m:fructose_dp>ودابا عندنا "
       "<r:fructose_dp>le fructose diphosphate: six carbones، و deux phosphates. زوينة هادي، ياك؟ la cellule بغات "
       "l'énergie، وهي كتبدا بالعطا! بحال ملي خاصك تخلص ف الباب باش تدخل: كتعطي deux ATP دابا، ومن بعد غادي تربح "
       "كثر.",
    bullets=["Phase 1 : activation.", "2 ATP consommés : glucose → fructose diphosphate."],
    cahier="Phase 1, activation : le glucose (C6) reçoit 2 phosphates ; 2 ATP sont consommés.",
)

diapo(
    id="rf_g2_scission", type="simulation", demarche=5, comp=["C5"],
    titre="Phase 2 : couper en deux",
    lead="Une chaîne de six carbones devient deux chaînes de trois ; tout se passe ensuite deux fois.",
    page=REF + "glycolyse-phases.html?depart=fructose_dp&demarche=5", legende="Glycolyse, phase 2 : la scission",
    alt="Le fructose diphosphate se coupe en deux chaînes de trois carbones ; un taxi se charge sur chaque branche",
    montre="Le fructose diphosphate se coupe en deux C3-P ; sur chaque branche un taxi NAD⁺ se charge (NADH,H⁺), "
           "puis un phosphate inorganique entre : P-C3-P.",
    fr="Le fructose diphosphate est prêt, et voici la deuxième phase : la scission, c'est-à-dire la coupure. "
       "Regarde : la chaîne de six carbones s'est coupée en deux, une ici et une là. Chacune a trois carbones et un "
       "phosphate. Maintenant tout va se passer deux fois : une fois de chaque côté. Du premier côté, deux "
       "hydrogènes sont enlevés, et un taxi les prend : NAD plus devient NADH,H plus. Et du deuxième côté, la même "
       "chose. Nous avons donc deux NADH,H plus. Ensuite, un nouveau phosphate entre de chaque côté, sans dépenser "
       "d'ATP. Chaque chaîne a maintenant deux phosphates.",
    mx="le fructose diphosphate واجد، وجات <r:phase2>la phase الثانية: la scission، يعني القسمة. <m:scission>شوف: "
       "السلسلة ديال six carbones تقسمات على جوج، <r:c3_gauche>وحدة هنا <r:c3_droite>ووحدة هنا. كل وحدة فيها trois "
       "carbones، و un phosphate. ودابا كلشي غادي يوقع جوج مرات: مرة ف كل جهة. <m:taxi1>ف الجهة الأولى، كيتحيدو "
       "deux hydrogènes، وطاكسي كيهز les hydrogènes: N A D plus كيولي N A D H, H plus. <m:taxi2>وف الجهة الثانية، نفس الحاجة. "
       "<r:taxis>إذن عندنا جوج ديال الطاكسيات عامرين. <m:pi>ومن بعد، كيدخل un phosphate جديد ف كل جهة، بلا ما "
       "نعطيو ATP. دابا كل سلسلة فيها deux phosphates.",
    bullets=["Phase 2 : scission, C6 → 2 C3.", "2 NAD⁺ réduits en 2 NADH,H⁺."],
    cahier="Phase 2, scission : le C6 est coupé en 2 C3 ; 2 NAD⁺ sont réduits en 2 NADH,H⁺.",
)

diapo(
    id="rf_g3_oxydation", type="simulation", demarche=5, comp=["C5"],
    titre="Phase 3 : l'énergie récupérée",
    lead="Deux ATP de chaque côté ; il reste deux acides pyruviques.",
    page=REF + "glycolyse-phases.html?depart=pi&demarche=5", legende="Glycolyse, phase 3 : la formation d'énergie",
    alt="Sur chaque branche, deux phosphates passent sur deux ADP et donnent deux ATP ; il reste deux acides pyruviques",
    montre="Sur chaque branche, les deux phosphates passent sur deux ADP : deux ATP, puis deux autres ; les deux "
           "chaînes de trois carbones sont les acides pyruviques (CH₃-CO-COOH).",
    fr="Voici le moment où la cellule gagne. C'est la troisième phase : l'énergie en sort. Du premier côté : les "
       "deux phosphates passent sur deux ADP, et donnent deux ATP. Et du deuxième côté : deux autres ATP. Comptons : "
       "deux plus deux égale quatre ATP. Et que reste-t-il des chaînes ? Deux molécules d'acide pyruvique, chacune à "
       "trois carbones. C'est l'acide pyruvique que nous avons suivi avec le glucose marqué. Sa formule : "
       "CH3-CO-COOH. Tu vois ? On a donné au début, et maintenant on a gagné.",
    mx="جا الوقت باش la cellule تربح. <r:phase3>هادي la phase الثالثة: فيها كتخرج l'énergie. <m:atp_branche1>ف "
       "الجهة الأولى: <r:c3_gauche>les deux phosphates كيمشيو ل deux ADP، وكيعطيو deux ATP. <m:atp_branche2>وف الجهة "
       "الثانية: <r:c3_droite>deux ATP أخرى. <r:atp_gagnes>نحسبو: deux plus deux égale quatre ATP. "
       "<m:pyruvates>وشنو بقا من السلاسل؟ <r:pyruvates>deux molécules ديال l'acide pyruvique، كل وحدة فيها trois "
       "carbones. هادا هو l'acide pyruvique اللي تبعنا ب le glucose marqué. و la formule ديالو: C H trois, C O, C O "
       "O H. شفتي؟ عطينا ف اللول، ودابا ربحنا.",
    bullets=["Phase 3 : 2 ATP par C3, donc 4 ATP.", "Il reste 2 acides pyruviques : CH₃-CO-COOH."],
    cahier="Phase 3, formation d'énergie : 4 ATP sont formés ; il reste 2 acides pyruviques (CH₃-CO-COOH).",
)

diapo(
    id="rf_g4_bilan", type="simulation", demarche=6, comp=["C5"], etoile=True,
    titre="Le bilan de la glycolyse",
    lead="Quatre ATP formés, deux consommés : la glycolyse fait gagner deux ATP.",
    page=REF + "glycolyse-phases.html?depart=pyruvates&demarche=6", legende="Le bilan de la glycolyse",
    alt="Les trois bandes de la glycolyse finies ; les ATP payés et gagnés s'allument et se comptent, puis l'équation",
    montre="Les ATP gagnés (4) et payés (2) s'allument un à un : 4 − 2 = 2 ; puis l'équation globale s'écrit.",
    fr="Faisons maintenant le compte de toute la glycolyse. Cette partie tombe souvent au national, concentre-toi "
       "bien. D'abord l'ATP : nous en avons gagné quatre, et donné deux. Quatre moins deux égale deux : la cellule a "
       "gagné deux ATP. Nous avons aussi deux NADH,H plus, et deux acides pyruviques. Et tout s'est passé dans le "
       "hyaloplasme, sans dioxygène : c'est la glycolyse de notre carte. On écrit le bilan : glucose plus deux ADP "
       "plus deux phosphates plus deux NAD plus donne deux acides pyruviques plus deux ATP plus deux NADH,H plus. "
       "Autrement dit : tu as coupé le billet en deux, tu as donné deux pièces, et on t'en a rendu quatre. Je "
       "relis : la glycolyse donne deux acides pyruviques, deux ATP et deux NADH,H plus.",
    mx="نديرو دابا الحساب ديال la glycolyse كاملة. هاد الجزء كيجي بزاف ف le national، ركز مزيان. <m:compte_atp>l'ATP "
       "اللول: <r:atp_gagnes>ربحنا quatre، <r:atp_payes>وعطينا deux. <c:4 ATP formés − 2 ATP consommés = 2 "
       "ATP>Quatre moins deux égale deux: ربحنا deux ATP. <r:taxis>وعندنا deux N A D H, H plus، "
       "<r:pyruvates>و deux acides pyruviques. وكلشي وقع ف le hyaloplasme، بلا dioxygène: هادي هي la glycolyse ديال "
       "la carte ديالنا. <m:bilan>كنكتبو le bilan: <c:C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃-CO-COOH + 2 ATP + 2 "
       "NADH,H⁺>glucose, plus deux A D P, plus deux phosphates, plus deux N A D plus, <r:bilan>donne deux acides "
       "pyruviques, plus deux A T P, plus deux N A D H, H plus. بطريقة أخرى: قسمتي الورقة على جوج، <r:atp_payes>عطيتي "
       "deux، وردو ليك quatre. نعاود نقرا: la glycolyse donne deux acides pyruviques, deux A T P, et deux N A D H, "
       "H plus.",
    question="rf_g4_bilan",
    bullets=["Bilan en ATP : 4 − 2 = 2 ATP.", "Dans le hyaloplasme, sans dioxygène."],
    cahier="Formule : C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃-CO-COOH + 2 ATP + 2 NADH,H⁺\n"
           "Bilan : 4 ATP formés − 2 ATP consommés = 2 ATP, dans le hyaloplasme, sans dioxygène.",
)

# ───────────────────────── Séance 5 — bloc 8 : la mitochondrie utilise l'acide pyruvique ─────────────────────────

diapo(
    id="rf_m1_principe", type="simulation", demarche=3, comp=["C6"], etoile=True,
    titre="Comment isoler des mitochondries ?",
    lead="La centrifugation : tourner vite pour séparer selon la densité.",
    page=REF + "centrifugation.html?vue=principe&demarche=3", legende="Le principe de la centrifugation",
    alt="Une essoreuse à salade qui tourne ; puis un tube qui tourne : les grains lourds vont au fond",
    montre="L'essoreuse à salade : ce qui tourne vite part vers le bord. Puis un tube qui tourne : les grains "
           "lourds se déposent au fond (le culot), le reste au-dessus (le surnageant) ; les deux mots s'écrivent.",
    fr="Nous savons que l'acide pyruvique entre dans la mitochondrie. Pour en être sûrs, il nous faut des "
       "mitochondries seules, hors de la cellule. Comment les isoler ? Je te veux avec moi maintenant, cette partie "
       "est importante. Pense à l'essoreuse à salade : quand elle tourne vite, l'eau part sur le côté. La même "
       "idée : on met le mélange dans un tube, et on le fait tourner vite. Ce qui est lourd descend en bas : c'est "
       "le culot. Et ce qui est léger reste dans le liquide du dessus : c'est le surnageant. Cette méthode s'appelle "
       "la centrifugation. Autrement dit : la rotation sépare le lourd du léger. Je relis : la centrifugation sépare "
       "les constituants selon leur densité.",
    mx="عرفنا أن l'acide pyruvique كيدخل ل la mitochondrie. باش نتأكدو، خاصنا les mitochondries بوحدهم، برا الخلية. "
       "كيفاش نعزلوهم؟ بغيتك تكون معايا دابا، هاد الجزء مهم. <m:manege>تفكر l'essoreuse ديال la salade: ملي كتدور "
       "بسرعة، الما كيمشي للجنب. <m:tube>نفس الفكرة: كنديرو كلشي ف <r:tube>واحد le tube، وكيدور بسرعة. "
       "<m:culot>اللي lourd كيهبط لتحت: <r:culot>هادا le culot. واللي خفيف كيبقى ف السائل اللي الفوق: "
       "<r:surnageant>هادا le surnageant. هاد الطريقة سميتها <c:Centrifugation : séparer selon la densité, par une "
       "rotation rapide>la centrifugation. بطريقة أخرى: الدورة بسرعة كتفرق اللي lourd على اللي خفيف. نعاود نقرا: la "
       "centrifugation sépare les constituants, selon leur densité.",
    bullets=["Centrifugation : séparer selon la densité.", "Au fond : le culot ; au-dessus : le surnageant."],
    cahier="Définition : la centrifugation sépare les constituants d'un mélange selon leur densité, par une "
           "rotation rapide (culot au fond, surnageant au-dessus).",
)

diapo(
    id="rf_m1_etapes", type="simulation", demarche=3, comp=["C6"],
    titre="La centrifugation fractionnée",
    lead="Deux centrifugations de suite : la deuxième isole les mitochondries.",
    page=REF + "centrifugation.html?vue=etapes&demarche=3", legende="La centrifugation fractionnée",
    alt="Des fragments de foie broyés, une centrifugeuse qui tourne, un culot de noyaux, puis un culot de mitochondries",
    montre="Les fragments de foie dans la solution de saccharose, le broyage, la première centrifugation à faible "
           "vitesse et son culot de noyaux. Arrêt : question. Puis le surnageant versé dans un nouveau tube, la "
           "deuxième centrifugation à grande vitesse et le culot de mitochondries.",
    fr="Appliquons la centrifugation à de vraies cellules. On prend de petits morceaux de foie, dans une solution "
       "de saccharose. On les broie avec le broyeur : les cellules sont cassées, et tout en sort : les noyaux et "
       "les mitochondries. Premier tour : la centrifugeuse tourne doucement. Qui est descendu en bas ? Les noyaux, "
       "car ce sont eux les plus lourds. Les mitochondries sont plus légères que les noyaux. Réfléchis à l'endroit "
       "où elles sont. Les mitochondries sont légères, donc elles sont restées en haut, dans le surnageant. On le "
       "verse dans un nouveau tube. Deuxième tour : cette fois, très vite. Et maintenant les mitochondries sont "
       "descendues en bas. On l'appelle la centrifugation fractionnée : chaque tour isole une partie.",
    mx="نطبقو la centrifugation على خلايا ديال بصح. <m:foie>كناخدو <r:foie>شي قطع صغار ديال le foie، ف واحد la "
       "solution ديال le saccharose. <m:broyage>كنهرسو هاد القطع ب <r:broyeur>le broyeur: الخلايا كيتحلو، وكيخرج منهم "
       "كلشي: les noyaux و les mitochondries. <m:centri1>الدورة الأولى: <r:centrifugeuse>la centrifugeuse كتدور "
       "بالشوية. <m:culot_noyaux>شكون هبط لتحت؟ <r:culot_noyaux>les noyaux، حيت هما اللي lourd. و les mitochondries "
       "خفيفة على les noyaux. فكر فين غادي يكونو. <m:surnageant>les mitochondries خفيفة، إذن بقاو الفوق، "
       "<r:surnageant>ف le surnageant. كنحولوه ل tube جديد. <m:centri2>الدورة الثانية: هاد المرة بسرعة كبيرة. "
       "<m:culot_mitochondries>ودابا <r:culot_mitochondries>les mitochondries هبطو لتحت. <m:bilan>هادي سميتها la "
       "centrifugation fractionnée: كل دورة كتعزل جزء.",
    obs="rf_m1_etapes",
    bullets=["Faible vitesse : culot de noyaux.", "Grande vitesse : culot de mitochondries."],
    cahier="Centrifugation fractionnée : broyage, puis faible vitesse (noyaux), puis grande vitesse (mitochondries).",
)

diapo(
    id="rf_m2_glucose", type="simulation", demarche=4, comp=["C6", "C1"],
    titre="Des mitochondries seules : on ajoute du glucose",
    lead="Hypothèse : si la mitochondrie utilise le glucose, le dioxygène doit baisser.",
    page=REF + "exao-mitochondries.html?demarche=4", legende="Mitochondries isolées et glucose",
    alt="Un bioréacteur de mitochondries avec un oxymètre ; à l'écran, le dioxygène reste à 275 µmol/L après le glucose",
    montre="Le bioréacteur de mitochondries et son oxymètre ; les axes ; le palier à 275 µmol/L ; le glucose est "
           "injecté à t1. Arrêt : question. Puis le palier continue : rien ne change.",
    fr="Les mitochondries, nous les avons maintenant seules, et nous pouvons leur demander : que consommez-vous ? "
       "Nous les avons mises dans un bioréacteur, dans une eau qui contient du dioxygène, avec l'oxymètre : la sonde "
       "qui mesure le dioxygène. Les axes : le temps en minutes, et le dioxygène en micromoles par litre. Au début, "
       "le dioxygène est stable : deux cent soixante-quinze micromoles par litre. L'hypothèse : si la mitochondrie "
       "utilise le glucose, alors le dioxygène va diminuer. On ajoute le glucose, à cet instant. Regarde la courbe. "
       "Rien ! Le dioxygène est resté stable. Les mitochondries n'ont pas utilisé le glucose. Notre hypothèse est "
       "donc fausse, et c'est normal en science : c'est l'expérience qui décide.",
    mx="les mitochondries دابا عندنا بوحدهم، ونقدرو نسولو: شنو كيستهلكو؟ <r:mitochondries>درناهم ف bioréacteur، ف "
       "الما اللي فيه le dioxygène، <r:oxymetre>ومعاهم l'oxymètre: la sonde ديال le dioxygène. <m:axes>les axes: le "
       "temps en minutes، و le dioxygène en micromoles par litre. <m:t0>ف البداية، <r:courbe>le dioxygène ثابت: "
       "deux cent soixante-quinze micromoles par litre. l'hypothèse: يلا كانت la mitochondrie كتستعمل le glucose، "
       "إذن le dioxygène غادي ينقص. <m:glucose_injecte>كنزيدو <r:seringue>le glucose، <r:t1>ف هاد اللحظة. شوف la "
       "courbe. <m:rien>والو! le dioxygène بقا ثابت. les mitochondries ما استعملوش le glucose. إذن l'hypothèse "
       "ديالنا غالطة، وهادا عادي ف العلم: التجربة هي اللي كتحكم.",
    obs="rf_m2_glucose",
    bullets=["Mitochondries isolées + glucose.", "Le dioxygène reste stable : le glucose n'est pas utilisé."],
    cahier="Des mitochondries isolées ne consomment pas de dioxygène en présence de glucose.",
)

diapo(
    id="rf_m2_pyruvate", type="simulation", demarche=5, comp=["C6", "C1"], etoile=True,
    titre="On ajoute l'acide pyruvique",
    lead="Avec l'acide pyruvique, le dioxygène baisse : la mitochondrie l'utilise.",
    page=REF + "exao-mitochondries.html?depart=rien&demarche=5", legende="Mitochondries isolées et acide pyruvique",
    alt="Après l'ajout d'acide pyruvique, la courbe du dioxygène descend régulièrement de 275 à 215 µmol/L",
    montre="L'acide pyruvique est injecté à t2 ; le dioxygène baisse régulièrement de 275 à 215 µmol/L pendant que "
           "les mitochondries de la cuve absorbent le dioxygène ; la description puis la déduction s'écrivent.",
    fr="Ce n'est pas le glucose. Alors quoi ? Rappelle-toi le glucose marqué : qui est entré dans la mitochondrie ? "
       "L'acide pyruvique. Essayons-le. Suis-moi doucement, c'est un résultat dont tu auras toujours besoin. On "
       "ajoute l'acide pyruvique, à cet instant. Et regarde la courbe : le dioxygène diminue ! Les mitochondries "
       "consomment le dioxygène. Décrivons : après l'ajout de l'acide pyruvique, le dioxygène diminue, de deux cent "
       "soixante-quinze à deux cent quinze micromoles par litre. Donc : la mitochondrie utilise l'acide pyruvique, "
       "et non le glucose. Autrement dit : la centrale ne fonctionne pas avec le billet entier, seulement avec le "
       "billet coupé. Je relis : la mitochondrie utilise l'acide pyruvique, produit par la glycolyse, et non le "
       "glucose.",
    mx="ماشي le glucose. إذن شنو؟ تفكر le glucose marqué: شكون اللي دخل ل la mitochondrie؟ l'acide pyruvique. "
       "نجربو. تبعني بالشوية، هادي نتيجة غادي تحتاجها ديما. <m:pyruvate_injecte>كنزيدو <r:seringue>l'acide "
       "pyruvique، <r:t2>ف هاد اللحظة. <m:o2_baisse>وشوف <r:courbe>la courbe: le dioxygène كينقص! "
       "<r:mitochondries>les mitochondries كيستهلكو le dioxygène. <m:decrire>la description: après l'ajout de l'acide "
       "pyruvique, le dioxygène diminue, de deux cent soixante-quinze, à deux cent quinze micromoles par litre. "
       "<m:deduire>Donc: <c:Donc la mitochondrie utilise l'acide pyruvique, et non le glucose>la mitochondrie "
       "utilise l'acide pyruvique, <r:conclusion>et non le glucose. بطريقة أخرى: la centrale ما كتخدمش ب الورقة "
       "كاملة، كتخدم غير ب الورقة مقسومة. نعاود نقرا: la mitochondrie utilise l'acide pyruvique, produit par la "
       "glycolyse, et non le glucose.",
    question="rf_m2_pyruvate",
    bullets=["Acide pyruvique ajouté : le dioxygène diminue.", "La mitochondrie utilise l'acide pyruvique, pas le glucose."],
    cahier="Donc la mitochondrie utilise l'acide pyruvique, produit par la glycolyse, et non le glucose.",
)

# ───────────────────────── Séance 5 — bloc 9 : l'ultrastructure ─────────────────────────

diapo(
    id="rf_m3_zoom", type="simulation", demarche=4, comp=["C7"],
    titre="De la cellule à la mitochondrie",
    lead="Deux agrandissements successifs au microscope électronique.",
    page=REF + "zoom.html?demarche=4", legende="De la cellule aux sphères pédonculées",
    alt="Une cellule × 8 000, un cadre rouge sur une mitochondrie, la mitochondrie × 45 000, puis des sphères sur une crête",
    montre="La cellule × 8 000 et ses mitochondries roses ; un cadre rouge ; le zoom animé sur une mitochondrie "
           "× 45 000 (double membrane, crêtes) ; sa taille ; un second cadre ; le zoom sur les sphères pédonculées.",
    fr="Cette mitochondrie qui utilise l'acide pyruvique, comment est-elle faite à l'intérieur ? Approchons-nous "
       "avec le microscope électronique. Voici une cellule, agrandie huit mille fois : les mitochondries sont ces "
       "éléments roses. On en choisit une, et on l'agrandit encore : quarante-cinq mille fois. Regarde : elle a deux "
       "membranes, et la membrane intérieure fait des replis. Et quelle est sa taille ? Entre zéro virgule cinq et "
       "un micromètre. Le micromètre, c'est un millième de millimètre : très petite ! Approchons-nous encore, et "
       "nous voyons de petites boules attachées à la membrane intérieure. Toutes ces parties ont un nom, et nous "
       "allons les apprendre maintenant.",
    mx="هاد la mitochondrie اللي كتستعمل l'acide pyruvique، كيفاش دايرة من الداخل؟ نشوفوها ب le microscope "
       "électronique. <m:cellule>هادي <r:cellule>خلية، مكبرة huit mille fois: les mitochondries هما هاد الحوايج "
       "الصغار. <m:cadre>ناخدو وحدة منهم، <m:mitochondrie>ومكبرة كثر: quarante-cinq mille fois. <r:mitochondrie>شوف: "
       "عندها جوج ديال الأغشية، <r:cretes>والغشاء الداخلي كيدخل ويخرج. <m:taille>وشحال الحجم ديالها؟ Entre zéro "
       "virgule cinq, et un micromètre. و le micromètre هو un millième de millimètre: صغيرة بزاف! <m:cadre2>نزيدو "
       "نكبرو، <m:spheres>وكنشوفو <r:spheres>كورات صغار لاصقين ف الغشاء الداخلي. كل جزء من هاد الأجزاء عندو السمية ديالو، وغادي "
       "نعرفوها دابا.",
    bullets=["Mitochondrie : 0,5 à 1 µm de diamètre.", "1 µm = un millième de millimètre."],
    cahier="La mitochondrie est un organite en bâtonnet, de 0,5 à 1 µm de diamètre.",
)

diapo(
    id="rf_m3_legender", type="simulation", comp=["C7"], etoile=True,
    titre="La mitochondrie : six mots",
    lead="Le schéma que le bac fait légender.",
    page=RAP + "mitochondrie.html?depart=0", legende="La mitochondrie en coupe",
    alt="La mitochondrie en coupe : deux membranes, des crêtes, la matrice, et une crête agrandie avec ses sphères",
    montre="La mitochondrie en coupe ; ses légendes se posent une à une : membrane externe, membrane interne, "
           "crêtes, espace intermembranaire, matrice ; dans le médaillon, les sphères pédonculées.",
    fr="Allons-y, nommons chaque partie de la mitochondrie. S'il y a une chose qui doit te rester de cette séance, "
       "c'est ce schéma : très important à l'examen. Il a six mots. La membrane du dehors : la membrane externe. La "
       "membrane du dedans : la membrane interne. Elle fait des replis : ce sont les crêtes. Entre les deux "
       "membranes : l'espace intermembranaire. Et tout ce qui est au centre : la matrice, où se trouve aussi l'ADN "
       "de la mitochondrie. Et dans le cercle, les petites boules : les sphères pédonculées, attachées à la membrane "
       "interne. Autrement dit : les crêtes sont comme des étagères : elles donnent plus de place dans la centrale. "
       "Je relis : membrane externe, espace intermembranaire, membrane interne, crêtes, matrice, sphères "
       "pédonculées.",
    mx="يلا نسميو كل جزء ف la mitochondrie. إلى كانت شي حاجة غادي تبقى فراسك من هاد الحصة، هي هاد le schéma: مهم "
       "بزاف ف الامتحان. فيه ستة ديال الكلمات. <m:membrane_externe>الغشاء اللي برا: <r:membrane_externe>la membrane "
       "externe. <m:membrane_interne>الغشاء اللي لداخل: <r:membrane_interne>la membrane interne. <m:cretes>وهي كتدخل "
       "وتخرج: <r:cretes>هادو les crêtes. <m:espace_intermembranaire>بين جوج الأغشية: "
       "<r:espace_intermembranaire>l'espace intermembranaire. <m:matrice>وكل اللي ف الوسط: <r:matrice>la matrice، "
       "وفيها حتى l'ADN ديال la mitochondrie. <r:medaillon>وف الدائرة، <m:spheres_pedonculees>الكورات الصغار: "
       "<r:spheres_pedonculees>les sphères pédonculées، لاصقين ف la membrane interne. بطريقة أخرى: les crêtes بحال "
       "des étagères: كيزيدو البلاصة ف la centrale. <c:Mitochondrie : membrane externe · espace intermembranaire · "
       "membrane interne · crêtes · matrice · sphères pédonculées>نعاود نقرا: membrane externe, espace "
       "intermembranaire, membrane interne, crêtes, matrice, sphères pédonculées.",
    bullets=["Un organite à double membrane.", "Les crêtes portent les sphères pédonculées."],
    cahier="Mitochondrie : membrane externe, espace intermembranaire, membrane interne (crêtes, sphères "
           "pédonculées), matrice (avec l'ADN mitochondrial).",
)

diapo(
    id="rf_m3_construire", type="simulation", comp=["C7"],
    titre="À toi de légender",
    lead="Pose les six étiquettes au bout des flèches, comme au bac.",
    page=RAP + "mitochondrie.html?vue=construire&depart=0", legende="Légender la mitochondrie",
    alt="La mitochondrie en coupe sans ses noms, une crête agrandie, six flèches et six étiquettes à glisser",
    montre="La même mitochondrie sans ses noms, six flèches et six étiquettes à glisser ; une étiquette bien "
           "placée devient verte ; si l'élève ne bouge rien, le tuteur les place.",
    fr="Et maintenant, c'est ton tour : voici la même mitochondrie, mais sans les noms. En bas, il y a six "
       "étiquettes : membrane externe, membrane interne, crêtes, espace intermembranaire, matrice, sphères "
       "pédonculées. Glisse chacune jusqu'au bout de sa flèche : si elle est à sa place, elle devient verte. Je te "
       "donne un conseil : en haut, les deux membranes et l'espace entre elles. En bas, la membrane interne et la "
       "matrice. Et à droite, dans la crête agrandie, les sphères pédonculées. Prends ton temps, rien ne presse. Et "
       "si tu ne bouges rien, c'est moi qui les placerai.",
    mx="ودابا النوبة ديالك: <m:etiquettes>هادي <r:schema>نفس la mitochondrie، ولكن بلا الأسماء. <r:etiquettes>لتحت "
       "كاينين six étiquettes: membrane externe، membrane interne، crêtes، espace intermembranaire، matrice، sphères "
       "pédonculées. جر كل وحدة حتى للراس ديال السهم ديالها: يلا كانت ف البلاصة ديالها، كتولي خضرا. نعطيك واحد "
       "نصيحة: <r:zone_membranes>الفوق، جوج الأغشية و l'espace اللي بيناتهم. <r:zone_interieur>ولتحت، la membrane "
       "interne و la matrice. <r:medaillon>وعلى اليمين، ف la crête المكبرة، les sphères pédonculées. خود الوقت "
       "ديالك، عندك الوقت. ويلا ما درتي والو، أنا اللي غادي نحطهم.",
    legende_eleve=True,
    bullets=["Repère : les sphères pédonculées sont sur la membrane interne."],
    cahier="Schéma à savoir légender : la mitochondrie en coupe (6 légendes).",
)

# ───────────────────────── Séance 5 — bloc 10 : la composition ─────────────────────────

diapo(
    id="rf_m4_membranes", type="simulation", demarche=5, comp=["C8"],
    titre="De quoi sont faites les deux membranes ?",
    lead="Deux membranes, deux compositions : la membrane interne est très riche en protéines.",
    page=REF + "composition.html?demarche=5", legende="La composition des deux membranes",
    alt="Une coupe de mitochondrie ; deux barres se remplissent : 40 / 60 pour la membrane externe, 20 / 80 pour l'interne",
    montre="La coupe peinte ; pour la membrane externe deux barres se remplissent (40 % lipides, 60 % protéines), "
           "comparée à la membrane de la cellule ; pour la membrane interne (20 % / 80 %) ; puis ses enzymes et "
           "transporteurs se dessinent, et la sphère pédonculée s'allume : ATP synthase.",
    fr="Chaque partie a maintenant son nom. Mais pour comprendre son travail, il faut savoir de quoi elle est "
       "faite. Commençons par la membrane externe : quarante pour cent de lipides, et soixante pour cent de "
       "protéines. Elle ressemble à la membrane de la cellule : elle laisse seulement passer les substances. "
       "Maintenant la membrane interne : vingt pour cent de lipides, et quatre-vingts pour cent de protéines. "
       "Beaucoup ! Pourquoi toutes ces protéines ? Parce que ce sont elles qui travaillent : des enzymes, "
       "c'est-à-dire des protéines qui font les réactions, et des transporteurs d'électrons. Et il y a aussi la "
       "sphère pédonculée : elle contient l'ATP synthase, une enzyme qui produit l'ATP. Donc la membrane interne "
       "n'est pas un simple mur : c'est un lieu de travail.",
    mx="كل جزء عرفنا سميتو. ولكن باش نفهمو الخدمة ديالو، خاصنا نعرفو من شنو مكون. <m:externe>نبداو ب "
       "<r:membrane_externe>la membrane externe: quarante pour cent lipides، و soixante pour cent protéines. "
       "<m:comme_cellule>هادي قريبة من la membrane ديال la cellule: غير كتخلي الحوايج يدوزو. <m:interne>ودابا "
       "<r:membrane_interne>la membrane interne: vingt pour cent lipides، و quatre-vingts pour cent protéines. بزاف! "
       "علاش هاد les protéines كاملين؟ <m:enzymes_interne>حيت هما اللي خدامين: des enzymes، يعني des protéines اللي "
       "كيديرو les réactions، و des transporteurs d'électrons. <m:atp_synthase>وكاينة حتى <r:sphere>la sphère "
       "pédonculée: فيها l'ATP synthase، une enzyme اللي كتنتج l'ATP. يعني la membrane interne ماشي غير الحيط: هي "
       "بلاصة ديال الخدمة.",
    bullets=["Membrane externe : 40 % lipides, 60 % protéines.", "Membrane interne : 20 % lipides, 80 % protéines."],
    cahier="Membrane interne : 80 % de protéines (enzymes d'oxydoréduction, transporteurs d'électrons, ATP synthase).",
)

diapo(
    id="rf_m4_matrice", type="simulation", demarche=6, comp=["C8"], etoile=True,
    titre="La matrice : deux familles d'enzymes",
    lead="Dans la matrice : de l'acide pyruvique, pas de glucose, et deux familles d'enzymes.",
    page=REF + "composition.html?depart=atp_synthase&demarche=6", legende="La composition de la matrice",
    alt="Dans la matrice : acide pyruvique, ATP, transporteurs, un glucose barré ; une enzyme retire un CO₂, une autre des H",
    montre="Le contenu de la matrice (acide pyruvique, transporteurs, ATP, ADP, Pi ; un glucose barré) ; puis la "
           "décarboxylase retire un CO₂ et la déshydrogénase retire des hydrogènes vers un taxi ; l'hypothèse pour "
           "la suite s'écrit.",
    fr="Il nous reste la matrice. C'est ici que beaucoup d'élèves se trompent : c'est important, suis-la bien. Qu'y "
       "a-t-il dans la matrice ? L'acide pyruvique, l'ATP, l'ADP et les transporteurs d'hydrogène. Et le glucose ? "
       "Il n'y en a pas, et cela nous le savons. Elle contient deux types d'enzymes. Les décarboxylases : dé veut "
       "dire enlever, et carboxyl, c'est le CO2. Elles enlèvent donc du dioxyde de carbone. Et les "
       "déshydrogénases : elles enlèvent des hydrogènes, et les donnent au taxi, NAD plus. Autrement dit : les unes "
       "coupent un carbone, les autres remplissent les taxis. Nous avons donc une hypothèse pour le prochain cours : "
       "dans la matrice, l'acide pyruvique est dégradé, et il donne du dioxyde de carbone et des taxis pleins. Je "
       "relis : décarboxylases, elles retirent le CO2. Déshydrogénases, elles retirent les hydrogènes.",
    mx="بقات لينا la matrice. هنا بالضبط فين كاين المشكل عند بزاف ديال التلاميذ: هادي مهمة، تبع مزيان. <m:matrice>شنو "
       "كاين ف <r:matrice>la matrice؟ l'acide pyruvique، l'ATP، l'ADP، و les transporteurs d'hydrogène. و le "
       "glucose؟ ما كاينش، وهادشي كنعرفوه. <m:enzymes_matrice>وفيها نوعين ديال les enzymes. <r:decarboxylase>les "
       "décarboxylases: dé يعني كتحيد، و carboxyl هو C O deux. <c:Décarboxylases : retirent du CO₂ · "
       "Déshydrogénases : retirent des hydrogènes>يعني كتحيد le dioxyde de carbone. <r:deshydrogenase>و les "
       "déshydrogénases: كتحيد les hydrogènes، والطاكسي كيهزهم، N A D plus. بطريقة أخرى: وحدة كتحيد le carbone، "
       "ووحدة كتعمر الطاكسي. <m:hypothese>إذن عندنا hypothèse ل الدرس الجاي: ف la matrice، l'acide pyruvique "
       "كيتفكك، وكيعطي le dioxyde de carbone، وطاكسيات عامرين. نعاود نقرا: décarboxylases, elles retirent le C O "
       "deux. Déshydrogénases, elles retirent les hydrogènes.",
    question="rf_m4_matrice",
    bullets=["Décarboxylases : retirent du CO₂.", "Déshydrogénases : retirent des hydrogènes (vers NAD⁺)."],
    cahier="Matrice : acide pyruvique, pas de glucose ; décarboxylases (retirent du CO₂) et déshydrogénases "
           "(retirent des hydrogènes).",
)

# ───────────────────────── Séance 5 — bloc 11 : le bilan ─────────────────────────

diapo(
    id="rf_b1_bilan", type="synthesis", acquis=True,
    titre="Ce qu'il faut retenir",
    lead="La fiche du chapitre, point par point, puis ta page : ce qu'il te reste à retravailler.",
    page=REF + "bilan.html", legende="Ce qu'il faut retenir",
    alt="Une fiche de révision à la craie, écrite point par point, puis la page de l'élève",
    montre="La fiche « Ce qu'il faut retenir » s'écrit point par point au rythme de la voix, puis la page de "
           "l'élève : ce qu'il lui reste à retravailler. Bouton imprimer.",
    fr="Voici la fiche du cours. Premier point, la respiration cellulaire : oxydation complète du glucose, avec le "
       "dioxygène, et beaucoup d'énergie. Deuxième, la fermentation : sans dioxygène, oxydation incomplète, elle "
       "donne l'éthanol, et peu d'énergie. Troisième, les lieux : la fermentation dans le hyaloplasme, et la "
       "respiration a besoin de la mitochondrie. Quatrième, la glycolyse : dans le hyaloplasme, elle donne deux "
       "acides pyruviques, deux ATP et deux transporteurs réduits. Cinquième : la mitochondrie utilise l'acide "
       "pyruvique, pas le glucose. Et sixième : la mitochondrie a une double membrane, et sa membrane interne est "
       "riche en enzymes. Et maintenant ta page : regarde ce qu'il te reste à revoir.",
    mx="هادي la fiche ديال الدرس: <m:respiration>النقطة الأولى، la respiration cellulaire: oxydation complète du "
       "glucose، مع le dioxygène، وبزاف ديال l'énergie. <m:fermentation>الثانية، la fermentation: بلا dioxygène، "
       "oxydation incomplète، كتعطي l'éthanol، و l'énergie قليلة. <m:lieux>الثالثة، البلايص: la fermentation ف le "
       "hyaloplasme، و la respiration كتحتاج la mitochondrie. <m:glycolyse>الرابعة، la glycolyse: ف le hyaloplasme، "
       "كتعطي deux acides pyruviques، deux ATP، و deux transporteurs réduits. <m:mitochondrie>الخامسة: la "
       "mitochondrie كتستعمل l'acide pyruvique، ماشي le glucose. <m:structure>والسادسة: la mitochondrie عندها double "
       "membrane، و la membrane interne ديالها عامرة ب les enzymes. <m:lacunes>ودابا الصفحة ديالك: شوف شنو باقي "
       "خاصك تراجع.",
    bullets=["Respiration : oxydation complète ; fermentation : oxydation incomplète.",
             "Glycolyse commune ; la mitochondrie utilise l'acide pyruvique."],
    cahier="Bilan : la glycolyse (hyaloplasme) est commune ; avec O₂ la mitochondrie dégrade l'acide pyruvique ; "
           "sans O₂ : fermentation.",
)

diapo(
    id="rf_b2_voyage", type="synthesis", acquis=True,
    titre="La carte complète du voyage",
    lead="Tout le chapitre en une image, et la question du prochain cours.",
    page=REF + "voyage.html?etape=4", legende="La carte du voyage (complète)",
    alt="La carte complète : glycolyse détaillée, deux routes, la mitochondrie détaillée, et « à suivre » sur la matrice",
    montre="La carte complète se redessine flèche par flèche : l'entrée, la glycolyse détaillée (2 ATP, 2 "
           "NADH,H⁺), l'acide pyruvique, les deux routes, la mitochondrie détaillée, et « à suivre » sur la matrice.",
    fr="Je termine avec la carte du voyage, complète cette fois. Le glucose entre dans la cellule. Dans le "
       "hyaloplasme, la glycolyse : elle donne deux ATP, en gagne quatre, et charge deux NAD plus. Il en sort deux "
       "acides pyruviques. Sans dioxygène : la fermentation, dans le hyaloplasme, donne l'éthanol et le dioxyde de "
       "carbone. Et avec le dioxygène : l'acide pyruvique entre dans la mitochondrie, jusqu'à la matrice, où se "
       "trouvent les décarboxylases et les déshydrogénases. Et ici s'arrête notre carte : que devient l'acide "
       "pyruvique dans la matrice, et comment sort la grande énergie ? C'est le prochain cours. Tu connais "
       "maintenant tout le chemin du glucose, du pain jusqu'à la mitochondrie.",
    mx="ونسالي ب la carte ديال الرحلة، كاملة هاد المرة. <m:entree>le glucose كيدخل ل la cellule. <m:glycolyse>ف le "
       "hyaloplasme، la glycolyse: <m:detail_glycolyse>كتعطي deux ATP، كتاخد quatre، وكتعمر deux N A D plus. "
       "<m:pyruvate>كيخرجو منها deux acides pyruviques. <m:sans_o2>بلا dioxygène: la fermentation، ف le hyaloplasme، "
       "كتعطي l'éthanol و le dioxyde de carbone. <m:avec_o2>ومع le dioxygène: l'acide pyruvique كيدخل ل la "
       "mitochondrie، <m:detail_mitochondrie>حتى ل la matrice، فين كاينين les décarboxylases و les déshydrogénases. "
       "<m:a_suivre>وهنا كتوقف la carte ديالنا: شنو كيوقع ل l'acide pyruvique ف la matrice، وكيفاش كتخرج l'énergie "
       "الكبيرة؟ هادا هو الدرس الجاي. دابا كتعرف الطريق كاملة ديال le glucose، من الخبز حتى ل la mitochondrie.",
    bullets=["Le voyage du glucose : de la cuve à la mitochondrie.", "À suivre : que devient l'acide pyruvique dans la matrice ?"],
    cahier="À suivre : que devient l'acide pyruvique dans la matrice ?",
)

diapo(
    id="rf_fermeture_cours", type="synthesis", fermeture=True,
    titre="Ce qu'il faut retenir, et comment réviser",
    lead="Trois idées à retenir, et comment réviser.",
    montre="Aucune animation : les cartes s'écrivent quand la voix les dit.",
    fr="Nous arrivons à la fin du cours : Consommation de la matière organique, et flux d'énergie. Que faut-il "
       "retenir ? Trois idées. Première : avec le dioxygène, la respiration, dans la mitochondrie, et beaucoup "
       "d'énergie. Deuxième : sans dioxygène, la fermentation, dans le hyaloplasme, et peu d'énergie. Troisième : "
       "la glycolyse est commune aux deux, et elle donne deux acides pyruviques et deux ATP. Maintenant, comment "
       "réviser ? Relis ton cahier, et refais seul les exercices du national. Quand tu réponds sur un document : "
       "d'abord décrire, puis déduire, puis expliquer, car chacun a ses points. Le jour de l'examen, partage ton "
       "temps, et commence par la question qui te paraît facile. La veille, repose-toi bien. Écris ces conseils "
       "dans ton cahier. Tu as bien travaillé, bon courage ! Le prochain cours : dans la matrice et la membrane "
       "interne, nous verrons comment sort la grande énergie. On s'y retrouve !",
    mx="وصلنا للخر ديال الدرس: Consommation de la matière organique، et flux d'énergie. شنو خاصك تحفظ؟ <c:Retenir : "
       "avec O₂, respiration (mitochondrie) · sans O₂, fermentation (hyaloplasme)>ثلاثة ديال الأفكار. اللولة: مع le "
       "dioxygène، la respiration، ف la mitochondrie، وبزاف ديال l'énergie. الثانية: بلا dioxygène، la "
       "fermentation، ف le hyaloplasme، و l'énergie قليلة. <c:Glycolyse commune : 2 acides pyruviques + 2 "
       "ATP>الثالثة: la glycolyse كاينة ف جوج، وكتعطي deux acides pyruviques و deux ATP. دابا، كيفاش تراجع؟ "
       "<c:Réviser : relire le cahier, refaire les exercices du national>عاود قرا الدفتر ديالك، وعاود دير les "
       "exercices ديال le national بوحدك. <c:Rédiger : décrire → déduire → expliquer>ملي تجاوب على document، اللول "
       "décrire، من بعد déduire، من بعد expliquer، حيت كل وحدة عندها النقطة ديالها. <c:Jour J : gérer son temps · "
       "bien dormir la veille>ونهار الامتحان، قسم الوقت ديالك، وبدا بالسؤال اللي ساهل عليك. وقبل الامتحان، ترتاح "
       "مزيان فالليل. كتب هادشي ف الدفتر ديالك. راك خدمتي مزيان، الله يعاونك! <c:Prochain cours : la matrice et la membrane interne>الدرس الجاي: ف la matrice و la "
       "membrane interne، غادي نشوفو كيفاش كتخرج l'énergie الكبيرة. نتلاقاو فيه!",
    bullets=["Retenir : avec O₂, respiration (mitochondrie) · sans O₂, fermentation (hyaloplasme)",
             "Glycolyse commune : 2 acides pyruviques + 2 ATP",
             "Réviser : relire le cahier, refaire les exercices du national",
             "Rédiger : décrire → déduire → expliquer", "Jour J : gérer son temps · bien dormir la veille",
             "Prochain cours : la matrice et la membrane interne"],
    cahier="Pour réviser : relire le cahier ; refaire seul les exercices du national ; rédiger : décrire → déduire "
           "→ expliquer ; le jour J, partager son temps ; la veille, bien dormir.",
)
