# huoutage
Read outage data from Huntsville Utilities and report:
* How many outage reports and (approximate) affected customers appear within a specified polygon
* How many outage reports and (approximate) affected customers appear within a given distance from the center of that polygon
* How many outage reports and (approximate) affected customers exist in total

## Dependencies
* requests
* geojson
* turfpy

## Configuration
Configuration options reside in an INI file; this script looks for them at `./huoutage.ini` by default.

| Parameter        | Value                                                                                                                              |
|------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `data_url`       | The URL where the power outage data resides.                                                                                       |
| `user_agent`     | HTTP user-agent string to send. Their server doesn't seem to like the ones from Requests or cURL.                                  |
| `campus_radius`  | The distance from the center of the specified polygon in which outages outside the polygon should be counted/described separately. |

## Arguments
| Parameter  | Value                             |
|------------|-----------------------------------|
| `--config` | Path to an alternate config file. |
| `--debug`  | Print debug output.               |

## To-do
* An example polygon outlining the approximate boundaries of the UAH campus is currently hardcoded in the script but I should make it so that this is defined in the configuration file. Unless you're really interested in power outages affecting UAH for some reason, you will probably want to change this to suit your purpose.

## Disclaimer
This script is not supported by, endorsed by, or otherwise affiliated with, Huntsville Utilities. They might change the location or format of their outage report data, or cease making it available entirely, at any time. In any of those circumstances, this script would no longer work.
