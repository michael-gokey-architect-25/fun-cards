import json
import random
import os
import time
from datetime import datetime

class FlashcardsApp:
    def __init__(self):
        self.flashcard_sets = {}
        self.current_set = None
        self.stats = {
            "correct": 0,
            "incorrect": 0,
            "cards_studied": 0,
            "study_time": 0
        }
    
    def load_flashcards(self, filename):
        """Load flashcards from a JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                set_name = data.get('title', os.path.basename(filename))
                self.flashcard_sets[set_name] = data
                print(f"Loaded {len(data['cards'])} flashcards from '{set_name}'")
                return set_name
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: '{filename}' is not a valid JSON file.")
            return None
    
    def save_flashcards(self, set_name, filename):
        """Save the current flashcard set to a JSON file."""
        if set_name in self.flashcard_sets:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.flashcard_sets[set_name], file, indent=2)
            print(f"Saved flashcard set '{set_name}' to {filename}")
        else:
            print(f"Error: Flashcard set '{set_name}' not found.")

    def create_sample_flashcards(self):
        """Create a sample flashcard set."""
        sample_data = {
            "title": "General Knowledge Flashcards",
            "description": "A set of general knowledge flashcards for practice",
            "cards": [
                {
                    "id": 1,
                    "front": "What is the capital of France?",
                    "back": "Paris",
                    "category": "Geography",
                    "difficulty": "easy"
                },
                {
                    "id": 2,
                    "front": "Who wrote 'Romeo and Juliet'?",
                    "back": "William Shakespeare",
                    "category": "Literature",
                    "difficulty": "easy"
                },
                {
                    "id": 3,
                    "front": "What is the chemical symbol for gold?",
                    "back": "Au",
                    "category": "Science",
                    "difficulty": "medium"
                },
                {
                    "id": 4,
                    "front": "What is the largest planet in our solar system?",
                    "back": "Jupiter",
                    "category": "Astronomy",
                    "difficulty": "easy"
                },
                {
                    "id": 5,
                    "front": "What is the square root of 144?",
                    "back": "12",
                    "category": "Mathematics",
                    "difficulty": "medium"
                }
            ],
            "metadata": {
                "version": "1.0",
                "created": datetime.now().strftime("%Y-%m-%d"),
                "totalCards": 5,
                "categories": ["Geography", "Literature", "Science", "Astronomy", "Mathematics"]
            }
        }
        
        set_name = sample_data["title"]
        self.flashcard_sets[set_name] = sample_data
        print(f"Created sample flashcard set: '{set_name}'")
        return set_name
    
    def select_flashcard_set(self, set_name):
        """Select a flashcard set to study."""
        if set_name in self.flashcard_sets:
            self.current_set = set_name
            print(f"Selected flashcard set: '{set_name}'")
            return True
        else:
            print(f"Error: Flashcard set '{set_name}' not found.")
            return False
    
    def list_flashcard_sets(self):
        """List all available flashcard sets."""
        if not self.flashcard_sets:
            print("No flashcard sets available.")
            return
        
        print("\nAvailable Flashcard Sets:")
        for i, set_name in enumerate(self.flashcard_sets.keys(), 1):
            card_count = len(self.flashcard_sets[set_name]["cards"])
            print(f"{i}. {set_name} ({card_count} cards)")
    
    def filter_cards(self, category=None, difficulty=None):
        """Filter cards by category and/or difficulty."""
        if not self.current_set:
            print("No flashcard set selected.")
            return []
        
        cards = self.flashcard_sets[self.current_set]["cards"]
        
        if category:
            cards = [card for card in cards if card.get("category") == category]
        
        if difficulty:
            cards = [card for card in cards if card.get("difficulty") == difficulty]
        
        return cards
    
    def list_categories(self):
        """List all categories in the current set."""
        if not self.current_set:
            print("No flashcard set selected.")
            return []
        
        categories = set()
        for card in self.flashcard_sets[self.current_set]["cards"]:
            if "category" in card:
                categories.add(card["category"])
        
        return sorted(list(categories))
    
    def practice_flashcards(self, cards=None, random_order=True):
        """Practice flashcards in the current set."""
        if not self.current_set:
            print("No flashcard set selected.")
            return
        
        if cards is None:
            cards = self.flashcard_sets[self.current_set]["cards"]
        
        if not cards:
            print("No cards available to practice with the current filters.")
            return
        
        if random_order:
            random.shuffle(cards)
        
        print(f"\nStarting practice session with {len(cards)} cards...")
        print("Press Enter to flip the card, type 'q' to quit the session.")
        
        start_time = time.time()
        cards_studied = 0
        
        for card in cards:
            print("\n" + "="*50)
            print(f"Card {cards_studied + 1} of {len(cards)}")
            
            # Show the front
            print("\nFront:", card["front"])
            
            user_input = input("\nPress Enter to flip or 'q' to quit: ")
            if user_input.lower() == 'q':
                break
            
            # Show the back
            print("\nBack:", card["back"])
            
            # Ask if they got it right
            while True:
                response = input("\nDid you get it right? (y/n): ").lower()
                if response == 'y':
                    self.stats["correct"] += 1
                    break
                elif response == 'n':
                    self.stats["incorrect"] += 1
                    break
                else:
                    print("Please enter 'y' or 'n'.")
            
            cards_studied += 1
        
        self.stats["cards_studied"] += cards_studied
        self.stats["study_time"] += (time.time() - start_time)
        
        print("\nPractice session ended.")
        self.show_session_stats(cards_studied, time.time() - start_time)
    
    def show_session_stats(self, cards_studied, study_time):
        """Show statistics for the current session."""
        if cards_studied == 0:
            print("No cards were studied in this session.")
            return
        
        print("\nSession Statistics:")
        print(f"Cards studied: {cards_studied}")
        print(f"Time spent: {int(study_time//60)} min {int(study_time%60)} sec")
        
        session_correct = self.stats["correct"]
        session_incorrect = self.stats["incorrect"]
        total_answered = session_correct + session_incorrect
        
        if total_answered > 0:
            accuracy = (session_correct / total_answered) * 100
            print(f"Correct answers: {session_correct}")
            print(f"Incorrect answers: {session_incorrect}")
            print(f"Accuracy: {accuracy:.1f}%")
    
    def show_overall_stats(self):
        """Show overall statistics."""
        print("\nOverall Statistics:")
        print(f"Total cards studied: {self.stats['cards_studied']}")
        
        total_time = self.stats["study_time"]
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)
        print(f"Total study time: {minutes} min {seconds} sec")
        
        total_answered = self.stats["correct"] + self.stats["incorrect"]
        if total_answered > 0:
            accuracy = (self.stats["correct"] / total_answered) * 100
            print(f"Overall accuracy: {accuracy:.1f}%")
    
    def run(self):
        """Run the main application loop."""
        print("\nWelcome to the Flashcards App!")
        
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (1-9): ")
            
            if choice == '1':
                # Create sample flashcards
                set_name = self.create_sample_flashcards()
                self.select_flashcard_set(set_name)
            
            elif choice == '2':
                # Load flashcards from file
                filename = input("Enter the JSON file path: ")
                set_name = self.load_flashcards(filename)
                if set_name:
                    self.select_flashcard_set(set_name)
            
            elif choice == '3':
                # List available flashcard sets
                self.list_flashcard_sets()
                if self.flashcard_sets:
                    try:
                        index = int(input("\nSelect a set by number (or 0 to cancel): "))
                        if index == 0:
                            continue
                        
                        set_names = list(self.flashcard_sets.keys())
                        if 1 <= index <= len(set_names):
                            self.select_flashcard_set(set_names[index-1])
                        else:
                            print("Invalid selection.")
                    except ValueError:
                        print("Please enter a valid number.")
            
            elif choice == '4':
                # Practice all flashcards
                if self.current_set:
                    self.practice_flashcards()
                else:
                    print("No flashcard set selected.")
            
            elif choice == '5':
                # Practice by category
                if self.current_set:
                    categories = self.list_categories()
                    if categories:
                        print("\nAvailable categories:")
                        for i, category in enumerate(categories, 1):
                            print(f"{i}. {category}")
                        
                        try:
                            index = int(input("\nSelect a category by number (or 0 to cancel): "))
                            if index == 0:
                                continue
                            
                            if 1 <= index <= len(categories):
                                selected_category = categories[index-1]
                                cards = self.filter_cards(category=selected_category)
                                self.practice_flashcards(cards)
                            else:
                                print("Invalid selection.")
                        except ValueError:
                            print("Please enter a valid number.")
                    else:
                        print("No categories available in the current set.")
                else:
                    print("No flashcard set selected.")
            
            elif choice == '6':
                # Practice by difficulty
                if self.current_set:
                    difficulties = ["easy", "medium", "hard"]
                    print("\nDifficulty levels:")
                    for i, diff in enumerate(difficulties, 1):
                        print(f"{i}. {diff}")
                    
                    try:
                        index = int(input("\nSelect a difficulty by number (or 0 to cancel): "))
                        if index == 0:
                            continue
                        
                        if 1 <= index <= len(difficulties):
                            selected_difficulty = difficulties[index-1]
                            cards = self.filter_cards(difficulty=selected_difficulty)
                            self.practice_flashcards(cards)
                        else:
                            print("Invalid selection.")
                    except ValueError:
                        print("Please enter a valid number.")
                else:
                    print("No flashcard set selected.")
            
            elif choice == '7':
                # Save current set to file
                if self.current_set:
                    filename = input("Enter filename to save (e.g., flashcards.json): ")
                    self.save_flashcards(self.current_set, filename)
                else:
                    print("No flashcard set selected.")
            
            elif choice == '8':
                # Show statistics
                self.show_overall_stats()
            
            elif choice == '9':
                # Exit
                print("Thank you for using the Flashcards App. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def show_menu(self):
        """Display the main menu."""
        current_set_info = ""
        if self.current_set:
            card_count = len(self.flashcard_sets[self.current_set]["cards"])
            current_set_info = f" (Current set: '{self.current_set}' with {card_count} cards)"
        
        print("\n" + "="*50)
        print(f"FLASHCARDS APP MENU{current_set_info}")
        print("="*50)
        print("1. Create sample flashcards")
        print("2. Load flashcards from file")
        print("3. Select flashcard set")
        print("4. Practice all flashcards")
        print("5. Practice by category")
        print("6. Practice by difficulty")
        print("7. Save current set to file")
        print("8. Show statistics")
        print("9. Exit")


if __name__ == "__main__":
    app = FlashcardsApp()
    app.run()
