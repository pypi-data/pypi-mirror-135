from pathlib import Path


def leap_save_model(target_file_path: Path):
    # Load your model
    # Save it to the path supplied as an arugment (has a .h5 suffix)

    print(f'Saving the model as {target_file_path}. Safe to delete this print.')
