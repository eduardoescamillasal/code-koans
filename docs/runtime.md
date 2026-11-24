# Bounded mock-agent runtime

The trusted caller supplies a policy string and a sequence of retrieved document
strings. The model receives a fresh copy of a dictionary with three entries.

| Key | Value |
| --- | --- |
| `policy` | Trusted policy, supplied by the caller |
| `documents` | Opaque strings. Embedded role labels have no authority |
| `results` | Ordered tool attempt records for unique call IDs |

The model returns one JSON string per step. The parser implements the Protocol
koan contract and raises `ValueError` on invalid input. The runtime reports
`(status, final_text_or_none, results)`. A result record has an `id`, a Boolean
`ok`, and a `value`. Tools should return JSON-compatible data. Normalize results
through JSON serialization to prevent later mutation. A tool exception or an
unserializable result records `"tool failed"`, with `ok` set to false. Model
exceptions propagate to the caller.

| Status | Trigger |
| --- | --- |
| `final` | A valid final message |
| `protocol` | A non-string model reply or a reply rejected by the parser |
| `context` | Context or reply exceeds the byte budget |
| `conflict` | A call ID is reused with a different name or arguments |
| `steps` | The model-call count reaches the step limit |

Count the context as sorted-key JSON with ASCII escaping using default
separators. Count model replies as UTF-8 bytes using `surrogatepass`. Check
context before calling the model and check the reply before parsing it. Each
model call costs a step, including repeated calls. Reject negative steps and
nonpositive budgets with `ValueError`. Zero steps produces an empty report.

Serialize the tool name and flat arguments as sorted-key JSON to form the call
fingerprint. Equivalent key orders represent the same call. JSON booleans and
numbers are distinct. Within one run, a matching repeated ID preserves the
original result and skips execution, even after a recorded failure. A
conflicting reuse stops the run and returns work already attempted. IDs are
scoped to one invocation. Side effects that succeed just before a process
crash are outside this in-process model. The tools and model are deterministic
in-process fixtures that return control. A step limit bounds call count.
