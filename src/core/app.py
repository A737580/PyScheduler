from src.core.command_router import CommandRouter
class App:
    def __init__(self, command_router:CommandRouter):
        self.router = command_router

    def run(self):
        print("Application started. Type 'help' for commands, 'exit' to quit.")
        
        while True:
            try:
                command_line = input("> ").strip()
                
                result = self.router.dispatch(command_line)
                
                if result == "EXIT_COMMAND":
                    print("Exiting application.")
                    break
                elif result: 
                    print(result)
            except KeyboardInterrupt:
                print("Exiting application.")
                break
            except EOFError:
                print("Exiting application.")
                break