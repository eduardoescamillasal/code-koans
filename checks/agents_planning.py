def predict(t, s):
    graph = {"package": {"compile"}, "compile": set(), "test": {"compile"}}
    t.assertEqual(s.prediction, tuple(job for job, deps in graph.items() if not deps))


def contrast(t, s):
    graph = {"package": {"compile"}, "compile": {"package"}, "test": {"compile"}}
    t.assertEqual(s.contrast, tuple(job for job, deps in graph.items() if not deps))


def implement(t, s):
    jobs = {"export": ["clean", "review"], "prepare": [], "review": ["prepare"],
            "clean": ["prepare", "prepare"]}
    t.assertEqual(s.plan(jobs), ["prepare", "clean", "review", "export"])


def break_cases(t, s):
    for graph in ({"x": ["missing"]}, {"idle": [], "x": ["y"], "y": ["x"]}, {"x": ["x"]}):
        with t.assertRaises(ValueError):
            s.plan(graph)
    t.assertEqual(s.plan({}), [])


def transfer(t, s):
    graph = {"z-audit": [], "a-package": iter(["b-build"]), "b-build": [],
             "release": iter(["a-package", "z-audit"]), "review": ["z-audit"]}
    t.assertEqual(s.rebuild(graph, "b-build"), ["b-build", "a-package", "release"])
    with t.assertRaises(ValueError):
        s.rebuild({"a": []}, "missing")
