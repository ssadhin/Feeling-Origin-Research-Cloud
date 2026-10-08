"""Regression tests for Eon's pinned Microsoft Playwright MCP adapter."""
from __future__ import annotations
import asyncio
import importlib.util
import tempfile
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SRC=Path(__file__).resolve().parent.parent / "src" / "eon_playwright_browser.py"
spec=importlib.util.spec_from_file_location("eon_playwright_browser",SRC)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestBrowserAdapter(unittest.TestCase):
 def test_immutable_upstream_backend(self):
  stat=m.status()
  self.assertEqual(stat["upstream"],"microsoft/playwright-mcp")
  self.assertEqual(stat["upstream_version"],"0.0.83")
  self.assertEqual(stat["license"],"Apache-2.0")
  self.assertTrue(stat["installed_and_pinned"])
  self.assertEqual(stat["chrome_profile"],"Profile 2")
  self.assertEqual(stat["browser_session"].split(";")[0],"EXISTING signed-in Chrome")
 def test_project_id_no_cross_project(self):
  target=m.PROJECT_URL
  ok="https://chatgpt.com/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5-research-2/c/a"
  self.assertTrue(m.project_match(ok,target))
  self.assertTrue(m.project_match(target,target))
  for notok in [
   "https://evil.com/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5/project",
   "https://chatgpt.com/g/g-p-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/project",
   "https://chatgpt.com/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5-unrelated.com",
   "http://chatgpt.com/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5/project",
   "https://chatgpt.com.evil.com/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5/project",
  ]:
   with self.subTest(notok=notok):self.assertFalse(m.project_match(notok,target))
 def test_snapshot_requires_page_header(self):
  def result(txt):
   return SimpleNamespace(content=[SimpleNamespace(type="text",text=txt)])
  u="https://chatgpt.com/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5/project"
  self.assertEqual(m.snapshot_page_url(result("### Page\n- Page URL: "+u+"\n- Page Title: Test")),u)
  self.assertIsNone(m.snapshot_page_url(result("- paragraph: Page URL: "+u)))
  self.assertIsNone(m.snapshot_page_url(result("Hello "+u)))
 def test_browsing_mutation_needs_explicit_approval(self):
  with self.assertRaisesRegex(PermissionError,"BROWSER_MUTATION_NOT_AUTHORIZED"):
   asyncio.run(m.run("browser_type",{"target":"e2","text":"Do not type"}))
  with self.assertRaisesRegex(ValueError,"UNRECOGNIZED"):
   asyncio.run(m.run("browser_delete_all_cookies",{}))
 def test_configuration_confirmation_and_modes(self):
  with tempfile.TemporaryDirectory() as d:
   with patch.object(m,"SETTINGS",Path(d)/"config.json"),patch.object(m,"BROWSER_HOME",Path(d)):
    s=m.config()
    self.assertEqual(s["profile"],"Profile 2")
    with self.assertRaisesRegex(ValueError,"EXPLICIT_USER_CONFIRMATION"):
     m._set_config({"allow_mutating_tools":True})
    with self.assertRaisesRegex(ValueError,"CHOOSE"):
     m._set_config({"backend":"native_profile_copy"})
    s=m._set_config({"backend":"chrome_cdp","profile":"Profile 2"})
    self.assertFalse(s["mutating_actions_authorized"])
 def test_python_module_safety(self):
  self.assertIn("browser_type",m.ALLOWED)
  self.assertNotIn("browser_run_code",m.ALLOWED)
  self.assertTrue(m.test_offline()["ok"])
 def test_mcp_catalog_has_no_new_chatgpt_plugin(self):
  x=m.catalog()
  self.assertFalse(x["extra_chatgpt_mcp_required"])
  self.assertTrue(any(t["action"]=="browser_type" for t in x["actions"]))
  self.assertTrue(any(t["action"]=="browser_click" for t in x["actions"]))
if __name__=="__main__":unittest.main()
