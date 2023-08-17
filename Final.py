import xml.etree.ElementTree as ET
import json
import argparse
import os
from pymongo import MongoClient


def process_node(node, node_dict, final_list, depth=0):
    node_attributes = node.attrib
    transformed_dict = {}
    for key in node_attributes.keys():
        new_key = f'{node.tag}@{key}'
        transformed_dict[new_key] = node_attributes[key]
    node_dict.update(transformed_dict)
    if node.text and node.text.strip():
        node_dict[node.tag + "@" + "Text"] = node.text.strip()
    for child in node:
        process_node(child, node_dict, final_list, depth + 1)
    if len(node) == 0:
        final_list.append(node_dict.copy())
    for key in node_attributes.keys():
        transformed_key = f'{node.tag}@{key}'
        if transformed_key in node_dict:
            del node_dict[transformed_key]
    node_text_key = node.tag + "@" + "Text"
    if node_text_key in node_dict:
        del node_dict[node_text_key]


def main():
    parser = argparse.ArgumentParser(description='Process an XML file and generate a JSON output.')
    parser.add_argument('--xml_directory', type=str, help='Path to the directory containing XML files')
    parser.add_argument('--json_file', type=str, help='Path to the output JSON file')
    parser.add_argument('--db_name', type=str, help='Name of the MongoDB database')
    parser.add_argument('--collection_name', type=str, help='Name of the MongoDB collection')
    parser.add_argument('--connection_string', type=str, default='mongodb://localhost:27017/',
                        help='MongoDB connection string')
    args = parser.parse_args()

    final_list = []
    for filename in os.listdir(args.xml_directory):
        if filename.endswith(".xml"):
            tree = ET.parse(os.path.join(args.xml_directory, filename))
            root = tree.getroot()

            node_attributes_dict = {}
            process_node(root, node_attributes_dict, final_list)

    with open(args.json_file, 'w') as f:
        json.dump(final_list, f)

    client = MongoClient(args.connection_string)

    db = client[args.db_name]
    collection = db[args.collection_name]

    collection.insert_many(final_list)


if __name__ == "__main__":
    main()
