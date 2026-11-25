import json, sys
B2 = sys.argv[1]
F = chr(92) + 'frac'


def C(s, i, n, note, t, dessin=None):
    d = {'sujet': s, 'id': i, 'niveau': n, 'note_prof': note, 'texte': t.replace('FRAC', F)}
    if dessin:
        d['dessin'] = dessin
    return d


c = [
 C('svt_tc', '2', 'juste', 1, "2) a) Vrai\nb) Faux\nc) Vrai\nd) Faux"),
 C('svt_tc', '2', 'presque', 0.75, "2- a- vrai   b- faux\n   c- vrai   d- vrai"),
 C('svt_tc', '2', 'faux', 0, "2) a) F  b) V  c) F  d) V"),
 C('svt_tc', '2-2', 'juste', 1, "2-2) Le CAH est chargé négativement car il retient les\ncations (bleu de méthylène) et repousse les anions (éosine).\nIl est formé d'argile et d'humus."),
 C('svt_tc', '2-2', 'presque', 0.5, "2-2) le complexe argilo-humique est chargé négativement."),
 C('svt_tc', '2-2', 'faux', 0, "2-2) Le CAH est chargé positivement, il est formé\nde sable et de calcaire."),
 C('svt_tc', '1-6', 'juste', 1, "1-6) Dans le sol A (sableux) l'eau de gravité s'écoule vite,\nil reste peu d'eau capillaire, la seule utilisable par la plante.\nOn arrive vite au point de flétrissement : il ne reste que l'eau\nhygroscopique, inutilisable. Le sol B retient beaucoup d'eau\ncapillaire donc la plante flétrit plus tard."),
 C('svt_tc', '1-6', 'presque', 0.5, "1-6) Le sol A est sableux, il ne retient pas l'eau donc\nla plante n'a plus d'eau et flétrit vite.\nLe sol B retient plus d'eau capillaire."),
 C('svt_tc', '1-6', 'faux', 0, "1-6) La plante flétrit sur le sol A car il contient trop\nd'eau de gravité qui noie les racines."),
 C('svt_tc', '3-1', 'juste', 1, "3-1) Le nombre d'espèces ne change plus à partir de 16 m²\n(palier à 15 espèces) donc l'aire minimale = 16 m²"),
 C('svt_tc', '3-1', 'presque', 0.75, "3-1) aire minimale = 16"),
 C('svt_tc', '3-1', 'faux', 0, "3-1) Aire minimale = 64 m² car c'est la plus grande surface."),
 C('svt_tc', '3-4', 'juste', 0.5, "3-4) S = 6 × 2 = 12 m²\nD = 60/12 = 5 individus/m²"),
 C('svt_tc', '3-4', 'presque', 0.25, "3-4) D = 60/12 = 5"),
 C('svt_tc', '3-4', 'faux', 0, "3-4) D = 60/6 = 10 individus/m²"),
 C('physique', '1-3', 'juste', 3.25, "1-3) L' = FRAC{2λD}{a'} = FRAC{2 × 6,4×10^{-7} × 2,5}{8×10^{-5}}\nL' = 4×10^{-2} m = 4 cm\nQuand a diminue, L augmente (a est au dénominateur)."),
 C('physique', '1-3', 'presque', 2.5, "1-3) L' = 2λD/a' = 2×6,4×10^{-7}×2,5/(8×10^{-5})\nL' = 4 cm"),
 C('physique', '1-3', 'faux', 0, "1-3) L' = 2λD × a' = 2×6,4×10^{-7}×2,5×8×10^{-5}\nL' = 2,6×10^{-10} m   donc L diminue."),
 C('chimie', '1-2', 'juste', 2.75, "1-2) [H₃O^{+}]_{éq} = 10^{-pH} = 10^{-3,29}\n[H₃O^{+}]_{éq} = 5,1×10^{-4} mol/L"),
 C('chimie', '1-2', 'presque', 2.5, "1-2) [H₃O^{+}] = 10^{-3,29} = 5,1×10^{-4}"),
 C('chimie', '1-2', 'faux', 0, "1-2) [H₃O^{+}] = -log(3,29) = -0,52 mol/L"),
 C('chimie', '2-2', 'juste', 2, "2-2) [H₃O^{+}]éq = 10^{-pH} = 10^{-3,09}\n= 8,1×10^{-4} mol/L"),
 C('chimie', '2-2', 'presque', 1, "2-2) [H₃O^{+}]éq = 10^{-pH} = 10^{-3,09} = 1,2×10^{-3} mol/L"),
 C('chimie', '2-2', 'faux', 0, "2-2) [H₃O^{+}]éq = C = 5×10^{-2} mol/L"),
 C('tcf', '1-1', 'juste', 1, "1-1) ① réfrigérant à boules\n② ballon\n③ chauffe-ballon\n④ entrée de l'eau froide"),
 C('tcf', '1-1', 'presque', 0.75, "1-1)  ① B   ② C   ③ A   ④ A"),
 C('tcf', '1-1', 'faux', 0, "1-1) ① ballon\n② réfrigérant\n③ bécher\n④ sortie des vapeurs"),
 C('tcf', '1-4', 'juste', 0.5, "1-4) Rf(A) = FRAC{h}{H} = FRAC{3}{10} = 0,3"),
 C('tcf', '1-4', 'presque', 0.25, "1-4) Rf(A) = 0,3"),
 C('tcf', '1-4', 'faux', 0, "1-4) Rf(A) = FRAC{H}{h} = FRAC{10}{3} = 3,3"),
 C('tcf', '1-6', 'juste', 1, "1-6) Une tache de C est à la même hauteur que B (Rf = 0,7)\ndonc C contient l'acétate d'isoamyle. C n'est pas pur car il donne\ndeux taches : l'autre a le même Rf que A (0,3), il reste de\nl'alcool isoamylique."),
 C('tcf', '1-6', 'presque', 0.75, "1-6) C contient l'acétate (même Rf que B = 0,7).\nC n'est pas pur car il y a deux taches."),
 C('tcf', '1-6', 'faux', 0, "1-6) C ne contient pas l'acétate car ses taches sont\ndifférentes de A. Il est pur."),
 C('tcf', '2-3', 'juste', 1, "2-3) m ≈ A × m_{p} = 24 × 1,67×10^{-27}\nm ≈ 4,0×10^{-26} kg"),
 C('tcf', '2-3', 'presque', 0.5, "2-3) m = Z × m_{p} = 12 × 1,67×10^{-27} = 2×10^{-26} kg"),
 C('tcf', '2-3', 'faux', 0, "2-3) m = 24 × 1,6×10^{-19} = 3,8×10^{-18} kg"),
 C('tcf', '2-4', 'juste', 1, "2-4) L'atome est neutre : 12 électrons (Z = 12)\n(K)^{2}(L)^{8}(M)^{2}\ncouche externe : M avec 2 électrons"),
 C('tcf', '2-4', 'presque', 0.5, "2-4) (K)^{2}(L)^{8}(M)^{2}"),
 C('tcf', '2-4', 'faux', 0, "2-4) (K)^{2}(L)^{10}\ncouche externe : L avec 10 électrons"),
 C('tcf', '2-6', 'juste', 0.5, "2-6) q = +2e = 2 × 1,6×10^{-19} = 3,2×10^{-19} C"),
 C('tcf', '2-6', 'presque', 0.25, "2-6) q = 2 × 1,6×10^{-19} = 3,2×10^{-19}"),
 C('tcf', '2-6', 'faux', 0, "2-6) q = -2e = -3,2×10^{-19} C"),
 C('tcf', '3-3', 'juste', 1, "3-3) v₃ = FRAC{M₂M₄}{2τ} = FRAC{0,08}{0,04} = 2 m/s"),
 C('tcf', '3-3', 'presque', 0.5, "3-3) v₃ = FRAC{M₂M₄}{2τ} = FRAC{8}{40} = 0,2 m/s"),
 C('tcf', '3-3', 'faux', 0, "3-3) v₃ = d × t = 4 × 20 = 80 m/s"),
 C('tcf', '3-5', 'juste', 1, "3-5) mouvement rectiligne uniforme : x(t) = v·t + x₀\nv = 2 m/s ; x₀ = M₀M₁ = 0,04 m\nx(t) = 2t + 0,04"),
 C('tcf', '3-5', 'presque', 0.5, "3-5) x(t) = 2t"),
 C('tcf', '3-5', 'faux', 0, "3-5) x(t) = 4t + 20"),
 C('tcf', '4-2', 'juste', 1, "4-2) Système : le palet. Forces : le poids P (vertical, vers\nle bas) et la réaction R de la glace\n(perpendiculaire, sans frottement).\nG a un mouvement rectiligne uniforme donc d'après le principe\nd'inertie le palet est pseudo-isolé : P + R = 0 (vecteurs).", {'type': 'forces', 'juste': True}),
 C('tcf', '4-2', 'presque', 0.25, "4-2) Le palet est soumis à son poids P et à la réaction R.", {'type': 'forces', 'juste': True}),
 C('tcf', '4-2', 'faux', 0, "4-2) forces : le poids, la réaction et une force de\nfrottement. Le palet accélère donc les forces ne se compensent pas.", {'type': 'forces', 'juste': False}),
 C('tcf', '4-4', 'juste', 1, "4-4) G₁G = FRAC{m₂}{m₁ + m₂} × G₁G₂ = FRAC{600}{200 + 600} × 20\nG₁G = 15 cm"),
 C('tcf', '4-4', 'presque', 0.25, "4-4) G₁G = FRAC{m₁}{m₁ + m₂} × G₁G₂ = FRAC{200}{800} × 20 = 5 cm"),
 C('tcf', '4-4', 'faux', 0, "4-4) G₁G = 20/2 = 10 cm"),
]
json.dump(c, open(B2 + '/copies.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(c))
