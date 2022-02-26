from hela import Catalog
from hela.math.tf_idf import find_similar_occurrences
from hela.math.preprocessing import clean_document
from hela.errors import ValidationError
from collections import defaultdict


def validate_description_similarity(root_catalog: Catalog, min_similarity: float = .75) -> True:
    """Runs a validation check to make sure there descriptions too similar within the catalog.

    This check does not consider duplicated descriptions, for that use validate_no_duplicated_descriptions().

    Args:
        root_catalog: The root catalog of your project
        max_similarity: The minimum required similarity score before raising a validation error (0 to 1)

    Returns:
        True if no description was too similar to another.

    Raises:
        ValidationError:    Raised when descriptions were found that too closely resembles each other.
    """

    desc_dict = {sd.description: sd for sd in root_catalog._all_descriptions()}

    similar_descriptions = find_similar_occurrences(list(desc_dict.keys()), min_similarity=min_similarity)
    msgs = []
    for sd in similar_descriptions:
        obj1 = desc_dict[sd.target_string]
        obj2 = desc_dict[sd.match_string]
        msgs.append(
            f'{obj1.type} <{obj1.name}> too closely resembles {obj2.type} <{obj2.name}>'
            f' ({round(sd.score, 2)}), descriptions:\n'
            f'<{obj1.name}> {obj1.description}\n<{obj2.name}> {obj2.description}'
        )
    if msgs:
        msgs = ['Found descriptions too close in similarity:'] + msgs
        raise ValidationError('\n'.join(msgs))
    return True


def validate_no_description_duplication(root_catalog: Catalog) -> True:
    """Runs a validation check to make sure no descriptions are duplicated within the catalog.

    Args:
        root_catalog: The root catalog of your project

    Returns:
        True if no descriptions were duplicated

    Raises:
        ValidationError: If any duplicated descriptions were found.
    """

    desc_dict = defaultdict(list)
    for sd in root_catalog._all_descriptions():
        if sd is not None:
            desc_dict[clean_document(sd.description)].append(sd)

    msgs = []
    for description, objects in desc_dict.items():
        if len(objects) > 1:
            obj_list = [f'{obj.name} ({obj.type})' for obj in objects]
            msgs.append(
                f'The following objects share the (tokenized) description <{description}>: {", ".join(obj_list)}'
            )
    if msgs:
        msgs = ['Duplicated descriptions found:'] + msgs
        raise ValidationError('\n'.join(msgs))
    return True
