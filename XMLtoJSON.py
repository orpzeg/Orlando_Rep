import xml.etree.ElementTree as ET
import json
import argparse
import os
from pymongo import MongoClient


class XMLProcessor:
    def __init__(self, xml_directory):
        self.xml_directory = xml_directory
        self.final_list = []

    def process_node(self, node, node_dict, depth=0):
        """Recursively process XML node and its children."""
        node_attributes = node.attrib
        transformed_dict = {f'{node.tag}@{key}': value for key, value in node_attributes.items()}
        node_dict.update(transformed_dict)

        if node.text and node.text.strip():
            node_dict[node.tag + "@" + "Text"] = node.text.strip()

        for child in node:
            self.process_node(child, node_dict, depth + 1)

        if len(node) == 0:
            self.final_list.append(node_dict.copy())

        for key in node_attributes.keys():
            del node_dict[f'{node.tag}@{key}']

        if f'{node.tag}@Text' in node_dict:
            del node_dict[f'{node.tag}@Text']

    def process_xml_files(self):
        """Process all XML files in the given directory."""
        for filename in os.listdir(self.xml_directory):
            if filename.endswith(".xml"):
                tree = ET.parse(os.path.join(self.xml_directory, filename))
                root = tree.getroot()
                node_attributes_dict = {}
                self.process_node(root, node_attributes_dict)


class DataSaver:
    def __init__(self, data, args):
        self.data = data
        self.args = args

    def add_additional_data(self):
        """Add additional data from arguments to the data list."""
        for value_dict in self.data:
            value_dict.update({
                'build_number': self.args.build_number,
                'jobid': self.args.jobid,
                'platform': self.args.platform,
                'is_test': self.args.istest,
                'branch': self.args.branch
            })

    def save_to_json(self):
        """Save data to a JSON file."""
        with open(self.args.json_file, 'w') as f:
            json.dump(self.data, f)

    def save_to_mongo(self):
        """Save data to a MongoDB collection."""
        client = MongoClient(self.args.connection_string)
        db = client[self.args.db_name]
        collection = db[self.args.collection_name]
        collection.insert_many(self.data)


def main():
    parser = argparse.ArgumentParser(description='Process an XML file and generate a JSON output.')
    parser.add_argument('--xml_directory', type=str, help='Path to the directory containing XML files')
    parser.add_argument('--json_file', type=str, help='Path to the output JSON file')
    parser.add_argument('--db_name', type=str, help='Name of the MongoDB database')
    parser.add_argument('--collection_name', type=str, help='Name of the MongoDB collection')
    parser.add_argument('--connection_string', type=str, default='mongodb://localhost:27017/',
                        help='MongoDB connection string')
    parser.add_argument('--build_number', type=str, default='',
                        help='Build Number + Platform')
    parser.add_argument('--jobid', type=str, default='',
                        help='Job Id')
    parser.add_argument('--platform', type=str, default='',
                        help='Platform')
    parser.add_argument('--istest', type=str, default='',
                        help='Is Test?')
    parser.add_argument('--branch', type=str, default='',
                        help='Branch name')

    args = parser.parse_args()
    processor = XMLProcessor(args.xml_directory)
    processor.process_xml_files()

    saver = DataSaver(processor.final_list, args)
    saver.add_additional_data()
    saver.save_to_json()
    saver.save_to_mongo()


if __name__ == "__main__":
    main()
