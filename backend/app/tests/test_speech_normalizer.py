import unittest
from unittest.mock import AsyncMock, patch

from app.services import tts_service
from app.services.speech_normalizer import _LATIN_RE, normalize_for_speech


class SpeechNormalizerTests(unittest.TestCase):
    def test_french_percent_decimal_and_unit(self):
        self.assertEqual(
            normalize_for_speech("25% et 2,5 mol/L", "fr"),
            "vingt-cinq pour cent et deux virgule cinq moles par litre",
        )

    def test_fractions_powers_and_scientific_notation(self):
        self.assertEqual(
            normalize_for_speech("3/16 ; 10⁻³ ; 1,5×10⁻³", "fr"),
            "trois sur seize; dix puissance moins trois; "
            "un virgule cinq fois dix puissance moins trois",
        )

    def test_latex_is_spoken_instead_of_removed(self):
        self.assertEqual(
            normalize_for_speech(r"$E = mc^2$ et $\frac{3}{16}$", "fr"),
            "E égal mc puissance deux et trois sur seize",
        )

    def test_plain_text_multiplication_survives_markup_cleanup(self):
        cleaned = tts_service.clean_for_tts("Calculer 1,5 * 10^-3 et H_2O.")
        self.assertIn("*", cleaned)
        self.assertIn("H_2O", cleaned)
        self.assertEqual(
            normalize_for_speech(cleaned, "fr"),
            "Calculer un virgule cinq fois dix puissance moins trois et H deux O.",
        )

    def test_emojis_and_ascii_emoticons_are_removed_from_tts_copy(self):
        cleaned = tts_service.clean_for_tts("مزيان 😊 ! Bravo ✅ :) <3")
        self.assertNotIn("😊", cleaned)
        self.assertNotIn("✅", cleaned)
        self.assertNotIn(":)", cleaned)
        self.assertNotIn("<3", cleaned)
        self.assertIn("مزيان", cleaned)
        self.assertIn("Bravo", cleaned)

    def test_arabic_article_is_separated_from_nouns(self):
        spoken = normalize_for_speech(
            "ركزو مع التمرين الأول اللي جا ف الامتحان الوطني.", "mixed"
        )
        self.assertIn("ال تمرين", spoken)
        self.assertIn("ال امتحان", spoken)
        self.assertIn("اللي", spoken)
        self.assertNotIn("التمرين", spoken)

    def test_lexical_arabic_forms_are_not_broken(self):
        spoken = normalize_for_speech("الله كيعلم، والذي نجح.", "mixed")
        self.assertIn("الله", spoken)
        self.assertIn("الذي", spoken)

    def test_ratio_is_not_mistaken_for_a_time(self):
        self.assertEqual(normalize_for_speech("Le rapport est 1:2.", "fr"), "Le rapport est un:deux.")

    def test_school_abbreviations_formulas_and_name_lexicon(self):
        """Les sigles et les noms viennent du lexique, les formules de la règle.

        `formulas` est vide dans les deux langues : une formule a UNE seule
        écriture parlée, celle du corpus d'entraînement, et elle ne dépend plus
        d'une entrée à tenir à jour.
        """
        self.assertEqual(
            normalize_for_speech("SVT, ADN, pH, H2O et Newton", "fr"),
            "ès vé té, a dé enne, P H, H deux O et Nioutonne",
        )

    def test_date_time_and_ordinal(self):
        self.assertEqual(
            normalize_for_speech("Le 08/08/2026 à 14h30, chapitre 2e.", "fr"),
            "Le huit août deux mille vingt-six à quatorze heures trente, "
            "chapitre deuxième.",
        )

    def test_darija_mixed_uses_arabic_spoken_forms(self):
        result = normalize_for_speech("النسبة هي 25% والسرعة 5 km/h و ADN", "mixed")
        self.assertIn("خمسة وعشرين فالمية", result)
        self.assertIn("خمسة كيلومترات فالساعة", result)
        self.assertIn("آ دي إن", result)
        self.assertEqual(normalize_for_speech("2,5", "mixed"), "deux virgule cinq")
        self.assertIn("جوج فاصلة خمسة", normalize_for_speech("القيمة 2,5", "mixed"))

    def test_ph_is_spelled_out_for_academy(self):
        spoken = normalize_for_speech("الـ 7 هو pH محايد.", "mixed")
        self.assertIn("P H", spoken)
        self.assertNotIn("pH", spoken)

    def test_frequency_and_basic_si_units_are_not_misread_as_time(self):
        spoken = normalize_for_speech(
            "La fréquence est 4 Hz, la distance est 6,0 m et la durée est 0,5 s.",
            "fr",
        )
        self.assertIn("quatre hertz", spoken)
        self.assertNotIn("heuresz", spoken)
        self.assertIn("six virgule zéro mètres", spoken)
        self.assertIn("zéro virgule cinq secondes", spoken)

    def test_student_names_are_spoken_in_arabic(self):
        self.assertEqual(
            normalize_for_speech(
                "سلام Zouhair، مرحبا Ferdaous و Yassine.", "mixed"
            ),
            "سلام زهير، مرحبا فردوس و ياسين.",
        )

    def test_markup_is_removed_but_math_is_preserved_for_next_stage(self):
        cleaned = tts_service.clean_for_tts(
            "<board>ne pas lire 25%</board> Résultat : $E=mc^2$."
        )
        self.assertNotIn("ne pas lire", cleaned)
        self.assertIn("$E=mc^2$", cleaned)

    def test_mixed_darija_does_not_attach_arabic_article_to_french_terms(self):
        spoken = normalize_for_speech(
            "مرات اللي كيعاود فيها الـ motif نفسو فـ ثانية وحدة. "
            "وحدتها الـ Hertz (Hz). والعلاقة بينها وبين la période هي: N = 1/T.",
            "mixed",
        )
        self.assertNotIn("الـ motif", spoken)
        self.assertNotIn("الـ Hertz", spoken)
        self.assertIn("la fréquence كتساوي واحد على la période", spoken)
        self.assertNotIn("N يساوي", spoken)

    def test_generic_formula_slash_is_spoken_as_a_fraction(self):
        spoken = normalize_for_speech("La relation est N = 1/T.", "fr")
        self.assertIn("la fréquence est égale à un sur la période", spoken)

    def test_known_formula_does_not_repeat_its_subject(self):
        spoken = normalize_for_speech(
            "La vitesse est v = λ × N, avec une fréquence de 4 Hz.", "fr"
        )
        self.assertEqual(
            spoken,
            "la vitesse est égale à la longueur d'onde fois la fréquence, "
            "avec une fréquence de quatre hertz.",
        )

    def test_ohm_law_is_spoken_as_words(self):
        self.assertEqual(
            normalize_for_speech("U = R × I", "fr"),
            "la tension est égale à la résistance fois l'intensité",
        )

    def test_tts_copie_ferme_la_derniere_phrase(self):
        self.assertEqual(tts_service._ensure_terminal_period("Une phrase"), "Une phrase.")
        self.assertEqual(tts_service._ensure_terminal_period("Une question ?"), "Une question ?")


class TTSIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_academy_receives_spoken_copy_and_caption_keeps_original(self):
        source = "La probabilité est 25% en SVT."
        with (
            patch.object(tts_service, "_route", return_value=("academy", "prof", "wav")),
            patch.object(tts_service, "_get_cache", return_value=None),
            patch.object(
                tts_service,
                "_synthesize_academy",
                new=AsyncMock(return_value=b"RIFF-test-audio"),
            ) as academy,
        ):
            segment = await tts_service._synthesize_one_segment(source, "fr")

        self.assertIsNotNone(segment)
        self.assertEqual(segment.text, source)
        academy.assert_awaited_once_with(
            "La probabilité est vingt-cinq pour cent en ès vé té.", "fr"
        )


if __name__ == "__main__":
    unittest.main()


# ── Frontieres d'ecriture (code-switching darija / francais) ──────

def test_la_tatweel_ne_se_prononce_pas():
    """« فـ le noyau » : ce trait est une decoration typographique, pas une
    lettre. Le TTS la traite comme un caractere et racle au milieu du mot."""
    parle = normalize_for_speech("كاينة فـ le noyau", "mixed")
    assert "ـ" not in parle
    assert "ف le noyau" in parle


def test_un_mot_latin_colle_a_l_arabe_est_detache():
    """« وla proteine » est un token hybride que le moteur ne sait lire
    dans aucune des deux langues."""
    assert normalize_for_speech("وla proteine", "mixed").startswith("و la")


def test_le_detachement_ne_perd_aucune_lettre():
    """Le premier correctif ecrivait un caractere de controle a la place de
    la lettre capturee : elle disparaissait du texte parle."""
    parle = normalize_for_speech("الطبق، وla proteine", "mixed")
    assert "و" in parle
    assert not [c for c in parle if ord(c) < 32]


def test_les_sigles_composes_sont_epeles():
    """« ARN » ne peut pas attraper « ARNm » : la frontiere de mot du lexique
    s'arrete avant le suffixe."""
    assert "ARNm" not in normalize_for_speech("le ARNm sort du noyau", "fr")


