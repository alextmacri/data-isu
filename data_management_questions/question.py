import re

class Question:
    def __init__(self, prompt_base: str, prompt_data: list[float], answer: list[list[float]]) -> None:
        self.prompt_data = prompt_data
        self.prompt = self.make_prompt(prompt_base) if re.findall(r'%\S*%', prompt_base) else prompt_base
        self.answer = answer

    def make_prompt(self, prompt_base: str):
        replacements = {
            '%data%': [str(x) for x in self.prompt_data],
            '%name%': ['mike', 'alex', 'jack', 'mickey', 'jamie']
        }
        for key in replacements:
            for i in range(prompt_base.count(key)):
                start_idx = prompt_base.find(key)
                end_idx = start_idx + len(key)
                prompt_base = prompt_base[:start_idx] + replacements[key][i] + prompt_base[end_idx:]
        return prompt_base