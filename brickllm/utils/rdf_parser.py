import re


def extract_rdf_graph(llm_response: str) -> str:

    all_lines = llm_response.splitlines()
    for i, line in enumerate(all_lines):
        all_lines[i] = line.strip()
    llm_response = "\n".join(all_lines).strip()

    if not llm_response.strip().startswith("@prefix "):
        # Try to find RDF content within backticks
        backtick_pattern = re.compile(r"```(.*?)```", re.DOTALL)
        match = backtick_pattern.search(llm_response)
        if match:
            llm_response = match.group(1).strip()
            # return rdf_graph
        # If no backticks, look for RDF starting with @prefix
        rdf_start_pattern = re.compile(r"@prefix [^\s]*: <[^>]*", re.DOTALL)
        match = rdf_start_pattern.search(llm_response)
        if match:
            start_index = match.start()
            rdf_content = llm_response[start_index:].strip()
        else:
            # If no valid RDF content is found, raise an error
            raise ValueError("No valid RDF found in the provided graph content.")
    else:
        rdf_content = llm_response.strip()
    lines = rdf_content.splitlines()
    if lines and lines[-1].strip().endswith("```"):
        rdf_graph = "\n".join(lines[:-1])  # Remove the last line
    else:
        flag_last_line = False
        while not flag_last_line:
            last_line = lines[-1].strip() if lines else ""
            if any(
                word in last_line
                for word in ["note", "Note", "Please", "please", "Here", "here"]
            ):
                lines.pop()
                # TODO: Extract user namespace from instructions and insert instead of bldg:
            elif not (
                last_line.startswith("bldg:")
                or last_line.startswith("ref:")
                or last_line.startswith("unit:")
                or last_line.startswith("brick:")
                or last_line.startswith("a")
            ):  # or any(["note", "Note", "Please"]) in last_line:
                lines.pop()
            elif "```" in last_line.strip():
                lines.pop()
            else:
                flag_last_line = True
        rdf_graph = "\n".join(lines).strip()

        return rdf_graph
