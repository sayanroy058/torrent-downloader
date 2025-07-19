#!/bin/bash

apt-get update && apt-get install -y python3-libtorrent
python3 app.py
