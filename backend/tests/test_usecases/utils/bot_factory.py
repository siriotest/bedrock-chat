import sys
import unittest

sys.path.append(".")

from app.agents.tools.internet_search import internet_search_tool
from app.repositories.models.custom_bot import (
    ActiveModelsModel,
    AgentModel,
    AgentToolModel,
    BotAliasModel,
    BotModel,
    GenerationParamsModel,
    KnowledgeModel,
)


def create_test_private_bot(
    id,
    is_pinned,
    owner_user_id,
    instruction="Test Bot Prompt",
    sync_status="RUNNING",
    include_internet_tool=False,
    set_dummy_knowledge=True,
    bedrock_knowledge_base=None,
    bedrock_guardrails=None,
):
    return BotModel(
        id=id,
        title="Test Bot",
        description="Test Bot Description",
        instruction=instruction,
        create_time=1627984879.9,
        last_used_time=1627984879.9,
        # Pinned
        is_pinned=is_pinned,
        public_bot_id=None,
        owner_user_id=owner_user_id,
        generation_params=GenerationParamsModel(
            max_tokens=2000,
            top_k=250,
            top_p=0.999,
            temperature=0.6,
            stop_sequences=["Human: ", "Assistant: "],
        ),
        agent=AgentModel(
            tools=(
                [
                    AgentToolModel(
                        name=internet_search_tool.name,
                        description=internet_search_tool.description,
                    )
                ]
                if include_internet_tool
                else []
            )
        ),
        knowledge=(
            KnowledgeModel(
                source_urls=["https://aws.amazon.com/"],
                sitemap_urls=["https://aws.amazon.sitemap.xml"],
                filenames=["test.txt"],
                s3_urls=["s3://example/doc/"],
            )
            if set_dummy_knowledge
            else KnowledgeModel(
                source_urls=[], sitemap_urls=[], filenames=[], s3_urls=[]
            )
        ),
        sync_status=sync_status,
        sync_status_reason="reason",
        sync_last_exec_id="",
        published_api_stack_name=None,
        published_api_datetime=None,
        published_api_codebuild_id=None,
        display_retrieved_chunks=True,
        conversation_quick_starters=[],
        bedrock_knowledge_base=bedrock_knowledge_base,
        bedrock_guardrails=bedrock_guardrails,
        active_models=ActiveModelsModel(),
    )


def create_test_public_bot(
    id,
    is_pinned,
    owner_user_id,
    public_bot_id=None,
    instruction="Test Public Bot Prompt",
    bedrock_knowledge_base=None,
    bedrock_guardrails=None,
):
    return BotModel(
        id=id,
        title="Test Public Bot",
        description="Test Public Bot Description",
        instruction=instruction,
        create_time=1627984879.9,
        last_used_time=1627984879.9,
        is_pinned=is_pinned,
        public_bot_id=public_bot_id,
        owner_user_id=owner_user_id,
        generation_params=GenerationParamsModel(
            max_tokens=2000,
            top_k=250,
            top_p=0.999,
            temperature=0.6,
            stop_sequences=["Human: ", "Assistant: "],
        ),
        agent=AgentModel(
            # tools=[
            #     AgentToolModel(
            #         name=internet_search_tool.name,
            #         description=internet_search_tool.description,
            #     )
            # ]
            tools=[]
        ),
        knowledge=KnowledgeModel(
            source_urls=["https://aws.amazon.com/"],
            sitemap_urls=["https://aws.amazon.sitemap.xml"],
            filenames=["test.txt"],
            s3_urls=["s3://example/doc/"],
        ),
        sync_status="RUNNING",
        sync_status_reason="reason",
        sync_last_exec_id="",
        published_api_stack_name=None,
        published_api_datetime=None,
        published_api_codebuild_id=None,
        display_retrieved_chunks=True,
        conversation_quick_starters=[],
        bedrock_knowledge_base=bedrock_knowledge_base,
        bedrock_guardrails=bedrock_guardrails,
        active_models=ActiveModelsModel(),
    )


def create_test_bot_alias(id, original_bot_id, is_pinned):
    return BotAliasModel(
        id=id,
        # Different from original. Should be updated after `fetch_all_bots_by_user_id`
        title="Test Alias",
        description="Test Alias Description",
        original_bot_id=original_bot_id,
        last_used_time=1627984879.9,
        create_time=1627984879.9,
        is_pinned=is_pinned,
        sync_status="RUNNING",
        has_knowledge=True,
        has_agent=False,
        conversation_quick_starters=[],
        active_models=ActiveModelsModel(),
    )


create_test_instruction_template = (
    lambda condition: f"いついかなる時も、{condition}返答してください。日本語以外の言語は認めません。"
)


if __name__ == "__main__":
    unittest.main()
