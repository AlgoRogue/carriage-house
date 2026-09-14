"""Motor adaptörleri — ağ yok, CLI çağrısı yok. Komut bayrakları ve sahte çıktı çözümlemesi."""
import json
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "bin"))
import motorlar  # noqa: E402

AYAR = {"model": None, "effort": None, "araclar": ["Read", "Write"], "butce_usd": 2,
        "json_sema": None, "sema_dosyasi": None, "maks_tur": 40}
SEMA = {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]}


class OrtakTesti(unittest.TestCase):
    def test_dort_motor_ve_ters_tablo(self):
        self.assertEqual(set(motorlar.MOTORLAR), {"claude", "agy", "codex", "grok"})
        for ureten, bekci in motorlar.TERS_MOTOR.items():
            self.assertNotEqual(ureten, bekci, "üreten kendini denetleyemez")
            self.assertIn(bekci, motorlar.MOTORLAR)
        self.assertEqual(motorlar.ters_motor("codex"), "claude")
        self.assertEqual(motorlar.ters_motor("claude"), "grok")

    def test_her_motor_ayni_yuzu_verir(self):
        for ad, modul in motorlar.MOTORLAR.items():
            self.assertEqual(set(modul.YETENEK), {"maliyet_raporlar", "arac_kisiti", "json_sema", "tur_tavani"}, ad)
            komut = modul.komut("selam", {**AYAR, "sema_dosyasi": "/tmp/s.json"})
            self.assertEqual(komut[0], ad)
            self.assertIn("selam", komut)
            bozuk = modul.cozumle("bu json değil")
            self.assertTrue(bozuk["hata"])
            self.assertEqual(set(bozuk), {"hata", "maliyet", "tur", "metin", "yapisal", "oturum"})

    def test_yapisal_coz(self):
        self.assertEqual(motorlar.yapisal_coz('önsöz {"a": 1} sonsöz'), {"a": 1})
        self.assertIsNone(motorlar.yapisal_coz("[1,2]"))
        self.assertIsNone(motorlar.yapisal_coz(""))


class ClaudeTesti(unittest.TestCase):
    def test_komut_butce_arac_ve_sema(self):
        k = motorlar.claude.komut("x", {**AYAR, "json_sema": SEMA, "model": "opus"})
        self.assertIn("--max-budget-usd", k)
        self.assertEqual(k[k.index("--allowedTools") + 1], "Read,Write")
        self.assertEqual(k[k.index("--model") + 1], "opus")
        self.assertEqual(json.loads(k[k.index("--json-schema") + 1]), SEMA)

    def test_cozumle_maliyet_ve_yapisal(self):
        c = motorlar.claude.cozumle(json.dumps({"is_error": False, "total_cost_usd": 0.42, "num_turns": 3,
                                                 "result": '{"a": "b"}'}))
        self.assertFalse(c["hata"])
        self.assertAlmostEqual(c["maliyet"], 0.42)
        self.assertEqual(c["tur"], 3)
        self.assertEqual(c["yapisal"], {"a": "b"})
        c2 = motorlar.claude.cozumle(json.dumps({"result": "x", "structured_output": {"a": "z"}, "session_id": "s1"}))
        self.assertEqual(c2["yapisal"], {"a": "z"})
        self.assertEqual(c2["oturum"], "s1")


class AgyTesti(unittest.TestCase):
    def test_komut_ve_cozumle(self):
        k = motorlar.agy.komut("x", {**AYAR, "effort": "high", "json_sema": SEMA})
        self.assertIn("--dangerously-skip-permissions", k)
        self.assertEqual(k[k.index("--effort") + 1], "high")
        self.assertIn("--json-schema", k)
        c = motorlar.agy.cozumle(json.dumps({"status": "SUCCESS", "num_turns": 2, "response": '{"a":"1"}'}))
        self.assertFalse(c["hata"])
        self.assertEqual(c["maliyet"], 0.0)
        self.assertEqual(c["yapisal"], {"a": "1"})
        self.assertTrue(motorlar.agy.cozumle(json.dumps({"status": "ERROR", "response": ""}))["hata"])


class CodexTesti(unittest.TestCase):
    def test_komut_semayi_dosyadan_verir(self):
        k = motorlar.codex.komut("x", {**AYAR, "json_sema": SEMA, "sema_dosyasi": "/tmp/s.json", "model": "gpt"})
        self.assertEqual(k[:2], ["codex", "exec"])
        self.assertEqual(k[k.index("--output-schema") + 1], "/tmp/s.json")
        self.assertEqual(k[k.index("-m") + 1], "gpt")
        self.assertNotIn("--output-schema", motorlar.codex.komut("x", {**AYAR, "json_sema": SEMA}))

    def test_cozumle_jsonl(self):
        satirlar = [{"type": "thread.started", "thread_id": "t9"}, {"type": "turn.started"},
                    {"type": "item.completed", "item": {"type": "agent_message", "text": "düşünüyorum"}},
                    {"type": "turn.completed"},
                    {"type": "item.completed", "item": {"type": "agent_message", "text": '{"a": "son"}'}},
                    {"type": "turn.completed"}]
        c = motorlar.codex.cozumle("\n".join(json.dumps(s) for s in satirlar))
        self.assertFalse(c["hata"])
        self.assertEqual(c["tur"], 2)
        self.assertEqual(c["yapisal"], {"a": "son"})
        self.assertIn("düşünüyorum", c["metin"])
        self.assertEqual(c["oturum"], "t9")
        self.assertTrue(motorlar.codex.cozumle(json.dumps({"type": "error"}))["hata"])


class GrokTesti(unittest.TestCase):
    def test_komut_arac_kisiti_ve_tur_tavani(self):
        k = motorlar.grok.komut("x", {**AYAR, "json_sema": SEMA, "effort": "low", "model": "grok-4"})
        self.assertEqual(k[:2], ["grok", "-p"])
        self.assertEqual(k[k.index("--tools") + 1], "read_file,list_dir,write")  # Claude adı → grok adı
        self.assertEqual(k[k.index("--max-turns") + 1], "40")
        self.assertIn("--disable-web-search", k)
        self.assertIn("--json-schema", k)
        self.assertIn("--rules", k)
        self.assertEqual(k[k.index("-m") + 1], "grok-4")
        k2 = motorlar.grok.komut("x", {**AYAR, "araclar": ["Read", "WebSearch"]})
        self.assertNotIn("--disable-web-search", k2)
        self.assertEqual(motorlar.grok.araclari_cevir(["Read", "Edit", "Glob", "Bash", "ozel"]),
                         ["read_file", "list_dir", "search_replace", "run_terminal_command", "ozel"])

    def test_cozumle_toleransli(self):
        c = motorlar.grok.cozumle(json.dumps({"result": '{"a": "g"}', "num_turns": 4}))
        self.assertFalse(c["hata"])
        self.assertEqual(c["tur"], 4)
        self.assertEqual(c["yapisal"], {"a": "g"})
        c2 = motorlar.grok.cozumle(json.dumps({"text": "metin", "structuredOutput": {"a": "s"},
                                                "sessionId": "g1", "total_cost_usd": 0.0039}))
        self.assertEqual(c2["yapisal"], {"a": "s"})
        self.assertEqual(c2["oturum"], "g1")
        self.assertAlmostEqual(c2["maliyet"], 0.0039)
        self.assertTrue(motorlar.grok.cozumle(json.dumps({"error": "kota"}))["hata"])
        self.assertTrue(motorlar.grok.cozumle("[1]")["hata"])


if __name__ == "__main__":
    unittest.main()
