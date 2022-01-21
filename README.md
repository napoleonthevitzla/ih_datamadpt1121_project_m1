# Show my bike! - IronHack Proyect
Ironhack Madrid - Data Analytics Part Time - January 2021 - Project Module 1 - Antonio Huerta
<p align="left"><img src="https://cdn-images-1.medium.com/max/184/1*2GDcaeYIx_bQAZLxWM4PsQ@2x.png"></p>

## BRIEFING  📌

Create a Python App (**Show my bike!**) that allow their potential users to find the nearest BiciMAD station to a set of places of interest.

There are 2 main datasources:

- **Azure SQL Database.** The database contains information from the BiciMAD stations including their location (i.e.: latitude / longitude). In order to access the database you may need the following credentials:
```
Server name:   sqlironhack
Database:      BiciMAD
```
- **API REST.** We will use the API REST from the [Portal de datos abiertos del Ayuntamiento de Madrid](https://datos.madrid.es/nuevoMadrid/swagger-ui-master-2.2.10/dist/index.html?url=/egobfiles/api.datos.madrid.es.json#/), where you can find the __Catálogo de datos__ with more than 70 datasets.

**Show my bike!** create a `Bicimad_AH.csv` file in "data" folder with a table of data. The info of the table will be all results by default but user can also choice the nearest BiciMAD station.


## Getting ready

These instructions will allow you to get to know the project and how it is works a little better.


### WorkFlow Description  📋

**Show My Bike!** ---- **Performing Process**

1st Data Extraction:
- We extract data with City Council (Data_Public_School and Data_Kinder_garden).
We incorporate data to identify each dataset in the ""Type of Place"" column

For them we will apply the following functions:
**getdata_public_school
getdata_escuelas_infantiles**

- We extract data from Bicimad source
For them we will apply the functions:
**GetData_Bicimad** ((includes the to_mercator function to identify geographic points of all bicimad data)

2º We add parameters and formulate the necessary information to be able to calculate distances:
For them we will apply the following functions:
**concat_dataset_ayuntamiento** (includes the to_mercator function to identify geographical points of all City Hall data)
**concat_dataset_project** (includes the Distance_M function to add to dataset the distance in m)

3º We obtain the solution:
We obtain the information by applying the following functions:
**Result_all**
**Result_one**
**Arg_parse**

ShowMybike will save a file in your data folder called ""location_mas_cercana.csv"" or ""Allbotications.csv"""


**Project WorkFlow image***
<p align="left"><img src="https://drive.google.com/file/d/1j0_XNpKh5O8BM5DFSg92UvRLc6AXmTRI/view?usp=sharing"></p>



### Into the box - Folders & files  📦

In This repo you will find the following folders:

- Data - Where info from source is hosted as bicimad.
- Result - Here you will find the result of your exercise
- Modules - Where you will find functions scripts
- Notebook - Here you will find main.py to exectute Showmybike

* You will also find 
**Project image***
<p align="left"><img src="https://drive.google.com/file/d/1aSxouxrdJIB3r3FS5kcgvT-RagOKrqM9/view?usp=sharing"></p>


### Requirements: Install libraries ⚙️

You will need to install the following libraries in your project enviroment to execute **ShowmyBike**

- [Python 3.7](https://www.python.org/) - Lenguaje principal

- [Azure SQL Database](https://portal.azure.com/)

- [Requests](https://requests.readthedocs.io/)

- [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/index.html)

- Module `geo_calculations.py`

- [Argparse](https://docs.python.org/3.7/library/argparse.html)

- [Numpy](https://docs.python.org/3.7/library/argparse.html)

- [Sys](https://docs.python.org/3.7/library/argparse.html)

- [Os](https://docs.python.org/3.7/library/argparse.html)


## Deployment 🚀

Follow this instructions to execute the program from your terminal:

To execute the program you must open your terminal and access the Notebook folder and run the following command:

```>>> Python Main.py.```

You can also execute including the default value, obtaining the same result as the previous statement:

```>>> Python Main.py -Excution nearest```

The program will request the user from the Input of the Child School or the Public School to identify Bicimad Stations.

```Example: INPUT >> Municipal Children's School Doña Francisquita```

By default, the program will install a document called **Bicimad_Ah.cvs** in the **Data** folder with the result of the nearest station.

To obtain the information of all the seasons close to a point you will be executed the following command:

```>>> Python Main.py -Excution nearest```

The program will install a document called **Bicimad_Ah.cvs** in the **Data** folder with the result of all bicimad stations.


### Documentation 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en esta [Presentación](https://github.com/tu/proyecto/wiki)


### Tools & Frameworks 🛠️

This tools help me to works better: 

* [Python](https://www.python.org/) - Lenguaje principal
* [Jupyter Notebook](https://jupyter.org/) - Usado como editor de código.
* [GitHub](https://jupyter.org/) - Usado como repositorio de código.
* [Trello](https://trello.com/) - Usado para la gestión y documentación del proyecto.
* [Visual Studio Code](https://code.visualstudio.com/) - Usado como editor de código.
* [Swagger](https://datos.madrid.es/nuevoMadrid/swagger-ui-master-2.2.10/dist/index.html?url=/egobfiles/api.datos.madrid.es.json) - Usado para extraer el data de Ayuntamiento source.
* [Azure SQL Database](https://portal.azure.com/) - Usado para extraer el data de bicimad source.


### Thanks to 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 😊.
* etc.


### Author ✒️

* **Antonio Huerta** - *Proyecto 1 IronHack*: Showmybike
---
⌨️ con ❤️ por [Antonio Huerta](https://github.com/napoleonthevitzla)🤓