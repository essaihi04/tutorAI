# Expression génétique 3D

Simulation WebGL locale de niveau BAC montrant l’expression d’un gène depuis
l’ouverture de l’ADN jusqu’au repliement du polypeptide. Elle respecte le
contrat `TEMPLATE_SIMULATION.html`, tient dans `100vh` et ne charge aucune
ressource depuis Internet.

## Scénario pédagogique

La démonstration contient 35 phénomènes déterministes :

1. reconnaissance du promoteur, fixation de l’ARN polymérase et ouverture
   locale d’une véritable double hélice avec ses paires de bases ;
2. synthèse de `5′ AUG GAA UUU CCG UAA 3′`, nucléotide par nucléotide, avec le
   nom de chaque base azotée et son complément sur le brin transcrit ;
3. libération de l’ARNm et passage par un pore nucléaire ;
4. initiation de la traduction : petite sous-unité, ARNt initiateur portant la
   méthionine, puis grande sous-unité ;
5. élongation : ARNt, anticodons, translocation, acides aminés nommés et
   liaisons peptidiques ;
6. terminaison au codon `UAA`, libération du polypeptide, dissociation du
   ribosome et repliement de la protéine.

La caméra accepte la rotation par glissement et le zoom à la molette ou au
pincement. Les commandes visibles sont `Démarrer`, `Pause` et `Relancer`.

## Intégration avec le tuteur

Identifiant : `svt_gene_expression_advanced_lab`.

Commandes `simulation_control` acceptées :

- `start`, `pause`, `next`, `previous`, `reset` ;
- `set_variant { variant_id: "demonstration" }` ;
- `set_speed { speed }` ;
- `highlight { target }` avec `dna`, `polymerase`, `mrna`, `pore`,
  `ribosome`, `trna` ou `peptide`.

Chaque changement de phénomène publie un `simulation_state` avec la phase
biologique, le nucléotide actif, l’ARNm déjà synthétisé, les codons complets,
les acides aminés déjà reliés, les lieux scientifiques et la progression.

## Dépendance embarquée

`vendor/three.module.min.js` et `vendor/three.core.min.js` proviennent de
Three.js 0.180.0, déjà utilisé par le frontend. La licence MIT correspondante
est conservée dans `vendor/THREE-LICENSE.txt`.
