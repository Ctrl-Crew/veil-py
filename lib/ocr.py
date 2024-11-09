from PIL import ImageOps,Image, ImageFilter
import pytesseract

def do_ocr(b64image):
    image = Image.open(b64image)
    
    # Convert image to grayscale.
    gray_image = ImageOps.grayscale(image)

    # Resize the image to enhance details.
    scale_factor = 2
    resized_image = gray_image.resize(
        (gray_image.width * scale_factor, gray_image.height * scale_factor),
        resample=Image.LANCZOS
    )

    # Apply adaptive thresholding using the `FIND_EDGES` filter.
    thresholded_image = resized_image.filter(ImageFilter.FIND_EDGES)

    # Extract text from the preprocessed image.
    improved_text = pytesseract.image_to_string(thresholded_image)

    # Print the extracted text.
    print(improved_text)

    # Optional: Save the preprocessed image for review.
    thresholded_image.save('preprocessed_image.jpg')