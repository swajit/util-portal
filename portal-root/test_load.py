import sys
import os

# Add portal-root to sys.path so core can be imported
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.discovery import discover_utilities

def test():
    registry = discover_utilities()
    print("Categories discovered:", list(registry.categories.keys()))
    
    total_utils = len(registry.utilities_by_id)
    print(f"Total utilities discovered: {total_utils}")
    
    for uid, util in registry.utilities_by_id.items():
        print(f"  - [{util.category}] {util.name} (Has Render? {'Yes' if util.render_func else 'No'}, Has Router? {'Yes' if util.router else 'No'})")
        
    if total_utils == 4:
        print("SUCCESS: All 4 utilities loaded.")
        sys.exit(0)
    else:
        print("FAILED: Expected 4 utilities.")
        sys.exit(1)

if __name__ == "__main__":
    test()
