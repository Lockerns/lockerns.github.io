import skimage.io as sio
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

def normalize_image(img: np.ndarray) -> np.ndarray:
    """
    Normalize the input image so that its values lie between 0 and 1.
    """
    max_value = img.max()
    min_value = img.min()
    img = (img - min_value) / (max_value - min_value + 1e-9)
    return img

def onclick(event):
    """
    Handle mouse click events on the displayed image. When a point in the
    image is clicked, its spectral signature is displayed on the second plot.
    """
    if event.xdata is not None and event.ydata is not None:
        # Ensure indices are within image boundaries
        x_idx = int(event.xdata)
        y_idx = int(event.ydata)
        if 0 <= y_idx < img.shape[0] and 0 <= x_idx < img.shape[1]:
            y = img[y_idx, x_idx, :]
            line.set_ydata(y)
            # Dynamically adjust y-axis range
            ax2.relim()
            ax2.autoscale_view()
            fig.canvas.draw_idle()
    else:
        print("Clicked outside the image")

def get_file_extension(filename: str) -> str:
    """
    Extract the file extension from a given filename.
    Returns the extension without the leading dot.
    """
    return os.path.splitext(filename)[-1].lstrip('.').lower()

def read_bil_file(file_path: str, num_samples: int, num_bands: int, 
                  dtype=np.uint16, raw_flag=False) -> np.ndarray:
    """
    Read a BIL format hyperspectral file.
    - file_path: path to the BIL file
    - num_samples: number of samples (width)
    - num_bands: number of bands (channels)
    - dtype: data type of the image
    - raw_flag: if True, the image is read as raw camera output and reversed in the last dimension
    """
    with open(file_path, 'rb') as file:
        data = np.fromfile(file, dtype=dtype)
    num_lines = data.size // (num_samples * num_bands)

    if raw_flag:
        # Raw camera image arrangement
        data = data.reshape((num_lines, num_samples, num_bands))
        data = data[:, :, ::-1]
    else:
        # Standard BIL arrangement
        data = data.reshape((num_lines, num_bands, num_samples))
        data = data.transpose((0, 2, 1))
    
    return data

def select_rgb_channels(num_bands: int) -> (int, int, int):
    """
    Select R, G, B channels proportionally based on the number of bands.
    Originally, R=145, G=79, B=26 out of 480 channels.
    We scale these indices according to the given number of bands.
    """
    # Original indices based on 480 channels
    base_r, base_g, base_b = 145, 79, 26
    base_total = 480.0

    # Scale proportionally
    r_ch = int(round((base_r / base_total) * num_bands))
    g_ch = int(round((base_g / base_total) * num_bands))
    b_ch = int(round((base_b / base_total) * num_bands))

    # Ensure indices are valid
    r_ch = min(r_ch, num_bands - 1)
    g_ch = min(g_ch, num_bands - 1)
    b_ch = min(b_ch, num_bands - 1)

    return r_ch, g_ch, b_ch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display hyperspectral image and interactively show spectral signatures.')
    parser.add_argument('--image_path', '-i', help='Input image path', required=True)
    parser.add_argument('--raw', '-r', action='store_true', help='Treat input as raw image captured by the camera')
    parser.add_argument('--channels', '-c', type=int, default=480, help='Number of spectral channels in the image')
    parser.add_argument('--samples', '-s', type=int, default=1200, help='Number of samples (width) in the image for BIL reading')
    args = parser.parse_args()

    raw_flag = args.raw
    file_name = args.image_path
    extension = get_file_extension(file_name)
    num_bands = args.channels
    num_samples = args.samples

    # Read image
    if extension == 'bil' or extension == 'os':
        img = read_bil_file(file_name, num_samples, num_bands, raw_flag=raw_flag)
    elif extension in ['tif', 'tiff']:
        img = sio.imread(file_name)
        # If the dimension order doesn't match, try to transpose accordingly
        if img.ndim == 3 and img.shape[2] != num_bands:
            # Attempt to reorder if needed. This is a heuristic.
            # We assume the band dimension might be the first or second dimension.
            # If it's not already in shape (H, W, Channels), try transposing.
            if img.shape[0] == num_bands:
                # If the first dimension is channels, transpose to (H, W, C)
                img = img.transpose((1, 2, 0))
            elif img.shape[1] == num_bands:
                # If the second dimension is channels, transpose to (H, W, C)
                img = img.transpose((0, 2, 1))

    # Select R,G,B channels proportionally
    r_ch, g_ch, b_ch = select_rgb_channels(num_bands)

    # Normalize and create RGB image for display
    img_r = normalize_image(img[:, :, r_ch])
    img_g = normalize_image(img[:, :, g_ch])
    img_b = normalize_image(img[:, :, b_ch])
    img_part = np.stack((img_r, img_g, img_b), axis=-1)

    # Create figure and subplots
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(img_part)
    ax1.axis('off')
    ax1.set_title('Image')

    # Initialize the spectral plot with the (0,0) pixel's spectrum
    x = np.arange(num_bands)
    y = img[0, 0, :]
    line, = ax2.plot(x, y, color='red')
    ax2.set_xlabel('Bands')
    ax2.set_ylabel('Value')
    ax2.set_title('Spectral Signature')

    # Adjust layout
    plt.tight_layout()

    # Register the mouse click event
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    # Show the plot
    plt.show()
