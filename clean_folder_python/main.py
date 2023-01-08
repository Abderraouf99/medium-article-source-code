from script_log import ScriptLogger
import json as json
import os
import shutil
import sys

logger = ScriptLogger()


def clean_folder(file_formats: dict, target_directory: str):
    logger.log(f"Starting to clean '{target_directory}' folder")

    dir_content = os.listdir(target_directory)

    for d_file in dir_content:
        try:
            if os.path.isdir(d_file):
                continue

            file_name, file_extension = os.path.splitext(d_file)
            if not file_extension.lower() in file_formats:
                continue

            target_path = f'{target_directory}/{file_formats[file_extension.lower()]}'

            if not os.path.isdir(target_path):
                os.mkdir(target_path)

            src_path = f'{target_directory}/{d_file}'
            dst_path = f'{target_path}/{d_file}'

            shutil.copyfile(src=src_path, dst=dst_path)

            os.remove(src_path)

        except:
            logger.log(f"Failed to move file {d_file}")

    logger.log(f"Finished cleaned '{target_directory}' folder")


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        raise Exception("Target folder must be passed to the command")
    target_directory = args[1]
    file_formats = dict()

    with open("file_formats.json", "r") as file:
        file_formats = json.load(file)

    if len(file_formats) == 0:
        logger.log("Failed to execute because of missing file formats")
    else:
        clean_folder(file_formats=file_formats,
                     target_directory=target_directory)
