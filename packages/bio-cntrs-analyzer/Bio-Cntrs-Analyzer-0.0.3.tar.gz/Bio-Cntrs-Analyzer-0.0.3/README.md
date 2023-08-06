# BCAnalyzer: Segmentation of patchy areas in biomedical images based on local edge density estimation

## Installation from binaries

```bash
pip install -U bio-cntrs-analyzer
```
## Build exe from source

```bash
pip install cx_Freeze
python setup.py build
```
## User manual

For starting appliation evualate in command line (terminal) the next command:

```bash
bcanalyzer
```

![UserManualFigure](images/UserManualFigure.PNG) 

Software user interface outline: (A) list of images submitted for the analysis; (B) segmentation algorithm options; (C) color channel import options; (D) selected image with on-the-fly with marked-up visualization of the segmentation results; (E) segmentation algorithm controls for online adjustment of sensitivity and resolution; (F) file export menu.

The typical algorithm of user interaction with the software is as follows:

* Selected images are imported by their drag-and-drop onto the program window. The image list appears in **A**.
* Global algorithm options can be adjusted in **B** and color channels for the analysis selected in **C**.
* The image selected in the list **A** is displayed in **D** with immediate effect of the segmentation algorithm visualized (using default parameters during the first run).
* Next the algorithm parameters (sensitivity and resolution) can be adjusted manually in **E**. Segmentation results are visualized on-the-fly for direct user control. Of note, global options and color channel selection can be readjusted at this stage as well. Following adjustment, the chosen algorithm parameters can be applied either to the entire imported image set, or solely to the currently analyzed image, with corresponding controls available in **E**.
* Once the algorithm parameters are adjusted for either a single or a few representative image(s), further processing and export can be performed as a fully automated procedure for the entire image set using file export options in **F**. Export options include visualizations of segmentation results, either as binary masks or as marked-up images similar to those appearing on the screen during analysis, as well as a *.csv table with summary statistics.

# Dataset

Link to downloading dataset:

https://drive.digiratory.ru/d/s/mrbRyk4HyFbOIEANc6DhQGxhCFNgq3xI/Jqbcbsq_eE5Cf8-bnJaM3dXL6RI1v7d7-d74AOY4RLgk

If something goes wrong, please, write to amsinitca[at]etu.ru

# Citation

If you find this project useful, please cite:

```bib
```

