from enum import Enum, unique

@unique
class ImageType(Enum):
    ORIGINAL = 1
    PYRAMID = 2
    MORPHOLOGY = 3

@unique
class ProcessingType(Enum):
    CONTRAST_ENHANCEMENT = 1
    CLASSIFICATION = 2

@unique
class Classification_Label(Enum):
    Bacterial_Spot = 0
    Early_Blight = 1
    Healthy = 2
    Late_blight = 3
    Leaf_Mold = 4
    Target_Spot = 5
    black_spot = 6

@unique
class Model_enum(Enum):
    VisionTransformer = 0