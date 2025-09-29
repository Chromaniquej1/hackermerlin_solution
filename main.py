from browser_automation import HackMerlinBot
from prompt_generator import generate_injection_prompt
from utils import extract_password
from config import MAX_TRIES_PER_LEVEL

def main():
    bot = HackMerlinBot()
    current_level = bot.get_current_level()
    history = []
    
    print(f"Starting at Level {current_level}")
    
    while current_level <= 7:  # Aim for 7 levels
        print(f"\n--- Attempting Level {current_level} ---")
        success = False
        for attempt in range(MAX_TRIES_PER_LEVEL):
            prompt = generate_injection_prompt("\n".join(history), current_level)
            print(f"Attempt {attempt + 1}: Sending prompt: {prompt}")
            
            response = bot.send_prompt(prompt)
            print(f"Merlin's response: {response}")
            
            history.append(f"User: {prompt}")
            history.append(f"Merlin: {response}")
            
            password = extract_password(response)
            if password:
                print(f"Password extracted: {password}")
                if bot.enter_password(password):
                    print(f"Level {current_level} completed!")
                    current_level = bot.get_current_level()
                    history = []  # Reset history for new level
                    success = True
                    break
                else:
                    print("Failed to submit password; retrying...")
            else:
                print("No password detected; generating next prompt...")
        
        if not success:
            print(f"Failed to beat Level {current_level} after {MAX_TRIES_PER_LEVEL} tries. Stopping.")
            break
    
    bot.close()
    print(f"Final level reached: {current_level - 1}")

if __name__ == "__main__":
    main()