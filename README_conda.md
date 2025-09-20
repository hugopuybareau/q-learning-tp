
## Installation environnement virtuel avec conda

[Conda](https://docs.conda.io/en/latest/) est un système de gestion de package permettant l'installation de multiples versions de logiciels au travers d'un mécanisme d'**environnements virtuels**. Vous pouvez ainsi isoler vos différents projets Python dans des environnements virtuels différents. Chaque environnement virtuel utilisera la version souhaitée de Python et des packages associés pour votre projet.

> Conda is an open source package management system and environment management system 
for installing multiple versions of software packages and their dependencies and 
switching easily between them. It works on Linux, OS X and Windows, and was created 
for Python programs but can package and distribute any software.



### 1. Installation d'Anaconda ou de miniconda

Vous pouvez au choix installer [Anaconda](https://www.anaconda.com/products/individual), qui contient le gestionnaire de paquet Conda, plus les bibliothèques scientifiques, un environnement de développement … ou uniquement le gestionnaire de paquet Conda appelé [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

Pour Anaconda, suivez les consignes sur leur site. Pour Miniconda, suivez les consignes ci-dessous:

> [Miniconda](https://docs.conda.io/en/latest/miniconda.html) is a free minimal installer for conda. 

**Télécharger** la denrière version de`miniconda` correspondant à votre système.

|        | Linux | Mac | Windows | 
|--------|-------|-----|---------|
| 64-bit | [64-bit (bash installer)][lin64] | [64-bit (bash installer)][mac64] | [64-bit (exe installer)][win64]
| 32-bit | [32-bit (bash installer)][lin32] |  | [32-bit (exe installer)][win32]

[win64]: https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe
[win32]: https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86.exe
[mac64]: https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
[lin64]: https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
[lin32]: https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86.sh

**Installer** [miniconda](http://conda.pydata.org/miniconda.html) sur votre machine:

- **Linux:** https://conda.io/projects/conda/en/latest/user-guide/install/linux.html
- **Mac:** https://conda.io/projects/conda/en/latest/user-guide/install/macos.html#install-macos-silent
- **Windows:** https://conda.io/projects/conda/en/latest/user-guide/install/windows.html

### 2. Creation et activation d'un environnement

Dans la suite, 
* pour Mac et Linux, les commandes sont à faire dans un terminal classique. 
* Pour Windows, il faut utiliser **Anaconda prompt** et pas un terminal de commande classique (taper "Anaconda Prompt" dans la barre de recherche Windows). 

Pour tous les OS:

Créer (et activer) un nouvel environnement, par exemple appelé `tppacman` avec Python 3.10. 

```
conda create --name tppacman python=3.10
conda activate tppacman
```

A ce niveau, votre ligne de commande doit ressembler à : `(tppacman) <User>: `. 

`(tppacman)` indique que l'environnement créé est actif, et vous pourrez maintenant installer des packages dans l'environnement si besoin.

Vous pouvez lister les environnements installés :
```
conda env list
```
Vous pouvez lister les packages installés dans l'environnement actif :
```
conda list
```
et installer d'autres packages dans votre environnement local si besoin.

