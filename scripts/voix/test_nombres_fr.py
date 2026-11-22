"""Règle de l'utilisateur (21-22/11/2026) : jamais un mot darija et un mot français successifs dans un nombre ou une
formule. Lancer : python -X utf8 -m pytest scripts/voix/test_nombres_fr.py"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from nombres_fr import convertir  # noqa: E402


@pytest.mark.parametrize("avant, apres", [
    ("جوج noyaux", "deux noyaux"),
    ("six virgule cinq fois dix أس ناقص خمسة", "six virgule cinq fois dix puissance moins cinq"),
    ("plus l'infini ناقص plus l'infini.", "plus l'infini moins plus l'infini."),
    ("حتى x زائد واحد ما كيتبدل", "حتى x plus un ما كيتبدل"),
    ("شوف، k يساوي trois هادا", "شوف، k égale trois هادا"),
    ("x كبر ولا يساوي moins un.", "x supérieur ou égal à moins un."),
    ("x وأصغر ولا يساوي un", "x و inférieur ou égal à un"),
    ("عرفتي بلي تسعمية nanomètre ماشي", "عرفتي بلي neuf cents nanomètre ماشي"),
    ("le stroboscope وجوج récepteurs.", "le stroboscope و deux récepteurs."),
    ("u indice n ناقص جوج على sept", "u indice n moins deux sur sept"),
    ("strictement croissante على I، يعني", "strictement croissante sur I، يعني"),
    ("هي un virgule خمسة سبعة fois dix", "هي un virgule cinq sept fois dix"),
    ("deux x جوج مرات؟ حاول", "deux x deux fois؟ حاول"),
    # mots cassés et nombres collés à un préfixe
    ("كيتصنعوش فالنoyau، كيتصنعوا", "كيتصنعوش فالnoyau، كيتصنعوا"),
    ("المجال من زéro حتى", "المجال من zéro حتى"),
    ("Mزيان، عرفتي", "مزيان، عرفتي"),
    ("الحالة fين الجوج formes", "الحالة فين الجوج formes"),
    ("x وtrois", "x و trois"),
    # mot darija juste avant un nombre français (22/11/2026 : « تقريبا huit » dit « thuit »)
    ("كياخد تقريبا huit minutes باش يوصل", "كياخد environ huit minutes باش يوصل"),
    ("كاع les termes كيساويو un. البلاصة", "كاع les termes égalent un. البلاصة"),
    ("إذن deux كتساوي un plus un", "إذن deux égale un plus un"),
    ("r تقريبا trente-huit virgule quatre", "r environ trente-huit virgule quatre"),
])
def test_converti(avant, apres):
    assert convertir(avant) == apres


@pytest.mark.parametrize("texte", [
    "عندنا جوج طرق باش نحسبو",       # darija seule : rien à changer
    "واحد la courbe",                 # article, pas un nombre
    "وواحد la courbe",
    "كنحطو على le spectre",            # préposition devant un article
    "كتزيد Pi على l'ADP",              # préposition, pas une division
    "ماشي dérivable في zéro",          # « في » = en, pas fois
    "زائد في ناقص كتعطي ناقص",        # règle des signes dite en darija
    "باش نétablir L، خاصنا",           # verbe français conjugué en darija : style du corpus
    "شوف فla courbe والcourbe",         # articles collés : style du corpus
    "un: شحال كتساوي g de x",           # « شحال égale » serait un autre mélange
    "تقريبا la moitié",                 # pas un nombre
])
def test_inchange(texte):
    assert convertir(texte) == texte
