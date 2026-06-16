import argparse
import sys

HTML_FILE = 'index.html'

def get_hook(category, amount):
    category_clean = 'BET' if category.lower() == '1v1' else category.upper()
    return f"<!-- {category_clean}_{amount}_HOOK -->"

def add_player(name, category, amount):
    hook = get_hook(category, amount)
    new_entry = f"<li>{name}</li>\n                                {hook}"
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if hook not in content:
        print(f"❌ Error: Hook {hook} not found.")
        return
    
    if f"<li>{name}</li>" in content:
        print(f"⚠️ Warning: {name} is already listed.")
        return

    new_content = content.replace(hook, new_entry)
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ Added: {name} to {category} {amount}")

def remove_player(name, category, amount):
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Target the specific line
    target_line = f"<li>{name}</li>"
    if target_line not in content:
        print(f"❌ Error: {name} not found.")
        return
    
    new_content = content.replace(target_line + "\n                                ", "")
    # Fallback if there was no newline
    new_content = new_content.replace(target_line, "")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"🗑️ Removed: {name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EDN Registration Manager")
    parser.add_argument("action", choices=["add", "remove", "replace"])
    parser.add_argument("name", help="Name of the player")
    parser.add_argument("category", choices=["league", "knockout", "1v1"])
    parser.add_argument("amount", help="Amount (e.g. 100, 150)")
    parser.add_argument("new_name", nargs="?", help="New name (required for replace)")

    args = parser.parse_args()

    if args.action == "add":
        add_player(args.name, args.category, args.amount)
    
    elif args.action == "remove":
        remove_player(args.name, args.category, args.amount)
        
    elif args.action == "replace":
        if not args.new_name:
            print("❌ Error: 'replace' requires a new name.")
        else:
            remove_player(args.name, args.category, args.amount)
            add_player(args.new_name, args.category, args.amount)