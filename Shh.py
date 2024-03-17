import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Label
from PIL import Image, ImageTk


def caesar_cipher_encode(text, shift):
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((ord(char) + shift - 65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + shift - 97) % 26 + 97)

    return result


def caesar_cipher_decode(text, shift):
    return caesar_cipher_encode(text, -shift)

def open_image_dialog():
    # Create the main window
    root = tk.Tk()
    root.title(" ")

    # Load the image (replace 'your_image.png' with your actual image file)
    image_path = "C:\\Users\\clyde\\OneDrive\\Desktop\\Designer.png"
    image = Image.open(image_path)
    image = image.resize((600, 400), Image.LANCZOS)  # Use LANCZOS for antialiasing

    # Convert the image to PhotoImage
    img_tk = ImageTk.PhotoImage(image)

    # Display the image in a label
    img_label = tk.Label(root, image=img_tk)
    img_label.pack()

    # Add a greeting message
    greeting_label: Label = tk.Label(root, text="Hello! Welcome to our little secret.")
    greeting_label.pack()

    # Create an "Enter" button
    def handle_enter():
        # Your logic for handling the button click goes here
        # For example, you can open prompts or perform other actions
        print("User clicked the Enter button!")

        # Close the greeting dialog by destroying the root window
        root.destroy()

    enter_button = tk.Button(root, text="Enter", command=handle_enter)
    enter_button.pack()

    # Run the main event loop
    root.mainloop()


# Call the function to open the image dialog
open_image_dialog()


# Ask the user for their name
name = simpledialog.askstring(" ", "Hello fellow Hacker, what should I call you?")

# Create a new Tkinter window
root = tk.Tk()

# Add a greeting message
greeting_label = tk.Label(root, text=f"{name}, what would you like to do?")
greeting_label.pack()
# Create two buttons, "Encode" and "Decode"
encode_button = tk.Button(root, text="Encode", command=lambda: encode())
decode_button = tk.Button(root, text="Decode", command=lambda: decode())

# Pack the buttons into the window
encode_button.pack()
decode_button.pack()

from stegano import lsb


def encode():
    text_to_encode = simpledialog.askstring(" ", "Please enter the text you want to encode:")
    shift = simpledialog.askinteger(" ", "Please enter the shift value for the Caesar cipher:")
    encoded_text = caesar_cipher_encode(text_to_encode, shift)

    # Ask the user for an image to hide the encoded text in
    image_path = filedialog.askopenfilename(title="Select an image to hide the encoded text in")

    # Hide the encoded text in the image
    secret_image = lsb.hide(image_path, encoded_text)
    secret_image.save("secret_image.png")

    # Inform the user that the encoded text has been hidden in the image
    messagebox.showinfo(" ", "The encoded text has been hidden in secret_image.png.")

    # Create a new window to display the encoded text
    result_window = tk.Toplevel(root)
    result_text = tk.Text(result_window)
    result_text.insert(tk.END, "The encoded text is: " + encoded_text)
    result_text.pack()


def decode():
    # Create a new Tkinter window
    decode_root = tk.Tk()

    # Add a message
    decode_label = tk.Label(decode_root, text="What would you like to decode?")
    decode_label.pack()

    # Create two buttons, "Decode Text" and "Decode Image"
    decode_text_button = tk.Button(decode_root, text="Decode Text", command=lambda: decode_text())
    decode_image_button = tk.Button(decode_root, text="Decode Image", command=lambda: decode_image())

    # Pack the buttons into the window
    decode_text_button.pack()
    decode_image_button.pack()

    # Run the main event loop
    decode_root.mainloop()


def decode_text():
    text_to_decode = simpledialog.askstring(" ", "Please enter the text you want to decode:")
    shift = simpledialog.askinteger(" ", "Please enter the shift value for the Caesar cipher:")
    decoded_text = caesar_cipher_decode(text_to_decode, shift)

    # Create a new window to display the decoded text
    result_window = tk.Toplevel(root)
    result_text = tk.Text(result_window)
    result_text.insert(tk.END, "The decoded text is: " + decoded_text)
    result_text.pack()


def decode_image():
    # Ask the user for an image to decode the text from
    image_path = filedialog.askopenfilename(title="Select an image to decode the text from")

    # Decode the text from the image
    decoded_text = lsb.reveal(image_path)

    # Create a new window to display the decoded text
    result_window = tk.Toplevel(root)
    result_text = tk.Text(result_window)
    result_text.insert(tk.END, "The decoded text is: " + decoded_text)
    result_text.pack()


# Run the main event loop
root.mainloop()
