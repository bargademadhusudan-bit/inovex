from flask import Flask, request, jsonify
import json
import price_engine  # This imports your script from Phase 1

app = Flask(__name__)

@app.route('/get-price', methods=['GET'])
def get_price():
    # 1. Get the 'crop' parameter from the URL (e.g., ?crop=Onion)
    crop_name = request.args.get('crop')

    if not crop_name:
        return jsonify({"error": "Please provide a crop name. Example: /get-price?crop=Onion"}), 400

    # 2. Call your logic from Phase 1
    # Since price_engine returns a JSON string, we load it back into a dict 
    # so Flask can serve it properly.
    try:
        json_result_string = price_engine.get_trusted_price(crop_name)
        data = json.loads(json_result_string)
        
        # 3. Return the result to the user
        return jsonify(data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 'debug=True' allows the server to auto-reload if you make code changes
    app.run(debug=True, port=5000)