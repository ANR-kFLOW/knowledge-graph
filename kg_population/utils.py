import json
import re
import uuid
from urllib.parse import urlparse

import pandas as pd
from rdflib import URIRef


def node_creation(path, entity_mention, base_add=''):
    """
    This function generates a URI for an entity
    :param path: A path that has to be added to the generated URI e.g. /sentence/
    :param entity_mention: The entity for which the generation is done
    :param base_add: Allows for more information to be added to the generated URI
    :return:
    """
    base = f"http://kflow.eurecom.fr{base_add}"
    uri = base + '/' + str(uuid.uuid5(uuid.NAMESPACE_DNS, path + entity_mention))
    return URIRef(uri)


def clean_text(text):
    """
    This is used to remove the html codes from the text
    :param text: The text to clean
    :return: Cleaned text
    """

    # Strip the last part of the text
    index_of_last_occurrence = text.rfind('</p><p>')
    if index_of_last_occurrence != -1:
        text = text[:index_of_last_occurrence]

    text = re.sub(r"<.*?>", " ", text)  # Strip all the special characters in the text

    text = text.strip()  # Remove the whitespace at the beginning, due to deletion

    return text


def uri_validator(x):
    """
    This function checks if a string is a URI/URI
    :param x: The URI/ URL to check
    :return:
    """
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


class MappingDict:

    def __init__(self, encoding_dict=None):
        """
        This function generates a dictionary used to lookup the unique ID's for words
        :param encoding_dict: A dictionary which already contains a mapping
        """
        if encoding_dict is None:
            encoding_dict = {}
        self.encoding_dict = encoding_dict
        self.max_key = self.get_max_key()

    def get_max_key(self):
        if len(self.encoding_dict) != 0:
            values = [int(value[1:]) for value in self.encoding_dict.values()]
            return max(values)
        else:
            return 0

    def increment_max_key(self):
        self.max_key += 1

    def add_words(self, words):

        for word in words:
            if word not in self.encoding_dict.keys():
                self.encoding_dict[word] = f"W{str(self.max_key + 1)}"
                self.increment_max_key()


def gen_mapping_dict(*args):
    import json
    total_instances = 0
    """
    This function generates a dictionary containing all the unique keys for the objects in the JointGT files
    :param args: paths to the jointGT files
    :return: the mapping dictionary
    """
    encoding_dict = {}
    filepaths = [*args]
    for dataset in filepaths:
        dataset = json.load(open(dataset))
        total_instances += len(dataset)

        for instance in dataset:

            for key, value in instance['kbs'].items():
                encoding_dict[value[0]] = key

    encoding_dict = MappingDict(encoding_dict)
    print(f"Processed {total_instances} instances")

    return encoding_dict, total_instances


def gen_jointgt_input_format(data, output_file, encoding_dict=None, subj_col='subject_values', rel_col='predicate',
                             obj_col='object_values', sent_col=None, single_event=True, start_id=0):
    """
    This function converts a dataset to a format suitable for the jointGT model.
    Each row is seen as one instance, unless the parameter inst_col is set.
    :param data: The dataset to process
    :param output_file: The name of the output file (.json should be added)
    :param encoding_dict: The dictionary containing the encodings for the words
    :param subj_col: The column that contains the subject
    :param rel_col: The column that contains the relation
    :param obj_col: The column that contains the object
    :param sent_col: The column that contains the sentence
    :param single_event: If the data is a single event, or each row should be seen as a single event
    :param start_id: the instance ID from which the count should start
    :return: the number of processed instances
    """

    if encoding_dict is None:
        encoding_dict = MappingDict()
        # encoding_dict.add_words(data[subj_col].to_list()) #Generate unique ID's per word (subject)
        encoding_dict.add_words(data[obj_col].to_list())  # Generate unique ID's per word (object)

    else:
        # encoding_dict.add_words(data[subj_col].to_list()) #For subject
        encoding_dict.add_words(data[obj_col].to_list())  # For object

    full_data = []
    kbs = {}
    data = data.reset_index(drop=True)
    for index, row in data.iterrows():
        # subj_id = encoding_dict.encoding_dict[row[subj_col]] #For subject
        obj_id = encoding_dict.encoding_dict[row[obj_col]]  # For object
        relation = row[rel_col].split('/')[-1]
        # kbs[subj_id] = [row[subj_col], row[subj_col], [[relation, str(row[obj_col])]]] #For subject
        kbs[obj_id] = [row[obj_col], row[obj_col], [[relation, str(row[subj_col])]]]

        if not single_event:
            json_dict = {"id": start_id + index,
                         "kbs": kbs,
                         "text": [row[sent_col] if sent_col is not None else None]}
            full_data.append(json_dict)
            kbs = {}

    if single_event:
        full_data = [{"id": 1,
                      "kbs": kbs,
                      "text": ["test"]}]

    with open(output_file, "w") as json_out:

        json.dump(full_data, json_out, indent=2)

    print(f"Processed {len(data)} instances")
    return len(data)


