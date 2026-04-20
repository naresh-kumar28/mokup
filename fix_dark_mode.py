import os
import re

# We will read all html files in the directory
directory = r"c:\Users\nares\Desktop\mokup"

html_files = [f for f in os.listdir(directory) if f.endswith(".html")]

replacements = {
    # backgrounds
    r'\bbg-white\b': 'bg-card',
    r'\bbg-slate-50\b': 'bg-muted',
    r'\bbg-\[\#fdfcfb\]\b': 'bg-background',
    
    # borders
    r'\bborder-slate-100\b': 'border-border',
    r'\bborder-slate-200\b': 'border-border',
    r'\bborder-slate-800\b': 'border-border',
    
    # text colors
    r'\btext-slate-900\b': 'text-foreground',
    r'\btext-slate-800\b': 'text-foreground',
    r'\btext-slate-700\b': 'text-muted-foreground',
    r'\btext-slate-500\b': 'text-muted-foreground',
    r'\btext-slate-400\b': 'text-muted-foreground',
    r'\btext-slate-600\b': 'text-muted-foreground',
}

# The javascript code for dark mode toggling
script_code = """
    <script>
        function toggleDarkMode() {
            document.documentElement.classList.toggle('dark');
            const isDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            updateDarkModeIcon();
        }

        function updateDarkModeIcon() {
            const isDark = document.documentElement.classList.contains('dark');
            const buttons = document.querySelectorAll('button[aria-label="Toggle Dark Mode"]');
            buttons.forEach(btn => {
                const icon = btn.querySelector('iconify-icon');
                if (icon) {
                    icon.setAttribute('icon', isDark ? 'lucide:sun' : 'lucide:moon');
                }
            });
        }

        // Initialize theme based on preference or system
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        
        // Set initial icon on load
        document.addEventListener('DOMContentLoaded', updateDarkModeIcon);
        
        // Add event listeners to all dark mode buttons
        document.addEventListener('DOMContentLoaded', () => {
            const buttons = document.querySelectorAll('button[aria-label="Toggle Dark Mode"]');
            buttons.forEach(btn => {
                btn.addEventListener('click', toggleDarkMode);
            });
        });
    </script>
</body>
"""

dark_css = """      .dark {
        --background: #0f1115;
        --card: #171923;
        --card-foreground: #f8fafc;
        --foreground: #f8fafc;
        --primary: #C5A059;
        --primary-foreground: #ffffff;
        --secondary: #1e293b;
        --secondary-foreground: #f8fafc;
        --tertiary: #1a1f28;
        --muted: #1e2532;
        --muted-foreground: #94a3b8;
        --accent: #1e293b;
        --destructive: #D9534F;
        --border: #2a3241;
        --input: #2a3241;
        --ring: #C5A059;
      }"""

for file in html_files:
    filepath = os.path.join(directory, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Apply regex replacements for tailwind classes ONLY inside class="..." or class='...' 
    # To be safe, we just replace globally. It's very unlikely 'bg-white' appears outside a class logic.
    original_content = content
    for old, new in replacements.items():
        content = re.sub(old, new, content)

    # 2. Add `.dark` variables right after `:root { ... }` in the CSS block
    if '.dark {' not in content:
        # Find where `:root {` ends. The format is a bit chaotic in the file, but we can just append it before `</style>`
        content = content.replace('</style>', dark_css + '\n    </style>')
        
    # 3. Inject JS script before </body>
    if 'function toggleDarkMode' not in content:
        content = content.replace('</body>', script_code)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
