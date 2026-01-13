import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageGrab
import os

from verification import verify_signature

# Image de référence (à adapter si besoin)
REFERENCE_PATH = "signature_selsabil.png"   # ou "image_test.png"


class SignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vérification de signature")

        # ----- Canvas de dessin -----
        self.canvas_width = 400
        self.canvas_height = 200
        self.canvas_bg = "white"
        self.pen_color = "black"
        self.pen_width = 3

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.canvas_bg
        )
        self.canvas.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Gestion du dessin
        self.drawing = False
        self.last_x = None
        self.last_y = None

        self.bind_mouse_events()

        # ----- Boutons -----
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=1, column=0, columnspan=3, pady=5)

        self.btn_clear = tk.Button(btn_frame, text="Effacer", command=self.clear_canvas)
        self.btn_clear.grid(row=0, column=0, padx=5)

        self.btn_verify = tk.Button(btn_frame, text="Vérifier", command=self.on_verify)
        self.btn_verify.grid(row=0, column=1, padx=5)

        # ----- Affichage image de référence -----
        self.ref_label = tk.Label(root, text="Signature de référence :")
        self.ref_label.grid(row=2, column=0, sticky="w", padx=10)

        self.ref_canvas = tk.Label(root)
        self.ref_canvas.grid(row=2, column=1, sticky="w", padx=10)

        self.load_reference_image()

    # --------------------------- Dessin ---------------------------

    def bind_mouse_events(self):
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_paint)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def on_paint(self, event):
        if not self.drawing:
            return
        x, y = event.x, event.y
        self.canvas.create_line(
            self.last_x,
            self.last_y,
            x,
            y,
            fill=self.pen_color,
            width=self.pen_width,
            capstyle=tk.ROUND,
            smooth=True
        )
        self.last_x, self.last_y = x, y

    def on_button_release(self, event):
        self.drawing = False
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")

    # --------------------------- Référence ---------------------------

    def load_reference_image(self):
        try:
            img = Image.open(REFERENCE_PATH)
            img = img.resize((200, 100))
            self.ref_photo = ImageTk.PhotoImage(img)
            self.ref_canvas.config(image=self.ref_photo)
        except Exception:
            self.ref_canvas.config(text="Référence introuvable")

    # --------------------------- Sauvegarde / Validation ---------------------------

    def save_canvas_image(self, path="temp_input.png"):
        """
        Capture le contenu du canvas et l'enregistre en PNG.
        """
        # Position absolue du canvas sur l'écran
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas_width
        y1 = y + self.canvas_height

        img = ImageGrab.grab(bbox=(x, y, x1, y1))
        img = img.convert("L")  # gris (optionnel)
        img.save(path)

    def count_black_pixels(self, img_path, threshold=200):
        """
        Retourne le nombre de pixels "sombres" (noirs) dans l'image.
        """
        img = Image.open(img_path).convert("L")
        # Pixels sombres = valeur < threshold
        bw = img.point(lambda p: 255 if p > threshold else 0, "1")
        black_pixels = bw.size[0] * bw.size[1] - sum(bw.getdata())
        return black_pixels

    def on_verify(self):
        input_path = "temp_input.png"
        self.save_canvas_image(input_path)

        # Vérifier que le dessin n'est pas vide
        try:
            black_pixels = self.count_black_pixels(input_path)
        except Exception:
            messagebox.showerror("Erreur", "Impossible d'analyser l'image dessinée.")
            return

        if black_pixels < 100:
            messagebox.showwarning(
                "Dessin insuffisant",
                "La signature est trop petite ou vide.\nDessine davantage avant de vérifier."
            )
            return

        if not os.path.exists(REFERENCE_PATH):
            messagebox.showerror(
                "Erreur",
                f"Image de référence introuvable : {REFERENCE_PATH}"
            )
            return

        match, msg = verify_signature(input_path, REFERENCE_PATH)
        messagebox.showinfo("Résultat de vérification", msg)


def main():
    root = tk.Tk()
    app = SignatureApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
