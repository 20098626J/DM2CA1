from importlib import metadata

import fitz  # pymupdf
import re
import os

# Topic keyword mapping
TOPIC_KEYWORDS = {
    "Sets & Relations": ["set", "venn", "union", "intersection", "relation",
                         "equivalence", "ordered pair", "digraph", "universal set",
                         "subset", "complement", "cartesian", "partition","elements of the following sets",
                         "list the elements","universal set","let p", "let q", "let r",
                         "equivalence relation","ordered pairs","draw a digraph",
                         "reflexive", "symmetric", "transitive",
                         "∧", "∨", "∩", "∪", "∈", "⊆", "⊂", r"\A", r"\B", r"\C"],
    "Functions": ["function", "inverse", "domain", "range", "bijection",
                  "injection", "surjection", "onto", "one-to-one", "composition",
                  "codomain", "surjective", "injective", "bijective", "f(f", "g °f"],
    "Logic & Boolean Algebra": ["truth table", "tautology", "logical", "boolean",
                                 "proposition", "implication", "predicate", "quantifier",
                                 "contrapositive", "negation", "conjunction", "disjunction",
                                 "∧", "∨", "→", "↔", "¬", "∀", "∃"],
    "Combinatorics": ["permutation", "combination", "binomial", "generating function",
                      "arrangement", "committee", "coefficient", "factorial", "choose",
                      "ways", "selections", "expand", "repeated", "digits"],
    "Graph Theory": ["graph", "vertex", "vertices", "edge", "eulerian", "hamiltonian",
                     "bipartite", "adjacency", "circuit", "degree", "path", "cycle",
                     "connected", "planar", "tree", "node"],
    "Sequences & Series": ["sequence", "series", "recursive", "partial fraction",
                            "recurrence", "summation", "arithmetic", "geometric",
                            "induction", "integer between", "even integer", "odd integer",
                            "prime", "divisible", "∑", "nk=", "2k"],
    "Number Systems & Binary": ["binary", "weight", "hexadecimal", "octal", "base",
                             "bits", "starts with 1", "decimal", "convert"],

    "Algorithms & Programming": ["python", "program", "algorithm", "variable", 
                              "function call", "return", "output", "input case",
                              "pseudocode", "calculate"],
}

def detect_topic(text):
    text_lower = text.lower()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        scores[topic] = sum(1 for kw in keywords if kw in text_lower)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General"

def extract_year(text, filename=""):
    match = re.search(r'\d{1,2}/\d{1,2}/((19|20)\d{2})', text)
    if match:
        return int(match.group(1))
    
    match = re.search(r'\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december),?\s+((19|20)\d{2})', text, re.IGNORECASE)
    if match:
        return int(match.group(2))

    match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+((19|20)\d{2})', text, re.IGNORECASE)
    if match:
        return int(match.group(2))

    match = re.search(r'\b(19|20)\d{2}\b', text)
    if match:
        return int(match.group())

    match = re.search(r'(19|20)\d{2}(\d{2})', filename)
    if match:
        century = match.group(1)[:2]
        return int(f"{century}{match.group(2)}")
    
    match = re.search(r'\b(19|20)\d{2}\b', filename)
    if match:
        return int(match.group())

    return None

