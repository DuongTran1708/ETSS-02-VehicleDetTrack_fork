# ==================================================================== #
# File name: aicity2021_main.py
# Author: Long H. Pham and Duong N.-N. Tran
# Date created: 03/27/2021
#
# The main run script.
# ==================================================================== #
import argparse
import os
from timeit import default_timer as timer

from tfe.camera import CameraMultiprocess
from tfe.io import compress_all_result
from tfe.utils import data_dir
from tfe.utils import prints
from tfe.utils import process_config

import torch

# MARK: - Args

parser = argparse.ArgumentParser(description="Config parser")
parser.add_argument(
	"--dataset",
	default="aicity2021_final",
	help="The dataset to run on."
)
parser.add_argument(
	"--queue_size",
	default=10,
	type=int,
	help="The max queue size"
)
parser.add_argument(
	"--visualize",
	default=False,
	help="Should visualize the processed images"
)
parser.add_argument(
	"--write_video",
	default=False,
	help="Should write processed images to video"
)

config_files = [
	"cam_1.yaml"
]

# MARK: - Main Function

def main():
	args = parser.parse_args()

	main_start_time = timer()

	for config in config_files:
		# TODO: Start timer
		process_start_time = timer()
		total_camera_init_time = 0

		camera_start_time = timer()

		# TODO: Get camera config
		config_path   = os.path.join(data_dir, args.dataset, "configs", config)
		camera_hprams = process_config(config_path=config_path)

		# TODO: Define camera
		camera = CameraMultiprocess(
			config      = camera_hprams,
			queue_size  = args.queue_size,
			visualize   = args.visualize,
			write_video = args.write_video
		)
		total_camera_init_time += timer() - camera_start_time
		# TODO: Process
		camera.run()

		# TODO: End timer
		total_process_time = timer() - process_start_time
		prints(f"Total processing time: {total_process_time} seconds.")
		prints(f"Total camera init time: {total_camera_init_time} seconds.")
		prints(f"Actual processing time: {total_process_time - total_camera_init_time} seconds.")

	prints(f"************************************************")
	main_total_time = timer() - main_start_time
	prints(f"Main processing time: {main_total_time} seconds.")

# # TODO: Compress result from tss.io import compress_all_result
# print("Compressing result")
# output_dir = os.path.join(data_dir, args.dataset, "outputs")
# compress_all_result(output_dir=output_dir)


# MARK: - Entry point

if __name__ == "__main__":
	main()
