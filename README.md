# IntelliSIEM

IntelliSIEM is a threat intelligence aggregator and reporter designed to enhance SIEM systems. It collects, analyzes,
and reports threat data from various sources to improve security operations.

## Features

- Aggregates threat data from multiple APIs.
- Scores and prioritizes threats based on relevance.
- Generates reports for SIEM integration.
- Includes robust error handling and logging.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/IntelliSIEM.git
   ```
2. Navigate to the project directory and create a virtual environment:
    ```bash
    cd IntelliSIEM
    python3 -m venv .venv
   ```
3. Activate the virtual environment and install dependencies:
    ```bash
    source .venv/bin/activate
    pip install -r requirements.txt
   ```
4. Copy `config_template.yaml` to `config.yaml` and fill in your API keys.
    ```bash
    cp config/config_template.yaml config/config.yaml
   ```

## Usage

To fetch and analyze threat data, run:

```bash
python src/data_collection.py
```

Check the `data/error.log` for any issues encountered during execution.
