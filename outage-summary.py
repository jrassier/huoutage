""" Summarize published Huntsville Utilities power outage data """

import datetime
import argparse
import configparser
import requests
from geojson import Point, Polygon, Feature
from turfpy.measurement import boolean_point_in_polygon, center, distance

debug = False

# noinspection PyTypeChecker
uah_campus = Polygon(
    [
        [
            (34.7298050119197, -86.6441363019506),
            (34.7261866392701, -86.6442780639526),
            (34.7261562601531, -86.6475744598294),
            (34.7239345362388, -86.6476367876865),
            (34.723969266297, -86.6442942032117),
            (34.7216511185446, -86.6443170621359),
            (34.7217303758792, -86.6467482711847),
            (34.7200569888755, -86.6468146662237),
            (34.7196397911189, -86.6479521997033),
            (34.7180456682426, -86.648613042663),
            (34.7179778367799, -86.6444806944003),
            (34.716496595056, -86.6438148456757),
            (34.7170332160291, -86.64180074118),
            (34.7182141988333, -86.6372117859013),
            (34.7191366387279, -86.633589058221),
            (34.7230427191228, -86.6335133901667),
            (34.7232584041338, -86.634424164476),
            (34.7261199913654, -86.6344405390545),
            (34.7261319997229, -86.6356655748095),
            (34.7276433565158, -86.6356042372727),
            (34.727678796214, -86.635960155703),
            (34.7348767065539, -86.6358861738798),
            (34.7347950909081, -86.6396764432458),
            (34.7345006552071, -86.6421338966481),
            (34.7343857100551, -86.6427238946934),
            (34.7343087132496, -86.6432057402933),
            (34.7342960022586, -86.6445118103154),
            (34.7348622495461, -86.6459740435538),
            (34.7348002683978, -86.6526220272942),
            (34.7349766223694, -86.6535507148243),
            (34.7298050119197, -86.6441363019506),
        ]
    ]

)

# noinspection PyTypeChecker
vbh_location = Feature(geometry=Point([34.721167, -86.641048]))


def write_debug(msg):
    if debug:
        print("{} {}".format(datetime.datetime.now(), msg))


def get_options():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="Path to a config file. Defaults to huoutage.ini", default="huoutage.ini")
    parser.add_argument("--debug", help="Enable debug output", action="store_true")
    return parser.parse_args()


def main():
    options = get_options()

    global debug
    debug = options.debug

    write_debug(f"Options: {options}")

    config = configparser.ConfigParser()
    config.read(options.config)

    headers = {'user_agent': config['huoutage']['user_agent'], 'accept': '*/*'}

    campus_center = center(uah_campus)
    data_result = requests.get(config['huoutage']['data_url'], headers=headers)

    data_result.raise_for_status()

    campus_reports = 0
    campus_customers = 0
    area_reports = 0
    area_customers = 0
    total_reports = 0
    total_customers = 0

    for report in data_result.json():
        splut = report['val'].split('_')
        lat = splut[0]
        long = splut[1]
        num_customers = int(splut[2])

        outage_map_point = Feature(geometry=Point((float(lat), float(long))))

        on_campus = boolean_point_in_polygon(outage_map_point, uah_campus)
        campus_distance = distance(outage_map_point, campus_center, units='mi')

        if on_campus:
            campus_reports += 1
            campus_customers += num_customers
            write_debug(f"{num_customers} customer(s) experiencing an outage ON CAMPUS at {lat} {long}")

        elif campus_distance <= float(config['huoutage']['campus_radius']):
            area_reports += 1
            area_customers += num_customers
            write_debug(f"{num_customers} customer(s) experiencing an outage within {config['huoutage']['campus_radius']} miles of campus at {lat} {long}")
        else:
            total_reports += 1
            total_customers += num_customers
            write_debug(f"{num_customers} customer(s) experiencing an outage {campus_distance} miles from campus at {lat} {long}")

    print(f"{campus_reports} reports of a power outage on campus")
    print(f"{area_reports} reports of a power outage within {config['huoutage']['campus_radius']} miles of campus. Approximately {area_customers} customers are affected.")
    print(f"{total_reports} total power outage reports among all Huntsville Utilities customers. Approximately {total_customers} customers are affected.")


if __name__ == "__main__":
    main()
