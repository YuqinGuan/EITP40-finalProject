from data_collection import detect_chars
from collection_class import DataCollection

## Data Collection
detect_chars('data/input/images/test4.jpg', 'data/output/images')

## If it is better to use a class, then go with
# dc = DataCollection('data/input/images/test.jpg', 'data/output/images')
# dc.detect_chars()