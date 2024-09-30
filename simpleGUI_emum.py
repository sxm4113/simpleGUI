from enum import Enum, unique

@unique
class ImageType(Enum):
    ORIGINAL = 1
    PYRAMID = 2
    MORPHOLOGY = 3
