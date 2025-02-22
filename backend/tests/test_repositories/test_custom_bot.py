import sys
import unittest

sys.path.insert(0, ".")


from app.repositories.custom_bot import (
    delete_alias_by_id,
    delete_bot_by_id,
    delete_bot_publication,
    find_all_published_bots,
    find_private_bot_by_id,
    find_private_bots_by_user_id,
    find_public_bots_by_ids,
    store_alias,
    store_bot,
    update_alias_last_used_time,
    update_bot,
    update_bot_last_used_time,
    update_bot_publication,
    update_bot_visibility,
    update_knowledge_base_id,
)
from app.repositories.models.custom_bot import (
    ActiveModelsModel,
    AgentModel,
    AgentToolModel,
    BotAliasModel,
    ConversationQuickStarterModel,
    GenerationParamsModel,
    KnowledgeModel,
)
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.repositories.models.custom_bot_kb import (
    AnalyzerParamsModel,
    BedrockKnowledgeBaseModel,
    FixedSizeParamsModel,
    OpenSearchParamsModel,
)
from app.repositories.models.custom_bot_kb import (
    SearchParamsModel as SearchParamsModelKB,
)
from app.usecases.bot import fetch_all_bots_by_user_id
from tests.test_repositories.utils.bot_factory import (
    create_test_private_bot,
    create_test_public_bot,
)


