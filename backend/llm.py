# connect to llm , give instructions , get info.json


import os
from pydantic import ValidationError
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from models import Info
from prompt import EXTRACTION_SYSTEM_PROMPT, EXTRACT_INFO_TOOL, build_repair_message

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "xai")
LLM_MODEL = os.getenv("LLM_MODEL", "grok-4")

_base_llm = init_chat_model(model=LLM_MODEL, model_provider=LLM_PROVIDER, max_tokens=2000)

# EXTRACT_INFO_TOOL is a flat {"name", "description", "input_schema"} dict -
# the OpenAI-function-style shape LangChain's convert_to_openai_tool expects.
# bind_tools translates this into whatever shape the underlying provider needs.
_llm_with_tool = _base_llm.bind_tools(
    [EXTRACT_INFO_TOOL],
    tool_choice="extract_info",  # force the model to call this exact tool
)


class ExtractionError(Exception):
    """Raised when the LLM output can't be validated against Info, even after retry."""
    pass


def _call_llm(resume_text: str, repair_note: str | None = None) -> dict:
    messages = [
        SystemMessage(content=EXTRACTION_SYSTEM_PROMPT),
        HumanMessage(content=resume_text),
    ]
    if repair_note:
        messages.append(HumanMessage(content=build_repair_message(repair_note)))

    response = _llm_with_tool.invoke(messages)

    for call in response.tool_calls:
        # LangChain normalizes tool_calls to {"name", "args", "id"} across
        # providers, so `call["args"]` is already a parsed dict - no
        # provider-specific JSON parsing needed here.
        if call["name"] == "extract_info":
            return call["args"]

    raise ExtractionError("LLM did not call extract_info tool")


def extract_info_from_resume(resume_text: str, max_retries: int = 1) -> Info:
    """
    Takes raw resume text (already parsed from the uploaded PDF), calls the
    LLM to extract structured fields, and validates the result against Info.
    Retries once with the validation error fed back to the model if the
    first attempt fails pydantic validation.
    """
    last_error = None

    for attempt in range(max_retries + 1):
        repair_note = str(last_error) if last_error else None
        raw_output = _call_llm(resume_text, repair_note=repair_note)

        # ids for embedded projects/certificates aren't LLM-generated -
        # we assign them here rather than asking the model to invent them
        for i, project in enumerate(raw_output.get("projects", [])):
            project["id"] = f"proj_{i}"
        for i, cert in enumerate(raw_output.get("certificates", [])):
            cert["id"] = f"cert_{i}"

        try:
            return Info.model_validate(raw_output)
        except ValidationError as e:
            last_error = e
            continue

    raise ExtractionError(
        f"Failed to extract valid Info after {max_retries + 1} attempts: {last_error}"
    )