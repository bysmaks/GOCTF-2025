from fontTools.ttLib import TTFont

def extract_y_coords(font_path):
    font = TTFont(font_path)
    glyf = font["glyf"]
    cmap = font.getBestCmap()

    y_coords = []

    for codepoint, glyph_name in cmap.items():
        char = chr(codepoint)
        glyph = glyf[glyph_name]
        if not glyph.isComposite() and glyph.numberOfContours > 0:
            coords = glyph.getCoordinates(font["glyf"])[0]
            max_y = max(y for x, y in coords)
            y_coords.append((char, max_y))

    candidates = [entry for entry in y_coords if entry[1] > 1000]
    return sorted(candidates, key=lambda x: x[1])

if __name__ == "__main__":
    coords = extract_y_coords("challenge.ttf")
    for char, y in coords:
        print(f"{char}: Y = {y}") 
