# Stitcher
Reconstruction of 3D Surfaces

# Introduction

  Based on ___ ,  we developed a code that could reconstruct a 3D surface given 2D planar contours to start from. The idea is to connect M points in a plane to N points on another plane in the most parsimonious way possible, which is accomplish-able by minimizing the total length of the connection lines. On the process of doing so, the program can also connect contours that belong to a same plane by making connecting their nearest points.
  A few tools have also been used to improve the final surface such as:

      . Artificially improving the resolution by interpolating the coefficients of the Fourier's Series of each contour;
      . Auto-selection of files;
      . Etc

  More text


# Libraries Used

    . Numpy

# The Input

  Input files should be organized as:


  And one should also provide a file containing the order in which the islands should be connected, as the program can not yet decide it in a parsimonious way. This file should be structured as follows:

              {"Stitches3D": [
              {"1":["f1.json","f2.json"],
                "2":[["f3.json","f4.json"],"f5.json"]}
              ],
              "CloseSurface": [
              {"1":[0]}
              ],
              "CloseBifurcation": [{
                "2":[0]
                }],
              "CloseExtra": [{
                "2":[[0,[1]]]
                }],
              "FileDir": "/path/to/conturs/json",
              "OutputDir": "/path/to/out/put/mesh",
              "Name": "BrainReconstruction",
              "MeshObjOutput": BOOLEAN}

  The "Stitches3D" key indicates which contours should be connect, and list means merging the contours only
  in that subroutine.
  The "CloseSurface" key indicates wherer to put a lid on, meaning a plane surface should
  close fill that specific closed contour. Note that the count starts at 0!
  In the given example, files f1 and f2 will stitched together and the plane triangulation to properly
  close the 3d surface will be on files f1 and f5.

# The Output
  ![Brain Example](img/example_result_alpha00.png)
  To get the output, simply call Surface().Vertices() and Surface().Edges(). The output can be saved to an obj file and visualized at any obj viewer, such as [Meshlab](https://metabio.netlify.app).
