import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"


class MobileAccessTests(unittest.TestCase):
    def test_web_app_manifest_is_local_and_installable(self) -> None:
        manifest = (DASHBOARD / "app" / "manifest.ts").read_text()
        self.assertIn("display: 'standalone'", manifest)
        self.assertIn("start_url: '/'", manifest)
        self.assertNotIn("https://", manifest)

    def test_mobile_metadata_declares_safe_area_viewport(self) -> None:
        layout = (DASHBOARD / "app" / "layout.tsx").read_text()
        self.assertIn("viewportFit: 'cover'", layout)
        self.assertIn("appleWebApp", layout)

    def test_mobile_navigation_targets_existing_sections(self) -> None:
        page = (DASHBOARD / "app" / "page.tsx").read_text()
        for target in ("#overview", "#history", "#relationships", "#health"):
            self.assertIn(f'href="{target}"', page)
        self.assertIn('className="mobile-nav"', page)
        self.assertIn("aria-label={t.mobileNavigation}", page)

    def test_mobile_layout_accounts_for_safe_area_and_touch_targets(self) -> None:
        styles = (DASHBOARD / "app" / "globals.css").read_text()
        self.assertIn("env(safe-area-inset-bottom)", styles)
        self.assertIn("min-height:44px", styles)


if __name__ == "__main__":
    unittest.main()
