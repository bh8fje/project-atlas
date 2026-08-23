import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "dashboard" / "app"


class DashboardInternationalizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.i18n = (APP / "i18n.ts").read_text()
        self.page = (APP / "page.tsx").read_text()

    def test_supports_chinese_and_requested_languages(self) -> None:
        self.assertIn("['zh', 'en', 'ru', 'ko']", self.i18n)
        self.assertIn("中文", self.i18n)
        self.assertIn("Русский", self.i18n)
        self.assertIn("한국어", self.i18n)

    def test_system_language_resolution_has_safe_english_fallback(self) -> None:
        self.assertIn("resolveSystemLanguage", self.i18n)
        self.assertIn("rawLanguage.toLowerCase().split('-')[0]", self.i18n)
        self.assertIn("return 'en'", self.i18n)

    def test_default_preference_follows_system(self) -> None:
        self.assertIn("useState<LanguagePreference>('system')", self.page)
        self.assertIn("preference === 'system' ? systemLanguage : preference", self.page)
        self.assertIn("languagechange", self.page)

    def test_explicit_choice_is_local_and_reversible(self) -> None:
        self.assertIn("localStorage.setItem(LANGUAGE_STORAGE_KEY", self.page)
        self.assertIn("localStorage.removeItem(LANGUAGE_STORAGE_KEY)", self.page)
        self.assertNotIn("fetch(", self.page)

    def test_language_selector_exposes_system_and_all_languages(self) -> None:
        self.assertIn('<option value="system">', self.page)
        self.assertIn("supportedLanguages.map", self.page)
        self.assertIn("aria-label={t.selectLanguage}", self.page)

    def test_active_language_updates_document_language(self) -> None:
        self.assertIn("document.documentElement.lang = language", self.page)


if __name__ == "__main__":
    unittest.main()
