from PIL import Image

# Wczytaj obraz
image = Image.open("legity.png")

# Zmniejsz rozdzielczość
image = image.resize((image.width // 3, image.height // 3))

# Zapisz skompresowany plik
image.save("output.png", optimize=True, quality=70)  # Dostosuj quality, aby osiągnąć 1MB
