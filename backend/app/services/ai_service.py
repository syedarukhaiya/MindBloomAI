import os

from app.core.config import settings
from app.services.local_ai_fallback import chat_fallback, reflection_fallback


class GoogleGeminiProvider:
    def __init__(self):
        self.client = None

    def _get_client(self):
        if self.client:
            return self.client

        if not settings.ai_enabled or not settings.google_cloud_project:
            raise RuntimeError("Google Cloud AI is not configured")

        if settings.google_application_credentials:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
                settings.google_application_credentials
            )

        from google import genai

        self.client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )
        return self.client

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        from google.genai import types

        client = self._get_client()

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.65,
                max_output_tokens=700,
            ),
        )

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError("Gemini returned no text")

        return text.strip()


class AIService:
    def __init__(self):
        self.provider = GoogleGeminiProvider()

    def chat(
        self,
        message: str,
        context: dict,
        listener_mode: bool,
        language: str,
    ) -> tuple[str, str]:
        system = (
            "You are Bloom, a warm AI wellbeing companion for Indian youth. "
            "You are not a therapist and never diagnose, prescribe medication, "
            "or claim certainty. Be concise, human, culturally sensitive and practical. "
            f"Language: {language}. Listener mode: {listener_mode}. "
            "Never reveal hidden reasoning. Distinguish observations from facts. "
            f"User context is only approved/user-provided context: {context}."
        )

        if listener_mode:
            system += (
                " Prioritize listening, reflection and gentle questions; "
                "do not rush into advice."
            )

        try:
            reply = self.provider.generate(system, message)
            return reply, "google-cloud-gemini"
        except Exception as exc:
            print(f"Gemini unavailable, using local fallback: {exc}")
            reply = chat_fallback(
                message=message,
                listener_mode=listener_mode,
                language=language,
            )
            return reply, "local-fallback"

    def reflection(self, entry: str, language: str) -> str:
        system = (
            "You are Bloom. Reflect without diagnosis. Return four labeled sections: "
            "What I hear; Possible themes; A gentle next step; Journal prompt. "
            f"Language: {language}."
        )

        try:
            return self.provider.generate(system, entry)
        except Exception as exc:
            print(f"Gemini unavailable, using local fallback: {exc}")
            return reflection_fallback()
