import numpy as np
import pandas as pd
from hela.data_types import String, Double, Long, DateTime, Date, Bool
from datetime import date, datetime


python_to_data_type_map = {
    str: String(),
    int: Long(),
    float: Double(),
    bool: Bool(),
    datetime: DateTime(),
    date: Date(),
    np.datetime64: DateTime(),
    pd.Timestamp: DateTime()
}
