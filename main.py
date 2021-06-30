import time
import requests
import json


def web_request(method_name, url, dict_data, is_urlencoded=True):
    """Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
    method_name = method_name.upper()  # 메소드이름을 대문자로 바꾼다
    if method_name not in ('GET', 'POST'):
        raise Exception('method_name is GET or POST plz...')

    if method_name == 'GET':  # GET방식인 경우
        response = requests.get(url=url, params=dict_data)
    elif method_name == 'POST':  # POST방식인 경우
        if is_urlencoded is True:
            response = requests.post(url=url, data=dict_data,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})

    dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']):  # JSON 형태인 경우
        return {**dict_meta, **response.json()}
    else:  # 문자열 형태인 경우
        return {**dict_meta, **{'text': response.text}}

def check_authentication(url, token):
    headers = {
        'Authorization': 'Bearer '+token
    }
    response = requests.get(url=url, headers=headers)
    dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']):  # JSON 형태인 경우
        return {**dict_meta, **response.json()}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
# POST방식 호출 테스트('Content-Type': 'application/x-www-form-urlencoded')
    login_url  = 'http://' # 접속할 사이트주소 또는 IP주소를 입력한다
    check_url='http://' # 접속이 성공적으로 수행되면 유효한지 체크해볼 사이트주소 또는 IP주소를 입력한다
    data = "client_id=JWT Open Access JPKIM&grant_type=password&client_secret=______&scope=openid&username=jpkim@kochamdev.com&password=a12345!@#"          # 요청할 데이터
    #client_secret 을 발행받은 secret에 맞추어 입력하세요.
    response = web_request(method_name='POST', url=login_url, dict_data=data)

    if response['ok'] == True:
        print("\n\n");
        print("ACCESS_TOKEN IS \n\n" + response['access_token'])
    # 성공 응답 시 액션
    else:
        print('ERROR')
    # 실패 응답 시 액션

    time.sleep(2)
    response_validation=check_authentication(url=check_url ,token=response['access_token'])
    print("\n\nIS THIS TOKEN AVAILABLE STILL?\n\n")
    print(response_validation)


