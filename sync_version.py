#!/usr/bin/env python3
import json

# Read root package.json
with open('package.json', 'r') as f:
   root_pkg = json.load(f)

# Read child package.json
with open('vue/dynamicforms/package.json', 'r') as f:
   child_pkg = json.load(f)

# Update version
child_pkg['version'] = root_pkg['version']

# Write updated child package.json
with open('vue/dynamicforms/package.json', 'w') as f:
   json.dump(child_pkg, f, indent=2, ensure_ascii=False)
   f.write('\n')
