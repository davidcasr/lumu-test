import json
import pandas as pd
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

lumu_client_id = os.getenv("LUMU_CLIENT_ID")
collector_id = os.getenv("COLLECTOR_ID")

API_URL = (
    f"https://api.lumu.io/v1/collectors/{collector_id}/dns/queries?key={lumu_client_id}"
)


def extract_data(log_entry):
    pattern = r"(?P<date>\d+-\w+-\d+) (?P<time>\d+:\d+:\d+\.\d+) queries: info: client @(?P<client>[\da-fx]+) (?P<client_ip>[\d.]+)#(?P<port>\d+) \((?P<host_queried>\S+)\): query: \S+ (?P<query_class>\S+)"
    match = re.search(pattern, log_entry)

    return match.groupdict() if match else {}


def create_dataframe(file_path: str):
    df = pd.read_csv(file_path, header=None, names=["log_entry"])
    df = pd.concat([df["log_entry"].apply(extract_data).apply(pd.Series)], axis=1)

    return df


def print_statistics(dataframe: pd.DataFrame, head: int = 5):
    num_rows = dataframe.shape[0]

    client_ips_rank = dataframe["client_ip"].value_counts().head(head)

    host_rank = dataframe["host_queried"].value_counts().head(head)

    print(f"Total Records {num_rows}\n")

    print("Client IPs Rank")
    print("------------------ --- -----")
    for ip, count in client_ips_rank.items():
        percentage = (count / num_rows) * 100
        print(f"{ip:<18} {count:<3} {percentage:.2f}%")
    print("------------------ --- -----\n")

    print("Host Rank")
    print("-------------------------------------------- ---- -----")
    for host, count in host_rank.items():
        percentage = (count / num_rows) * 100
        print(f"{host:<44} {count:<3} {percentage:.2f}%")
    print("-------------------------------------------- ---- -----")


def dataframe_to_json(dataframe: pd.DataFrame):
    selected_columns = ["date", "time", "host_queried", "client_ip"]
    subset_dataframe = dataframe[selected_columns].copy()
    subset_dataframe["timestamp"] = (
        subset_dataframe["date"] + " " + subset_dataframe["time"]
    )
    subset_dataframe.drop(["date", "time"], axis=1, inplace=True)
    subset_dataframe.rename(
        columns={"host_queried": "name", "client_ip": "client_ip"}, inplace=True
    )

    json_data = subset_dataframe.to_json(orient="records")
    return json_data


def send_data_to_api(records):
    response = requests.post(
        API_URL,
        json=records,
        headers={
            "Content-Type": "application/json",
        },
    )
    return response


def send_data_in_batches(data, batch_size: int = 500):
    json_size = json.loads(data)
    total_records = len(json_size)

    start = 0

    print("\n")
    print("Send data in batches")
    print("--------------------------")

    while start < total_records:
        batch = data[start : start + batch_size]
        response = send_data_to_api(batch)

        response_complete = {
            "status_code": response.status_code,
            "reason": response.reason,
            "json": response.json() if response.status_code == 200 else None,
        }

        print(f"Batch sent. Response: {response_complete}")

        start += batch_size


def main():
    file_path = "logs/queries"

    # Create dataframe
    df = create_dataframe(file_path)

    # Print statistics
    print_statistics(df)

    # Send data to API
    data = dataframe_to_json(df)
    send_data_in_batches(data)


if __name__ == "__main__":
    main()
