# detector-camera-system

Submodule for a Beta version of material detector machine.

This code will run in a RaspberriPi 4b

## Authors

David Tertre Boye


## Init Project

Crear entorno virtual

```bash
python3 -m venv .venv
```

Activar entorno virtual

```bash
source .venv/bin/activate
```

Instalar dependecias

```bash
pip install hatchling

pip install -e .
```


## more

Laton -> amarillo
cobre -> rojo
zinc -> plata


## Artificial vision.

### Steps to differentiate colors

1. Resize image

2. Segment image (get a boolean matrix that clasificates pixels if they are important or not)

3. When you have the important pixels you need an algorythm that classify if its a material or is another material. Methods:

    -  Mean Color (its simple).

    - train a neural network. We give a array of colors and its determine wich color is it. feedforwad nn if we give a list. convolutional network if we give a matrix.

    - Other tradicional filters.

# Metodo 1

Recoleccion de imagenes diferentes, sabiendo el material que hay en cada una. Etiquetar las imagenes. copper_001.png, y asi sucesivamente.

Cuando Tenemos una muestra considerable de imagenes tenemos definido el algoritmo de determinacion del color medio de una imagen, se debe sacar el color medio de todas las imagenes en conjunto, y asi sabremos el color medio del material.

Sabiendo el color medio de los diferentes materiales, cuando pasemos una foto y calculemos el color medio, elegiremos el material al que pertenece segun a cual color medio se aproxima mas.
