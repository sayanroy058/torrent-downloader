from flask import Flask, request, jsonify
import libtorrent as lt
import time
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    magnet_link = data.get('magnet')
    
    if not magnet_link:
        return jsonify({'error': 'Magnet link is required'}), 400

    try:
        ses = lt.session()
        ses.listen_on(6881, 6891)

        params = {
            'save_path': './downloads',
            'storage_mode': lt.storage_mode_t.storage_mode_sparse,
        }

        if not os.path.exists('./downloads'):
            os.makedirs('./downloads')

        handle = lt.add_magnet_uri(ses, magnet_link, params)

        while not handle.has_metadata():
            time.sleep(1)

        print("Starting download...")
        while handle.status().state != lt.torrent_status.seeding:
            s = handle.status()
            print(f"Progress: {s.progress * 100:.2f}%")
            time.sleep(1)

        return jsonify({'status': 'Download complete'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
