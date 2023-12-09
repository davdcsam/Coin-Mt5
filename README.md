Coin (codename 3doors)
==========================

Coin is a user interface application developed with DearPyGui that connects to the MetaTrader5 API. This application allows users to interact with the MetaTrader5 API in a more user-friendly and visual way.

The functionality is to be able to send an order of type ORDER_TYPE_BUY or ORDER_TYPE_SELL with lot, stoploss and take profit in a moment of time terminated by a start time and end time.

Requirements
----------

- Python 3.11.4
- Pipenv

Installation
-----------

1. Make sure you have Python 3.11.4 installed on your system. You can check your Python version with the following command:

``` Bash
python --version
```

1. Install Pipenv, which is a packaging tool for Python. You can install it with the following command:

``` Bash
pip install pipenv
```

1. Clone the Coin repository:

``` Bash
git clone https://github.com/davdcsam/coin.git
cd coin
```

1. Install the project dependencies with Pipenv:

``` Bash
pipenv install
```

Quick usage
----------

1. Activate Pipenv virtual environment:

``` Bash
pipenv shell
```

1. Run the main Coin script:

``` Bash
python main.py
```

This will open the Coin user interface, where you can interact with the MetaTrader5 API.


Creating an executable file
--------------------------

This project uses PyInstaller to convert the Python script into an executable file. To create the executable file, follow these steps:

1. Make sure you have PyInstaller installed. If you don't have it, you can install it with pip:

``` Bash
pip install pyinstaller
```

1. Run the following command in the root of the project:

``` Bash
pyinstaller --onefile --windowed --name=Coin --icon=assets/coin.ico main.py
```

This command tells PyInstaller to create an executable file from the `main.py` script. The options used are as follows:

- `--onefile`: Creates a single executable file.
- `--windowed`: Suppresses the console when running the application.
- `--name=Coin`: Sets the executable file name to "Coin".
- `--icon=assets/coin.ico`: Sets the icon of the executable file to "coin.ico" located in the "assets" folder.

Copying folders to the dist/ folder
------------------------------------

After creating the executable file, you can copy the `assets/`, `data/`, `files/`, and `build/` folders to the `dist/` folder with the following commands:

For Unix/Linux:

``` Bash
cp -r assets/ data/ files/ build/ dist/
```

For Windows:

``` Bash
xcopy /E /I assets dist/`assets
```

``` Bash
xcopy /E /I data dist\data
```

``` Bash
xcopy /E /E /I files dist\files
```

``` Bash
xcopy /E /E /I build distbuild distbuild
```

These commands will copy the `assets/`, `data/`, `files/`, and `build/` folders into the `dist/` folder.

Documentation
-------------

For more information on how to use Coin, see the [full documentation no available].

Contributions
--------------

Contributions are welcome.

License
--------

Coin is licensed under the a property license. See the `LICENSE` file for details.
