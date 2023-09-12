from typing import Literal, Optional
from chainlit.prompt import Prompt, PromptMessage # type: ignore
from chainlit.playground.providers.openai import ChatOpenAI # type: ignore
from planning_permission.chat.settings import OpenAIStreamSettings, default_settings
from langstream.contrib import OpenAIChatMessage

class MessageChatPrompt:
    """
    Represents a chat prompt message.
    
    Args:
        template (str): The content of the message template.
        role (Optional[Literal['system', 'assistant', 'user', 'function']]): The role of the message. Defaults to None.
        name (Optional[str]): The name of the message. Defaults to None.
    """
    def __init__(self, template: str, role: Optional[Literal['system', 'assistant', 'user', 'function']] = None, name: Optional[str] = None, input_map_fn = lambda input: {}):
        self.content = template
        self.template = template
        self.role = role
        self.name = name

class UserChatPrompt(MessageChatPrompt):
    """
    Represents a chat prompt message from the user.
    
    Args:
        template (str): The content of the message template.
    """
    def __init__(self, template: str):
        super().__init__(template, "user")

class SystemChatPrompt(MessageChatPrompt):
    """
    Represents a chat prompt message from the system.
    
    Args:
        template (str): The content of the message template.
    """
    def __init__(self, template: str):
        super().__init__(template, "system")
        
class FunctionChatPrompt(MessageChatPrompt):
    """
    Represents a chat prompt message from a function.
    
    Args:
        template (str): The content of the message template.
        name (str): The name of the function.
    """
    def __init__(self, template: str, name: str):
        super().__init__(template, "function", name)
        
class AssistantChatPrompt(MessageChatPrompt):
    """
    Represents a chat prompt message from the assistant.
    
    Args:
        template (str): The content of the message template.
    """
    def __init__(self, template: str):
        super().__init__(template, "assistant")
        
class ChatPrompt:
    """
    Represents a chat prompt.
    
    Args:
        name (str): The name of the chat prompt.
        messages (list[MessageChatPrompt], optional): The list of chat prompt messages. Defaults to [].
        settings (OpenAIStreamSettings, optional): The settings for the chat prompt. Defaults to default_settings.
    """
    def __init__(self, name: str, messages: list[MessageChatPrompt] = [], settings: OpenAIStreamSettings = default_settings):
        self.templates = messages
        self.input_vars = {}
        self.settings = settings
        self.name = name
        
    def format_prompt(self, input_vars: dict[str, str]):
        """
        Formats the chat prompt with the given input variables.
        
        Args:
            input_vars (dict[str, str]): The input variables to format the chat prompt with.
        """
        self.input_vars = input_vars
        print(input_vars)
        for template in self.templates:
            template.content = template.template.format(**{**input_vars})
        return self
            
    def to_messages(self) -> list[OpenAIChatMessage]:
        """
        Converts the chat prompt to a list of OpenAIChatMessage objects.
        
        Returns:
            list[OpenAIChatMessage]: The list of OpenAIChatMessage objects.
        """
        return [
            OpenAIChatMessage(content=prompt.content, role=prompt.role, name=prompt.name) # type: ignore
            for prompt in self.templates
        ]
        
    def to_prompt(self) -> Prompt:
        """
        Converts the chat prompt to a Prompt object.
        
        Returns:
            Prompt: The Prompt object.
        """
        return Prompt(
            provider=ChatOpenAI.id,
            inputs=self.input_vars,
            settings={**(self.settings if self.settings else {})},
            messages=[
                PromptMessage(template=prompt.template, formatted=prompt.content, role=prompt.role, name=prompt.name) # type: ignore
                for prompt in self.templates
            ],
        )