def gen_jointgt_input_format_multiple(data, output_file, encoding_dict=None, subj_col='subject_values',
                                      rel_col='predicate', obj_col='object_values', sent_col=None, inst_col='instance'):
    """
    This function converts a dataset with multiple instances to a format suitable for the jointGT model.
    Function similar to above, except that the column 'inst_col' refers to the instance that the row belongs to
    :param data: The dataset to process
    :param output_file: The name of the output file (.json should be added)
    :param encoding_dict: The dictionary containing the encodings for the words
    :param subj_col: The column that contains the subject
    :param rel_col: The column that contains the relation
    :param obj_col: The column that contains the object
    :param sent_col: The column that contains the sentence
    :param inst_col: The instance that the row corresponds to, should be numbered from 0, and in order
    :return: the number of processed instances
    """

    if encoding_dict is None:
        encoding_dict = MappingDict()
        # encoding_dict.add_words(data[subj_col].to_list()) #Generate unique ID's per word (subject)
        encoding_dict.add_words(data[obj_col].to_list())  # Generate unique ID's per word (object)

    else:
        # encoding_dict.add_words(data[subj_col].to_list()) #For subject
        encoding_dict.add_words(data[obj_col].to_list())  # For object

    full_data = []
    kbs = {}
    sentence = "None"
    data = data.reset_index(drop=True)
    current_instance = 0
    for index, row in data.iterrows():

        if (row[inst_col] != current_instance):
            json_dict = {"id": current_instance,
                         "kbs": kbs,
                         "text": [sentence]}
            full_data.append(json_dict)
            kbs = {}
            current_instance = row[inst_col]

        if index == len(data) - 1:
            # subj_id = encoding_dict.encoding_dict[row[subj_col]] #For subject
            obj_id = encoding_dict.encoding_dict[row[obj_col]]  # For object
            relation = row[rel_col].split('/')[-1]
            # kbs[subj_id] = [row[subj_col], row[subj_col], [[relation, str(row[obj_col])]]] #For subject
            kbs[obj_id] = [row[obj_col], row[obj_col], [[relation, str(row[subj_col])]]]
            sentence = row[sent_col] if sent_col != None else "None"

            json_dict = {"id": current_instance,
                         "kbs": kbs,
                         "text": [sentence]}
            full_data.append(json_dict)

        # subj_id = encoding_dict.encoding_dict[row[subj_col]] #For subject
        obj_id = encoding_dict.encoding_dict[row[obj_col]]  # For object
        relation = row[rel_col].split('/')[-1]
        # kbs[subj_id] = [row[subj_col], row[subj_col], [[relation, str(row[obj_col])]]] #For subject
        kbs[obj_id] = [row[obj_col], row[obj_col], [[relation, str(row[subj_col])]]]
        sentence = row[sent_col] if sent_col is not None else "None"

    with open(output_file, "w") as json_out:

        json.dump(full_data, json_out, indent=2)

    print(f"Processed {len(data)} instances")
    return len(data)


def convert_selected_triples_to_jointgt(data, output_file, mapping_dict=None):
    """
    This function converts the selected triples into the jointGT format
    :param data: The selected triples
    :param output_file: The name of the output file, including .json
    :return: None
    """

    converted_triples = []

    for key, item in data.items():

        if key == 'event_name':
            continue

        elif key == 'place':
            converted_triples.append((data['event_name'], 'location', item))

        elif key == 'Time':
            converted_triples.append((data['event_name'], 'date', item))

        elif key == 'beginTime':
            converted_triples.append((data['event_name'], 'begin date', item))

        elif key == 'endTime':
            converted_triples.append((data['event_name'], 'end date', item))

        elif key == 'actor':
            converted_triples.append((data['event_name'], 'participant', item))

        elif key == 'mentions':
            for triple in item:
                if triple[1] == 'causes':
                    converted_triples.append((triple[0], 'cause', triple[2]))

                elif triple[1] == 'prevents':
                    converted_triples.append((triple[0], 'prevent', triple[2]))

                elif triple[1] == 'intends_to_cause':
                    converted_triples.append((triple[0], 'intend', triple[2]))

                elif triple[1] == 'enables':
                    converted_triples.append((triple[0], 'enable', triple[2]))

                else:
                    print("Something went wrong when converting mention")
        else:
            print("Something went wrong")

    data = pd.DataFrame(converted_triples, columns=['subject_values', 'predicate', 'object_values'])

    gen_jointgt_input_format(data, output_file, mapping_dict)


def combine_jointgt_events(filepaths, output_file):
    """
    Combine the created json files for events together
    :param filepaths: path to the folder which has the events jsons
    :param output_file: Path to the output file
    :return: None
    """

    full_data = []
    for i, instance in enumerate(filepaths):
        instance = json.load(open(instance))

        if isinstance(instance, list):
            instance = instance[0]

        instance['id'] = i
        full_data.append(instance)

    with open(output_file, "w") as json_out:

        json.dump(full_data, json_out, indent=2)

        print("Done and saved")
