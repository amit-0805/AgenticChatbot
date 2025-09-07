from langgraph.graph import StateGraph, START, END
from src.langgraph.state.state import State
from src.langgraph.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph.tools.search_tool import create_tool_node, get_tools
from langgraph.prebuilt import tools_condition
from src.langgraph.nodes.chatbot_with_tool import ChatbotWithTool
from src.langgraph.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_build_graph(self):
        ## Define tool and toolNode
        tools = get_tools()
        tool_node = create_tool_node(tools)
        llm = self.llm

        obj_chatbot_with_tool = ChatbotWithTool(llm)
        chatbot_node = obj_chatbot_with_tool.create_chatbot(tools)

        #nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_builder_graph(self):

        obj_ai_news = AINewsNode(self.llm)



        self.graph_builder.add_node("fetch_news", obj_ai_news.fetch_news)
        self.graph_builder.add_node("Summarize_news", obj_ai_news.summarize_news)
        self.graph_builder.add_node("save_results", obj_ai_news.save_result)

        # self.graph_builder.add_edge(START, "fetch_news") write it like below
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "Summarize_news")
        self.graph_builder.add_edge("Summarize_news", "save_results")
        self.graph_builder.add_edge("save_results", END)

    def setup_graph(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Web":
            self.chatbot_with_tools_build_graph()
        if usecase == "AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()