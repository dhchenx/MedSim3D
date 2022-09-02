import requests
import urllib.parse
'''
url='https://ieee-dataport.s3.amazonaws.com/open/130023/9395/3D%20avatars%20OBJ/3Davatarbody_IBV_20191030/IEEEP2_01_R1_3Davatarbody_IBV_20191030.obj?AWSAccessKeyId=AKIAJOHYI4KJCE6Q7MIQ&Expires=1659251385&Signature=05Asas8oxLYAT%2Ba2TV0NcZVhxi8%3D'
r = requests.get(url, allow_redirects=True)
open('datasets/obj/test1.obj', 'wb').write(r.content)
'''

# url='https://ieee-dataport.s3.amazonaws.com/open/130023/9395/3D%20avatars%20OBJ/3Davatarbody_IBV_20191030/IEEEP2_01_R1_3Davatarbody_IBV_20191030.obj?AWSAccessKeyId=AKIAJOHYI4KJCE6Q7MIQ&Expires=1659251385&Signature=05Asas8oxLYAT%2Ba2TV0NcZVhxi8%3D'

root_url='https://ieee-dataport.s3.amazonaws.com/open/130023/9395/3D%20avatars%20OBJ/'

file_name='3DLOOK_3DLOOK_20200622/IEEEP2_01_R2_3DLOOK_3DLOOK_20200622.obj'

pars='?AWSAccessKeyId=AKIAJOHYI4KJCE6Q7MIQ&Expires=1659253167&Signature=1dGXd0PQw0tYP2HIQuW%2FA4ilzVE%3D'

url=root_url+file_name+pars

r = requests.get(url, allow_redirects=True)
print(r.status_code)
open('datasets/obj/test1.obj', 'wb').write(r.content)

