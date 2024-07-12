from PIL import Image

def create_transparent_image(path, size=(40, 40)):
    image = Image.new("RGBA", size, (255, 255, 255, 0))
    image.save(path)

if __name__ == "__main__":
    create_transparent_image("C:\\my_bot\\clanlogo\\transparent.png")
    print("Transparent image created successfully.")
