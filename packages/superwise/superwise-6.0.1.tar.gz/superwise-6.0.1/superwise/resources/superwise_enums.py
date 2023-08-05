from enum import Enum


class DataEntityRole(Enum):
    """ Data Entity Role enum"""

    ID = "id"
    TIMESTAMP = "time stamp"
    FEATURE = "feature"
    PREDICTION_PROBABILITY = "prediction probability"
    PREDICTION_VALUE = "prediction value"
    LABEL = "label"
    LABEL_TIMESTAMP = "label time stamp"
    LABEL_WEIGHT = "label weight"
    METADATA = "metadata"


class ModelTypes(Enum):
    """ Data Types enum"""

    BINARY_CLASSIFICATION = "Binary Classification"
    BINARY_ESTIMATION = "Binary Estimation"
    REGRESSION = "Regression"
    MULTICLASS_CLASSIFICATION = "Multiclass Classification"


class FeatureType(Enum):
    """ Feature Type enum"""

    NUMERIC = "Numeric"
    BOOLEAN = "Boolean"
    CATEGORICAL = "Categorical"
    TIMESTAMP = "Timestamp"
    UNKNOWN = "Unknown"


class CategoricalSecondaryType(Enum):
    """ Categorical Secondary Type enum"""

    CONSTANT = "Cat_constant"
    DENSE = "Cat_dense"
    SPARSE = "Cat_sparse"


class NumericSecondaryType(Enum):
    """ Numeric Secondary Type enum"""

    NUM_RIGHT_TAIL = "Num_right_tail"
    NUM_LEFT_TAIL = "Num_left_tail"
    NUM_CENTERED = "Num_centered"


class BooleanSecondaryType(Enum):
    """ Boolean Secondary Type enum """

    FLAG = "Boolean_flag"
    NUMERIC = "Boolean_numeric"


def get_enum_value(v):
    """
    ### Description:

    This function  enum property and return the value of the enum

    ### Args:

    `v`:  an enum object

    """
    if isinstance(v, Enum):
        return v.value
    else:
        return v
