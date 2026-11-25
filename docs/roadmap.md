# Curriculum roadmap

The curriculum started with five modules per track and one integration
challenge. Later releases add workflow, data, and model evaluation projects. Grow in
dependency order and review each module's contracts, reference, and failure
cases before adding the next.

| Track | Available now | Planned expansion |
| --- | --- | --- |
| Python | Object identity and aliasing, named tuples, numerical special methods, closures and lexical scope, metadata-preserving decorators, descriptor precedence and validation, iterator/generator state, coroutine scheduling and cancellation, REST service contracts | Evaluation order, a simplified property, attribute fallback and MRO, metaclasses, data model protocols, context managers, threading and multiprocessing, memory management, bytecode and interpreter behavior, profiling, dependency injection, event dispatch |
| Deep Learning | Linear maps and matrix products, binary64 precision, finite differences, cross-entropy, reverse-mode graphs and accumulation, rank-two broadcasting, stable masked attention, gradient descent, feature interactions, holdout evaluation | Explicit Jacobians for vector operations, general tensor shapes and reductions, affine layers and activations, alternative losses and optimizers, transformer blocks, tokenization and autoregressive generation |
| Agentic AI | Exact JSON message schemas, schema-based dispatch and permissions, cosine retrieval and excerpt budgets, dependency planning, bounded loops, per-run idempotency, partial failures, typed document boundaries, provider adapters, checkpointed workflows, grounded question answering, signed delivery retries | JSON Schema interoperability, context compression and memory policies, deterministic embeddings, concurrent tools, task decomposition and multi-agent coordination, retry policies, durable idempotency, evaluation harnesses, structured observability and cost accounting |
| Cross-track | Broadcast a trainable parameter, diagnose the trace, retrieve evidence, and route a permission-checked inspection through a mock runtime, audit missed positives by cohort | Closure-based graph adjoints, a decorator/descriptor tool registry and retrieval-grounded evaluation |

The current Python contracts target CPython 3.11–3.14. Binary64 examples assume
the typical IEEE 754 double-precision build. Future CPython-specific modules
should label interpreter and version constraints beside the behavior they test.
