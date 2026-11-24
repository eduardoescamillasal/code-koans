# API, agent, and workflow practice

The new modules use typed service classes, immutable payload objects, and
injected interfaces. Run any module directly. The deterministic fixtures model
application contracts and leave network transport, framework runtime, and
persistent storage outside the exercises.

| Command | Implement and explain |
| --- | --- |
| `python contemplate.py python rest_service` | Model REST creation, lookup, validation, and idempotent replays. Explain why replaying a creation response differs from fetching current resource state. |
| `python contemplate.py agents providers` | Adapt policy placement and usage counters for two model providers. Explain why throttling and invalid credentials need different handling. |
| `python contemplate.py agents workflow_graph` | Advance a graph from a checkpoint, stop on a node budget, and resume after failure. Explain what a committed revision guarantees about in-memory state. |
| `python contemplate.py agents grounded_qa` | Fit ranked evidence into a budget, validate citations, and score answers and abstentions. Explain what a cited document ID establishes about the answer. |
| `python contemplate.py agents webhooks` | Authenticate exact request bytes, deduplicate completed deliveries, and bound retries. Explain why an equivalent re-encoded JSON body can invalidate a signature. |

## Apply the same contracts in frameworks

- **FastAPI.** Put a typed request body at the route boundary. Call the job
  service and map its result to an HTTP status, body, and `Location` header.
  Compare an invalid request, a conflicting replay, and a missing resource.
  [FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/) ·
  [FastAPI status codes](https://fastapi.tiangolo.com/tutorial/response-status-code/)
- **Claude and Azure OpenAI.** Replace the mock transport with one adapter per
  API. Map the provider's real reply into the shared result type. Keep the
  fallback policy in the application and test how it handles throttling,
  authentication errors, and malformed replies independently.
  [Claude Messages API](https://platform.claude.com/docs/en/api/messages/create) ·
  [Azure OpenAI chat completions](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/chatgpt)
- **LangChain and LangGraph.** Use retriever and model boundaries to keep
  evidence selection and citation validation testable. Map reversible workflow
  transitions to graph nodes and conditional edges. Then compare the koan's
  in-memory checkpoint with a persisted graph run.
  [LangChain RAG resources](https://docs.langchain.com/oss/python/learn) ·
  [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- **n8n and Langflow.** Use the webhook exercise to reason about where a workflow
  authenticates, acknowledges, and deduplicates a request. In Langflow, map the
  grounded QA interfaces to components with explicit inputs and outputs. Keep
  workflow inputs, signed delivery envelopes, and application results distinct.
  [n8n Webhook node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/) ·
  [Langflow custom components](https://docs.langflow.org/components-custom-components)

## Failure cases to reason through

1. A worker writes to an external service and crashes before recording success.
   Which component owns the durable idempotency check, and what key can it use?
2. A secondary model gets the same text as the primary but a different policy
   representation. Which unit test would detect a change in policy placement?
3. A retrieved excerpt has a valid ID and says to ignore the question. What
   does the citation check establish, and what extra evidence would you need
   to evaluate whether the answer's claim follows from the excerpt?
4. A provider times out after accepting a request. How does that differ from a
   documented throttle response when deciding whether to retry a downstream
   action?