def extract_marks(text):
    match = re.search(r'\((\d+)\s+marks?\)', text, re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_metadata(first_page_text, filename=""):
    metadata = {
        "year": extract_year(first_page_text, filename),
        "institution": None,
        "course": None,
        "semester": 1,
        "is_repeat": "repeat" in filename.lower() or "august" in first_page_text.lower(),
        "duration": None,
    }

    if "WATERFORD" in first_page_text.upper() or "WIT" in first_page_text.upper():
        metadata["institution"] = "WIT"
    elif "SOUTH EAST TECHNOLOGICAL" in first_page_text.upper() or "SETU" in first_page_text.upper():
        metadata["institution"] = "SETU"

    course_match = re.search(r'(DISCRETE MATHEMATICS)', first_page_text, re.IGNORECASE)
    if course_match:
        metadata["course"] = course_match.group(1).title()

    semester_match = re.search(r'SEMESTER\s+(\d+)', first_page_text, re.IGNORECASE)
    if semester_match:
        metadata["semester"] = int(semester_match.group(1))

    duration_match = re.search(r'(\d+)\s+HOURS?', first_page_text, re.IGNORECASE)
    if duration_match:
        metadata["duration"] = int(duration_match.group(1))

    return metadata

def split_into_questions(full_text):
    
    pattern = r'(Question\s+\d+)'
    parts = re.split(pattern, full_text, flags=re.IGNORECASE)

    questions = []
    i = 1
    while i < len(parts) - 1:
        header = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        q_num_match = re.search(r'\d+', header)
        if q_num_match:
            questions.append({
                "question_number": int(q_num_match.group()),
                "text": body
            })
        i += 2
    return questions

def split_into_parts(question_text, question_number):
    parts = []

    
    main_parts = re.split(r'\n\s*\(([a-z])\)\s*', question_text)

    part_label = None
    for chunk in main_parts:
        if re.fullmatch(r'[a-z]', chunk.strip()):
            part_label = chunk.strip()
            continue

        if part_label is None:
            continue

        
        sub_parts = re.split(r'\((\s*(?:i{1,3}|iv|v|vi|vii|viii|ix|x|\d+))\s*\)', chunk, flags=re.IGNORECASE)

        if len(sub_parts) == 1:
        
            text = chunk.strip()
            marks = extract_marks(text)
            if text:
                parts.append({
                    "part": f"{part_label}",
                    "text": text,
                    "marks": marks,
                })
        else:
            sub_label = None
            for sub_chunk in sub_parts:
                stripped = sub_chunk.strip()
                if re.fullmatch(r'i{1,3}|iv|v|vi|vii|viii|ix|x|/d+', stripped, re.IGNORECASE):
                    sub_label = stripped
                    continue
                if sub_label and stripped:
                    marks = extract_marks(stripped)
                    parts.append({
                        "part": f"{part_label}({sub_label})",
                        "text": stripped,
                        "marks": marks,
                    })
                    sub_label = None

    return parts

def parse_pdf(filepath):
    
    doc = fitz.open(filepath)
    filename = os.path.basename(filepath)
    is_marking_scheme = filename.upper().endswith("_MS.PDF")

    full_text = ""
    page_texts = []
    for page in doc:
        text = page.get_text()
        page_texts.append(text)
        full_text += text + "\n"

    metadata = extract_metadata(page_texts[0], filename)
    year = metadata["year"]

    content_text = ""
    for text in page_texts:
        if re.search(r'laws of|table of logical|equivalence name', text, re.IGNORECASE):
            break
        content_text += text + "\n"

    questions = split_into_questions(content_text)

    rows = []
    for q in questions:
        parts = split_into_parts(q["text"], q["question_number"])

        for part in parts:
            text = part["text"]
            topic = detect_topic(text)

            rows.append({
                "filename": filename,
                "is_marking_scheme": is_marking_scheme,
                "year": year,
                "institution": metadata["institution"],
                "semester": metadata["semester"],
                "question_number": q["question_number"],
                "part": part["part"],
                "text": text,
                "marks": part["marks"],
                "topic": topic,
            })

    #only keep rows that have a marks value
    rows = [r for r in rows if r["marks"] is not None]


    doc.close()
    return rows


def parse_all_pdfs(exam_folder):
    
    all_rows = []
    if not os.path.exists(exam_folder):
        return all_rows

    for root, _, files in os.walk(exam_folder):
        for fname in files:
            if fname.lower().endswith(".pdf"):
                fpath = os.path.join(root, fname)
                try:
                    rows = parse_pdf(fpath)
                    all_rows.extend(rows)
                    print(f"Parsed {fname}: {len(rows)} question parts found")
                except Exception as e:
                    print(f"Error parsing {fname}: {e}")

    return all_rows

