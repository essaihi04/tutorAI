# Structure des Médias

## Organisation des dossiers

### Images (`/media/images/`)
Images statiques pour illustrations de cours
- `physics/ch1_ondes_mecaniques/` - Ondes mécaniques
- `physics/ch2_ondes_periodiques/` - Ondes périodiques
- `physics/ch3_ondes_lumineuses/` - Ondes lumineuses
- `chemistry/` - Chimie
- `svt/` - SVT

### Simulations (`/media/simulations/`)
Simulations HTML/JS interactives
- `physics/` - Simulations physique
- `chemistry/` - Simulations chimie
- `svt/` - Simulations SVT

### Vidéos (`/media/videos/`)
Vidéos explicatives courtes (< 2 min)
- `physics/` - Vidéos physique
- `chemistry/` - Vidéos chimie
- `svt/` - Vidéos SVT

## Utilisation

Les médias sont référencés dans les fichiers de leçons via le champ `media_resources`:

```json
{
  "media_resources": [
    {
      "type": "image",
      "url": "/media/images/physics/ch1_ondes_mecaniques/onde_transversale.png",
      "caption": "Onde transversale sur une corde",
      "trigger": "regarde ce schéma"
    }
  ]
}
```
