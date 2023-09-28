# autoluft-etl
This ETL is under construction.

[Temporary Tableau Link](https://public.tableau.com/views/autoluft-etl/TrafficinBerlin?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link) 
## Introduction
Traffic in Berlin is monitored by the ["Verkehrsinformationszentrale Berlin" (VIZ)](https://viz.berlin.de) . Via infrared sensors they count vehicles and measure their speed at various station throughout Berlin. The data generated from their traffic detection system is provided at their [API endpoint](https://api.viz.berlin.de/daten/verkehrsdetektion), which is available under the [Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de-by-2.0)](https://www.govdata.de/dl-de/by-2-0). 
The data is lacking an analysis as their "Verkehrsanalyse" returns a 404 on their website. Therefore this project will provide an ETL (extract, transform, load) pipeline to aggregate the data from the API, transform it into a suitable data model and visualize it. Geospatial data of Berlins district is added to the model from [Geoportal Berlin / bezirksgrenzen](https://daten.odis-berlin.de/de/dataset/bezirksgrenzen/).

# Methods

## Data model
The monthly datasets from VIZ will be aggregated into one dataframe called fact_table. The "mq_name" column contains the name of a sensor station which is made up out of two sensors for each direction of traffic. This id will be used to connect to the dataset "Stammdaten_Verkehrsdetektion_2022_07_20.xlsx" which contains the location data of the sensor stations, and will be called location_dim. The latitude/longitude information is used to identify in what district the sensor station is located.

![Data model for autoluft-etl showing the relationships between the transformed datasets](https://github.com/SonShua/autoluft-etl/blob/main/data_model.jpg)
## Tech Stacks
The main logic in this project will be written in Python and the code will be deployed in a [mage](https://www.mage.ai/pipeline). It is designed to run locally but I will provide endpoints in the pipeline to export the data to the Google Cloud Platform and Google BigQuery. 
The visualization of the data is done in Tableau Public.

### Installation
Clone the repo  
`git clone https://github.com/SonShua/autoluft-etl.git`  

Create a virtual environment  
`python -m venv .venv`  

Activate the virtual environment (on Windows)   
`.venv\Scripts\activate`  

Install wheel   
`python -m pip install wheel`  

Install other requirements  
`python -m pip install -r requirements.txt`  

Create data folder  
`mkdir data`

### Running the mage pipeline
Go into mage folder  
`cd mage-etl`  

Run mage  
`mage run`  

If your machine can't run the mage pipeline due to limiting RAM you can also run the jupyter notebook pipeline which is located in the 'alternative' folder

### Mage pipelines
You will find the two pipelines  
* `get_trafficdata_transform_to_facttable_datetimedim`  
* `get_traffic_sensor_location_to_locationdim`  

both with the variations  `_locally` and `_bigquery`.

The `_locally` will save the cleaned data in the root data folder while `_bigquery` is preconfigured to upload to Google BigQuery. The code in the export function need to be adjusted to reflect your dataset_id and dataset name on BigQuery.
#### Notes on BigQuery Upload
You need to have a properly configured [Google Service Account](https://cloud.google.com/compute/docs/access/service-accounts) and pass it to mage-ai. You can find additionally information [here](https://docs.mage.ai/integrations/databases/BigQuery).



