# CETONI SiLA 2 Core SDK
## Installation
Run `pip install .` from the root directory containing the file `setup.py`

## Usage
Run `python -m sila_cetoni_core --help` to receive a full list of available options

## Code generation
- generate
  ```console
  $ python -m sila2.code_generator new-package -n core_service -o ./sila_cetoni/core/sila/ ./sila_cetoni/core/features*.sila.xml
  ```
- update
  ```console
  $ python -m sila2.code_generator update -d ./sila_cetoni/core/sila/ ./sila_cetoni/core/features*.sila.xml
  ```
