# Not used

import re
from pylatexenc.latex2text import LatexNodes2Text 

def clean_lyrics(latex: str) -> str:
    return clean_latex(latex) # TODO: This last replace shouldn't be here. Idk why math mode doesn't handle it properly...

def clean_latex(latex: str) -> str:
    out = latex.replace("$\\|$", "||")
    out = out.replace("\\\\\n","\\\\")
    out = out.replace("\\newline", "\\\\")
    # out = re.sub(r"\\vspace{\dpt}", "\\\\", out)
    return LatexNodes2Text().latex_to_text(out).strip().replace("\n\n", "\n").replace(" \n", "\n")