import app
from app import modules
from app.modules import security_rules


app/modules/security_rules.py
# FILE: cornelius_os/app/modules/security_rules.py
RULES = []  # Initial empty rules list

# TODO: Add rules for static analysis.  Examples:
# RULES = [
#     {"type": "module", "module_name": "os", "node_type": "ast.Import", "description": "Import of the 'os' module (potentially dangerous)"},
#     {"type": "function", "function_name": "system", "node_type": "ast.Call", "description": "Call to 'os.system' (potentially dangerous)"},
# ]

#These would need to be checked manually, and converted to the format for the static analysis function.