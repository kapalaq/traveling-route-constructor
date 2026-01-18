"""Main application class for the budget planner."""
from wallet.wallet import Wallet
from commands.handlers import CommandFactory
from ui.display import Display
from ui.input_handler import InputHandler


class BudgetPlannerApp:
    """Main application class that orchestrates the budget planner."""
    
    def __init__(self):
        self._wallet = Wallet()
        self._command_factory = CommandFactory(self._wallet)
        self._running = False
    
    def _show_welcome(self):
        """Display welcome message and initial dashboard."""
        print("\n" + "=" * 50)
        print("   Welcome to Budget Planner!")
        print("=" * 50)
        Display.show_help()
        Display.show_dashboard(self._wallet)
    
    def _process_input(self) -> bool:
        """Process user input and return whether to continue."""
        command_str = InputHandler.get_command()
        command = self._command_factory.create_command(command_str)
        
        if command:
            return command.execute()
        else:
            Display.show_error(f"Unknown command: '{command_str}'. Type 'help' for available commands.")
            return True
    
    def run(self):
        """Run the main application loop."""
        self._running = True
        self._show_welcome()
        
        while self._running:
            try:
                self._running = self._process_input()
            except KeyboardInterrupt:
                print()
                Display.show_info("Use 'quit' to exit")
            except EOFError:
                self._running = False
                Display.show_info("Goodbye!")
