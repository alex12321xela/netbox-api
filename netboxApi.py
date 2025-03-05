import requests
import json
import csv
import argparse

def find_prefix(session, ip):
   
    res = session.get(settings['url']+'/api/ipam/prefixes/?q='+ip)
    #print(res.json())
    return res.json()
    
def get_ip_from_file(file):
    f = open(file,'r')
    ips = f.read().splitlines()
    f.close()
    return ips

def return_csv(values,file):
    f = open(file,'w')
    f.write('\n'.join(map(str,values)))
    f.close()
    


if __name__ == "__main__":
    
    
    settings = {}
    settings['token'] = 'token' # апи токен
    settings['url'] = 'url'   # netbox address
    session = requests.Session()
    session.headers.update({'Authorization':'TOKEN ' + settings['token']})
    
    parser = argparse.ArgumentParser(description='ip to ip+org by netbox REST api')
    parser.add_argument('-f','--file', type=str, help='path to file',required=True)
    parser.add_argument('-o','--output', type=str, help='write to filename')
    args = parser.parse_args()
    
    
    items = get_ip_from_file(args.file)
    
    values=[]
    
    for ip in items:
       values.append("\"{}\";\"{}\"".format(ip,find_prefix(session, ip)['results'][-1]['description']))
    
    
    if(args.output is None):
        print('\n'.join(map(str,values)))
    else:
        return_csv(values,args.output)
    
    
    
    
    #print(ip + ' ' + find_prefix(session, ip)['results'][-1]['description'])
    
