# Set up a virtual environment for the course

Below are instructions to install, update, and use the correct python programming environment for the course. We'll walk through this during the first section meeting, but here's the compressed version for those who want to get a head start.

## Concepts

This course uses python. Specifically, we'll use python in conjunction with Jupyter notebooks, which are documents that integrate code, outputs, and documentation in a single file.

To make this work, you need a few things:

1. A **package manager** that installs and updates the python software that you need. In our case, the package manager is `conda` (not to be confused with the Anaconda distribution of python, though `conda` is an Anaconda product and often installs python software distributed by Anaconda).
1. A **python environment**, including an interpreter that executes python code. If you type `python` at the command line, you're invoking the python interpreter, but that's not the only way to interact with it. In fact ...
1. A **Jupyter server** that renders Jupyter notebooks, passes code to the interpreter, and receives output back from the interpreter. (I'm waiving my hands here a bit, because the actual rendering is handled by a web browser or similar front end.)

Note that, when you're working with Jupyter notebooks, you're typically looking at a web browser that's displaying content served by a Jupyter server, which in turn is interacting (behind the scenes) with a python interpreter (also called a *kernel*). In most cases (including our work for this class), the browser, Jupyter server, and python kernel are running on the same machine (your laptop, for example). But this needn't always be the case. [Google Colab](https://colab.research.google.com/) is an example of a Jupyter server and kernel system that runs in the cloud.


## Setup details

To get things set up, you're going to:

1. Install `conda` (or confirm that it's already installed on your system)
2. Use `conda` to install python and the handful of libraries that you'll need for the course into a new virtual environment (so that it's isolated from anything you might do with python for other classes or projects)
3. Activate your new python environment
4. Start a JupyterLab server, which will allow you to work with Jupyter notebooks.

**Everything below happens in a terminal window/command prompt.**

  * Open a terminal window and run `conda update conda`. (On Windows, you might have to open an "Anaconda command prompt" or similar, if you already have `conda` installed.) If it works, move to the next step. If not, download and install [`miniconda`](https://docs.conda.io/en/latest/miniconda.html).
  * Download the course package list file from GitHub (`info-3350-packages.txt` in this `setup` directory). Pay attention to where you've saved it. Then:


```
conda update conda
conda config --add channels defaults
conda config --append channels conda-forge
conda create --name 3350 --file info-3350-packages.txt
```

  * Install some data files. You can skip the last line (installing spaCy's `en_core_web_lg` model) for now if you're tight on disk space.

```
conda activate 3350
python -m nltk.downloader omw-1.4 punkt sentiwordnet snowball_data stopwords treebank vader_lexicon
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg
```

Move on to the next section to test your installation.

## Daily use

  * From now on, **always and only** run `conda` (to install/update packages) and JupyterLab (to use your python environment) from the command line. Always first activate the `3350` virtual environment, like so:

```
conda activate 3350
jupyter lab
```

* If you need to update your install during the semester (unlikely, but not impossible), first re-pull the package list from GitHub, then:

```
conda update conda
conda activate 3350
conda update --file info-3350-packages.txt
```

If we add any packages to the list (possible during the second half of the semester), you'd also need to run `conda install --file info-3350-packages.txt` as a final step to install those newly added packages.

## The filesystem

Lectures, problem sets, projects, and other course material will be distributed as Jupyter notebook files. These files, if you ever have occasion to inspect them in a text editor, are just JSON documents. In the same way that raw HTML files look like plain text with a lot of angle brackets and so on, but become rendered web pages when displayed in a browser, so too are Jupyter notebooks only really useful when rendered (unless you're a developer of the underlying system).

You need to be able to *find* your Jupyter notebook files and *open* them in a running instance of JupyterLab. **Make sure you understand where these files live on your computer.** You'll need to open them via JupyterLab's built-in file browser. You'll also need to access them via your OS and/or browser's file picker in order to upload them to CMS for grading.