class TestCustomBotRepository(unittest.TestCase):
    def test_store_and_find_bot(self):
        bot = create_test_private_bot(
            "1",
            False,
            "user1",
            published_api_stack_name="TestApiStack",
            published_api_datetime=1627984879,
            published_api_codebuild_id="TestCodeBuildId",
            display_retrieved_chunks=True,
            conversation_quick_starters=[
                ConversationQuickStarterModel(title="QS title", example="QS example")
            ],
            bedrock_knowledge_base=BedrockKnowledgeBaseModel(
                embeddings_model="titan_v2",
                open_search=OpenSearchParamsModel(
                    analyzer=AnalyzerParamsModel(
                        character_filters=["icu_normalizer"],
                        tokenizer="kuromoji_tokenizer",
                        token_filters=["kuromoji_baseform"],
                    )
                ),
                search_params=SearchParamsModelKB(
                    max_results=20,
                    search_type="hybrid",
                ),
                chunking_configuration=FixedSizeParamsModel(
                    chunking_strategy="fixed_size",
                    max_tokens=2000,
                    overlap_percentage=0,
                ),
                parsing_model="anthropic.claude-3-sonnet-v1",
                web_crawling_scope="DEFAULT",
            ),
            bedrock_guardrails=BedrockGuardrailsModel(
                is_guardrail_enabled=True,
                hate_threshold=0,
                insults_threshold=0,
                sexual_threshold=0,
                violence_threshold=0,
                misconduct_threshold=0,
                grounding_threshold=0.0,
                relevance_threshold=0.0,
                guardrail_arn="arn:aws:guardrail",
                guardrail_version="v1",
            ),
        )
        store_bot("user1", bot)

        # Assert bot is stored and reconstructed correctly
        bot = find_private_bot_by_id("user1", "1")
        self.assertEqual(bot.id, "1")
        self.assertEqual(bot.title, "Test Bot")
        self.assertEqual(bot.description, "Test Bot Description")
        self.assertEqual(bot.instruction, "Test Bot Prompt")
        self.assertEqual(bot.create_time, 1627984879.9)
        self.assertEqual(bot.last_used_time, 1627984879.9)
        self.assertEqual(bot.is_pinned, False)

        self.assertEqual(bot.generation_params.max_tokens, 2000)
        self.assertEqual(bot.generation_params.top_k, 250)
        self.assertEqual(bot.generation_params.top_p, 0.999)
        self.assertEqual(bot.generation_params.temperature, 0.6)

        self.assertEqual(bot.knowledge.source_urls, ["https://aws.amazon.com/"])
        self.assertEqual(bot.knowledge.sitemap_urls, ["https://aws.amazon.sitemap.xml"])
        self.assertEqual(bot.knowledge.filenames, ["test.txt"])
        self.assertEqual(bot.knowledge.s3_urls, ["s3://test-user/test-bot/"])
        self.assertEqual(bot.sync_status, "RUNNING")
        self.assertEqual(bot.sync_status_reason, "reason")
        self.assertEqual(bot.sync_last_exec_id, "")
        self.assertEqual(bot.published_api_stack_name, "TestApiStack")
        self.assertEqual(bot.published_api_datetime, 1627984879)
        self.assertEqual(len(bot.conversation_quick_starters), 1)
        self.assertEqual(bot.conversation_quick_starters[0].title, "QS title")
        self.assertEqual(bot.conversation_quick_starters[0].example, "QS example")
        self.assertEqual(bot.bedrock_knowledge_base.embeddings_model, "titan_v2")
        self.assertEqual(
            bot.bedrock_knowledge_base.chunking_configuration.max_tokens, 2000
        )
        self.assertEqual(
            bot.bedrock_knowledge_base.chunking_configuration.overlap_percentage, 0
        )

        self.assertEqual(
            bot.bedrock_knowledge_base.open_search.analyzer.character_filters,
            ["icu_normalizer"],
        )
        self.assertEqual(
            bot.bedrock_knowledge_base.open_search.analyzer.tokenizer,
            "kuromoji_tokenizer",
        )
        self.assertEqual(
            bot.bedrock_knowledge_base.open_search.analyzer.token_filters,
            ["kuromoji_baseform"],
        )
        self.assertEqual(bot.bedrock_knowledge_base.search_params.max_results, 20)
        self.assertEqual(bot.bedrock_knowledge_base.search_params.search_type, "hybrid")
        self.assertEqual(bot.bedrock_guardrails.is_guardrail_enabled, True)
        self.assertEqual(bot.bedrock_guardrails.hate_threshold, 0)
        self.assertEqual(bot.bedrock_guardrails.insults_threshold, 0)
        self.assertEqual(bot.bedrock_guardrails.sexual_threshold, 0)
        self.assertEqual(bot.bedrock_guardrails.violence_threshold, 0)
        self.assertEqual(bot.bedrock_guardrails.misconduct_threshold, 0)
        self.assertEqual(bot.bedrock_guardrails.grounding_threshold, 0.0)
        self.assertEqual(bot.bedrock_guardrails.relevance_threshold, 0.0)
        self.assertEqual(bot.bedrock_guardrails.guardrail_arn, "arn:aws:guardrail")
        self.assertEqual(bot.bedrock_guardrails.guardrail_version, "v1")

        # Assert bot is stored in user1's bot list
        bot = find_private_bots_by_user_id("user1")
        self.assertEqual(len(bot), 1)
        self.assertEqual(bot[0].id, "1")
        self.assertEqual(bot[0].title, "Test Bot")
        self.assertEqual(bot[0].create_time, 1627984879.9)
        self.assertEqual(bot[0].last_used_time, 1627984879.9)
        self.assertEqual(bot[0].is_pinned, False)
        self.assertEqual(bot[0].is_pinned, False)
        self.assertEqual(bot[0].description, "Test Bot Description")
        self.assertEqual(bot[0].is_public, False)

        delete_bot_by_id("user1", "1")
        bot = find_private_bots_by_user_id("user1")
        self.assertEqual(len(bot), 0)

    def test_update_bot_last_used_time(self):
        bot = create_test_private_bot("1", False, "user1")
        store_bot("user1", bot)
        update_bot_last_used_time("user1", "1")

        bot = find_private_bot_by_id("user1", "1")
        self.assertIsNotNone(bot.last_used_time)
        self.assertNotEqual(bot.last_used_time, 1627984879.9)
        self.assertEqual(bot.display_retrieved_chunks, True)

        delete_bot_by_id("user1", "1")

    def test_update_delete_bot_publication(self):
        bot = create_test_private_bot("1", False, "user1")
        store_bot("user1", bot)
        update_bot_publication("user1", "1", "api1", "build1")

        bot = find_private_bot_by_id("user1", "1")
        # NOTE: Stack naming rule: ApiPublishmentStack{published_api_id}.
        # See bedrock-chat-stack.ts > `ApiPublishmentStack`
        self.assertEqual(bot.published_api_stack_name, "ApiPublishmentStackapi1")
        self.assertIsNotNone(bot.published_api_datetime)
        self.assertEqual(bot.published_api_codebuild_id, "build1")

        delete_bot_publication("user1", "1")
        bot = find_private_bot_by_id("user1", "1")
        self.assertIsNone(bot.published_api_stack_name)
        self.assertIsNone(bot.published_api_datetime)
        self.assertIsNone(bot.published_api_codebuild_id)

        delete_bot_by_id("user1", "1")

    def test_update_knowledge_base_id(self):
        bot = create_test_private_bot(
            "1",
            False,
            "user1",
            bedrock_knowledge_base=BedrockKnowledgeBaseModel(
                embeddings_model="titan_v2",
                open_search=OpenSearchParamsModel(
                    analyzer=AnalyzerParamsModel(
                        character_filters=["icu_normalizer"],
                        tokenizer="kuromoji_tokenizer",
                        token_filters=["kuromoji_baseform"],
                    )
                ),
                search_params=SearchParamsModelKB(
                    max_results=20,
                    search_type="hybrid",
                ),
                chunking_configuration=FixedSizeParamsModel(
                    chunking_strategy="fixed_size",
                ),
            ),
        )
        store_bot("user1", bot)
        update_knowledge_base_id("user1", "1", "kb1", ["ds1", "ds2"])
        bot = find_private_bot_by_id("user1", "1")
        self.assertEqual(bot.bedrock_knowledge_base.knowledge_base_id, "kb1")
        self.assertEqual(bot.bedrock_knowledge_base.data_source_ids, ["ds1", "ds2"])
        delete_bot_by_id("user1", "1")

    def test_update_bot(self):
        bot = create_test_private_bot("1", False, "user1")
        store_bot("user1", bot)
        update_bot(
            "user1",
            "1",
            title="Updated Title",
            description="Updated Description",
            instruction="Updated Instruction",
            generation_params=GenerationParamsModel(
                max_tokens=2500,
                top_k=250,
                top_p=0.99,
                temperature=0.2,
                stop_sequences=["Human: ", "Assistant: "],
            ),
            agent=AgentModel(
                tools=[
                    AgentToolModel(
                        name="updated_tool", description="updated description"
                    ),
                ]
            ),
            knowledge=KnowledgeModel(
                source_urls=["https://updated.com/"],
                sitemap_urls=["https://updated.xml"],
                filenames=["updated.txt"],
                s3_urls=["s3://test-user/test-bot/"],
            ),
            sync_status="RUNNING",
            sync_status_reason="reason",
            display_retrieved_chunks=False,
            conversation_quick_starters=[
                ConversationQuickStarterModel(title="QS title", example="QS example")
            ],
            bedrock_knowledge_base=BedrockKnowledgeBaseModel(
                embeddings_model="titan_v2",
                open_search=OpenSearchParamsModel(
                    analyzer=AnalyzerParamsModel(
                        character_filters=["icu_normalizer"],
                        tokenizer="kuromoji_tokenizer",
                        token_filters=["kuromoji_baseform"],
                    )
                ),
                search_params=SearchParamsModelKB(
                    max_results=20,
                    search_type="hybrid",
                ),
                chunking_configuration=FixedSizeParamsModel(
                    chunking_strategy="fixed_size",
                    max_tokens=2500,
                    overlap_percentage=20,
                ),
            ),
            bedrock_guardrails=BedrockGuardrailsModel(
                is_guardrail_enabled=True,
                hate_threshold=1,
                insults_threshold=2,
                sexual_threshold=3,
                violence_threshold=4,
                misconduct_threshold=5,
                grounding_threshold=0.1,
                relevance_threshold=0.2,
                guardrail_arn="arn:aws:guardrail",
                guardrail_version="v1",
            ),
            active_models=ActiveModelsModel(),
        )

        bot = find_private_bot_by_id("user1", "1")
        self.assertEqual(bot.title, "Updated Title")
        self.assertEqual(bot.description, "Updated Description")
        self.assertEqual(bot.instruction, "Updated Instruction")

        self.assertEqual(bot.generation_params.max_tokens, 2500)
        self.assertEqual(bot.generation_params.top_k, 250)
        self.assertEqual(bot.generation_params.top_p, 0.99)
        self.assertEqual(bot.generation_params.temperature, 0.2)

        self.assertEqual(bot.agent.tools[0].name, "updated_tool")
        self.assertEqual(bot.agent.tools[0].description, "updated description")

        self.assertEqual(bot.knowledge.source_urls, ["https://updated.com/"])
        self.assertEqual(bot.knowledge.sitemap_urls, ["https://updated.xml"])
        self.assertEqual(bot.knowledge.filenames, ["updated.txt"])
        self.assertEqual(bot.sync_status, "RUNNING")
        self.assertEqual(bot.sync_status_reason, "reason")
        self.assertEqual(bot.display_retrieved_chunks, False)
        self.assertEqual(len(bot.conversation_quick_starters), 1)
        self.assertEqual(bot.conversation_quick_starters[0].title, "QS title")
        self.assertEqual(bot.conversation_quick_starters[0].example, "QS example")

        self.assertEqual(bot.bedrock_knowledge_base.embeddings_model, "titan_v2")
        self.assertEqual(
            bot.bedrock_knowledge_base.chunking_configuration.max_tokens, 2500
        )
        self.assertEqual(
            bot.bedrock_knowledge_base.chunking_configuration.overlap_percentage, 20
        )
        self.assertEqual(
            bot.bedrock_knowledge_base.open_search.analyzer.character_filters,
            ["icu_normalizer"],
        )
        self.assertEqual(
            bot.bedrock_knowledge_base.open_search.analyzer.tokenizer,
            "kuromoji_tokenizer",
        )
        self.assertEqual(
            bot.bedrock_knowledge_base.open_search.analyzer.token_filters,
            ["kuromoji_baseform"],
        )
        self.assertEqual(bot.bedrock_knowledge_base.search_params.max_results, 20)
        self.assertEqual(bot.bedrock_knowledge_base.search_params.search_type, "hybrid")
        self.assertEqual(bot.bedrock_guardrails.is_guardrail_enabled, True)
        self.assertEqual(bot.bedrock_guardrails.hate_threshold, 1)
        self.assertEqual(bot.bedrock_guardrails.insults_threshold, 2)
        self.assertEqual(bot.bedrock_guardrails.sexual_threshold, 3)
        self.assertEqual(bot.bedrock_guardrails.violence_threshold, 4)
        self.assertEqual(bot.bedrock_guardrails.misconduct_threshold, 5)
        self.assertEqual(bot.bedrock_guardrails.grounding_threshold, 0.1)
        self.assertEqual(bot.bedrock_guardrails.relevance_threshold, 0.2)
        self.assertEqual(bot.bedrock_guardrails.guardrail_arn, "arn:aws:guardrail")
        self.assertEqual(bot.bedrock_guardrails.guardrail_version, "v1")

        delete_bot_by_id("user1", "1")


