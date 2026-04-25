-- Migration 003: Add Mathematiques subject, chapters, and lessons for 2BAC Sciences Physiques BIOF
-- This migration adds the complete Mathematics curriculum

BEGIN;

-- 1. Insert the Mathematiques subject
INSERT INTO subjects (id, name_fr, name_ar, description_fr, description_ar, icon, color, order_index)
VALUES (
  gen_random_uuid(),
  'Mathematiques',
  'الرياضيات',
  'Analyse, Suites, Nombres complexes, Probabilites - 2eme BAC Sciences Physiques BIOF',
  'التحليل، المتتاليات، الأعداد العقدية، الاحتمالات - الثانية باكالوريا علوم فيزيائية',
  'calculator',
  '#8b5cf6',
  3
)
ON CONFLICT DO NOTHING;

-- 2. Insert Math chapters (11 chapters)
DO $$
DECLARE
  math_subject_id UUID;
  ch_id UUID;
BEGIN
  SELECT id INTO math_subject_id FROM subjects WHERE name_fr = 'Mathematiques';

  IF math_subject_id IS NULL THEN
    RAISE EXCEPTION 'Mathematiques subject not found';
  END IF;

  -- Chapter 1: Limites et continuite
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 1,
    'Limites et continuite',
    'النهايات والاتصال',
    'Limites de fonctions, formes indeterminees, continuite, theoreme des valeurs intermediaires',
    'نهايات الدوال، الأشكال غير المحددة، الاتصال، مبرهنة القيم الوسطية',
    'intermediate', 5.0, 0);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Limites et continuite', 'النهايات والاتصال', 'theory',
    '{"sections":[{"title":"Limites d''une fonction en un point","body":"Limite finie, limite infinie, limites a droite et a gauche. Formes indeterminees: 0/0, inf/inf, inf-inf, 0*inf."},{"title":"Limites a l''infini","body":"Comportement asymptotique des fonctions polynomiales, rationnelles. Asymptotes horizontales, verticales et obliques."},{"title":"Continuite","body":"Definition de la continuite en un point et sur un intervalle. Prolongement par continuite. Theoreme des valeurs intermediaires (TVI)."},{"title":"Applications du TVI","body":"Existence de solutions d''equations f(x)=k. Methode de dichotomie pour encadrer une solution."}]}'::jsonb,
    '["Calculer les limites de fonctions en un point et a l''infini","Lever les formes indeterminees","Determiner les asymptotes d''une courbe","Appliquer le theoreme des valeurs intermediaires"]'::jsonb,
    60, 0, '[]'::jsonb);

  -- Chapter 2: Derivation et etude des fonctions
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 2,
    'Derivation et etude des fonctions',
    'الاشتقاق ودراسة الدوال',
    'Derivabilite, regles de derivation, etude de fonctions, extremums, tangentes',
    'الاشتقاقية، قواعد الاشتقاق، دراسة الدوال، القيم القصوى، المماسات',
    'intermediate', 5.0, 1);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Derivation et etude des fonctions', 'الاشتقاق ودراسة الدوال', 'theory',
    '{"sections":[{"title":"Derivabilite d''une fonction","body":"Definition du nombre derive. Derivabilite a droite et a gauche. Interpretation geometrique: pente de la tangente."},{"title":"Regles de derivation","body":"Derivees des fonctions usuelles. Derivee d''une somme, produit, quotient, composee. Derivee de f^n, racine, 1/f."},{"title":"Etude de fonctions","body":"Tableau de variation. Sens de variation et signe de la derivee. Extremums locaux et globaux. Points d''inflexion."},{"title":"Applications","body":"Equation de la tangente. Problemes d''optimisation. Encadrement et approximation."}]}'::jsonb,
    '["Calculer la derivee d''une fonction","Etudier le sens de variation d''une fonction","Determiner les extremums d''une fonction","Tracer la courbe representative d''une fonction"]'::jsonb,
    60, 0, '[]'::jsonb);

  -- Chapter 3: Suites numeriques
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 3,
    'Suites numeriques',
    'المتتاليات العددية',
    'Suites arithmetiques, geometriques, recurrentes, convergence, raisonnement par recurrence',
    'المتتاليات الحسابية، الهندسية، بالتراجع، التقارب، البرهان بالتراجع',
    'intermediate', 5.0, 2);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Suites numeriques', 'المتتاليات العددية', 'theory',
    '{"sections":[{"title":"Generalites sur les suites","body":"Definition d''une suite. Suite definie par une formule explicite ou par recurrence. Sens de variation d''une suite."},{"title":"Suites arithmetiques et geometriques","body":"Definition, terme general, somme des n premiers termes. Applications aux problemes concrets."},{"title":"Raisonnement par recurrence","body":"Principe de recurrence. Initialisation, heredite, conclusion. Exemples de demonstration."},{"title":"Convergence des suites","body":"Suite majoree, minoree, bornee. Suites monotones bornees. Theoreme de convergence. Suites adjacentes."}]}'::jsonb,
    '["Etudier le sens de variation d''une suite","Maitriser le raisonnement par recurrence","Calculer la somme des termes d''une suite arithmetique ou geometrique","Etudier la convergence d''une suite"]'::jsonb,
    60, 0, '[]'::jsonb);

  -- Chapter 4: Fonctions logarithmiques
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 4,
    'Fonctions logarithmiques',
    'الدوال اللوغاريتمية',
    'Logarithme neperien, proprietes, derivee, etude de fonctions avec ln',
    'اللوغاريتم النيبيري، الخاصيات، المشتقة، دراسة دوال تتضمن ln',
    'advanced', 4.0, 3);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Fonctions logarithmiques', 'الدوال اللوغاريتمية', 'theory',
    '{"sections":[{"title":"Logarithme neperien","body":"Definition de ln comme primitive de 1/x. Proprietes fondamentales: ln(ab)=ln(a)+ln(b), ln(a/b), ln(a^n)."},{"title":"Etude de la fonction ln","body":"Domaine de definition, derivee, sens de variation, limites aux bornes. Courbe representative."},{"title":"Logarithme decimal","body":"Definition de log. Relation entre ln et log. Applications aux calculs de pH, decibels."},{"title":"Equations et inequations avec ln","body":"Resolution d''equations et inequations logarithmiques. Etude de fonctions comportant ln."}]}'::jsonb,
    '["Connaitre les proprietes du logarithme neperien","Etudier des fonctions comportant ln","Resoudre des equations et inequations logarithmiques","Calculer des limites avec des logarithmes"]'::jsonb,
    55, 0, '[]'::jsonb);

  -- Chapter 5: Fonctions exponentielles
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 5,
    'Fonctions exponentielles',
    'الدوال الأسية',
    'Fonction exponentielle, proprietes, derivee, equations et inequations avec exp',
    'الدالة الأسية، الخاصيات، المشتقة، معادلات ومتراجحات تتضمن exp',
    'advanced', 4.0, 4);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Fonctions exponentielles', 'الدوال الأسية', 'theory',
    '{"sections":[{"title":"La fonction exponentielle","body":"Definition de exp comme reciproque de ln. Propriete fondamentale: exp(a+b)=exp(a)*exp(b). Notation e^x."},{"title":"Etude de la fonction exp","body":"Domaine R, derivee (exp''=exp), sens de variation (strictement croissante), limites en +inf et -inf. Courbe."},{"title":"Croissances comparees","body":"Comparaison de exp(x) avec x^n en +inf. Comparaison de ln(x) avec x^a. Applications aux calculs de limites."},{"title":"Equations et inequations avec exp","body":"Resolution d''equations et inequations exponentielles. Etude de fonctions avec exp et ln."}]}'::jsonb,
    '["Connaitre les proprietes de la fonction exponentielle","Appliquer les croissances comparees pour calculer des limites","Etudier des fonctions comportant exp","Resoudre des equations et inequations exponentielles"]'::jsonb,
    55, 0, '[]'::jsonb);

  -- Chapter 6: Fonctions primitives et calcul integral
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 6,
    'Fonctions primitives et calcul integral',
    'الدوال الأصلية والتكامل',
    'Primitives, integrale definie, proprietes, calcul d''aires, theoreme fondamental',
    'الدوال الأصلية، التكامل المحدد، الخاصيات، حساب المساحات، المبرهنة الأساسية',
    'advanced', 5.0, 5);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Fonctions primitives et calcul integral', 'الدوال الأصلية والتكامل', 'theory',
    '{"sections":[{"title":"Primitives","body":"Definition d''une primitive. Primitives des fonctions usuelles. Primitive et constante d''integration. Primitive de f''+g'', kf'', u''*u^n, u''/u."},{"title":"Integrale definie","body":"Definition de l''integrale de a a b. Relation avec les primitives (theoreme fondamental). Proprietes: linearite, relation de Chasles, positivite."},{"title":"Calcul d''aires","body":"Aire sous une courbe. Aire entre deux courbes. Unite d''aire. Applications geometriques."},{"title":"Integration par parties","body":"Formule d''integration par parties. Applications au calcul d''integrales. Valeur moyenne d''une fonction."}]}'::jsonb,
    '["Determiner les primitives des fonctions usuelles","Calculer une integrale definie","Calculer l''aire d''un domaine plan","Appliquer l''integration par parties"]'::jsonb,
    60, 0, '[]'::jsonb);

  -- Chapter 7: Equations differentielles
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 7,
    'Equations differentielles',
    'المعادلات التفاضلية',
    'Equations differentielles du premier ordre y''=ay+b, applications physiques',
    'المعادلات التفاضلية من الرتبة الأولى، التطبيقات الفيزيائية',
    'advanced', 3.0, 6);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Equations differentielles', 'المعادلات التفاضلية', 'theory',
    '{"sections":[{"title":"Equations differentielles du premier ordre","body":"Forme y''=ay+b avec a et b constantes reelles. Solution generale: y=Ce^(ax) - b/a. Determination de C par condition initiale."},{"title":"Resolution et verification","body":"Methode de resolution. Verification qu''une fonction est solution. Unicite de la solution avec condition initiale."},{"title":"Applications physiques","body":"Circuit RC (charge/decharge du condensateur). Desintegration radioactive. Croissance/decroissance exponentielle."}]}'::jsonb,
    '["Resoudre une equation differentielle y''=ay+b","Determiner la solution particuliere avec condition initiale","Appliquer les equations differentielles a des problemes physiques"]'::jsonb,
    50, 0, '[]'::jsonb);

  -- Chapter 8: Nombres complexes - Partie 1
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 8,
    'Nombres complexes - Partie 1',
    'الأعداد العقدية - الجزء 1',
    'Forme algebrique, operations, conjugue, module, argument',
    'الشكل الجبري، العمليات، المرافق، المعامل، العمدة',
    'intermediate', 4.0, 7);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Nombres complexes - Partie 1', 'الأعداد العقدية - الجزء 1', 'theory',
    '{"sections":[{"title":"Forme algebrique","body":"Nombre imaginaire i tel que i^2=-1. Forme algebrique z=a+bi. Partie reelle et partie imaginaire. Egalite de deux complexes."},{"title":"Operations sur les complexes","body":"Addition, soustraction, multiplication, division. Conjugue d''un complexe. Proprietes du conjugue."},{"title":"Module d''un nombre complexe","body":"Definition |z|=sqrt(a^2+b^2). Proprietes: |z1*z2|=|z1|*|z2|, |z1/z2|=|z1|/|z2|. Inegalite triangulaire."},{"title":"Representation geometrique","body":"Plan complexe (plan d''Argand). Affixe d''un point, affixe d''un vecteur. Distance et milieu en termes de complexes."}]}'::jsonb,
    '["Effectuer des operations sur les nombres complexes","Calculer le module et le conjugue d''un nombre complexe","Representer geometriquement un nombre complexe","Resoudre des equations dans C"]'::jsonb,
    55, 0, '[]'::jsonb);

  -- Chapter 9: Nombres complexes - Partie 2
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 9,
    'Nombres complexes - Partie 2',
    'الأعداد العقدية - الجزء 2',
    'Forme trigonometrique, exponentielle, equations dans C, applications geometriques',
    'الشكل المثلثي، الأسي، معادلات في C، التطبيقات الهندسية',
    'advanced', 4.0, 8);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Nombres complexes - Partie 2', 'الأعداد العقدية - الجزء 2', 'theory',
    '{"sections":[{"title":"Argument d''un nombre complexe","body":"Definition de l''argument arg(z). Argument et operations: arg(z1*z2)=arg(z1)+arg(z2). Argument du conjugue, de l''inverse."},{"title":"Forme trigonometrique","body":"z=r(cos(theta)+i*sin(theta)). Passage entre forme algebrique et trigonometrique. Formule de Moivre."},{"title":"Forme exponentielle","body":"Notation z=r*e^(i*theta). Formule d''Euler: e^(i*theta)=cos(theta)+i*sin(theta). Operations en forme exponentielle."},{"title":"Applications geometriques","body":"Transformations du plan: translation, rotation, homothetie en termes de complexes. Similitudes directes. Lieux geometriques."}]}'::jsonb,
    '["Ecrire un nombre complexe sous forme trigonometrique et exponentielle","Appliquer la formule de Moivre","Utiliser les nombres complexes pour resoudre des problemes geometriques","Determiner des lieux geometriques dans le plan complexe"]'::jsonb,
    55, 0, '[]'::jsonb);
  -- Chapter 10: Geometrie dans l'espace
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 10,
    'Geometrie dans l''espace',
    'الهندسة في الفضاء',
    'Produit scalaire dans l''espace, produit vectoriel, plans et droites, equations parametriques',
    'الجداء السلمي في الفضاء، الجداء المتجهي، المستويات والمستقيمات، المعادلات الوسيطية',
    'advanced', 5.0, 9);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Geometrie dans l''espace', 'الهندسة في الفضاء', 'theory',
    '{"sections":[{"title":"Produit scalaire dans l''espace","body":"Definition du produit scalaire. Proprietes: bilinearite, symetrie. Norme d''un vecteur. Orthogonalite. Projection orthogonale."},{"title":"Produit vectoriel","body":"Definition du produit vectoriel. Proprietes. Calcul avec les coordonnees. Applications: aire d''un parallelogramme, vecteur normal a un plan."},{"title":"Plans et droites dans l''espace","body":"Equation cartesienne d''un plan. Equations parametriques d''une droite. Positions relatives de droites et plans. Distance d''un point a un plan."},{"title":"Applications","body":"Intersection de plans et droites. Projection orthogonale sur un plan. Symetrie par rapport a un plan."}]}'::jsonb,
    '["Calculer le produit scalaire et le produit vectoriel dans l''espace","Determiner l''equation d''un plan et les equations d''une droite","Etudier les positions relatives de droites et plans","Calculer des distances et des angles dans l''espace"]'::jsonb,
    60, 0, '[]'::jsonb);

  -- Chapter 11: Denombrement et probabilites
  ch_id := gen_random_uuid();
  INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
  VALUES (ch_id, math_subject_id, 11,
    'Denombrement et probabilites',
    'التعداد والاحتمالات',
    'Arrangements, combinaisons, probabilites conditionnelles, variables aleatoires, loi binomiale',
    'الترتيبات، التوافيق، الاحتمالات الشرطية، المتغيرات العشوائية، قانون برنولي',
    'intermediate', 5.0, 10);
  INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
  VALUES (gen_random_uuid(), ch_id,
    'Denombrement et probabilites', 'التعداد والاحتمالات', 'theory',
    '{"sections":[{"title":"Denombrement","body":"Principe additif et multiplicatif. Permutations, arrangements, combinaisons. Formule du binome de Newton. Triangle de Pascal."},{"title":"Probabilites","body":"Espace probabilise fini. Equiprobabilite. Probabilite d''un evenement. Probabilites conditionnelles. Formule des probabilites totales."},{"title":"Variables aleatoires","body":"Variable aleatoire discrete. Loi de probabilite. Esperance, variance, ecart-type. Proprietes de l''esperance et de la variance."},{"title":"Loi binomiale","body":"Epreuve de Bernoulli. Schema de Bernoulli. Loi binomiale B(n,p). Esperance et variance de la loi binomiale. Applications."}]}'::jsonb,
    '["Calculer le nombre d''arrangements et de combinaisons","Calculer des probabilites conditionnelles","Determiner la loi de probabilite d''une variable aleatoire","Reconnaitre et utiliser la loi binomiale"]'::jsonb,
    60, 0, '[]'::jsonb);

END $$;

COMMIT;
