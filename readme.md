# Cost of Living Dashboard

## DESCRIPTION:

This repo contains all the code for the Cost of Living Dashboard. The dashboard is a Plotly Dash web app that uses sql
lite as it's database.

## INSTALLATION

### Recommended Install and execution (Docker)

The recommended method for installation is using docker compose. The docker compose file contains a docker container to
build and start the Dash app, and second container with nginx to manage traffic.

From a terminal window at the root level of this project run the following command.

    sudo docker-compose up --build --force-recreate --no-deps

The app should be live on [http://localhost:1234/]()

### Alternative installation method

You can also use a python 3.11 environment locally to install this project. The following commands will install the
required packaged and run the dash app.

    pip install -r requirements.txt

### Live web server

We also have the app running on a live web server which can be found here.

[https://cost-of-living-project.onrender.com/]()

## EXECUTION

If running locally, once the packages are installed use the following command to start a development server for the Dash
app.

    python app.py

The app should be live on [http://localhost:8080/]()

# Project Notes

## Tech stack and package notes

* Dash (uses Flask)
* Plotly
* dash bootstrap components (adds bootstrap css)
    * add any bootstrap class to "classname" of the html components.
* Pandas - integrates well with plotly
* Dash Tables
* SQLite - with sqlalchemy and pandas sql support

### app.py

Contains the app creation, layout for the tabs, and registers callbacks for tab selections.

See the example_tab.py example for how to set up each tab. You need to have a function that exports a layout when the
tab is first selected. And a function that registers all callback for UI interactions within the tab.

### Common Inputs

In order for the dashboard to work seamlessly across the different tabs, common input elements are used and are found in
tabs/summary/inputs.py. These inputs are hidden and shown based on what tab is selected in the app.py file.

### "tabs" folder

To make is easy to develop in parallel each cost of living component has it's own tab folder where the inputs and
interactions and visualizations can be developed. Each tab has a function that returns a layout and another function to
register callbacks which is integrated into app.py.

### "Database" folder

Sqlite database with sqlalchemy interface, or pandas

* contains the sqlite database file (data.db)
    * please add a prefix to your tables so they are grouped together
* database.py
    * contains a DB class for interacting with the database
    * there are 2 helper functions
        * Read full table to pandas df
        * Read SQL to pandas df (if you want to handle mergers, joins, data reduction in sql statements)
        * Feel free to add more as needed
    * function to read data and format as need for your dashboard
        * try to keep these grouped by tab for organization
* folder for each tab section for importing data to the database
    * you can add any data import scripts here. See "import_tax_data.py" as an example
    * **make sure to not commit large data files to the github!!**

### Development tips

I find it much easier to develop the plotly graph locally in something like jupyter notebook with variables for the
inputs. Once you get the charts dialed in then integrate into the dashboard with proper inputs and callbacks.


