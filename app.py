import os
import json
import base64
import traceback 
from flask import Flask, jsonify, request, make_response
from src.services.ant_colony import AntSystem
from src.services.genetic_algorithm import GeneticAlgorithm
from src.helpers.constants import MATRIX_FIELDS, DB_COLLECTIONS
from src.helpers.notify_helper import notifyUser
from src.helpers.transform import binaryTroughtMatrix 
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def getRoutes(data):
    # TODO: analisar se o body vira codificado ou não e o formato
    # geneticSystemArgs = json.loads(base64.b64decode(message['data']).decode('utf-8'))
    geneticSystemArgs = json.loads(data)
    antSystem = AntSystem()
    geneticSystem = GeneticAlgorithm(antSystem)
    geneticSystem.initialize(**geneticSystemArgs)
    geneticSystem.run()
    result = geneticSystem.decodeChromosome(geneticSystem.population[0])
    notifyUser(result)
    return result

@app.route("/", methods=["POST"])
def post():
    try:
        result = getRoutes(request.data)
        return make_response(jsonify(
            success=True,
            result=result
        ), 200)
    except Exception as err:
        message = err.args[0] if err.args and err.args[0] else "Internal Server Error"
        return make_response(jsonify(
            success=False,
            message=message,
            stack=traceback.format_exc()
        ), 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))