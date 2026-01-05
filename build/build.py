import json
import os
from typing import Any, Union, List, Dict
import copy

import confio
from confio import *

# class Build:
#     """
#     Ultimate JSON Config Manager
# 
#     Handles everything:
#     - Root ($), values (@), sub-namespaces (%) paths
#     - Lists, dicts, mixed types
#     - Type-safe getters (deep validation)
#     - Existence checks
#     - Creating / updating / atomic saving
#     - Diff tracking
#     - Iteration over subpaths
#     """
# 
#     def __init__(self, file: str):
#         """
#         Initialize with a JSON file path.
#         Nothing is loaded yet.
#         """
#         self.file = file
#         self.data: dict | None = None
#         self._original: dict | None = None
# 
# 
#     def load(self) -> dict:
#         """Load JSON into memory and snapshot original for diff"""
#         with open(self.file, "r", encoding="utf-8") as f:
#             self.data = json.load(f)
#         if not isinstance(self.data, dict):
#             raise ValueError("Root JSON must be a dict")
#         self._original = copy.deepcopy(self.data)
#         return self.data
# 
#     def reload_if_changed(self) -> bool:
#         """Reloads file if modified externally"""
#         if self.data is None:
#             self.load()
#             return True
#         current_mtime = os.path.getmtime(self.file)
#         if not hasattr(self, "_mtime"):
#             self._mtime = current_mtime
#             return False
#         if current_mtime != self._mtime:
#             self.load()
#             self._mtime = current_mtime
#             return True
#         return False
# 
#     def save(self, atomic: bool = True):
#         """Save memory back to JSON safely (atomic optional)"""
#         if self.data is None:
#             raise RuntimeError("Nothing to save!")
#         if atomic:
#             tmp = self.file + ".tmp"
#             with open(tmp, "w", encoding="utf-8") as f:
#                 json.dump(self.data, f, indent=4)
#             os.replace(tmp, self.file)
#         else:
#             with open(self.file, "w", encoding="utf-8") as f:
#                 json.dump(self.data, f, indent=4)
# 
# 
#     def _validate_key(self, key: str):
#         """Ensure valid prefixes: $, @, %, or integer for lists"""
#         if key.startswith("$") or key.startswith("@") or key.startswith("%") or key.isdigit():
#             return
#         raise ValueError(f"Invalid key prefix: {key}")
# 
# 
#     def resolve(self, path: str, default: Any = None) -> Any:
#         """
#         Traverse a path ($/@/%/indices). Return default if missing.
#         Supports:
#         - Primitive values
#         - Lists and nested lists
#         - Dicts and nested dicts
#         """
#         if self.data is None:
#             self.load()
#         if not path.startswith("$"):
#             raise ValueError("Path must start with $")
#         current: Any = self.data
#         for part in path.split("."):
#             self._validate_key(part)
#             if isinstance(current, dict):
#                 if part not in current:
#                     return default
#                 current = current[part]
#             elif isinstance(current, list):
#                 try:
#                     current = current[int(part)]
#                 except (ValueError, IndexError):
#                     return default
#             else:
#                 return default
#         return current
# 
# 
#     def exists(self, path: str) -> bool:
#         """Check if path exists"""
#         return self.resolve(path, default=object()) is not object()
# 
#     def is_dict(self, path: str) -> bool:
#         """Check if path is a dict"""
#         return isinstance(self.resolve(path), dict)
# 
#     def is_list(self, path: str) -> bool:
#         """Check if path is a list"""
#         return isinstance(self.resolve(path), list)
# 
#     def is_primitive(self, path: str) -> bool:
#         """Check if path is a primitive type (int, str, bool, float, None)"""
#         return isinstance(self.resolve(path), (int, str, bool, float, type(None)))
# 
#     def get(self, path: str) -> Any:
#         """Get value at path, raises KeyError if missing"""
#         val = self.resolve(path, default=object())
#         if val is object():
#             raise KeyError(f"Path not found: {path}")
#         return val
# 
#     def get_typed(self, path: str, t: type) -> Any:
#         """Get value and check it matches a single type"""
#         val = self.get(path)
#         if not isinstance(val, t):
#             raise TypeError(f"{path} must be {t.__name__}, got {type(val).__name__}")
#         return val
# 
#     def get_typed_deep(self, path: str, expected: Any) -> Any:
#         """
#         Get value and check type recursively.
#         expected can be:
#         - type: int, bool, str, float, NoneType
#         - [type]: uniform list
#         - dict: dict with specific key types
#         - nested combinations
#         """
#         val = self.get(path)
# 
#         def _check(v, exp):
#             if isinstance(exp, type):
#                 if not isinstance(v, exp):
#                     raise TypeError(f"Expected {exp.__name__}, got {type(v).__name__}: {v}")
#             elif isinstance(exp, list):
#                 if not isinstance(v, list):
#                     raise TypeError(f"Expected list, got {type(v).__name__}: {v}")
#                 if len(exp) > 0:
#                     for item in v:
#                         _check(item, exp[0])
#             elif isinstance(exp, dict):
#                 if not isinstance(v, dict):
#                     raise TypeError(f"Expected dict, got {type(v).__name__}: {v}")
#                 for k, t in exp.items():
#                     if k not in v:
#                         raise KeyError(f"Missing key {k} in {v}")
#                     _check(v[k], t)
#             else:
#                 raise TypeError(f"Invalid type specifier: {exp}")
#         _check(val, expected)
#         return val
# 
#     def set(self, path: str, value: Any):
#         """
#         Set or create value at path.
#         Auto-creates intermediate dicts as needed.
#         """
#         if self.data is None:
#             self.load()
#         parts = path.split(".")
#         current = self.data
#         for part in parts[:-1]:
#             self._validate_key(part)
#             if part not in current or not isinstance(current[part], dict):
#                 current[part] = {}
#             current = current[part]
#         current[parts[-1]] = value
# 
#     def keys(self, path: str = "$") -> List[str]:
#         """Return keys of a dict at path"""
#         val = self.get(path)
#         if not isinstance(val, dict):
#             raise TypeError(f"{path} is not a dict")
#         return list(val.keys())
# 
#     def items(self, path: str = "$") -> List[tuple]:
#         """Return items of a dict at path"""
#         val = self.get(path)
#         if not isinstance(val, dict):
#             raise TypeError(f"{path} is not a dict")
#         return list(val.items())
# 
#     def values(self, path: str = "$") -> list:
#         """Return values of a dict at path"""
#         val = self.get(path)
#         if not isinstance(val, dict):
#             raise TypeError(f"{path} is not a dict")
#         return list(val.values())
# 
#     def diff(self) -> None:
#         """Show added / changed keys since last load"""
#         if self.data is None or self._original is None:
#             print("No changes or not loaded")
#             return
# 
#         def recurse(old: dict, new: dict, path=""):
#             for key in new:
#                 full = f"{path}.{key}" if path else key
#                 if key not in old:
#                     print(f"[ADDED]   {full} = {new[key]}")
#                 elif old[key] != new[key]:
#                     print(f"[CHANGED] {full}: {old[key]} -> {new[key]}")
#                 if isinstance(new[key], dict) and key in old:
#                     recurse(old[key], new[key], full)
#         recurse(self._original, self.data)
# 
# 
#     def dump(self) -> None:
#         """Pretty print JSON"""
#         if self.data is None:
#             self.load()
#         print(json.dumps(self.data, indent=4))
# 
# 
# class JSONBuild(Build):
#     """
#     Extends UltimateBuild with:
#     - chtype(): set a type template at a path
#     - execute(): fill in the values after checking types
#     """
# 
#     def __init__(self, file: str):
#         super().__init__(file)
#         self._type_templates: dict[str, Any] = {}
# 
#     def template(self, path: str, type_list: list):
#         """
#         Set a type template at a path.
#         Example:
#             build.chtype("$settings.@enableComfirmations", [bool, str])
#         Internally, stores the template and replaces the values with placeholders.
#         """
#         self._type_templates[path] = type_list
#         placeholders = ["?" for _ in type_list]
#         self.set(path, placeholders)
# 
#     def execute(self, path: str, values: list):
#         """
#         Fill in values at a path according to type template set by chtype().
#         Raises TypeError if types do not match the template.
#         Example:
#             build.execute("$settings.@enableComfirmations", [True, "strict"])
#         """
#         if path not in self._type_templates:
#             raise ValueError(f"No type template set for {path}. Use chtype() first.")
#         template = self._type_templates[path]
# 
#         if len(template) != len(values):
#             raise ValueError(f"Length mismatch: template has {len(template)}, got {len(values)}")
# 
#         for i, (t, val) in enumerate(zip(template, values)):
#             if isinstance(t, type):
#                 if not isinstance(val, t):
#                     raise TypeError(f"Value {val} at index {i} does not match type {t.__name__}")
#             else:
#                 if val != t:
#                     raise TypeError(f"Value {val} at index {i} does not match literal {t}")
# 
#         self.set(path, values)
global jsonconf
jsoncfg = Confio("config.json")
jsoncfg.load()
