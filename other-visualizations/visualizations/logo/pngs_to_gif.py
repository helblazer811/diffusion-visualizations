import os
import imageio

# Directory containing the frames
frames_directory = 'LogoVideoFrames'

# Output GIF file path
output_gif_path = 'output.gif'

# Get list of image files in the directory
frame_files = sorted([os.path.join(frames_directory, f) for f in os.listdir(frames_directory) if f.endswith('.png')])

# Create GIF
with imageio.get_writer(output_gif_path, mode='I', duration=30) as writer:
    for frame_file in frame_files:
        image = imageio.imread(frame_file)
        writer.append_data(image)

print("GIF created successfully!")