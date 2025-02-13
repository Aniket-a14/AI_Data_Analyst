from .basic_operations import BASIC_EXAMPLES
from .statistical_operations import STATISTICAL_EXAMPLES
from .pandas_operations import PANDAS_EXAMPLES
from .numpy_operations import NUMPY_EXAMPLES
from .matplotlib_operations import MATPLOTLIB_EXAMPLES
from .seaborn_operations import SEABORN_EXAMPLES
from .advanced_analytics import ADVANCED_EXAMPLES
from .utils import create_prompt

def get_examples():
    """Returns all examples combined"""
    all_examples = []
    all_examples.extend(BASIC_EXAMPLES)
    all_examples.extend(STATISTICAL_EXAMPLES)
    all_examples.extend(PANDAS_EXAMPLES)
    all_examples.extend(NUMPY_EXAMPLES)
    all_examples.extend(MATPLOTLIB_EXAMPLES)
    all_examples.extend(SEABORN_EXAMPLES)
    all_examples.extend(ADVANCED_EXAMPLES)
    return all_examples 