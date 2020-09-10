# RCDB Scraper

A simple web scraper/data cleaner for the rollercoaster database site rcdb.com Usable data is found in **/data/rcdb_full.csv** and **/data/rcdb_strict.csv** (see differences below). Code is found in **scraper.py** and **clean_p1.py**.

# Data Collected

- **Metadata**: Coaster Name, Park Name, City, State/Province, Country
- **Design Data**: Type *(Wood or Steel)*, Design *(Sit Down, Inverted, Suspended, Wing, Flying, Stand Up, Bobsled, Pipeline)*, Scale *(Extreme, Thrill, Family, Kiddie)*
- **Specifications**: Length (feet), Height (ft), Max Drop (ft), Max Speed (mph), Number of Inversions, Vertical Angle (degrees), Duration (min:sec)

# rcdb_full vs. rcdb_strict

rcdb.com keeps all coasters, parks, locations, and people in numbered htm files, running from '1.htm' to roughly '18500.htm'.

This scraper iterates through this range, sorting pages into three categories.
- **Coasters**: When a page has the correct amount of data, it is scraped and added to the CSV.
- **Parks**: Whenever the scraper recognizes a park, adds its 'index' (meaning the page name) to a list of parks. Some of these may be anomalies that are falsely recognized as a park
- **Anomalies**: any pages not recognized as a coaster or a park. Some parks may be lost in the anomalies list.

rcdb_full (8,068 entries) and rcdb_strict (1,744 entries) *only* includes coasters
- rcdb_full requires a coaster to have at least one non-NA **Design Data** variable, at least one non-NA **Specification** variable, and a Name which is not 'unknown'
- rcdb_strict requires the same conditions, but also requires Length, Height, Speed, and Inversions to be non-NA.
