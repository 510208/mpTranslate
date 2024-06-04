class prompt():
    def __init__(self, output_language):
        self.short_prompts = """
            When translating Minecraft plugin YAML (`.yml`) configuration files, please adhere to the following rules for completing the translation:
            Target output language: {output_language}
            1. Key and property names: Keys and property names in the YAML file are usually directly referenced by plugin code to retrieve values from the configuration file. These key and property names should remain unchanged and not be translated.
            2. Namespaces and technical identifiers: Namespaces and technical identifiers, such as`minecraft:diamond_sword`, are part of Minecraft and plugin functionality. They need to remain unchanged to ensure the game and plugins operate correctly.
            3. Chinese and English punctuation: Use English punctuation, such as`:`, instead of`：` to ensure the structure of the yml file is not disrupted.
            4. Commands and permission nodes: Commands (e.g.,`/give`) and permission nodes (e.g.,`pluginname.command.give`) defined in the plugin are closely related to the plugin's internal logic. These should also remain unchanged, as translation could cause commands or permissions to be unrecognized.
            5. Formatting codes and color codes: The YAML file may use special formatting codes (e.g.,`&c` for red text) and color codes. These control the text display style and should not be translated.
            6. Data values and enumeration values: Some configuration options may accept a set of specific values (such as`true`/`false`, or specific enumeration values). These values are usually part of the code logic and should be kept in their original form.
            7. Special placeholders and variables: Special placeholders and variables, such as those mentioned for PlaceholderAPI (e.g.,`%player_name%`), are markers for dynamically replacing content and must remain unchanged.
            8. Reserved keywords: The plugin includes reserved keywords like`[refresh]`,`[console]`,`[close]`,`[message]`, etc. Please do not translate these.
            9. Item materials: Materials will be displayed as images in the game, such as the`green_stained_glass_pane` in`material: green_stained_glass_pane` is the game item's ID. Please do not translate these.
            10. Special expressions: Expressions starting with special symbols, like`type: "!has permission"` where`!has permission` is an expression, should not be translated.
            11. YAML file indentation: Pay attention to the indentation in the YAML file, and insert`\n` newline characters at the beginning or end of the file as necessary.
            12. YAML file key duplication: Key names in the YAML file are not allowed to be duplicated. If there are duplicates, please modify the key names.
            13. Special key names: Key names starting with`requirements` should not be translated and kept in their original format.
            14. Avoid adding extra symbols: When the YAML file contains`view_requirement` or`type: javascript`, do not add ``` symbols or other symbols.
            Please follow the rules above for translating the file, and do not modify the format of the input text.
        """