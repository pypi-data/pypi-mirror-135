
# Covid API Docs!!
---
---
### `class` *CovidClient*
**Key: `CovidClient.attribute` | `CovidClient.method`**
---
**► Methods:**
- `load_country(country)`
    Type: str
    Args: Name of the Country
    Return: `bool` (True/False)
    Raises: `CountryNotFoundError` if the specified country was not found.
---
**► Attributes:**
`country`
    Return: `str` (Name of the country...if you forgot it after loading it)
`population`
    Return: `int` (Population of the country)
flag_url
    Return: `str` (URL to flag of the country...mostly `png`)
country_id
    Return: `int` (Database id of the country...Not really needed)
total_cases
    Return: `int` (Total number of cases in the country till date)
total_death
    Return: `int` (Total number of deaths in the country till date)
total_recover
    Return: `int` (Total number of patients recovered in the country till date)
total_tests
    Return: `int` (Total number of tests done till date in the country)
active_cases
    Return: `int` (Number of active cases currently in the country...It is of the patients that are either in quarantine or under observation)
critical_cases
    Return: `int` (Number of critical cases currently in the country...It is of the patients who require ventilator and are facing serious problems in breathing)
today_cases
    Return: `int` (Number of cases which were recorded today)
today_death
    Return: `int` (Number of deaths recorded today)
today_recover
    Return: `int` (Number of patients who recovered today)
percent_cases
    Return: `int` (Percentage of cases in the country. Derived like: | [`total_cases`/`population`]*100 |)
percent_death
    Return: `int` (Percentage of deaths in the country. Derived like: | [`total_deaths`/`population`]*100 |)
percent_test
    Return: `int` (Percentage of tests done in the country. Derived like: | [`total_tests`/`population`]*100 |)
data
    Return: `dict` (A dictionary containing all these details..., then use `CovidClient.data`)
    Example:
    ```py
    # Assuming you have initialised the `CovidClient`
    country_data = cov.data
    country_data['totalCases'] # == CovidClient.total_cases
    ```
```