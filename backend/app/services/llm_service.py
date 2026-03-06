from typing import AsyncGenerator

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session

from app.config import settings
from app.services.analytics_service import AnalyticsService


class LLMService:
    """Service for LLM-powered chat with fitness data analysis."""

    def __init__(self, db: Session, user_id: int) -> None:
        self.db = db
        self.user_id = user_id
        self.analytics_service = AnalyticsService(db=db)
        self._setup_llm()

    def _setup_llm(self) -> None:
        """Initialize LangChain components."""
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0,
            streaming=True,
            api_key=settings.openai_api_key,
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )

        self.tools = self._create_tools()

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful fitness data analyst. You have access to the user's "
                "fitness activities data from Strava and Garmin. Answer questions about "
                "their training, provide insights, and create visualizations when appropriate. "
                "Always provide specific data-driven insights when possible.",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            return_intermediate_steps=True,
        )

    def _create_tools(self) -> list[Tool]:
        """Create LangChain tools for data analysis."""

        def get_activity_summary(query: str = "") -> str:
            """Get a summary of fitness activities."""
            import asyncio
            summary = asyncio.run(
                self.analytics_service.get_summary(user_id=self.user_id)
            )
            return str(summary)

        def query_activities(sql_query: str) -> str:
            """Execute a SQL query on the activities database."""
            import asyncio
            result = asyncio.run(
                self.analytics_service.execute_query(
                    query=sql_query, user_id=self.user_id
                )
            )
            return str(result)

        return [
            Tool(
                name="get_activity_summary",
                description=(
                    "Get a summary of fitness activities including total distance, "
                    "duration, and recent activities. Use this for general overviews."
                ),
                func=get_activity_summary,
            ),
            Tool(
                name="query_activities",
                description=(
                    "Query fitness activities with natural language or SQL-like queries. "
                    "Use this for specific data lookups like heart rate, pace, etc."
                ),
                func=query_activities,
            ),
        ]

    async def process_message(self, message: str) -> dict:
        """Process a chat message and return response."""
        try:
            result = await self.agent_executor.ainvoke({"input": message})
            return {
                "text": result.get("output", ""),
                "chart_data": None,
            }
        except Exception as e:
            return {
                "text": f"I encountered an error processing your request: {str(e)}",
                "chart_data": None,
            }

    async def stream_message(self, message: str) -> AsyncGenerator[str, None]:
        """Stream a chat response."""
        try:
            async for event in self.agent_executor.astream_events(
                {"input": message}, version="v1"
            ):
                if event["event"] == "on_llm_stream":
                    chunk = event["data"].get("chunk", "")
                    if hasattr(chunk, "content") and chunk.content:
                        yield chunk.content
        except Exception as e:
            yield f"Error: {str(e)}"
