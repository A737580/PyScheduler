from handlers.scheduler import Scheduler

class App:
    def __init__(self, scheduler_instance: Scheduler):
        self.scheduler = scheduler_instance

    def run(self):
        print("Application started. Type 'help' for commands, 'exit' to quit.")
        
        while True:
            command_line = input("> ").strip()
            
            if command_line == "exit":
                print("Exiting application.")
                break
            elif command_line == "help":
                print("Commands: ")
                print("  add <name> <date> - Add a new event")
                print("  list - List all events")
                print("  exit - Exit the application")
            elif command_line.startswith("add "):
                parts = command_line.split(" ", 2)
                if len(parts) == 3:
                    name = parts[1]
                    date = parts[2]
                    self.scheduler.add_event(name, date)
                    print(f"Event '{name}' on '{date}' added.")
                else:
                    print("Invalid 'add' command format. Usage: add <name> <date>")
            elif command_line == "list":
                events = self.scheduler.list_events()
                if events:
                    print("Current events:")
                    for event in events:
                        print(f"- Name: {event.get('name')}, Date: {event.get('date')}")
                else:
                    print("No events found.")
            else:
                print(f"Unknown command: '{command_line}'. Type 'help' for commands.")