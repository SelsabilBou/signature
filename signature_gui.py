# signature_gui.py
# Simple Tkinter GUI for drawing and verifying signatures
# This version is simplified for student level - no advanced features

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageTk
import os
from datetime import datetime
import call_processing  # This is your processing module

class SignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signature Verification System")
        self.root.geometry("1200x600")
        
        # Drawing variables
        self.drawing = False
        self.last_x = None
        self.last_y = None
        
        # Create folder for signatures
        self.signatures_folder = "saved_signatures"
        if not os.path.exists(self.signatures_folder):
            os.makedirs(self.signatures_folder)
        
        # Create the layout
        self.create_layout()
        
        # Create PIL image for drawing
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        
        # Bind mouse for drawing
        self.bind_mouse_events()
    
    def create_layout(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side - Reference
        left_frame = tk.LabelFrame(main_frame, text="Reference Signature", padx=10, pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.ref_label = tk.Label(left_frame, text="No reference loaded\nClick 'Load Reference'", bg="white", relief="sunken")
        self.ref_label.pack(fill="both", expand=True)
        
        # Right side - Drawing
        right_frame = tk.LabelFrame(main_frame, text="Draw Signature", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.canvas = tk.Canvas(right_frame, width=600, height=400, bg="white", cursor="pencil")
        self.canvas.pack()
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Load Reference", command=self.load_reference).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Save Signature", command=self.save_signature).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Effacer", command=self.clear_canvas).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Vérifier", command=self.verify_signature).grid(row=0, column=3, padx=10)
        
        # Status
        self.status_label = tk.Label(self.root, text="Ready to draw")
        self.status_label.pack(pady=5)
    
    def bind_mouse_events(self):
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_signature)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
    
    def start_draw(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
    
    def draw_signature(self, event):
        if self.drawing:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=3, fill="black")
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill="black", width=3)
            self.last_x = event.x
            self.last_y = event.y
    
    def stop_draw(self, event):
        self.drawing = False
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.status_label.config(text="Canvas cleared")
        messagebox.showinfo("Cleared", "Signature cleared!")
    
    def save_signature(self):
        # Simple validation
        if self.image.getbbox() is None:
            messagebox.showerror("Error", "No signature to save!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"signature_{timestamp}.png"
        filepath = os.path.join(self.signatures_folder, filename)
        
        self.image.save(filepath)
        self.status_label.config(text=f"Saved: {filename}")
        messagebox.showinfo("Saved", f"Signature saved as {filename}")
    
    def load_reference(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG", "*.png"), ("All", "*.*")])
        if file_path:
            try:
                ref_img = Image.open(file_path)
                ref_img = ref_img.resize((400, 300), Image.Resampling.LANCZOS)
                self.reference_photo = ImageTk.PhotoImage(ref_img)
                self.ref_label.config(image=self.reference_photo, text="")
                self.ref_label.image = self.reference_photo
                self.status_label.config(text="Reference loaded")
                messagebox.showinfo("Loaded", "Reference signature loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {e}")
    
    def verify_signature(self):
        if self.image.getbbox() is None:
            messagebox.showerror("Error", "No signature to verify!")
            return
        
        # Save temp
        self.image.save("temp_signature.png")
        
        # Process
        result = call_processing.process_image("temp_signature.png")
        
        if result['success']:
            features = result['features']
            message = f"Features: Width={features['width']}, Height={features['height']}, Black Pixels={features['black_pixels']}"
            self.status_label.config(text="Verification done")
            messagebox.showinfo("Verified", message)
        else:
            messagebox.showerror("Error", f"Processing failed: {result['error']}")

# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = SignatureApp(root)
    root.mainloop()