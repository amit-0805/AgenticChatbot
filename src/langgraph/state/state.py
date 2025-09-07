from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[List, add_messages]