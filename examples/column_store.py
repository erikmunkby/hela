from hela import column_store, Col
from hela.data_types import DateTime, String, Array, Date, Int


@column_store()
class ColumnStore:
    timestamp = Col('timestamp', DateTime(), 'Unix style timestamp in UTC.')
    product_codes = Col('product_codes', Array(Int()),
                        'A list of product codes, sent whenever a hit related to products is triggered.')
    store = Col('store', Int(), 'An integer identificator of a store')
    country = Col('country', String(), 'A descriptive name of a country e.g. "Sweden"')
    user_id = Col('user_id', String(), 'The id of the user if logged in.')
    date = Col('date', Date(), 'The date of datapoint occurence, usually used for dataset partitioning.')
    product_code = Col('product_code', Int(), 'An integer representing a specific beer or other product.')
    product_name = Col('product_name', String(), 'The name of the product.')
    product_category = Col('product_category', String(), 'The category of the product e.g. "lager"')