class TestFindAllBots(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        bot1 = create_test_private_bot("1", is_pinned=True, owner_user_id="user1")
        bot2 = create_test_private_bot("2", is_pinned=True, owner_user_id="user1")
        bot3 = create_test_private_bot("3", is_pinned=False, owner_user_id="user1")
        bot4 = create_test_private_bot("4", is_pinned=False, owner_user_id="user1")
        public_bot1 = create_test_public_bot(
            "public1", is_pinned=True, owner_user_id="user2"
        )
        public_bot2 = create_test_public_bot(
            "public2", is_pinned=True, owner_user_id="user2"
        )

        alias1 = BotAliasModel(
            id="alias1",
            # Different from original. Should be updated after `find_all_bots_by_user_id`
            title="Test Alias",
            description="Test Alias Description",
            original_bot_id="public1",
            last_used_time=1627984879.9,
            create_time=1627984879.9,
            # Pinned
            is_pinned=True,
            sync_status="RUNNING",
            has_knowledge=True,
            has_agent=True,
            conversation_quick_starters=[
                ConversationQuickStarterModel(title="QS title", example="QS example")
            ],
            active_models=ActiveModelsModel(),
        )
        alias2 = BotAliasModel(
            id="alias2",
            title="Test Alias",
            description="Test Alias Description",
            original_bot_id="public2",
            last_used_time=1627984879.9,
            create_time=1627984879.9,
            # Not Pinned
            is_pinned=False,
            sync_status="RUNNING",
            has_knowledge=True,
            has_agent=True,
            conversation_quick_starters=[
                ConversationQuickStarterModel(title="QS title", example="QS example")
            ],
            active_models=ActiveModelsModel(),
        )
        store_bot("user1", bot1)
        store_bot("user1", bot2)
        store_bot("user1", bot3)
        store_bot("user1", bot4)
        store_bot("user2", public_bot1)
        store_bot("user2", public_bot2)
        update_bot_visibility("user2", "public1", True)
        update_bot_visibility("user2", "public2", True)
        store_alias("user1", alias1)
        store_alias("user1", alias2)
        update_bot_publication("user2", "public1", "api1", "build1")

    def tearDown(self) -> None:
        delete_bot_by_id("user1", "1")
        delete_bot_by_id("user1", "2")
        delete_bot_by_id("user1", "3")
        delete_bot_by_id("user1", "4")
        delete_bot_by_id("user2", "public1")
        delete_bot_by_id("user2", "public2")
        delete_alias_by_id("user1", "alias1")
        delete_alias_by_id("user1", "alias2")

    def test_limit(self):
        # Only private bots
        bots = find_private_bots_by_user_id("user1", limit=3)
        self.assertEqual(len(bots), 3)
        fetched_bot_ids = set(bot.id for bot in bots)
        expected_bot_ids = {"1", "2", "3", "4"}
        self.assertTrue(fetched_bot_ids.issubset(expected_bot_ids))

    async def test_find_public_bots_by_ids(self):
        bots = await find_public_bots_by_ids(["public1", "public2", "1", "2"])
        # 2 public bots and 2 private bots
        self.assertEqual(len(bots), 2)

    async def test_find_all_published_bots(self):
        bots, next_token = find_all_published_bots()
        # Bot should not contain unpublished bots
        for bot in bots:
            self.assertIsNotNone(bot.published_api_stack_name)
            self.assertIsNotNone(bot.published_api_datetime)
        # Next token should be None
        self.assertIsNone(next_token)


class TestUpdateBotVisibility(unittest.TestCase):
    def setUp(self) -> None:
        bot1 = create_test_private_bot("1", is_pinned=True, owner_user_id="user1")
        bot2 = create_test_private_bot("2", is_pinned=True, owner_user_id="user1")
        public1 = create_test_public_bot(
            "public1", is_pinned=True, owner_user_id="user2"
        )
        alias1 = BotAliasModel(
            id="4",
            title="Test Alias",
            description="Test Alias Description",
            original_bot_id="public1",
            last_used_time=1627984879.9,
            create_time=1627984879.9,
            is_pinned=True,
            sync_status="RUNNING",
            has_knowledge=True,
            has_agent=True,
            conversation_quick_starters=[
                ConversationQuickStarterModel(title="QS title", example="QS example")
            ],
            active_models=ActiveModelsModel(),
        )
        store_bot("user1", bot1)
        store_bot("user1", bot2)
        store_bot("user2", public1)
        update_bot_visibility("user2", "public1", True)
        store_alias("user1", alias1)

    def tearDown(self) -> None:
        delete_bot_by_id("user1", "1")
        delete_bot_by_id("user1", "2")
        delete_bot_by_id("user2", "public1")
        delete_alias_by_id("user1", "4")

    def test_update_bot_visibility(self):
        # Change original tilte
        update_bot(
            "user2",
            "public1",
            title="Updated Title",
            description="",
            instruction="",
            generation_params=GenerationParamsModel(
                max_tokens=2000,
                top_k=250,
                top_p=0.999,
                temperature=0.6,
                stop_sequences=["Human: ", "Assistant: "],
            ),
            agent=AgentModel(tools=[]),
            knowledge=KnowledgeModel(
                source_urls=[], sitemap_urls=[], filenames=[], s3_urls=[]
            ),
            sync_status="RUNNING",
            sync_status_reason="",
            display_retrieved_chunks=True,
            conversation_quick_starters=[],
            active_models=ActiveModelsModel(),
        )
        bots = fetch_all_bots_by_user_id("user1", limit=3)
        self.assertEqual(len(bots), 3)
        self.assertEqual(bots[0].id, "1")
        self.assertEqual(bots[1].id, "2")
        self.assertEqual(bots[2].id, "public1")
        self.assertEqual(bots[2].title, "Updated Title")
        self.assertEqual(bots[2].available, True)

        # Make private
        update_bot_visibility("user2", "public1", False)
        bots = fetch_all_bots_by_user_id("user1", limit=3)
        self.assertEqual(len(bots), 3)
        self.assertEqual(bots[0].id, "1")
        self.assertEqual(bots[1].id, "2")
        self.assertEqual(bots[2].id, "public1")
        # Public bot is NOT available. But title is still the latest one
        self.assertEqual(bots[2].title, "Updated Title")
        self.assertEqual(bots[2].available, False)


if __name__ == "__main__":
    unittest.main()
