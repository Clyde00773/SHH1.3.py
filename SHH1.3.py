import tkinter as tk
from tkinter import filedialog, messagebox
import keyboard
from PIL import Image, ImageTk
from stegano import lsb


def terminate_program():
    print("Terminating program.")
    root.destroy()


# Bind the keys 'ctrl' and 'q' to terminate the program
keyboard.add_hotkey('ctrl+q', terminate_program)


def caesar_cipher_encode(text, shift):
    # Replace spaces with '/'
    text = text.replace(' ', '/')
    result = ""
    for i in range(len(text)):
        char = text[i]
        # Only apply the Caesar cipher to alphabetic characters
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            # Leave non-alphabetic characters as they are
            result += char
    return result


def caesar_cipher_decode(text, shift):
    decoded_text = ""
    for i in range(len(text)):
        char = text[i]
        # Only apply the Caesar cipher to alphabetic characters
        if char.isalpha():
            decoded_text += caesar_cipher_encode(char, -shift)
        else:
            # Leave non-alphabetic characters as they are
            decoded_text += char
    # Convert '/' back to spaces
    decoded_text = decoded_text.replace('/', ' ')
    return decoded_text


def encode():
    # Create an Entry widget for the user to enter the message
    message_label = tk.Label(root, text="Please enter the message you want to encode:", bg='black', fg='green')
    message_entry = tk.Entry(root, bg='black', fg='green')
    message_label.pack()
    message_entry.pack()

    # Create an Entry widget for the user to enter the shift value
    shift_label = tk.Label(root, text="Please enter the shift value for the Caesar cipher:", bg='black', fg='green')
    shift_entry = tk.Entry(root, bg='black', fg='green')
    shift_label.pack()
    shift_entry.pack()

    def handle_encode_confirm(event=None):  # Add 'event=None' here
        # Get the message and shift value from the Entry widgets
        message = message_entry.get()
        shift = int(shift_entry.get())

        # Remove the widgets for entering the message and shift value
        message_label.pack_forget()
        message_entry.pack_forget()
        shift_label.pack_forget()
        shift_entry.pack_forget()
        confirm_button.pack_forget()

        # Encode the message using the Caesar cipher
        encoded_message = caesar_cipher_encode(message, shift)

        # Ask the user for an image to hide the encoded text in
        image_path = filedialog.askopenfilename(title="Select an image to hide the encoded text in")

        # Hide the encoded text in the image
        secret_image = lsb.hide(image_path, encoded_message)
        secret_image.save("secret_image.png")

        # Define the images to be displayed
        images = [r"C:\Users\clyde\OneDrive\Desktop\Codes\LB01.png", r"C:\Users\clyde\OneDrive\Desktop\Codes\LB06.png",
                  r"C:\Users\clyde\OneDrive\Desktop\Codes\LB43.png", r"C:\Users\clyde\OneDrive\Desktop\Codes\LB99.png",
                  "C:\\Users\\clyde\\OneDrive\\Desktop\\Designer.png"]

        def change_image(i):
            if i < len(images):
                # Open the image and resize it
                image = Image.open(images[i])
                image = image.resize((600, 400), Image.LANCZOS)

                # Convert the image to a PhotoImage
                img_tk = ImageTk.PhotoImage(image)

                # Update the image displayed in the Label widget
                img_label.config(image=img_tk)
                img_label.image = img_tk  # Keep a reference to the image

                # Schedule the next image change
                root.after(1000, change_image, i + 1)
            else:
                # Inform the user that the encoded text has been hidden in the image
                messagebox.showinfo(" ", "The encoded text has been hidden in secret_image.png.",
                                    bg='black', fg='green')

                # Display the encoded text
                result_text.insert(tk.END, "The encoded text is: " + encoded_message)

        # Start changing images
        change_image(0)

    # Create a button for confirming the message and shift value
    confirm_button = tk.Button(root, text="Confirm", command=handle_encode_confirm, bg='black', fg='green')
    confirm_button.pack()

    # Bind the 'Enter' key to the handle_encode_confirm function
    root.bind('<Return>', lambda event: handle_encode_confirm())


