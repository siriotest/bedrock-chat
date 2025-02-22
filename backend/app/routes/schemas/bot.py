from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Type, get_args

from app.routes.schemas.base import BaseSchema
from app.routes.schemas.bot_guardrails import (
    BedrockGuardrailsInput,
    BedrockGuardrailsOutput,
)
from app.routes.schemas.bot_kb import (
    BedrockKnowledgeBaseInput,
    BedrockKnowledgeBaseOutput,
)
from app.routes.schemas.conversation import type_model_name
from pydantic import Field, create_model, validator

if TYPE_CHECKING:
    from app.repositories.models.custom_bot import BotModel

# Knowledge sync status type
# NOTE: `ORIGINAL_NOT_FOUND` is used when the original bot is removed.
type_sync_status = Literal[
    "QUEUED",
    "KNOWLEDGE_BASE_STACK_CREATED",
    "RUNNING",
    "SUCCEEDED",
    "FAILED",
    "ORIGINAL_NOT_FOUND",
]


def _create_model_activate_input(model_names: List[str]) -> Type[BaseSchema]:
    fields: Dict[str, Any] = {
        name.replace("-", "_").replace(".", "_"): (bool, True) for name in model_names
    }
    return create_model("ActiveModelsInput", **fields, __base__=BaseSchema)


ActiveModelsInput = _create_model_activate_input(list(get_args(type_model_name)))


def create_model_activate_output(model_names: List[str]) -> Type[BaseSchema]:
    fields: Dict[str, Any] = {
        name.replace("-", "_").replace(".", "_"): (bool, True) for name in model_names
    }
    return create_model("ActiveModelsOutput", **fields, __base__=BaseSchema)


ActiveModelsOutput = create_model_activate_output(list(get_args(type_model_name)))


class GenerationParams(BaseSchema):
    max_tokens: int
    top_k: int
    top_p: float
    temperature: float
    stop_sequences: list[str]


class AgentTool(BaseSchema):
    name: str
    description: str


class Agent(BaseSchema):
    tools: list[AgentTool]


class AgentInput(BaseSchema):
    tools: list[str] = Field(..., description="List of tool names")


class Knowledge(BaseSchema):
    source_urls: list[str]
    sitemap_urls: list[str]
    filenames: list[str]
    s3_urls: list[str]

    @validator("s3_urls", each_item=True)
    def validate_s3_url(cls, v):
        if not v.startswith("s3://"):
            raise ValueError(f"Invalid S3 URL format: {v}")

        url_parts = v.replace("s3://", "").split("/")
        if len(url_parts) < 1:
            raise ValueError(f"Invalid S3 URL format: {v}")

        bucket_name = url_parts.pop(0)
        prefix = "/".join(url_parts)

        if not bucket_name:
            raise ValueError(f"Invalid S3 URL format: {v}")

        if not v.endswith("/"):
            raise ValueError(f"Invalid S3 URL format (must end with a '/'): {v}")

        return v


class KnowledgeDiffInput(BaseSchema):
    source_urls: list[str]
    sitemap_urls: list[str]
    s3_urls: list[str]
    added_filenames: list[str]
    deleted_filenames: list[str]
    unchanged_filenames: list[str]


class ConversationQuickStarter(BaseSchema):
    title: str
    example: str


class BotInput(BaseSchema):
    id: str
    title: str
    instruction: str
    description: str | None
    generation_params: GenerationParams | None
    agent: Optional[AgentInput] = None
    knowledge: Knowledge | None
    display_retrieved_chunks: bool
    conversation_quick_starters: list[ConversationQuickStarter] | None
    bedrock_knowledge_base: BedrockKnowledgeBaseInput | None = None
    bedrock_guardrails: BedrockGuardrailsInput | None = None
    active_models: ActiveModelsInput  # type: ignore


