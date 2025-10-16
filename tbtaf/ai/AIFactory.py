from .GenAIInterface import GenAIInterface
from .OllamaGenAIInterface import OllamaGenAIInterface
# In the future, you could add more imports here:
# from .GeminiGenAIInterface import GeminiGenAIInterface

class AIFactory:
    """
    Implements the Factory Method design pattern.
    Its sole responsibility is to create and return an instance of the
    correct AI interface based on a requested type.
    """

    @staticmethod
    def create_ai_interface(interface_type: str) -> GenAIInterface:
        """
        Creates an instance of a GenAIInterface implementation.

        Args:
            interface_type: The type of interface to create (e.g., "ollama").

        Returns:
            An instance of a class that implements GenAIInterface.
        
        Raises:
            ValueError: If the requested interface type is not supported.
        """
        if interface_type.lower() == "ollama":
            return OllamaGenAIInterface()        
        else:
            raise ValueError(f"Unsupported AI interface type: {interface_type}")

