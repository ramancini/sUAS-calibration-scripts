from src.thermal_cal.visualization import Visualization


visual = Visualization()

new_path = (
    "/local/data/imgs589/field_data/100060_20250117_Foil_2025_01_17_16_47_13/tam640"
)
save_path = "data/cam_sheets/images/longer_test.mp4"

visual.video(new_path, "quick test", 10, save_path)

# files = finder.search(new_path)

# final_img = utils.combine(files)

# print(final_img.shape)

# visual.visualize(reshaped_img,150,"data/cam_sheets/images/more_test.png")
