import json
import time

import httpx
from openai import OpenAI


def parse_config(config_json: str | None) -> dict:
    if not config_json:
        return {}

    try:
        return json.loads(config_json)

    except json.JSONDecodeError:
        raise ValueError(
            "Invalid JSON configuration"
        )


def execute_http_request(
    config: dict,
) -> dict:
    url = config.get("url")

    method = config.get(
        "method",
        "GET",
    ).upper()

    headers = config.get(
        "headers",
        {},
    )

    body = config.get("body")

    if not url:
        raise ValueError(
            "HTTP_REQUEST requires url"
        )

    allowed_methods = {
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }

    if method not in allowed_methods:
        raise ValueError(
            "Unsupported HTTP method"
        )

    with httpx.Client(
        timeout=15.0,
    ) as client:
        response = client.request(
            method=method,
            url=url,
            headers=headers,
            json=body,
        )

    try:
        response_body = response.json()

    except Exception:
        response_body = response.text

    return {
        "status_code": response.status_code,
        "response": response_body,
    }


def execute_delay(
    config: dict,
) -> dict:
    seconds = config.get(
        "seconds",
        1,
    )

    try:
        seconds = int(seconds)

    except (TypeError, ValueError):
        raise ValueError(
            "Delay seconds must be a number"
        )

    if seconds < 0 or seconds > 30:
        raise ValueError(
            "Delay must be between 0 and 30 seconds"
        )

    time.sleep(seconds)

    return {
        "delayed_seconds": seconds
    }


def execute_ai_process(
    config: dict,
) -> dict:
    prompt = config.get("prompt")

    if not prompt:
        raise ValueError(
            "AI_PROCESS requires prompt"
        )

    model = config.get(
        "model",
        "gpt-5.6-luna",
    )

    client = OpenAI()

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return {
        "model": model,
        "output": response.output_text,
    }


def execute_step(
    action_type: str,
    config_json: str | None,
) -> dict:
    config = parse_config(
        config_json
    )

    if action_type == "HTTP_REQUEST":
        return execute_http_request(
            config
        )

    if action_type == "DELAY":
        return execute_delay(
            config
        )

    if action_type == "AI_PROCESS":
        return execute_ai_process(
            config
        )

    raise ValueError(
        f"Unsupported action type: {action_type}"
    )