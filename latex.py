try:
    import matplotlib.pyplot as plt
except ImportError:
    import sys

    sys.path.append("./libs")
    import matplotlib.pyplot as plt

import hashlib
import os

OUTPUT_DIR = "latex_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

import hashlib
import os

import matplotlib.pyplot as plt


def get_hashed_filename(latex_expr):
    """Generates a hashed filename for a given LaTeX expression.

    Args:
        latex_expr (str): The LaTeX expression to hash.

    Returns:
        str: A hashed filename with a .png extension based on the LaTeX expression.
    """
    return hashlib.md5(latex_expr.encode()).hexdigest() + ".png"


def render_latex(latex_expr):
    """Renders a LaTeX expression as a PNG image and saves it to a file.

    This function checks if an image for the given LaTeX expression already exists.
    If it does, the function returns the path to the existing image. If not, it
    generates a new image, saves it to the specified output directory, and returns
    the path to the newly created image.

    Args:
        latex_expr (str): The LaTeX expression to render.

    Returns:
        str or None: The path to the rendered image if successful, or None if an error
                     occurs during rendering.
    """
    img_filename = get_hashed_filename(latex_expr)
    img_path = os.path.join(OUTPUT_DIR, img_filename)  # safe across platforms

    if os.path.exists(img_path):
        return img_path

    try:
        _, ax = plt.subplots(figsize=(0.5, 0.5), dpi=300)
        ax.text(0.5, 0.5, f"${latex_expr}$", fontsize=10, ha="center", va="center")
        ax.axis("off")

        plt.savefig(img_path, format="png", bbox_inches="tight", pad_inches=0.1)
        plt.close()
        return img_path
    except Exception as e:
        print(f"Error rendering LaTeX: {e}")
        return None