# ── Respiration ──────────────────────────────────────────────────

def test_le_deux_points_d_annonce_ouvre_une_pause():
    assert ": transcription" in normalize_for_speech("les etapes:transcription", "fr")


def test_le_deux_points_d_un_ratio_reste_colle():
    """Applique tot, tant que les chiffres sont encore des chiffres."""
    assert "un:deux" in normalize_for_speech("le rapport 1:2", "fr")


def test_une_heure_survit_a_la_regle_du_deux_points():
    assert "heures" in normalize_for_speech("il est 14:30", "fr")


def test_une_enumeration_en_lignes_recoit_ses_points():
    """Sans point, les elements se collent et sortent d'un seul souffle."""
    parle = normalize_for_speech("la periode\nla frequence\nla longueur", "fr")
    assert parle.count(".") >= 2


# ── Formules, sigles et charges : la convention du corpus ─────────
#
# Le modele Academy a appris ses prononciations sur les transcriptions
# normalisees par `scripts/normalize_combined_dataset.py` (depot DARIJA TTS).
# Une forme ecrite qu'il n'a jamais vue a l'entrainement le fait improviser :
# ces tests verrouillent l'alignement sur ce corpus, chiffres et signes dits
# en francais dans les deux langues.

def test_formule_chimique_inconnue_du_lexique_est_dite():
    """« CH4 » repartait brut : rien ne l'epelait hors du lexique."""
    assert normalize_for_speech("CH4", "fr") == "C H quatre"
    assert normalize_for_speech("C6H12O6", "fr") == "C six H douze O six"


def test_les_chiffres_dune_formule_forment_un_nombre():
    """« H12 » se dit « H douze », jamais « H un deux »."""
    assert "douze" in normalize_for_speech("C6H12O6", "fr")


def test_la_charge_ionique_est_dite_en_francais():
    """Le « + » et le « - » d'un ion, dans les deux langues."""
    assert normalize_for_speech("H3O+", "fr") == "H trois O plus"
    assert normalize_for_speech("H3O+", "ar") == "H trois O plus"


def test_la_charge_en_exposant_vaut_la_charge_ecrite_a_plat():
    """« Ca²⁺ » disait « Ca au carre » : une charge n'est pas une puissance.

    Le nom de l'element vient de `_NOMS_ELEMENTS` ; ce que ce test verrouille,
    c'est que les deux ecritures de la charge donnent la meme phrase.
    """
    assert normalize_for_speech("Ca²⁺", "fr") == "calcium deux plus"
    assert normalize_for_speech("Ca2+", "fr") == "calcium deux plus"


def test_le_compte_de_charge_survit_a_lespace():
    """« SO4 2- » : le « 2 » appartient a la charge, pas au discours."""
    assert normalize_for_speech("SO4 2-", "fr") == "S O quatre deux moins"
    assert normalize_for_speech("SO₄²⁻", "fr") == "S O quatre deux moins"


def test_une_puissance_negative_nest_pas_prise_pour_une_charge():
    """Garde-fou du meme correctif : « 10⁻³ » reste une puissance."""
    assert "puissance moins trois" in normalize_for_speech("10⁻³ mol/L", "fr")


def test_un_sigle_inconnu_est_epele():
    """Hors lexique, un sigle repartait brut vers le modele."""
    assert normalize_for_speech("le TGV", "fr") == "le T G V"


def test_un_sigle_lu_comme_un_mot_nest_pas_epele():
    assert normalize_for_speech("SIDA", "fr") == "Sida"


def test_la_liste_des_sigles_lus_comme_des_mots_reste_celle_du_corpus():
    """Mesure sur les 9 997 transcriptions : le professeur epelle « P I B ».

    Y ajouter un sigle au juge se paie immediatement — « PIB » y avait ete mis
    et faisait dire « Pib » 183 fois.
    """
    assert normalize_for_speech("le PIB", "fr") == "le P I B"
    assert normalize_for_speech("la TVA", "fr") == "la T V A"


def test_un_mot_ordinaire_nest_jamais_epele():
    """« Ne », « Si », « As », « In » sont des symboles ET des mots courants.

    C'est le risque de cette etape : elle voit tous les mots latins et doit
    n'en toucher aucun qui ne soit pas une formule.
    """
    for phrase in ("Ne bouge pas", "Si tu veux", "As-tu compris", "In fine",
                   "Bonjour les eleves", "Newton a explique"):
        parle = normalize_for_speech(phrase, "fr")
        assert parle.split()[0] not in {"N", "S", "A", "I", "B"}, phrase


