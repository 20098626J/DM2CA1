import fitz  # pymupdf
import re
import os

# Topic keyword mapping
TOPIC_KEYWORDS = {
    "Sets & Relations": ["set", "venn", "union", "intersection", "relation", "equivalence", "ordered pair", "digraph", "universal set"],
    "Functions": ["function", "inverse", "domain", "range", "bijection", "injection", "surjection", "f(x)", "g(x)"],
    "Logic & Boolean Algebra": ["truth table", "tautology", "logical", "boolean", "proposition", "implication", "induction", "predicate", "quantifier"],
    "Combinatorics": ["permutation", "combination", "binomial", "generating function", "arrangement", "committee", "coefficient"],
    "Graph Theory": ["graph", "vertex", "vertices", "edge", "eulerian", "hamiltonian", "bipartite", "adjacency", "circuit", "degree"],
    "Sequences & Series": ["sequence", "series", "recursive", "partial fraction", "induction", "recurrence"],
}

def detect_topic(text):
    text_lower = text.lower()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        scores[topic] = sum(1 for kw in keywords if kw in text_lower)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General"

def extract_year(text):
    match = re.search(r'\b(19|20)\d{2}\b', text)
    return int(match.group()) if match else None

def extract_marks(text):
    match = re.search(r'\((\d+)\s+marks?\)', text, re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_metadata(first_page_text):
    metadata = {
        "year": extract_year(first_page_text),
        "institution": None,
        "course": None,
        "semester": None,
        "duration": None,
    }

    if "WATERFORD" in first_page_text.upper() or "WIT" in first_page_text.upper():
        metadata["institution"] = "WIT / SETU"

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
    # Split on "Question N" headers
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

    # Match sub-parts like (a), (b), (c)
    main_parts = re.split(r'\n\s*\(([a-z])\)\s*', question_text)

    part_label = None
    for chunk in main_parts:
        if re.fullmatch(r'[a-z]', chunk.strip()):
            part_label = chunk.strip()
            continue

        if part_label is None:
            continue

        # Further split into sub-parts like (i), (ii), (iii)
        sub_parts = re.split(r'\((\s*(?:i{1,3}|iv|v|vi|vii|viii|ix|x))\s*\)', chunk, flags=re.IGNORECASE)

        if len(sub_parts) == 1:
            # No sub-parts, treat whole chunk as one part
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
                if re.fullmatch(r'i{1,3}|iv|v|vi|vii|viii|ix|x', stripped, re.IGNORECASE):
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

    # Extract all text
    full_text = ""
    page_texts = []
    for page in doc:
        text = page.get_text()
        page_texts.append(text)
        full_text += text + "\n"

    # Get metadata from first page
    metadata = extract_metadata(page_texts[0])
    year = metadata["year"]

    # Skip reference/law pages (usually last 2-3 pages)
    # Heuristic: pages with "Laws of" or "Table of" are reference pages
    content_text = ""
    for text in page_texts:
        if re.search(r'laws of|table of logical|equivalence name', text, re.IGNORECASE):
            break
        content_text += text + "\n"

    # Split into questions
    questions = split_into_questions(content_text)

    rows = []
    for q in questions:
        parts = split_into_parts(q["text"], q["question_number"])

        for part in parts:
            text = part["text"]
            topic = detect_topic(text)

            rows.append({
                "filename": filename,
                "year": year,
                "institution": metadata["institution"],
                "semester": metadata["semester"],
                "question_number": q["question_number"],
                "part": part["part"],
                "text": text,
                "marks": part["marks"],
                "topic": topic,
            })

    doc.close()
    return rows


def parse_all_pdfs(exam_folder):
    """
    Parse all PDFs in the exam folder.
    Returns a list of all question dicts across all papers.
    """
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
