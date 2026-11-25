# Le code de la craie (texte écrit au tableau par les simulations)

Fixé le 25 novembre 2026 (finitions des cours de /TCF, demande de l'utilisateur « veuillez prendre en considération la
charte de couleur adéquate »), d'après les cours de 2ᵉ Bac (`physics/ondes-tableau/` : τ = … calculé en vert). Le même dans
tous les cours ; les noms sont ceux du kit (`Tableau.COULEURS` de `shared/tableau/tableau.js`).

| Ce qui est écrit | Craie | Exemple |
|---|---|---|
| titre de la vue, mot-clé, règle / loi énoncée, symbole écrit en grand (A de ᴬ_Z X) | `jaune` | « Règle 2 : on remplit K, puis L, puis M » |
| légende d'un objet, valeur DONNÉE, étape d'un calcul | `blanc` | « un tube de verre », « m ≈ 16 × 1,67 × 10⁻²⁷ kg » |
| **résultat calculé, conclusion** (et son encadré, `rect` vert à fond vert léger) | `vert` | « m ≈ 2,67 × 10⁻²⁶ kg », « l'atome est surtout du vide » |
| erreur fréquente, piège, « ⚠ » | `rose` | « ⚠ ne pas oublier les électrons » |
| ce qui désigne un objet (flèche, repère, nom de l'objet, sa grandeur) | **la couleur de l'objet** | électron / charge − : `cyan` ; proton, noyau, Z, charge + : `rose` ; particule α : `orange` |
| note secondaire, unité expliquée | `faible` | « e : la charge élémentaire ; C : le coulomb » |

- L'`orange` n'est plus une couleur de conclusion : il est laissé aux objets qui l'ont (particule α, point M, feu…).
- Jamais de bleu foncé, de noir ou de gris foncé sur le tableau vert.
- Les cartes `concentration.centre` et le cahier gardent la charte du cahier (skill `cahier-de-l-eleve` § 6 : « Donc… »
  orange, « Définition : » vert…) : c'est une autre surface, rendue par le lecteur.
- En code : `Lexique.physique.ECRITURE` (`titre`, `motCle`, `relation` → jaune ; `legende`, `donnee` → blanc ;
  `resultat`, `conclusion` → vert ; `piege` → rose). Mécanique : [mecanique.md](mecanique.md).
