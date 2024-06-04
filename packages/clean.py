import glob
import os

__all__ = ['clean']
def clean() -> list[str]:
    files = glob.glob("*.session*")

    errors: list[str] = []
    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except:
            errors.append(file)
    return errors
