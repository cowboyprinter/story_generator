import json
import random
import os

# --- Configuration ---
#  Explicitly set the data path relative to the script's directory.
#  This is the MOST robust way to handle file paths.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Absolute path to the script's directory.
DATA_PATH = os.path.join(SCRIPT_DIR, "data")  #  "data" subdirectory within the script's directory.
CHARACTER_FILE = os.path.join(DATA_PATH, "characters.json")
SETTING_FILE = os.path.join(DATA_PATH, "settings.json")
EVENT_FILE = os.path.join(DATA_PATH, "events.json")
TEMPLATE_FILE = os.path.join(DATA_PATH, "story_templates.json")

# --- Helper Functions ---
def load_json_data(filepath):
    """Loads data from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not data:
            print(f"Warning: No data found in {filepath}")
            return []
        return data
    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return []

def get_random_element(data_list):
    """Selects a random element from a list."""
    if not data_list:
        return None
    return random.choice(data_list)

# --- Main Story Generation Logic ---
def generate_story_snippet():
    """Generates a single story snippet based on templates and data."""
    
    # Load all necessary data
    characters = load_json_data(CHARACTER_FILE)
    settings = load_json_data(SETTING_FILE)
    events = load_json_data(EVENT_FILE)
    story_templates = load_json_data(TEMPLATE_FILE)

    # Ensure all data components are available
    if not all([characters, settings, events, story_templates]):
        return "Error: Missing essential data. Please check your JSON files."

    # Select random components
    character = get_random_element(characters)
    setting = get_random_element(settings)
    event = get_random_element(events)
    template = get_random_element(story_templates)

    if not all([character, setting, event, template]):
        return "Error: Failed to select one or more story components. Check data integrity."

    # Prepare data for template filling
    # Using .get() with default values to prevent KeyErrors if a field is missing
    story_data = {
        "character_name": character.get("name", "A mysterious figure"),
        "character_type": character.get("type", "of unknown origin"),
        "character_trait": character.get("trait", "a peculiar disposition"),
        "character_goal": character.get("goal", "an unknown objective"),
        "character_quote": character.get("quote", "..."),
        "setting_name": setting.get("name", "A desolate place"),
        "setting_description": setting.get("description", "lost to time"),
        "setting_feature": setting.get("feature", "a strange landmark"),
        "setting_atmosphere": setting.get("atmosphere", "an unsettling silence"),
        "event_type": event.get("type", "A peculiar incident"),
        "event_action_present": event.get("action_present", "causes"),
        "event_action_past": event.get("action_past", "caused"),
        "event_object_catalyst": event.get("object_catalyst", "something strange"),
        "event_consequence": event.get("consequence", "unforeseen results")
    }

    # Fill the template
    try:
        snippet = template.format(**story_data)
        return snippet
    except KeyError as e:
        return f"Error: Template formatting error. Missing key: {e}. Check your template and JSON data fields."
    except Exception as e:
        return f"An unexpected error occurred during template formatting: {e}"

# --- Main Execution ---
if __name__ == "__main__":
    print("--- The Cowboy Printer Daily - Fresh Off The Data Press! ---\n")
    
    num_stories = 3 # Generate 3 news items
    for i in range(num_stories):
        story = generate_story_snippet()
        print(f"Story #{i+1}:\n{story}\n")
        print("----------------------------------------------------------\n")

    print("To generate new content, simply run this script again!")
    print("You can expand the .json files with more characters, settings, events, and templates.")
