import unittest
from unittest.mock import AsyncMock, patch

from app.services import tts_service
from app.services.speech_normalizer import normalize_for_speech


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
            "Calculer un virgule cinq fois dix puissance moins trois et ache deux o.",
        )

    def test_ratio_is_not_mistaken_for_a_time(self):
        self.assertEqual(normalize_for_speech("Le rapport est 1:2.", "fr"), "Le rapport est un:deux.")

    def test_school_abbreviations_formulas_and_name_lexicon(self):
        self.assertEqual(
            normalize_for_speech("SVT, ADN, pH, H2O et Newton", "fr"),
            "ès vé té, a dé enne, pé ache, ache deux o et Nioutonne",
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

    def test_markup_is_removed_but_math_is_preserved_for_next_stage(self):
        cleaned = tts_service.clean_for_tts(
            "<board>ne pas lire 25%</board> Résultat : $E=mc^2$."
        )
        self.assertNotIn("ne pas lire", cleaned)
        self.assertIn("$E=mc^2$", cleaned)


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
