import shodan
import cv2
import uuid
import codecs
import sys
import json


def default_run(generated_uuid, count, total, api):
    try:
        query = 'hipcam'
        result = api.search(query, page=count)
        
        for service in result['matches']:
            client_url = f"rtsp://{service['ip_str']}:{service['port']}/11"
            
            print(f"Testing {service['ip_str']} {str(count)}/{str(total)}")
            
            try:
                cap = cv2.VideoCapture(client_url)
                if cap.isOpened():
                    # Use UTF-8 otherwise it won't process the accentuated city names.
                    f = codecs.open(f'cams-{generated_uuid}.m3u', 'a', encoding='utf8')
                    print('----')
                    print(f"Found service in {service['location']['city']}")
                    print(f"Formatted output: {client_url}")
                    # Messy generate of the m3u entry, could be improved but works.
                    f.write(f"#EXTVLCOPT:network-caching=1000\n#EXTINF:-1,{service['hash']}-{service['location']['city'].replace(' ', '_')}-{service['location']['country_name'].replace(' ', '_').replace(',', '_')}\n{client_url}\n")
                    f.close()
            except Exception as e:
                print("Exception ", e)
                pass
            count += 1
        return count

    except Exception as e:
        print('Error %s', e)
        return 0

def generation(run=1):
    try:
        api = shodan.Shodan(API_KEY)
    except:
        print("Error: invalid or missing api key.")
        return
    generated_uuid = uuid.uuid4().hex
    f = codecs.open(f'cams-{generated_uuid}.m3u', 'a')
    f.write('#EXTM3U\n')
    f.close()
    count = 1
    total = 100 * run
    
    for i in range(0, run):
        count = default_run(generated_uuid, count, total, api)
    

if __name__ == '__main__':
      try:
          with open('config.json', 'r') as f:
              config = json.load(f)
          API_KEY = config['apikey']
      except:
          API_KEY = None
      
      if not API_KEY:
          print("Missing or invalid API_KEY")
      else:
          if(len(sys.argv) < 2):
            generation()
          else:
              generation(int(sys.argv[1]))
