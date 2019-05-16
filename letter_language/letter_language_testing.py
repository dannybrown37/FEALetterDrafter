from openpyxl import load_workbook

with open("violations.txt") as f:
    chunks = f.read().replace("\t", "").split("\n\n")
    for chunk in chunks:
        lines = chunk.split("\n")
        data = {
            "category" : lines[0],
            "cites" : lines[1],
            "description" : lines[2]
        }
        lang = raw_input(
            data["description"] +
            "\nYou alleged that..."
            "\nIt was alleged that... > "
        )
        
        data["r_lang"] = "It was alleged that " + lang
        data["r_lang"] += " in violation of " + data["cites"] + "."
        data["r_lang"] = data["r_lang"].replace("F.S.", "Florida Statutes")
        data["r_lang"] = data["r_lang"].replace(
            "F.A.C.", "Florida Administrative Rules"
        )

        data["c_lang"] = "You alleged that " + lang + "."

        # openpyxl stuff starts here
        wb = load_workbook("letter_language.xlsx")
        ws = wb.active
        
        ws.append([
            data["category"],
            data["cites"],
            data["description"],
            data["c_lang"],
            data["r_lang"]
        ])

        wb.save(filename="letter_language.xlsx")
        
