
import pylatexenc.latexwalker as lw
import pylatexenc.macrospec as ms
import pylatexenc.latex2text as l2t

LW_CTX = lw.get_default_latex_context_db()
LW_CTX.add_context_category(
    'digital',
    prepend=True,
    macros=[
        ms.MacroSpec("chaptertitle", r"{{"),
        ms.MacroSpec("chaptertitlenobr", r"{{"),

        ms.MacroSpec("songtitle", r"{{"),
        ms.MacroSpec("songsubtitle", "{"),
        ms.MacroSpec("songsubtitlelarge", "{"),
        
        ms.MacroSpec("sheetmusicnotice", "{"),
        ms.MacroSpec("sheetmusicnoticenormal", "{"),
        ms.MacroSpec("sheetmusicnoticefootnote", "{"),

        ms.MacroSpec("mel", "{"),
        ms.MacroSpec("auth", "{"),
        ms.MacroSpec("digitalonly", "{"),

        ms.MacroSpec("nysida", r"{{"),
        ms.MacroSpec("sidindex", r"{{"),
    ],
    environments=[
        ms.EnvironmentSpec("lyrics", "")
    ]
)



L2T_CTX = l2t.get_default_latex_context_db()
L2T_CTX.add_context_category(
    'digital',
    prepend=True,
    macros=[
        l2t.MacroTextSpec("digitalonly", simplify_repl=r'%(1)s'),
        # l2t.MacroTextSpec("textbf", simplify_repl=r'<b>%(1)s</b>'), # Disabled in testing
        # l2t.MacroTextSpec("textit", simplify_repl=r'<i>%(1)s</i>'),
        l2t.MacroTextSpec("newline", simplify_repl=r'\n'),
        l2t.MacroTextSpec("newpage", simplify_repl=r'\n'),
    ],
    environments=[
    ],
    specials=[
        # l2t.SpecialsTextSpec('`', "‘"),
    ],
)