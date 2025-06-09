import os
import json
import argparse
import pandas as pd
import re
from bs4 import BeautifulSoup
from openpyxl.styles import Alignment


def simplify_latex(latex):
    latex = latex.strip()
    # Remove $$ ... $$ or \( ... \)
    latex = re.sub(r"^\$\$(.*)\$\$$", r"\1", latex)
    latex = re.sub(r"\\\((.*)\\\)", r"\1", latex)

    # Replace common LaTeX commands with unicode or simple text
    replacements = {
        r"\\times": "×",
        r"\\pi": "π",
        r"\\frac{([^}]*)}{([^}]*)}": r"\1 ∕ \2",
        r"\^n": "ⁿ",
        r"\^(\d+)": lambda m: ''.join({'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}[d] for d in m.group(1)),
        r"\\left": "",
        r"\\right": "",
        r"\s+": " ",
    }

    for pattern, repl in replacements.items():
        latex = re.sub(pattern, repl, latex)

    latex = latex.replace("{", "").replace("}", "")
    latex = latex.replace("--", "−")
    latex = latex.replace("\\", "")

    return latex.strip()


def extract_and_simplify_latex(html):
    # Find LaTeX blocks between <!-- LaTeX Start --> and <!-- LaTeX End -->
    latex_blocks = re.findall(r"<!-- LaTeX Start -->(.*?)<!-- LaTeX End -->", html, re.DOTALL)
    simplified_latex = []
    for block in latex_blocks:
        simplified_latex.append(simplify_latex(block.strip()))

    for orig, simple in zip(latex_blocks, simplified_latex):
        html = html.replace(f"<!-- LaTeX Start -->{orig}<!-- LaTeX End -->", simple)

    return html


def html_to_text_with_semicolon(html):
    html = extract_and_simplify_latex(html)
    soup = BeautifulSoup(html, "html.parser")
    texts = []
    # Collect text from block elements (paragraphs, divs, list items)
    for element in soup.find_all(['p', 'div', 'li']):
        text = element.get_text(separator=" ", strip=True)
        if text:
            # Escape literal semicolons to prevent breaking in later processing
            text = text.replace(";", r"\;")
            texts.append(text)
    # Join paragraphs with semicolon 
    return ";".join(texts).strip()


def clean_msg_with_semicolon(html):
    text = html_to_text_with_semicolon(html)
    
    # Temporarily protect escaped semicolons (\;) by replacing them with a unique placeholder
    placeholder = "__ESCAPED_SEMICOLON__"
    text = text.replace(r"\;", placeholder)

    # Normalize spaces around real semicolons (which are paragraph breaks)
    text = re.sub(r"\s*;\s*", "\n;\n", text)

    # Escape all vertical bars
    text = text.replace("|", r"\|")

    # Restore the escaped semicolons
    text = text.replace(placeholder, "\;")

    return text.strip()


def extract_image(html):
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find("img")
    return img["src"].split("/")[-1] if img else ""


def handle_puzzle(data):
    title = data["title"]
    _id = title.lower().replace(" ", "_")
    mv = data.get("main_version", {})
    ext1 = data.get("extension_1", {})
    ext2 = data.get("extension_2", {})
    info = data.get("additional_information", {})

    row = {
        "ID": _id,
        "title": title,
        "references": ";\n".join([html_to_text_with_semicolon(ref) for ref in info.get("references", [])]),
        "statement": clean_msg_with_semicolon(mv.get("statement", "")),
        "statement_image": extract_image(mv.get("statement", "")),
        "correct_answer": mv.get("correct_answer", ""),
        "hint": clean_msg_with_semicolon(mv.get("hint", "")),
        "explanation": clean_msg_with_semicolon(mv.get("explanation", "")),
        "explanation_image": extract_image(mv.get("explanation", "")),
        "extension1_statement": clean_msg_with_semicolon(ext1.get("statement", "")),
        "extension1_statement_image": extract_image(ext1.get("statement", "")),
        "extension1_correct_answer": ext1.get("correct_answer", ""),
        "extension1_hint": clean_msg_with_semicolon(ext1.get("hint", "")),
        "extension1_explanation": clean_msg_with_semicolon(ext1.get("explanation", "")),
        "extension1_explanation_image": extract_image(ext1.get("explanation", "")),
        "extension2_statement": clean_msg_with_semicolon(ext2.get("statement", "")),
        "extension2_statement_image": extract_image(ext2.get("statement", "")),
        "extension2_correct_answer": ext2.get("correct_answer", ""),
        "extension2_hint": clean_msg_with_semicolon(ext2.get("hint", "")),
        "extension2_explanation": clean_msg_with_semicolon(ext2.get("explanation", "")),
        "extension2_explanation_image": extract_image(ext2.get("explanation", "")),
        "about_msg_list": clean_msg_with_semicolon(info.get("about", "")),
    }
    return row


def handle_game(data):
    title = data["title"]
    _id = title.lower().replace(" ", "_")
    mv = data.get("main_version", {})
    ext = data.get("extension_1", {})
    info = data.get("additional_information", {})

    row = {
        "ID": _id,
        "title": title,
        "references": ";\n".join([html_to_text_with_semicolon(ref) for ref in info.get("references", [])]),
        "statement_msg_list": clean_msg_with_semicolon(mv.get("statement", "")),
        "statement_image": extract_image(mv.get("statement", "")),
        "further_instructions_msg_list": clean_msg_with_semicolon(mv.get("further_instructions", "")),
        "strategy_tips_msg_list": clean_msg_with_semicolon(mv.get("strategy_tips", "")),
        "about": clean_msg_with_semicolon(info.get("about", "")),
    }
    return row


def handle_funfact(data):
    title = data["title"]
    _id = title.lower().replace(" ", "_")
    mv = data.get("main_version", {})
    ext = data.get("extension_1", {})
    info = data.get("additional_information", {})

    row = {
        "ID": _id,
        "references": ";\n".join([html_to_text_with_semicolon(ref) for ref in info.get("references", [])]),
        "statement_msg_list": clean_msg_with_semicolon(mv.get("statement", "")),
        "statement_image": extract_image(mv.get("statement", "")),
        "hint_msg_list": clean_msg_with_semicolon(mv.get("hint", "")) or clean_msg_with_semicolon(ext.get("hint", "")),
        "explanation_msg_list": clean_msg_with_semicolon(mv.get("explanation", "")) or clean_msg_with_semicolon(ext.get("explanation", "")),
        "about_msg_list": clean_msg_with_semicolon(info.get("about", "")),
    }
    return row


def _format_sheet(ws):
    # Set all columns width to 40 and enable wrap text
    for col_cells in ws.columns:
        col_letter = col_cells[0].column_letter
        ws.column_dimensions[col_letter].width = 40
        for cell in col_cells:
            cell.alignment = Alignment(wrap_text=True)


def process_folder(input_folder, output_excel):
    puzzle_rows = []
    game_rows = []
    funfact_rows = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            path = os.path.join(input_folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data_type = data.get("metadata", {}).get("type")

            if data_type in ("puzzle", "counting"):
                puzzle_rows.append(handle_puzzle(data))
            elif data_type == "game":
                game_rows.append(handle_game(data))
            elif data_type == "funfact":
                funfact_rows.append(handle_funfact(data))
            else:
                print(f"Skipping unknown type in {filename}")

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        if puzzle_rows:
            df = pd.DataFrame(puzzle_rows)
            df.to_excel(writer, sheet_name="puzzle", index=False)
            _format_sheet(writer.sheets["puzzle"])
        if game_rows:
            df = pd.DataFrame(game_rows)
            df.to_excel(writer, sheet_name="game", index=False)
            _format_sheet(writer.sheets["game"])
        if funfact_rows:
            df = pd.DataFrame(funfact_rows)
            df.to_excel(writer, sheet_name="funfact", index=False)
            _format_sheet(writer.sheets["funfact"])

    print(f"Exported Excel file: {output_excel}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder", help="Folder containing .json files")
    parser.add_argument("-o", "--output", default="combined_output.xlsx", help="Name of the output Excel file")
    args = parser.parse_args()

    process_folder(args.input_folder, args.output)
