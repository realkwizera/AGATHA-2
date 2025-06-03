import subprocess
import platform

class ActionMapper:
    def execute_action(self, action_name):
        # Placeholder: map to real system commands
        if action_name == 'open_notepad':
            if platform.system() == 'Windows':
                subprocess.Popen(['notepad'])
            elif platform.system() == 'Linux':
                subprocess.Popen(['gedit'])
        elif action_name == 'increase_volume':
            # Add volume control code for your OS
            pass
        else:
            print(f"No mapping found for action: {action_name}")
