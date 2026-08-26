# AI Architecture

`AIService` is provider-agnostic. `GoogleGeminiProvider` uses the Google Gen AI SDK in Vertex AI mode. Business logic never depends directly on SDK objects. Context is concise and user-scoped. No chain-of-thought is stored or exposed.

AI tasks: conversation, reflection, micro-intervention wording, wellbeing insight generation and multilingual response generation.