def decode():
    # Make the encode text widget and Caesar shift encode text widget disappear if showing

    shift_label = tk.Label(root, text="Please enter the shift value for the Caesar cipher:", bg='black', fg='green')
    shift_entry = tk.Entry(root, bg='black', fg='green')

    # Ask the user for an image to decode the text from
    image_path = filedialog.askopenfilename(title="Select an image to decode the text from")

    # Create an Entry widget for the user to enter the shift value
    shift_label = tk.Label(root, text="Please enter the shift value for the Caesar cipher:", bg='black', fg='green')
    shift_entry = tk.Entry(root, bg='black', fg='green')
    shift_label.pack()
    shift_entry.pack()

    # Create a Text widget for displaying the decoded text with specified colors
    result_text = tk.Text(root, bg='black', fg='green')

    def handle_decode_confirm(event=None):  # Added event parameter to handle the key press event
        # Get the shift value from the Entry widget
        shift = int(shift_entry.get())

        # Remove the widgets for entering the message and shift value
        shift_label.pack_forget()
        shift_entry.pack_forget()
        confirm_button.pack_forget()

        # Decode the text from the image
        decoded_text = lsb.reveal(image_path)

        # Decode the text using the Caesar cipher
        decoded_text = caesar_cipher_decode(decoded_text, shift)

        # Define the images to be displayed
        images = [r"C:\Users\clyde\OneDrive\Desktop\Codes\LB01.png", r"C:\Users\clyde\OneDrive\Desktop\Codes\LB06.png",
                  r"C:\Users\clyde\OneDrive\Desktop\Codes\LB43.png", r"C:\Users\clyde\OneDrive\Desktop\Codes\LB99.png",
                  "C:\\Users\\clyde\\OneDrive\\Desktop\\Designer.png"]

        def change_image(i):
            if i < len(images):
                # Open the image and resize it
                image = Image.open(images[i])
                image = image.resize((600, 400), Image.LANCZOS)

                # Convert the image to a PhotoImage
                img_tk = ImageTk.PhotoImage(image)

                # Update the image displayed in the Label widget
                img_label.config(image=img_tk)
                img_label.image = img_tk  # Keep a reference to the image

                # Schedule the next image change
                root.after(1000, change_image, i + 1)
            else:
                # Inform the user that the text has been decoded
                messagebox.showinfo(" ", "The text has been decoded.")

                # Ensure the result_text widget is packed into the window
                result_text.pack()

                # Display the decoded text
                result_text.insert(tk.END, "The decoded text is: " + decoded_text)

                # Make the 'Encode' button disappear
                encode_button.pack_forget()

                # Create a 'Return to Encode' button
                return_button = tk.Button(root, text="Return to Encode", bg='black', fg='green')
                return_button.pack()

                def return_to_encode():
                    # Clear the Text widget
                    result_text.delete('1.0', tk.END)

                    # Hide the Text widget
                    result_text.pack_forget()

                    # Hide the 'Return to Encode' button
                    return_button.pack_forget()

                    # Show the 'Encode' and 'Decode' buttons
                    encode_button.pack()
                    decode_button.pack()

                # Set the command of the 'Return to Encode' button
                return_button.config(command=return_to_encode)

        # Start changing images
        change_image(0)

    # Create a button for confirming the shift value
    confirm_button = tk.Button(root, text="Confirm", command=handle_decode_confirm, bg='black', fg='green')
    confirm_button.pack()

    # Bind the 'Enter' key to the handle_decode_confirm function
    root.bind('<Return>', handle_decode_confirm)


# Create a new Tkinter window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg='black')  # Change the color of the window to black


# Set the title of the window
root.title("SHH1.3")

# Add a greeting message
greeting_label = tk.Label(root, text="Hello! Welcome to our little secret..."
                                     "('ctrl'+'Q' = Terminate Program).", bg='black', fg='green')
greeting_label.pack()

# Add the image
image_path = "C:\\Users\\clyde\\OneDrive\\Desktop\\Designer.png"
image = Image.open(image_path)
image = image.resize((600, 400), Image.LANCZOS)
img_tk = ImageTk.PhotoImage(image)
img_label = tk.Label(root, image=img_tk)
img_label.pack()

# Add an Entry widget for the user to enter their name
name_label = tk.Label(root, text="Hello fellow Hacker, what should I call you?", bg='black', fg='green')
name_entry = tk.Entry(root)
name_entry = tk.Entry(root, bg='black', fg='green')
name_entry.pack()
name_label.pack_forget()  # Hide the widget initially
name_entry.pack_forget()  # Hide the widget initially

# Create a button for confirming the name
confirm_button = tk.Button(root, text="Confirm", bg='black', fg='green')
confirm_button.pack_forget()  # Hide the button initially

# Create buttons for encoding and decoding
encode_button = tk.Button(root, text="Encode", command=encode, bg='black', fg='green')
decode_button = tk.Button(root, text="Decode", command=decode, bg='black', fg='green')

# Initially hide the buttons
encode_button.pack_forget()
decode_button.pack_forget()


def handle_enter(event=None):  # Added event parameter to handle the key press event
    # Remove the Enter button
    enter_button.pack_forget()

    # Show the widgets for entering the name
    name_label.pack()
    name_entry.pack()

    def handle_confirm(event=None):  # Added event parameter to handle the key press event
        # Get the user's name from the Entry widget
        name = name_entry.get()
        greeting_label.config(text=f"{name}, what would you like to do?", bg='black', fg='green')

        # Change the image to 'designer2.png'
        image_path2 = "C:\\Users\\clyde\\OneDrive\\Desktop\\Designer2.png"
        image2 = Image.open(image_path2)
        image2 = image2.resize((600, 400), Image.LANCZOS)
        img_tk2 = ImageTk.PhotoImage(image2)
        img_label.config(image=img_tk2)
        img_label.image = img_tk2  # Keep a reference to the image

        # Remove the widgets for entering the name
        name_label.pack_forget()
        name_entry.pack_forget()
        confirm_button.pack_forget()

        # Show the encode and decode buttons
        encode_button.pack()
        decode_button.pack()

        # Set the focus to the decode button
        decode_button.focus_set()

        # Bind the 'Enter' key to the function of the button that currently has focus
        def handle_enter_key(event=None):
            if root.focus_get() == encode_button:
                encode()
            elif root.focus_get() == decode_button:
                decode()

        root.bind('<Return>', handle_enter_key)

        # Change the image back to the original after a delay
        root.after(7000, lambda: img_label.config(image=img_tk))

    # Update the command of the Confirm button and pack it into the window
    confirm_button.config(command=handle_confirm)
    confirm_button.pack()

    # Bind the 'Enter' key to the handle_confirm function
    root.bind('<Return>', handle_confirm)


# Create an Enter button and bind the 'Enter' key to the handle_enter function
enter_button = tk.Button(root, text="Enter", command=handle_enter, bg='black', fg='green')
enter_button.pack()
root.bind('<Return>', handle_enter)

# Create a Text widget for displaying the encoded/decoded text
result_text = tk.Text(root)
result_text.pack_forget()  # Hide the widget initially

# Run the main event loop
root.mainloop()
