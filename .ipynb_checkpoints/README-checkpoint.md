# Ruang Edukasi Indonesia 
It starts with New Zonasi Rule from Govt Indonesia that seems unfair for certain people (based on viral news). This project has a goal to propose new method to determind the Education Region in Indonesia. This project is running within June to Nov 2019. 


Methodology :

    [/] Get The data from scrapping the website (just Elementary School in first trial)
    [/] Get Maps of Indonesia from (here)[https://gadm.org/download_country_v3.html], and visualize it with geopandas -- (gadm36_IDN_2.shp)
    [/] Get The data from scrapping the website (Get All Information table for second trial) -- (20190901_all_sekolah_genap2019_data_latlong.csv)
    [/] Create reference data for convention name -- (reference_our_data_to_map_used.csv)
    [/] Explore the data
    [/] Simulate the Radius Principle
    [/] Voronoi and Clustering (KMeans)


Hierarchy

    |--data
        |--raw
        |--interim
        |--processed
        |--externals
    |--models
    |--notebooks
    |--reports
        |--figures
    |--src
    |--requirements.txt


