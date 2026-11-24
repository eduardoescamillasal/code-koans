import json


def predict(t, s):
    t.assertEqual(s.prediction, json.loads('{"limit":1,"limit":9}')["limit"])


def contrast(t, s):
    grouped = json.loads('{"limit":1,"limit":9}', object_pairs_hook=list)
    t.assertEqual(s.contrast, grouped)


def implement(t, s):
    raw = '{"type":"call","id":"c1","name":"lookup","args":{"count":2,"prefix":"ab"}}'
    t.assertEqual(s.parse(raw), {"type": "call", "id": "c1", "name": "lookup",
                                 "args": {"count": 2, "prefix": "ab"}})


def break_cases(t, s):
    for raw in (None, "{", "[]", '{"type":"final","text":true}',
                '{"type":"final","text":"a","text":"b"}',
                '{"type":"final","text":"a","extra":3}',
                '{"type":"call","id":"1","name":"read","args":{"n":1e999}}',
                '{"type":"call","id":"1","name":"read","args":{"n":{}}}',
                '{"type":"call","id":"1","name":"read","args":{"n":1,"n":2}}'):
        with t.assertRaises(ValueError):
            s.parse(raw)


def transfer(t, s):
    replies = [
        json.dumps({"type": "final", "text": '{"type":"call"}'}),
        json.dumps({"type": "call", "id": "1", "name": "read", "args": {}}),
        json.dumps({"type": "final", "text": "complete"}),
    ]
    t.assertEqual(s.archive_text(replies), ['{"type":"call"}', "complete"])
    with t.assertRaises(ValueError):
        s.archive_text([*replies, '{"type":"final"}'])
