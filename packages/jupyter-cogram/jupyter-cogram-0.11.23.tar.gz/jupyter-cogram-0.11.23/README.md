<a href="https://cogram.com">                                                        
<img src="https://uploads-ssl.webflow.com/61294dc1bd225d7c490b4389/61937bb4a85d5300ca43795b_Cogram_2COlr.png" 
width="250" align="right"/>
</a>

# Cogram: Intuitive coding with natural language

Cogram brings intuitive coding with natural language to Jupyter Notebook.

[![pypi Version](https://img.shields.io/pypi/v/jupyter-cogram.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/jupyter-cogram/)
[![Cogram on Slack](https://img.shields.io/badge/Slack-pink.svg)](https://join.slack.com/t/cogram-community/shared_invite/zt-wkr7493p-gv6h~KLrTaCm8fdlEd024Q)

## 📖 Documentation

| Documentation              |                                                                |
| -------------------------- | -------------------------------------------------------------- |
| 🚀️ **[Sign up]**        | Sign up to get your API token and get started!              |
| ⭐️ **[How to]**        | New to Cogram? Check out our videos!              |
| 📚 **[Community]**      | Have questions our comments? Join our Slack!                             |

[sign up]: https://get.cogram.com
[how to]: https://www.youtube.com/channel/UCS8ERxnoWV1w-hBgXc93Jfw
[community]: https://join.slack.com/t/cogram-community/shared_invite/zt-wkr7493p-gv6h~KLrTaCm8fdlEd024Q

## Features

- AI-powered coding for Jupyter Notebooks
- Supports Python: ideal for data science tasks
- Cycle through different suggestions

## ⏳ Install cogram

### Requirements

- **API token**: If you don't have one yet, [sign up]
- **Operating system**: macOS · Linux · Windows
- **Python version**: Python 3.6+ (only 64 bit)
- **Package managers**: [pip]

[pip]: https://pypi.org/project/spacy/
[conda]: https://anaconda.org/conda-forge/spacy

### Installation

The easiest way to install Cogram for Jupyter Notebook is using pip.

```bash
pip install -U jupyter-cogram
jupyter nbextension enable jupyter-cogram/main
```

Next, you should install your API token available on your 
[My Account](https://get.cogram.com/account) page. Install it with

```bash
python -m jupyter_cogram --token YOUR_TOKEN
```

That's it! You can now start a new Jupyter Notebook server with 
```bash
jupyter notebook
```

and you're ready to go!


### Updating Cogram

The easiest way to upgrade to a new version of Cogram is using pip:

```bash
pip install -U jupyter-cogram
```

You'll then have to kill any active Jupyter Notebook servers and start a new one with 
```bash
jupyter notebook
```

### Uninstalling Cogram

To remove Cogram from your system, simply use pip:

```bash
pip uninstall jupyter-cogram
```

Finally, remove Cogram from the list of extensions Jupyter will load when you 
start a Notebook:
```bash
jupyter nbextension disable jupyter-cogram/main
```

## 📚 Use Cogram

### 🛫 First start

If you've installed Cogram by following the instructions on your [My Account](https://get.cogram.com/account) page your API token
will automatically be saved. You can open a Jupyter Notebook and get started.  

You may be asked for your API token when you open a new Notebook for the first time. If this happens, paste the API token from your [My Account](https://get.cogram.com/account) page into the prompt box that opens when you start a new Jupyter Notebook.

The Cogram extension is on by default. You can toggle the extension off and on by clicking the Cogram button 
(<img align="center" width="14" src="https://uploads-ssl.webflow.com/61294dc1bd225d7c490b4389/6131d7249979f73249363dd0_icon_black_64.png" />) in the toolbar of your Jupyter Notebook. The green circle indicates that Cogram is on. 
  
### 🔮 Working with Cogram

You can use Cogram in two ways:

- Generating code from plain language by writing a comment and completing with the Tab key
- Comleting code you've written with the Tab key

The status light will turn orange indicating that Cogram is busy. 
 
For example, writing the comment
```python
# fibonacci sequence
```
and hitting the Tab key will generate a function that produces the Fibonacci sequence.

Alternatively, writing the code
```python
def fibonacci
```
and hitting the Tab key will complete the function to produce the Fibonacci sequence.
 
Once your code has been generated you can explore different options with the ← and → keys. 
If you're happy with a suggestion you can accept it with the Tab key.

### 💡 Tips for working with Cogram

Cogram works especially well if you give it some context. Cogram knows the code in your notebook above the current position of your cursor. 
The more code you've already written, the better Cogram will work.

### 📚 Support 

For help with Cogram please join our support channel in [community].
