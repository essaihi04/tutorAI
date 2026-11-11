# Le texte parlé et le dataset d'entraînement de la voix (7 novembre 2026)

## Source
- Dataset : `zouhairessaihi/academy-v4-selection`, fichier `selection_train.jsonl`.
- 38 852 phrases, 6 sources (Driss, academy, Lamsaf, Tahiri, Mouhib, TOP PC…).
- C'est le corpus qui a servi à entraîner le modèle v4 (`ferdaous04/academy-v4-entrainement`).
- Langues : 28 % de mots français, 72 % de darija.
- Aucun chiffre : les nombres sont écrits en lettres.

## Constat sur le script exemple des ondes
- Le script a 30 % de mots français, donc à peu près la même proportion que le corpus.
- **33 mots français du script sont vus moins de 20 fois dans le corpus.** Ceux que le corpus ne contient jamais (0 fois) :
  - thêta (le corpus écrit « teta », 335 fois) ;
  - manip, bouée, queue, réfléchi, divisée, trajet, clap, l'échographie, impulsion, oscillogramme, l'écho, barème.
- **176 mots darija du script sont rares (moins de 20 fois).** Beaucoup n'apparaissent jamais :
  - des formes collées : وفالأخير، فالمراية، وفمدة ;
  - des mots peu courants : مزحزحين، كتحسم، كيتضغط.
- À la transcription, « la bouée » a été entendu « la boue ». Les passages douteux (diapositives 2.2, 5.2, 6.2 et 6.3) contiennent justement ces mots rares.

## Ce que le corpus contient bien
- **Nombres**, en français et en darija :
  - français : deux 4 675, zéro 3 549, trois 1 932, virgule 418 ; « zéro virgule » 177 ;
  - darija : واحد 11 143, جوج 6 297, ثلاثة 1 768, فاصلة 358.
- **Mots français simples** : donc 3 179, alors 880, c'est 874, bien 861, voilà 587, d'accord 354.
- **Termes des ondes** :
  - l'onde 289, la perturbation 216, la propagation 178, transversale 106, longitudinale 70, la célérité 68 ;
  - le retard 122, le front 91, le signal 135, la source 243, le milieu 322 ;
  - l'élongation 62, l'aspect 64, l'oscilloscope 33 ;
  - teta 335, tau 426, delta t 239, y grec 7.
- **Mots de liaison darija** :
  - ديال 17 264, هادي 5 375, شنو 5 243, يعني 5 019, دابا 3 890, مثلا 3 921, باش 3 548 ;
  - يلا 3 505 (contre إذا/إلا 492), إذن 2 551, شحال 2 531, مزيان 2 354.

## Règle ajoutée au skill professeur (règle 17)
- Le français est réservé à trois cas :
  - les termes techniques du programme ;
  - les nombres ;
  - les mots français simples.
- Tout autre mot passe en darija simple, avec des mots présents dans le corpus.
- Les symboles s'écrivent comme dans le corpus : teta, tau, y grec, delta t.
- Les phrases sont courtes.
- Avant de générer, chaque mot est vérifié dans le corpus.
