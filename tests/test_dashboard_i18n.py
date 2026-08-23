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

    def test_chinese_is_the_source_language(self) -> None:
        self.assertLess(self.i18n.index("zh: {"), self.i18n.index("en: {"))
        self.assertIn("Chinese is the source of meaning", self.i18n)

    def test_chinese_product_copy_avoids_known_internal_jargon(self) -> None:
        chinese = self.i18n.split("zh: {", 1)[1].split("en: {", 1)[0]
        for phrase in ("供应商无关", "分析契约", "类型化关系", "显式命令", "声明副作用", "尚未注册处理器", "架构演进", "基线全部通过", "ADR"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, chinese)

    def test_other_languages_remove_old_jargon_translation(self) -> None:
        for phrase in ("Provider-neutral analysis contracts", "Контракты анализа без привязки к провайдеру", "공급자 중립적 분석 계약"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.i18n)

    def test_repository_defines_plain_language_rules(self) -> None:
        rules = (ROOT / "docs" / "PRODUCT_LANGUAGE.md").read_text()
        agents = (ROOT / "AGENTS.md").read_text()
        self.assertIn("先写专业、清晰的中文", rules)
        self.assertIn("docs/PRODUCT_LANGUAGE.md", agents)

    def test_phase_names_use_professional_clear_language(self) -> None:
        chinese = self.i18n.split("zh: {", 1)[1].split("en: {", 1)[0]
        for name in ("基础架构", "项目发现", "项目历史", "AI 项目分析", "多语言支持"):
            with self.subTest(name=name):
                self.assertIn(name, chinese)
        for casual_phrase in ("打好基础", "找到项目", "AI 帮助", "更多智能功能"):
            with self.subTest(casual_phrase=casual_phrase):
                self.assertNotIn(casual_phrase, chinese)

    def test_each_development_phase_has_visible_feature_details(self) -> None:
        self.assertEqual(self.i18n.count("features: ["), 32)
        self.assertIn("已实现功能", self.i18n)
        self.assertIn("phase.features.map", self.page)
        self.assertIn("phase.summary", self.page)

    def test_development_phases_are_keyboard_accessible(self) -> None:
        self.assertIn('className="phase-row"', self.page)
        self.assertIn('type="button"', self.page)
        self.assertIn("aria-expanded", self.page)
        self.assertIn("aria-controls", self.page)


if __name__ == "__main__":
    unittest.main()