class BotModifyInput(BaseSchema):
    title: str
    instruction: str
    description: str | None
    generation_params: GenerationParams | None
    agent: Optional[AgentInput] = None
    knowledge: KnowledgeDiffInput | None
    display_retrieved_chunks: bool
    conversation_quick_starters: list[ConversationQuickStarter] | None
    bedrock_knowledge_base: BedrockKnowledgeBaseInput | None = None
    bedrock_guardrails: BedrockGuardrailsInput | None = None
    active_models: ActiveModelsInput  # type: ignore

    def _has_update_files(self) -> bool:
        return self.knowledge is not None and (
            len(self.knowledge.added_filenames) > 0
            or len(self.knowledge.deleted_filenames) > 0
        )

    def _has_update_source_urls(self, current_bot_model: BotModel) -> bool:
        return self.knowledge is not None and (
            len(self.knowledge.source_urls) > 0
            and (
                set(self.knowledge.source_urls)
                != set(current_bot_model.knowledge.source_urls)
            )
        )

    def _is_crawling_scope_modified(self, current_bot_model: BotModel) -> bool:
        if (
            self.bedrock_knowledge_base is None
            or current_bot_model.bedrock_knowledge_base is None
        ):
            return False
        return (
            self.bedrock_knowledge_base.web_crawling_scope
            != current_bot_model.bedrock_knowledge_base.web_crawling_scope
        )

    def _is_crawling_filters_modified(self, current_bot_model: BotModel) -> bool:
        if (
            self.bedrock_knowledge_base is None
            or current_bot_model.bedrock_knowledge_base is None
            or self.bedrock_knowledge_base.web_crawling_filters is None
            or current_bot_model.bedrock_knowledge_base.web_crawling_filters is None
        ):
            return False
        return set(
            self.bedrock_knowledge_base.web_crawling_filters.exclude_patterns
        ) != set(
            current_bot_model.bedrock_knowledge_base.web_crawling_filters.exclude_patterns
        ) or set(
            self.bedrock_knowledge_base.web_crawling_filters.include_patterns
        ) != set(
            current_bot_model.bedrock_knowledge_base.web_crawling_filters.include_patterns
        )

    def is_guardrails_update_required(self, current_bot_model: BotModel) -> bool:
        # Check if self.bedrock_guardrails is None
        if not self.bedrock_guardrails:
            return False

        # Check if guardrails are enabled or any of the settings have changed
        if self.bedrock_guardrails.is_guardrail_enabled == True or (
            current_bot_model.bedrock_guardrails
            and (
                self.bedrock_guardrails.is_guardrail_enabled
                != current_bot_model.bedrock_guardrails.is_guardrail_enabled
                or self.bedrock_guardrails.hate_threshold
                != current_bot_model.bedrock_guardrails.hate_threshold
                or self.bedrock_guardrails.insults_threshold
                != current_bot_model.bedrock_guardrails.insults_threshold
                or self.bedrock_guardrails.sexual_threshold
                != current_bot_model.bedrock_guardrails.sexual_threshold
                or self.bedrock_guardrails.grounding_threshold
                != current_bot_model.bedrock_guardrails.grounding_threshold
                or self.bedrock_guardrails.relevance_threshold
                != current_bot_model.bedrock_guardrails.relevance_threshold
            )
        ):
            return True

        # If none of the conditions above are met, guardrails are not required
        return False

    def is_embedding_required(self, current_bot_model: BotModel) -> bool:
        if self._has_update_files():
            return True

        if self._has_update_source_urls(current_bot_model):
            return True

        if self._is_crawling_scope_modified(current_bot_model):
            return True

        if self._is_crawling_filters_modified(current_bot_model):
            return True

        if self.knowledge is not None and current_bot_model.has_knowledge():
            if (
                set(self.knowledge.source_urls)
                == set(current_bot_model.knowledge.source_urls)
                and set(self.knowledge.sitemap_urls)
                == set(current_bot_model.knowledge.sitemap_urls)
                and set(self.knowledge.s3_urls)
                == set(current_bot_model.knowledge.s3_urls)
            ):
                pass
            else:
                return True

        return False


class BotModifyOutput(BaseSchema):
    id: str
    title: str
    instruction: str
    description: str
    generation_params: GenerationParams
    agent: Agent
    knowledge: Knowledge
    conversation_quick_starters: list[ConversationQuickStarter]
    bedrock_knowledge_base: BedrockKnowledgeBaseOutput | None
    bedrock_guardrails: BedrockGuardrailsOutput | None
    active_models: ActiveModelsOutput  # type: ignore


class BotOutput(BaseSchema):
    id: str
    title: str
    description: str
    instruction: str
    create_time: float
    last_used_time: float
    is_public: bool
    is_pinned: bool
    # Whether the bot is owned by the user
    owned: bool
    generation_params: GenerationParams
    agent: Agent
    knowledge: Knowledge
    sync_status: type_sync_status
    sync_status_reason: str
    sync_last_exec_id: str
    display_retrieved_chunks: bool
    conversation_quick_starters: list[ConversationQuickStarter]
    bedrock_knowledge_base: BedrockKnowledgeBaseOutput | None
    bedrock_guardrails: BedrockGuardrailsOutput | None
    active_models: ActiveModelsOutput  # type: ignore


class BotMetaOutput(BaseSchema):
    id: str
    title: str
    description: str
    create_time: float
    last_used_time: float
    is_pinned: bool
    is_public: bool
    owned: bool
    # Whether the bot is available or not.
    # This can be `False` if the bot is not owned by the user and original bot is removed.
    available: bool
    sync_status: type_sync_status


class BotSummaryOutput(BaseSchema):
    id: str
    title: str
    description: str
    create_time: float
    last_used_time: float
    is_pinned: bool
    is_public: bool
    has_agent: bool
    owned: bool
    sync_status: type_sync_status
    has_knowledge: bool
    conversation_quick_starters: list[ConversationQuickStarter]
    active_models: ActiveModelsOutput  # type: ignore


class BotSwitchVisibilityInput(BaseSchema):
    to_public: bool


class BotPinnedInput(BaseSchema):
    pinned: bool


class BotPresignedUrlOutput(BaseSchema):
    url: str
