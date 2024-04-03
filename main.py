from utils import headers, url
import requests
import json
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor




def get_data(url, next_key=None):
    if next_key is not None:
        url += f"&next={next_key}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None

def run_threads(next_key=None):
    # results = []
    count = 0
    # print("How")
    with ThreadPoolExecutor() as executor:

        if next_key is None:
            f = executor.submit(get_data, url=url)
            res = f.result()
            next_key = res["next"]
            # print("bla")
            # print(json.dumps(res, indent=4))
        while next_key is not None:
            # print("here")
            count += 1
            f = executor.submit(get_data, url=url, next_key=next_key)
            res = f.result()
            # print(res)
            if "next" in res:
                # print("Check")
                next_key = res["next"]
            else:
                print("end")
                next_key = None
            print(count)
            # print(json.dumps(res, indent=4))
            # results.append(res)
        with open("out1.json", "a") as outfile:
            json.dump(res, outfile, indent=2)



def main():
    with ProcessPoolExecutor() as executor:
        run_threads()



if __name__ == '__main__':
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"All the data is loaded in {end - start} time")
