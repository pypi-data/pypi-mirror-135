# TigerGraph ML Workbench

`tgml` provides a python toolkit for machine learning practitioners to integrate TigerGraph into their existing workflow. The core component of `tgml` is the graph loader, which behaves like a data loader for typical machine learning tasks. Putting differently, users can write their model training code as before but only replace the previous data loader with our graph loader; they will get batches of graph data for training as if the data is read from their local disk. `tgml` also provides syntactic sugar to the graph data processing APIs, so users can run algorithms such as PageRank on their graphs in TG as calling a normal Python function. Under the hood, `tgml` takes care of all the communications with the Graph Data Processing Service and convert the final output to a format that users need (dataframes and PyG graphs for now).

See the [tutorial notebooks](https://github.com/TigerGraph-DevLabs/tgml/tree/main/docs/examples) in the docs/examples folder on how to use the package. For `tgml` to work, the [Graph Data Processing Service](https://github.com/TigerGraph-DevLabs/GDPS) has to be running on the TigerGraph server. 

### Getting Started
Install from pypi 
```
pip install tgml
```

Install from github for the hottest changes:
```
pip install git+https://github.com/TigerGraph-DevLabs/tgml.git -f https://data.pyg.org/whl/torch-1.10.0+cpu.html
```
