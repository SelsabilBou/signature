# signature_gui.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from verification import verify_signature

REFERENCE_PATH = "image_test.png"   # image de référence


class SignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vérification de signature")

        # Canvas où tu dessines
        self.canvas = tk.Canvas(root, width=400, height=200, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        # Dessin à la souris
        self.canvas.bind("<B1-Motion>", self.draw)

        # Bouton Vérifier
        self.btn_verify = tk.Button(root, text="Vérifier", command=self.on_verify)
        self.btn_verify.grid(row=1, column=0, pady=10)

        # Affichage image de référence
        self.ref_label = tk.Label(root, text="Signature de référence :")
        self.ref_label.grid(row=0, column=1, sticky="n", padx=10)

        self.ref_canvas = tk.Label(root)
        self.ref_canvas.grid(row=0, column=2, sticky="n", padx=10)

        self.load_reference_image()

    def draw(self, event):
        r = 2
        self.canvas.create_oval(
            event.x - r, event.y - r, event.x + r, event.y + r,
            fill="black", outline="black"
        )

    def load_reference_image(self):
        try:
            img = Image.open(REFERENCE_PATH)
            img = img.resize((200, 100))
            self.ref_photo = ImageTk.PhotoImage(img)
            self.ref_canvas.config(image=self.ref_photo)
        except Exception:
            self.ref_canvas.config(text="Référence introuvable")

    def save_canvas_image(self, path="temp_input.png"):
        # TEMPORAIRE : on utilise la même image que référence pour tester
        import shutil
        shutil.copy("image_test.png", path)

    def on_verify(self):
        input_path = "temp_input.png"
        self.save_canvas_image(input_path)

        match, msg = verify_signature(input_path, REFERENCE_PATH)

        messagebox.showinfo("Résultat de vérification", msg)


def main():
    root = tk.Tk()
    app = SignatureApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
