from openai import OpenAI

from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL
)


def run_ai_step(
    step_title: str,
    step_prompt: str,
    input_text: str
):

    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    prompt = f"""
You are executing one step of an AI workflow.

Step:
{step_title}

Instruction:
{step_prompt}

Input:
{input_text}

Complete only this workflow step.
Return a useful result for the next step.
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt
    )

    return response.output_text