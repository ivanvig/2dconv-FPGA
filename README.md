# 2D Convolution Hardware Implementation

## About this repo

This is the code corresponding to the implementation of the hardware design described in [this paper](docs/PROJECT_DOC.pdf). It takes into account the reduced amount of memory available in the FPGA and makes an efficient use of those resources. It also achieves high throughout due to the pixel parallel processing.

<p style="text-align: center;">
<img src=docs/schematics/general-blockdiagram.png width=75%>
  
*Simplified block diagram of the system.*
</p>

For a more detailed design description see [this](docs/pps.pdf) (in Spanish)

## Publication

The hardware design implemented here was published in Argentina's [CASE 2018](http://www.sase.com.ar/case18/ ) as a technical forum. The paper in this repository can also be found in [CASE 2018 Collection of articles](https://drive.google.com/file/d/1yCnoOdT11zj-F6tbj7h3EdRZK2gGX1SY/view)

### Cite
If you use Containernet for your research and/or other publications,
please cite the following paper to reference our work:

```bibtex
@article{2dconv-FPGA,
author  = {Martin Casabella and Sergio Sulca and Ivan Vignolles and Ariel Pola},
title   = {Dynamic Reuse of Memory in 2D Convolution Applied to Image Processing},
journal = {CASE},
year    = {2018},
pages   = {145-150},
isbn    = {978-987-46297-5-3},
month   = {8},
note    = {\url{https://drive.google.com/file/d/1yCnoOdT11zj-F6tbj7h3EdRZK2gGX1SY/view?usp=sharing}}
}
```

## Authors

- [Ivan Vignolles](https://github.com/martincasabella)
- [Martin Casabella](https://github.com/martincasabella)
- [Sergio Sulca](https://github.com/ser0090)
- [Ariel Pola](https://github.com/apola83)
