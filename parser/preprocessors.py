import re

def clean_lyrics(latex: str) -> str:
    out = latex.replace("\n", "\\n").replace("$\|$", "||").replace("\"", "\\\"")
    out = re.sub(r"\\vspace{(\d{0,1})pt}", "\\n", out) # TODO, perhaps do multiple newlines if the first capture group > 15
    
    return out