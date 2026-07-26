from pathlib import Path

path = Path("sw4_inverse_problem_paper.tex")
text = path.read_text(encoding="utf-8")

text = text.replace(
    "pdfauthor={[AUTHOR NAME]}",
    "pdfauthor={Shadow (curator and public releaser)}",
)

title_start = text.index("\\title{")
date_end = text.index("\\date{}", title_start) + len("\\date{}")
public_title = r"""\title{An AI-Generated Candidate Solution to the\\
Steiner--Wiener $4$-Index Inverse Problem for Finite Trees}
\author{AI-generated research artifact\\
\small Curated, archived, and publicly released by Shadow\\
\small Released for independent mathematical verification}
\date{}"""
text = text[:title_start] + public_title + text[date_end:]

text = text.replace(
    "We determine exactly which positive integers fail to occur\n"
    "as such an index.  The proof combines",
    "This manuscript presents a candidate determination of which positive integers fail to occur\n"
    "as such an index.  The candidate proof combines",
)

marker = "\\section*{Provenance and verification status}"
if marker not in text:
    abstract_end = "\\end{abstract}\n"
    notice = r"""

\section*{Provenance and verification status}

The mathematical derivations, proof construction, manuscript text, source
code, computational certificates, and internal checks in this release were
generated through extended ChatGPT sessions initiated by Shadow. Shadow
curated, archived, and publicly released the resulting materials, but does not
claim mathematical authorship and has not independently verified the proof.
No independent human expert review has yet been completed.

This manuscript is therefore released as an unverified candidate solution.
Its purpose is to provide a public, reproducible record and invite qualified
mathematicians to examine, reproduce, confirm, correct, or refute the claimed
result. The complete public archive is available at
\url{https://github.com/ShadowUR0/shadow-ai-sw4-candidate-solution}.
"""
    pos = text.index(abstract_end) + len(abstract_end)
    text = text[:pos] + notice + text[pos:]

text = text.replace(
    "\\texttt{[AUTHOR NAME]},\n\\emph{Supplementary exact certificates",
    "Shadow AI Mathematics Project,\n\\emph{Supplementary exact certificates",
)

text = text.replace(
    "accompanying reproducibility archive,\nSHA-256",
    "public reproducibility archive,\\\\\n"
    "\\url{https://github.com/ShadowUR0/shadow-ai-sw4-candidate-solution},\n"
    "SHA-256",
)

placeholders = ("[AUTHOR NAME]", "[AFFILIATION]", "[EMAIL]", "[ORCID]")
remaining = [item for item in placeholders if item in text]
if remaining:
    raise SystemExit(f"Author placeholders remain: {remaining}")

path.write_text(text, encoding="utf-8")
