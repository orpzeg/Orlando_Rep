
# XML and Directory Analyzer

This repository contains a collection of Python scripts designed to process XML files, scan directories, retrieve file metadata, and save processed data to both JSON and MongoDB.

## Features

- XML Processor: Extracts data from XML files and augments the data with additional command-line provided metadata.
- Directory Scanner: Scans a specified directory to gather detailed properties of each file. This includes file size, date modified, date created, file type, and more.
- Command Runner: Executes shell commands and captures their outputs.
- Unit Tests: Tests to verify the correctness of the command outputs.

# Getting Started

## Prerequisites

- Python 3.x
- MongoDB (if leveraging database functionality)
- 'win32api'and 'win32com' packages for handling Windows-specific file metadata
- 'pymongo' for MongoDB interactions.
## Installation

1. Clone the repository to your local machine:
```bash
  git clone https://github.com/orpzeg/Orlando_Rep
```
2. Navigate to the project directory and install the necessary modules:
```bash
  pip install -r requirements.txt
```
3. Each utility is designed to be standalone. Navigate to the specific tool's directory and follow any in-script documentation or guidelines for usage.
## Testing

Unit tests are available for the Command Runner utility. To execute them, navigate to the project directory and run:
```bash
  python -m unittest
```


## Contribution

Feedback, improvements, and pull requests are always welcome. Please follow standard Git practices: fork the repository, make your changes in a separate branch, and then submit a pull request.


## License & Acknowledgements

This repository is open-source and free to use under the MIT License. Contributions, suggestions, and enhancements are welcome.

[MIT](https://choosealicense.com/licenses/mit/)

