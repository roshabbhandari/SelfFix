from agent import CodingAgent


def test_parse_action_accepts_plain_json(tmp_path):
    agent = CodingAgent(str(tmp_path), "issue")
    action = agent._parse_action('{"tool":"finish","args":{"summary":"ok"}}')
    assert action["tool"] == "finish"
    assert action["args"]["summary"] == "ok"


def test_parse_action_accepts_json_fence(tmp_path):
    agent = CodingAgent(str(tmp_path), "issue")
    action = agent._parse_action('```json\n{"tool":"finish","args":{}}\n```')
    assert action["tool"] == "finish"
