import pyodbc
from flask import Flask, request, jsonify
from openapi_core.casting.schemas.exceptions import CastError
from openapi_core.deserializing.parameters.exceptions import EmptyParameterValue
from openapi_core.exceptions import MissingParameterError, OpenAPIParameterError
from openapi_core.unmarshalling.schemas.exceptions import InvalidSchemaValue

import db
from open_api import OpenApi

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
open_api = OpenApi()


@app.route('/sample')
def get_sample():
    # リクエストのバリデーションチェック
    open_api.validate(request)

    # リクエストパラメータを辞書型で取得
    param_dict = open_api.get_params(request)

    res = db.sql_execute("select * from xxx where id=", param_dict["id"])
    return jsonify(res)

@app.errorhandler(CastError)
@app.errorhandler(EmptyParameterValue)
@app.errorhandler(InvalidSchemaValue)
@app.errorhandler(MissingParameterError)
@app.errorhandler(OpenAPIParameterError)
def handle_field_error(e):
    print(e)
    res = jsonify({
        "error_message": "バリデーションエラー：パラメータが正しくありません。"
    })
    return res, 400

@app.errorhandler(404)
def handle_notfound_error(e):
    print(e)
    res = jsonify({
        "error_message": "対象のパスが見つかりません。"
    })
    return res, 404


@app.errorhandler(pyodbc.Error)
def handle_server_error(e):
    res = jsonify({
        "error_message": "サーバ内部エラーです。"
    })
    return res, 500
