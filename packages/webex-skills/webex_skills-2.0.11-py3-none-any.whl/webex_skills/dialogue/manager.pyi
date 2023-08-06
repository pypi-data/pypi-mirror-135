from ..models.mindmeld import DialogueState as DialogueState, ProcessedQuery as ProcessedQuery
from ..types import (
    DialogueHandler as DialogueHandler,
    DialogueQuery as DialogueQuery,
    QueryHandler as QueryHandler,
    SimpleHandler as SimpleHandler,
)
from .rules import MMDialogueStateRule as MMDialogueStateRule, SimpleDialogueStateRule as SimpleDialogueStateRule
from typing import Any, Dict, Optional, Protocol

class MissingHandler(Exception): ...

NLPRuleMap = Dict[MMDialogueStateRule, QueryHandler]
SimpleRuleMap = Dict[SimpleDialogueStateRule, SimpleHandler]

class DialogueManager(Protocol):
    rules: Dict[Any, Any]

class MMDialogueManager:
    rules: Any
    default_handler: Any
    def __init__(self, rules: Optional[NLPRuleMap] = ..., default_handler: Optional[QueryHandler] = ...) -> None: ...
    def get_handler(self, query: ProcessedQuery, target_state: Optional[str] = ...) -> Optional[QueryHandler]: ...
    def add_rule(
        self,
        *,
        name: Optional[str] = ...,
        default: bool = ...,
        domain: Any | None = ...,
        intent: Any | None = ...,
        entities: Any | None = ...,
        targeted_only: bool = ...
    ): ...
    async def handle(self, query: DialogueQuery, current_state: DialogueState): ...

class SimpleDialogueManager:
    rules: Any
    default_handler: Any
    def __init__(
        self, rules: Optional[SimpleRuleMap] = ..., default_handler: Optional[SimpleHandler] = ...
    ) -> None: ...
    def add_rule(
        self, *, name: Optional[str] = ..., pattern: Optional[str] = ..., default: bool = ..., targeted_only: bool = ...
    ): ...
    def get_handler(self, query: str, target_state: Optional[str] = ...) -> Optional[SimpleHandler]: ...
    async def handle(self, query: str, current_state: DialogueState): ...
