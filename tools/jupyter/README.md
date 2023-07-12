# Planning Permission Notebook

This Jupyter Notebook is designed to help you in understanding planning permissions using the OpenAI API.

## Prerequisites

- Python 3.6 or higher
- git
- pip
- Visual Studio Code with plugin [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) installed

## Quickstart

### 1. Clone the Repository

To get started, you need to clone the repository containing the notebook. Use the following command to clone the repository:

```sh
git clone https://github.com/zilaei/jupyter-workflow.git planning-permission-notebook
cd planning-permission-notebook
```


### 2. Install Dependencies
It's recommended to create a virtual environment to keep the dependencies required by this project separate from your global Python environment.

Create and activate the virtual environment:
```sh
python -m venv planning-env
source planning-env/bin/activate  # On Windows, use `planning-env\Scripts\activate`
```

Use pip to install the required Python dependencies from the requirements.txt file:

```sh
pip3 install -r requirements.txt
```

### 3. Copy Your Document

Copy the document you want to process into the ./data folder within the cloned repository:

```sh
cp path/to/your/document.pdf ./data/
```

### 4 Set up environment variables
Create a file named .env in the root of the cloned repository for environment variables.
There is a file named `.env_example` that can be used as a template:

```text
OPENAI_API_KEY=YOUR_OPENAI_API_KEY

PLANNING_PERMISSION_FILE_PATH=./data/planning_permission_document.pdf

LOGGING_LEVEL=INFO
```

#### 4.1 Set Up API Keys

You'll need an API key from OpenAI for this notebook. If you don’t have a key, you can create one by signing up at OpenAI.

Add your API key to `.env` by setting variable `"OPENAI_API_KEY=your_api_key_here"`. 

Replace your_api_key_here with your actual API key.

#### 4.2 Setup up logging level (optinal)

You can also set up logging level by adding setting variable `LOGGING_LEVEL=INFO` in `.env`.

Replace INFO with your desired logging level (e.g. DEBUG, INFO, WARNING, ERROR, CRITICAL).

#### 4.3 Set Up Document Path
Additionally, you need to specify the file path to your document in the `.env` file by setting variable `"PLANNING_PERMISSION_FILE_PATH=./data/your_document.pdf`.

Replace your_document.ext with your actual document name and extension.

### 5 Run the Notebook

#### 5.1 VS Code
Open notebook project in VS code. 

Select your previously created virtual environemnt by pressing button "Select Kernel" (top right corner).

Press the "Run All" button to run all the cells.

Information about how to use Jupyter in VS code can be found at [Jupyter Notebooks in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).

#### 5.2 Jupyter
Optionally you could run the notebook in Jupyter:
```sh
jupyter notebook
```
This will open the Jupyter Notebook interface in your web browser. Navigate to the planning_permission.ipynb file and open it. 

Select your previously created virtual environment `venv` under menu Kernel -> Change kernel. 

Wait for the Kernel to restart and press the button "Not Trusted" button -> Press "Trust" in the pop-up.

Run all cells by selecting Kernel -> Restart & Run All -> Press "Restart and Run All Cells" in the pop-up.

Wait for all the cells to be run (an asterisk '*' will be displayd for not compleated cells).

More information about how to setup and use Jupyter notebook can be found at [jupyter](https://docs.jupyter.org/en/latest/).

### Troubleshooting

Make sure that:
- You have installed all the dependencies from the requirements.txt file.
- You have set up your `.env` file correctly with the OpenAI API key and the path to your document.