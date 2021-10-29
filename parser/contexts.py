
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
        ms.MacroSpec("course", "{"),
        ms.MacroSpec("instruction", "{"),
        ms.MacroSpec("digitalonly", "{"),
        ms.MacroSpec("physicalonly", "{"),

        ms.MacroSpec("nysida", r"{{"),
        ms.MacroSpec("sidindex", r"{{"),

        ms.MacroSpec("forsangare", r"{"),
        ms.MacroSpec("alla", r"{"),
    ],
    environments=[
        ms.EnvironmentSpec("lyrics", ""),
        ms.EnvironmentSpec("minipage", "[{")
    ]
)



L2T_CTX = l2t.get_default_latex_context_db()
L2T_CTX.add_context_category(
    'digital',
    prepend=True,
    macros=[
        l2t.MacroTextSpec("digitalonly", simplify_repl=r'%(1)s'),
        l2t.MacroTextSpec("newline", simplify_repl='\n'),
        l2t.MacroTextSpec("newpage", simplify_repl='\n'),
        l2t.MacroTextSpec("includegraphics", simplify_repl=''),
        l2t.MacroTextSpec("forsangare", simplify_repl=r'F: %(1)s'),
        l2t.MacroTextSpec("alla", simplify_repl=r'A: %(1)s'),
        # l2t.MacroTextSpec("textbf", simplify_repl=r'<b>%(1)s</b>'), # Disabled in testing
        # l2t.MacroTextSpec("textit", simplify_repl=r'<i>%(1)s</i>'),
    ],
    environments=[
        l2t.EnvironmentTextSpec("minipage", simplify_repl=r'%(body)s'),
    ],
    specials=[
        # l2t.SpecialsTextSpec('_2', "₂"), # Fungerar ej.
    ],
)