import os
from dotenv import load_dotenv
import oss2

def upload_to_oss(file_path, object_name=None):
    load_dotenv()
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT')
    OSS_BUCKET = os.getenv('OSS_BUCKET')
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET')
    if not all([OSS_ENDPOINT, OSS_BUCKET, OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET]):
        raise ValueError('请在.env中配置OSS_ENDPOINT, OSS_BUCKET, OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET')
    auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)
    if object_name is None:
        object_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        result = bucket.put_object(
            object_name,
            f,
            headers={'Content-Type': 'text/html'}
        )
    if result.status == 200:
        url = f'https://{OSS_BUCKET}.{OSS_ENDPOINT.replace("https://","").replace("http://","")}/{object_name}'
        print(f'上传成功: {url}')
        return url
    else:
        print(f'上传失败: {result.status}')
        return None

if __name__ == '__main__':
    upload_to_oss('crossword.html')
