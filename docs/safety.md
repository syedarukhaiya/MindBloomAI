# Safety

Bloom has a deterministic safety pre-check for high-risk and distress language. High-risk requests are intercepted and receive a supportive escalation message instead of normal generation. Safety events are recorded without storing the raw message in the safety table. AI output is also kept behind a policy gate; production hardening should add a second model/policy evaluator before public deployment.

Resources must be verified for the user's current region. MindBloomAI never invents a phone number or claims to have called emergency services.
