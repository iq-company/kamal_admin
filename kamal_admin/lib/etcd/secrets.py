import argparse
import json
import etcd3

client = etcd3.client()

def store_secret(key: str, value: str):
    client.put(key, value)

def fetch_secrets(prefix: str):
    data = {}
    for kv in client.get_prefix(prefix):
        k = kv[1].key.decode()
        v = kv[0].decode()
        data[k] = v
    print(json.dumps([{'key': k, 'value': v} for k, v in data.items()]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    store = subparsers.add_parser('store')
    store.add_argument('--key', required=True)
    store.add_argument('--value', required=True)

    fetch = subparsers.add_parser('fetch')
    fetch.add_argument('--prefix', required=True)

    args = parser.parse_args()
    if args.cmd == 'store':
        store_secret(args.key, args.value)
    elif args.cmd == 'fetch':
        fetch_secrets(args.prefix)

