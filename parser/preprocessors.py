import re

MATHMODE_LOOKUP = {
    "\\alpha": "α",
    "\\beta": "β",
    "\\Gamma": "Γ",
    "\\gamma": "γ",
    "\\Delta": "Δ",
    "\\delta": "δ",
    "\\varepsilon": "ε",
    "\\zeta": "ζ",
    "\\eta": "η",
    "\\Theta": "Θ",
    "\\theta": "θ",
    "\\iota": "ι",
    "\\kappa": "κ",
    "\\Lambda": "Λ",
    "\\lambda": "λ",
    "\\mu": "μ",
    "\\nu": "ν",
    "\\pi": "π",
    "\\tau": "τ",
    "\\phi": "ϕ",
    "\\Sigma": "Σ",
    "\\sigma": "σ",
    "\\infty": "∞",
    "\\emptyset": "∅",
    "\\|": "||"
}

LATEX_IGNORES = [
    r"%.*\n",
    r"\\small",
    r"\\Large",# TODO: Handle better.
    r"\\setlength{\\oddsidemargin}{-?\d+(\.\d+)?in}",
    r"\\vspace{-\d+pt}"
] 

# TODO: Double-check \n count in output
LATEX_LOOKUP = {
    "\\\\": "\\n",
    "\\newline": "\\n", 
    "\n": "\\n",
    "\"": "\\\"",
    "\\noindent": "",
    "\\newpage": "",
    "\\indent": "\\t",
    }

LATEX_REPLACEMENTS = {# Regex substitutions
    r"\\vspace{\dpt}": r"\\n",
    r"\\vspace{\d\dpt}": r"\\n\\n",
    r"(\\begin\{center\})\n?(.+(?:\n+.+)*)\n?(\\end\{center\})": r"\1", #Ignore for now. Alt: r"<span style='text-align: center'>\2</span>",
    r"(\\textit\{)\n?(.+(?:\n+.+)*)\n?(\})": r"<i>\2</i>", # TODO: This will fail if bracketed commands are used inside of the \textit command.
    r"(\\textbf\{)\n?(.+(?:\n+.+)*)\n?(\})": r"<b>\2</b>", # TODO: This will fail if bracketed commands are used inside of the \textbf command.
}

def clean_lyrics(latex: str) -> str:
    return clean_latex(latex).replace("$\\|$", "||") # TODO: This last replace shouldn't be here. Idk why math mode doesn't handle it properly...

def clean_latex(latex: str) -> str:
    out = latex
    for ignore in LATEX_IGNORES:
        out = re.sub(ignore, "", out)
    for match in re.finditer(r"(\$(.*?)\$)", latex):
        out = out.replace(match.group(1), clean_mathmode(match.group(2)) + "") + ""
    for (find, replacement) in LATEX_LOOKUP.items():
        out = out.replace(find, replacement)
    for (find, substitute) in LATEX_REPLACEMENTS.items():
        out = re.sub(find, substitute, out)
    return out.strip()

def clean_mathmode(mm: str) -> str:
    out = mm + ""
    for (find, replacement) in MATHMODE_LOOKUP.items():
        out = out.replace(find, replacement) + ""
    return out