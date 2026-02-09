import tkinter as tk
from PIL import Image, ImageTk
import os

# ui driver for tkinter
class DashboardViewer:
    def __init__(self, output_folder, report_data):
        self.output_folder = output_folder
        self.report_data = report_data
        
        self.root = tk.Tk()
        self.root.title("GDP ANALYZER")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e3c72')
        
        self.create_scrollable_window()
        self.root.mainloop()
    
    # initial window
    def create_scrollable_window(self):
        main_frame = tk.Frame(self.root, bg='#1e3c72')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame, bg='#1e3c72', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        self.scroll_frame = tk.Frame(canvas, bg='#1e3c72')
       
        self.canvas_window = canvas.create_window(
            (0, 0), 
            window=self.scroll_frame, 
            anchor="nw"
        )
        
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        
        def on_canvas_configure(event):
          
            canvas.itemconfig(self.canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        
       

        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        self.add_content()
        
    # section adder
    # section adder
    def add_content(self):
        self.add_header()
        self.add_summary()

        try:
            files = [f for f in os.listdir(self.output_folder) if f.lower().endswith('.png')]
            files.sort()           
            for filename in files:               
                               
                self.add_graph_section(filename)

        except Exception as e:
            tk.Label(self.scroll_frame, text=f"Error reading folder: {e}", fg="red").pack()
            
        self.add_footer()

    def add_header(self):
        title_frame = tk.Frame(self.scroll_frame, bg='#1e3c72', pady=40)
        title_frame.pack(fill=tk.X)
        
        tk.Label(title_frame, text="GDP ANALYZER", font=('Arial Black', 50, 'bold'), fg='white', bg='#1e3c72').pack()
        tk.Label(title_frame, text="Modular Functional Analysis System", font=('Arial', 18), fg='#bdc3c7', bg='#1e3c72').pack()
        tk.Frame(title_frame, bg='#3498db', height=4).pack(fill=tk.X, padx=100, pady=20)

    def add_summary(self):
        config = self.report_data.get('config', {})
        region = config.get('region', 'Unknown')
        year = config.get('year', 'Unknown')
        op = config.get('operation', 'Unknown').upper()

        text = f"ANALYSIS TARGET: {region} ({year})\nOPERATION: {op}\n\n"
        
        lbl = tk.Label(self.scroll_frame, text=text, font=('Consolas', 14), fg='white', bg='#2c3e50', pady=20, padx=20, justify="left", relief="solid")
        lbl.pack(pady=20, padx=50, fill="x")

    # graph adder
    def add_graph_section(self, filename):
        container = tk.Frame(self.scroll_frame, bg='#2c3e50', pady=15)
        container.pack(fill=tk.X, padx=50, pady=20)
        
        
        
        path = os.path.join(self.output_folder, filename)
        if os.path.exists(path):
            try:
                pil_img = Image.open(path)
                
                
                base_width = 1000
                w_percent = (base_width / float(pil_img.size[0]))
                h_size = int((float(pil_img.size[1]) * float(w_percent)))
                pil_img = pil_img.resize((base_width, h_size), Image.Resampling.LANCZOS)
                
                tk_img = ImageTk.PhotoImage(pil_img)
                
                img_lbl = tk.Label(container, image=tk_img, bg='#2c3e50')
                img_lbl.image = tk_img
                img_lbl.pack(pady=10)
            except Exception as e:
                tk.Label(container, text=f"Error: {e}", fg="red").pack()
        else:
            tk.Label(container, text=f"Image not found: {filename}", fg="red").pack()

    def add_footer(self):
        tk.Label(self.scroll_frame, text="Analysis Complete", font=('Arial', 12), fg='#7f8c8d', bg='#1e3c72', pady=30).pack()