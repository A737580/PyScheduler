
from typing import Callable, List, Dict, Tuple

CommandHandlerMethod = Callable[[List[str]], str] 

class CommandRouter:
    def __init__(self):
        self._routes: Dict[str, Tuple[CommandHandlerMethod, str]] = {}

    def register_command(self, command_name: str, handler_method: CommandHandlerMethod, syntax_description: str):
        if command_name in self._routes:
            print(f"Команда: '{command_name}' уже сущестсует и будет пререзаписана.")
        self._routes[command_name] = (handler_method, syntax_description)

    def dispatch(self, command_line: str) -> str:
        parts = command_line.strip().split(maxsplit=1)
        if not parts:
            return "" 

        command_name = parts[0].lower() 
        args_str = parts[1] if len(parts) > 1 else "" 

        if command_name == "help":
            return self._get_help_message()
        elif command_name == "exit":
            return "EXIT_COMMAND" 

        if command_name not in self._routes:
            return f"Неизвестная команда'{command_name}'. Напишите 'help' для просмотра доступных команд."

        handler_method, _ = self._routes[command_name]
        
        try:
            return handler_method(args_str) 
        except Exception as e:
            return f"Ошибка выполнения команды: '{command_name}': {e}"

    def _get_help_message(self) -> str:
        help_msg = "Доступные команды:\n"
        for cmd, (method, desc) in self._routes.items():
            help_msg += f"  {cmd} {desc}\n"
        help_msg += "  help - Показывает команды приложения\n"
        help_msg += "  exit - Выход из приложения"
        return help_msg