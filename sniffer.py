import argparse
from flow_session import FlowSession
from csvcreator import csv_creator
from tqdm import tqdm

def argument_parser():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='PE malware feature extraction.')

    parser.add_argument('--input_path', required=False, default="data/2013-11-15-Gondad-EK-traffic.pcap",
                        help='add your pcap file path.')
    parser.add_argument('--output_folder', required=False, default="pcap_result",
                        help='add your output folder path.')


    parser.add_argument('--output_name', required=False, default="pcap_result.csv",
                        help='add your output name.')

    return parser




def main():
    # Get the argument parser object
    args = argument_parser().parse_args()

    if not args.output_name.split(".")[-1] == "csv":
        raise Exception("output_name must be .csv")

    input_path = args.input_path
    flows = FlowSession(input_path)
    print("*** start create flows ***")
    flows.create_flows()
    flow_result = flows.get_flows()
    flow_list = [i for i in flow_result]

    data_list=[]

    print("*** start extract features from flows ***")
    for i in tqdm(range(len(flow_list))):
        data = flow_list[i].get_data()
        data_list.append(data)

    csv_creator(data_list, args.output_folder, args.output_name)

if __name__ == "__main__":
    main()