def test_les_chiffres_romains_ne_sont_pas_des_sigles():
    """Le cours de SVT en est plein : « Anaphase II », pas « Anaphase I I »."""
    assert normalize_for_speech("Anaphase II", "fr") == "Anaphase deux"
    assert normalize_for_speech("division IV", "fr") == "division quatre"


def test_les_symboles_mathematiques_du_corpus_sont_tous_dits():
    """Ce qui restait brut ici, le modele l'inventait."""
    attendus = {
        "A ⇒ B": "implique", "x ∈ E": "appartient à", "√2": "racine carrée de",
        "3 ± 1": "plus ou moins", "∑ f": "somme de", "∫ f": "intégrale de",
        "π": "pi", "θ": "thêta", "ρ": "rho", "σ": "sigma", "∞": "l'infini",
        "30 °": "degrés",
    }
    for source, attendu in attendus.items():
        assert attendu in normalize_for_speech(source, "fr"), source


def test_une_unite_composee_se_dit_sans_nombre_devant():
    """« la concentration en mol/L » se lisait « mol sur L »."""
    assert normalize_for_speech("en mol/L", "fr") == "en moles par litre"
    assert normalize_for_speech("en m/s", "fr") == "en mètres par seconde"


def test_la_table_darija_connait_les_memes_unites_que_la_francaise():
    """Douze unites manquaient cote darija : elles repartaient en symboles."""
    for source in ("5 µm", "3 kJ", "1013 hPa", "2 mA"):
        parle = normalize_for_speech(source, "ar")
        assert not _LATIN_RE.search(parle), f"{source} -> {parle}"


# ── Ions monoatomiques : le nom de l'élément, pas ses lettres ─────

def test_un_ion_monoatomique_porte_le_nom_de_son_element():
    """« Ca²⁺ » se dit « calcium deux plus » en classe, pas « cé a deux plus »."""
    assert normalize_for_speech("Ca²⁺", "fr") == "calcium deux plus"
    assert normalize_for_speech("Fe3+", "fr") == "fer trois plus"
    assert normalize_for_speech("Cl-", "fr") == "chlore moins"
    assert normalize_for_speech("Zn2+", "ar") == "zinc deux plus"


def test_le_chiffre_colle_au_signe_compte_les_charges():
    """« Fe3+ » : le 3 est un nombre de charges, pas un indice de formule."""
    assert normalize_for_speech("Fe3+", "fr") == normalize_for_speech("Fe³⁺", "fr")
    assert normalize_for_speech("Ca2+", "fr") == normalize_for_speech("Ca²⁺", "fr")


def test_une_formule_a_plusieurs_elements_garde_ses_symboles():
    """Personne ne dit « hydrogène trois oxygène plus »."""
    assert normalize_for_speech("H3O+", "fr") == "H trois O plus"
    assert normalize_for_speech("SO4 2-", "fr") == "S O quatre deux moins"


def test_un_symbole_dune_seule_lettre_nest_pas_nomme():
    """« H plus », « O deux moins » sont ce que dit le professeur."""
    assert normalize_for_speech("H+", "fr") == "H plus"
    assert normalize_for_speech("O2-", "fr") == "O deux moins"


def test_un_tiret_de_ponctuation_nest_pas_une_charge():
    """« Ne », « Si », « Te » sont des symboles ET des mots courants.

    Accepter une espace devant un signe sans compte suffisait à faire dire
    « néon moins regarde ».
    """
    for phrase in ("Ne - regarde", "Si - alors", "Te - rappelles-tu"):
        assert normalize_for_speech(phrase, "fr") == phrase


def test_le_lexique_survit_a_un_mot_compose():
    """La garde anti-charge ne doit pas couper « pH-mètre » du lexique."""
    assert "P H" in normalize_for_speech("le pH-mètre", "fr")
    assert "a dé enne" in normalize_for_speech("ADN-polymérase", "fr")


def test_toutes_les_formules_ont_la_meme_ecriture_dans_les_deux_langues():
    """`formulas` vidé des deux côtés : plus aucun doublon avec la règle.

    Le lexique donnait « ache deux o » en français et « آش جوج أو » en darija
    pour la même molécule. Le modèle a appris « H deux O » — c'est cette
    écriture, et elle seule, qui doit lui parvenir.
    """
    for langue in ("fr", "ar"):
        assert normalize_for_speech("H2O", langue) == "H deux O"
        assert normalize_for_speech("CO2", langue) == "C O deux"
        assert normalize_for_speech("NaCl", langue) == "N A C L"
        assert normalize_for_speech("HCl", langue) == "H C L"
        assert normalize_for_speech("O2", langue) == "O deux"
