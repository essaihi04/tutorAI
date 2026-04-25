# Examen SVT 2023 Rattrapage

## Structure attendue

```
2023-rattrapage/
├── pdfs/               # Déposez ici sujet.pdf et correction.pdf
│   ├── sujet.pdf
│   └── correction.pdf
├── pages/              # Auto-généré (PDF → JPEG) par batch_ocr.py
├── assets/             # Découpez et placez les documents ici
│   ├── doc1p1.png      # Document 1 de la page 1
│   ├── doc2p1.png      # Document 2 de la page 1
│   ├── doc1p2.png      # Document 1 de la page 2
│   └── ...
├── extraction.json     # Auto (texte OCR + descriptions docs)
└── exam.json           # Auto (structure générée par DeepSeek)
```

## Pipeline

1. Déposez `sujet.pdf` et `correction.pdf` dans `pdfs/`
2. Lancez : `python backend/scripts/batch_ocr.py svt/2023-rattrapage`
3. Découpez manuellement les documents du sujet et placez-les dans `assets/` avec le nommage `docXpY.png`
4. Lancez : `python backend/scripts/batch_build_json.py svt/2023-rattrapage`
5. Vérifiez l'examen dans l'UI
