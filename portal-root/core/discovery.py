import os
import importlib.util
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional, Any
from fastapi import APIRouter
import markdown

UTILITIES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "utilities")

class UtilityMeta(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str
    category: str
    name: str
    description: str
    tags: List[str]
    path: str
    render_func: Any = None
    router: Optional[APIRouter] = None

class Registry:
    def __init__(self):
        self.categories: Dict[str, List[UtilityMeta]] = {}
        self.utilities_by_id: Dict[str, UtilityMeta] = {}

def parse_readme(readme_path: str) -> dict:
    name = "Unknown Utility"
    description = ""
    tags = []
    
    if not os.path.exists(readme_path):
        return {"name": name, "description": "No description provided.", "tags": tags}
        
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("# ") and name == "Unknown Utility":
            name = line.replace("# ", "").strip()
        elif line.lower().startswith("tags:"):
            # Format -> Tags: csv, data, tool
            tags_part = line.split(":", 1)[1]
            tags = [tag.strip() for tag in tags_part.split(",") if tag.strip()]
        elif line and not line.startswith("# "):
            if not description:
                description = line
                
    return {"name": name, "description": description, "tags": tags}

def discover_utilities() -> Registry:
    registry = Registry()
    
    if not os.path.exists(UTILITIES_DIR):
        print(f"Warning: Utilities directory not found at {UTILITIES_DIR}")
        return registry

    for category in os.listdir(UTILITIES_DIR):
        cat_path = os.path.join(UTILITIES_DIR, category)
        if not os.path.isdir(cat_path) or category.startswith("__"):
            continue
            
        registry.categories[category] = []
        
        for util_dir in os.listdir(cat_path):
            util_path = os.path.join(cat_path, util_dir)
            if not os.path.isdir(util_path) or util_dir.startswith("__"):
                continue
                
            readme_path = os.path.join(util_path, "README.md")
            app_path = os.path.join(util_path, "app.py")
            
            meta_info = parse_readme(readme_path)
            
            # Dynamically load the module to get render() and router
            render_func = None
            router = None
            
            if os.path.exists(app_path):
                try:
                    spec = importlib.util.spec_from_file_location(f"{category}.{util_dir}", app_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, "render") and callable(module.render):
                        render_func = module.render
                    if hasattr(module, "router") and isinstance(module.router, APIRouter):
                        router = module.router
                except Exception as e:
                    print(f"Error loading {app_path}: {e}")

            util_id = f"{category}/{util_dir}"
            utility = UtilityMeta(
                id=util_id,
                category=category,
                name=meta_info["name"],
                description=meta_info["description"],
                tags=meta_info["tags"],
                path=util_path,
                render_func=render_func,
                router=router
            )
            
            registry.categories[category].append(utility)
            registry.utilities_by_id[util_id] = utility
            
    return registry
