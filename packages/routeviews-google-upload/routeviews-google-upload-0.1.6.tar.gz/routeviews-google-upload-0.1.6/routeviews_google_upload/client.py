import argparse
import sys
import os

from hashlib import md5

import grpc

# The next 3 lines enable gRPC to operate even when we are calling this from the context of a python package (e.g.
# installed via setup.py, e.g. into the user global site-package directory).
import routeviews_google_upload
this_package_path = os.path.dirname(routeviews_google_upload.__file__)
sys.path.append(this_package_path)
from routeviews_google_upload import rv_pb2
from routeviews_google_upload import rv_pb2_grpc


def read_bytes(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def run(args):
    upload(args.dest, args.file, args.to_sql)


def upload(grpc_server, file_path, to_sql=False):
    # 1. Read the provided file.
    content = read_bytes(file_path)

    # 2. Package that file in a gRPC protobuf.
    fr = rv_pb2.FileRequest()
    fr.filename = file_path
    fr.project = 1  # TODO should this be an argument rather than hardcoded?
    fr.convert_sql = to_sql
    fr.content = content
    fr.md5sum = md5(content).hexdigest()

    # 3. Send to a gRPC endpoint.
    with grpc.insecure_channel(grpc_server) as channel:
        client = rv_pb2_grpc.RVStub(channel)
        response = client.FileUpload(fr)
        print("Status: " + str(response.status))
        if response.error_message:
            print("Error Message: " + response.error_message)


def config_parser(parser):
    parser.add_argument('--file', required=True, help='The file to be sent to the Google Cloud.')
    parser.add_argument('--dest', required=True,
                        help="The gRPC server where to send the file (use 'localhost:50051' for local development)")
    parser.add_argument('--to-sql', action='store_true', help='Convert to sql (for uploading to BigQuery).')


def main(args):
    parser = argparse.ArgumentParser()
    config_parser(parser)
    run(args)


if __name__ == '__main__':
    main(sys.argv[1:])
