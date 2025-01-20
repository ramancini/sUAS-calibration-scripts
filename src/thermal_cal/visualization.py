from src.thermal_cal.cal_utils import CalUtils
from src.thermal_cal.file_search import FileSearch
from src.thermal_cal.image_reader import ImageReader
from tqdm import tqdm

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os


class Visualization:
    def __init__(self):
        self.cal = CalUtils()
        self.finder = FileSearch()
        self.reader = ImageReader()

    def visualize(self, image, channel, save_path=None):
        """
        Visualize an image.

        Args:
            image (np.ndarray): Image array
            save_path (str, optional): Path to save the image. Defaults to None.
        """
        # Select a single channel
        norm_img_visual = image[:, :, channel]

        # Plot the image
        plt.imshow(norm_img_visual)
        plt.colorbar()
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def update(self, frame, image_cube, ax, title, im):
        im.set_array(image_cube[:, :, frame])
        ax.set_title(f"{title} Frame {frame}")
        return [im]

    def frame_generator(self, total_frames):
        for frame in tqdm(range(total_frames), desc="Animating"):
            yield frame

    def video(self, path, title, refresh_rate, save_path=None):
        """
        Create a video from a sequence of images.

        Args:
            path (str): Path to the folder containing the images or a single image file
            title (str): Title of the video
            refresh_rate (int): Refresh rate of the video
            save_path (str, optional): Path to save the video. Defaults to None.
        """
        if os.path.isfile(path):
            image_cube = self.reader.read(path)
        elif os.path.isdir(path):
            files = self.finder.search(path)
            image_cube = self.cal.combine(files)
        else:
            print(
                f"The path '{path}' does not exist or is not a valid file or directory."
            )
            return

        print(f"Animating image cube of {image_cube.shape}")

        fig, ax = plt.subplots(figsize=(10, 8))

        # Initialize the image plot
        im = ax.imshow(
            image_cube[:, :, 0],
            cmap="plasma",
            vmin=image_cube.min(),
            vmax=image_cube.max(),
        )
        fig.colorbar(im, ax=ax)

        # Create the animation
        anim = FuncAnimation(
            fig,
            self.update,
            fargs=(image_cube, ax, title, im),
            frames=self.frame_generator(image_cube.shape[2]),
            interval=refresh_rate,
            blit=True,
            cache_frame_data=False,
        )

        # Save the animation
        if save_path:
            anim.save(save_path, writer="ffmpeg")

        plt.show()
