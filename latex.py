try:
    import matplotlib.pyplot as plt
except ImportError:
    import sys
    sys.path.append('./libs')
    import matplotlib.pyplot as plt

import hashlib
import os

OUTPUT_DIR = "latex_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_hashed_filename(latex_expr):
    return hashlib.md5(latex_expr.encode()).hexdigest() + ".png"

def render_latex(latex_expr):
    img_filename = get_hashed_filename(latex_expr)
    img_path = os.path.join(OUTPUT_DIR, img_filename)

    if os.path.exists(img_path):
        return img_path

    try:
        fig, ax = plt.subplots(figsize=(0.5, 0.5), dpi=300)
        ax.text(0.5, 0.5, f"${latex_expr}$", fontsize=10, ha="center", va="center")
        ax.axis("off")

        plt.savefig(img_path, format="png", bbox_inches="tight", pad_inches=0.1)
        plt.close()
        return img_path
    except Exception as e:
        print(f"Error rendering LaTeX: {e}")
        return None

