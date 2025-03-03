import pandas as pd
from moclo_syntax_model.datamodel import PartDefinition
from Bio.Seq import reverse_complement
import re

df = pd.read_csv("spreadsheet.csv")
with open("images/template_overhangs.svg", "r") as f:
    svg_template_overhangs = f.read()

with open("images/template_box.svg", "r") as f:
    svg_template_box = f.read()

part_definitions = []

for _, row in df.iterrows():
    part_definitions.append(PartDefinition(**dict(row)))


start = "GGAG"
end = "CGCT"

possible_assemblies = list()


def get_path_from_svg(file_name: str):
    path_pattern = re.compile(r'^\s+d="([^"]*)"')
    out = list()
    with open(file_name, "r") as f:
        for line in f:
            match = path_pattern.search(line)
            if match:
                out.append(match.group(1))
    if len(out) == 0:
        return ""

    print(out)
    paths = [
        """
        <path 
        d="{path}"
        style="stroke:#000000;fill:none;stroke-width:3"
        id="inline-cds"/>
        """.format(
            path=path
        )
        for path in out
    ]
    print("\n".join(paths))
    return "\n".join(paths)


path_dictionary = {
    "cds": get_path_from_svg("images/sbol/cds.svg"),
    "promoter": get_path_from_svg("images/sbol/promoter.svg"),
    "rbs": get_path_from_svg("images/sbol/ribosome-entry-site.svg"),
    "terminator": get_path_from_svg("images/sbol/terminator.svg"),
}


def make_overhang_svg(part_definition: PartDefinition):
    svg = svg_template_overhangs
    svg = svg.replace("CCCC", part_definition.left_overhang)
    svg = svg.replace("GGGG", reverse_complement(part_definition.left_overhang))
    svg = svg.replace("AAAA", part_definition.right_overhang)
    svg = svg.replace("TTTT", reverse_complement(part_definition.right_overhang))
    svg = svg.replace("{{path}}", path_dictionary[part_definition.feature_type])
    svg = svg.replace("{{color}}", part_definition.color)
    return svg


def make_box_svg(part_definition: PartDefinition):
    svg = svg_template_box
    svg = svg.replace("{{path}}", path_dictionary[part_definition.feature_type])
    svg = svg.replace("{{color}}", part_definition.color)
    return svg


def find_paths(part_defs, start_overhang, end_overhang, current_path=None):
    if current_path is None:
        current_path = []

    # Base case - if last part's right overhang matches end_overhang, we found a valid path
    if current_path and current_path[-1].right_overhang == end_overhang:
        return [current_path[:]]

    valid_paths = []

    # Get the overhang we're looking to match
    current_overhang = start_overhang if not current_path else current_path[-1].right_overhang

    # Find parts that can connect
    for part in part_defs:
        if part.left_overhang == current_overhang and part not in current_path:
            current_path.append(part)
            paths = find_paths(part_defs, start_overhang, end_overhang, current_path)
            valid_paths.extend(paths)
            current_path.pop()

    return valid_paths


# Find all valid paths
paths = find_paths(part_definitions, start, end)
# Sort paths by length before converting to IDs
paths.sort(key=len)

# Convert paths to list of part IDs for easier printing
for path in paths:
    possible_assemblies.append([part.id for part in path])

# Double-check
for assembly in paths:
    for p1, p2 in zip(assembly, assembly[1:]):
        assert p1.right_overhang == p2.left_overhang


# Make svgs for each part

for part in part_definitions:
    svg = make_overhang_svg(part)
    with open(f"images/overhang_parts/{part.id}.svg", "w") as f:
        f.write(svg)

    box_svg = make_box_svg(part)
    with open(f"images/box_parts/{part.id}.svg", "w") as f:
        f.write(box_svg)
