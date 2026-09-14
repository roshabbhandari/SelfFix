import pytest

from agent import CodingAgent


def test_parse_action_rejects_invalid_json(tmp_path):
    agent = CodingAgent(str(tmp_path), "issue")
    with pytest.raises(Exception):
        agent._parse_action("not json")


def test_parse_action_extracts_embedded_object(tmp_path):
    agent = CodingAgent(str(tmp_path), "issue")
    action = agent._parse_action('prefix {"tool":"finish","args":{}} suffix')
    assert action["tool"] == "finish"
