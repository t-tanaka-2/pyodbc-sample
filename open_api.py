import yaml
from openapi_core import create_spec
from openapi_core.contrib.flask import FlaskOpenAPIRequest
from openapi_core.exceptions import MissingParameterError, OpenAPIParameterError
from openapi_core.validation.request.validators import RequestValidator


class OpenApi:
    validator = None

    # 初期化処理
    def __init__(self):
        with open(file='./openapi/openapi.yaml', mode='r', encoding='utf-8') as spec_file:
            spec_dict = yaml.safe_load(spec_file)
            spec = create_spec(spec_dict)
            self.openapi_dict = spec_dict
            self.validator = RequestValidator(spec)

    # リクエストパラメータのバリデーション
    def validate(self, request: FlaskOpenAPIRequest):
        openapi_request = FlaskOpenAPIRequest(request)
        result = self.validator.validate(openapi_request)
        print(f'Request Validation Result: {result}')
        result.raise_for_errors()
        # GETメソッドでパラメータにAPI定義されていないものが存在する場合は例外を投げる
        if openapi_request.method == 'get':
            self._check_defined_query_param_key(request)
        # パラメータが全て空の場合は例外を投げる
        self._check_empty_params(openapi_request)

    # OpenAPIで定義していないクエリパラメータのキーが渡ってきた時にバリデーションエラーとする
    def _check_defined_query_param_key(self, request):
        request_params = self.get_params(request)
        openapi_params = self.openapi_dict['paths'][request.path]['get']['parameters']
        for request_params_key in request_params.keys():
            is_exist = False
            # nameに定義されている項目名を取得し、存在チェック
            for openapi_param in openapi_params:
                is_exist = request_params_key == openapi_param['name']
                if is_exist:
                    break
            if not is_exist:
                print(f'OpenAPI Parameter Error : {OpenAPIParameterError}')
                raise OpenAPIParameterError

    def _check_empty_params(self, openapi_request):
        if not openapi_request.parameters.query:
            print(f'Missing Parameter Error : {MissingParameterError}')
            raise MissingParameterError

    def get_params(self, request: FlaskOpenAPIRequest):
        return dict(FlaskOpenAPIRequest(request).parameters.query)
