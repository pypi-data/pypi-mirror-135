# 安装SDK pip install git+https://github.com/panyunsuo/AlgorithmicMicroserviceSDK.git
# SDK使用文档 https://www.yuque.com/fenfendeyouzhiqingnian/algorithm/ffdma4
import time
from algorithm_mic_sdk.algorithms.photo_to_cartoon import PhotoToCartoon
from algorithm_mic_sdk.auth import AuthInfo
from algorithm_mic_sdk.tools import FileInfo
from threading import Thread

host = 'http://nyasu.leqi.us:17013'  # 算法host地址
user_name = 'panso'
password = '0bdca2d8-4a3d-11eb-addb-0242c0a80006'
filename = 'src/漫画/1.png'  # 图片文件名

beauty_level = {
    "leyelarge": 5,
    "reyelarge": 5,
    "mouthlarge": 5,
    "skinwhite": 5,
    "skinsoft": 5,
    "coseye": 5,
    "facelift": 5
}
beauty_level = None
file_info = FileInfo.for_file_bytes(open(filename, 'rb').read() + b'124544')  # 创建文件对象
auth_info = AuthInfo(host=host, user_name=user_name, extranet=True, password=password,
                     gateway_cache=False)  # 初始化验证信息
style = 'Disney_crown'
styles = ['White', 'Summer', 'Watercolor', 'Draw', 'Disney_crown', 'Disney_baby', '18th_painting', '20th_painting']
styles = [styles[0]]
# styles = ['20th_painting']
# process = 'image/resize,m_lfit,w_100,h_100,limit_1/auto-orient,1/format,png'
fluorescent_pen_recognition = PhotoToCartoon(auth_info, file_info,
                                             styles=styles, cutout=True, beauty_level=beauty_level)  # 创建算法对象
# fluorescent_pen_recognition.algo_name='photo_to_cartoon_qiman'

def run():
    for i in range(50):
        try:
            resp = fluorescent_pen_recognition.synchronous_request(timeout=100)  # 同步请求算法
        except Exception:
            pass

def run2(n):
    th = []
    for _ in range(n):
        t = Thread(target=run)
        t.start()
        th.append(t)
        time.sleep(min(60//n, 10))

    for t in th:
        t.join()

ths = []
for i in range(1, 20, 1):
    t = Thread(target=run2, args=(i, ))
    t.start()
    ths.append(t)
    time.sleep(60)

for t in ths:
    t.join()

