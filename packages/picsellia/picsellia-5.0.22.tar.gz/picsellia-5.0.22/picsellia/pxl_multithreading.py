import requests
import os
import sys
import time 
from picsellia.decorators import retry
from picsellia.pxl_exceptions import ResourceNotFoundError

def pool_init(t, directory, counter, interactive):
    global dl
    global total_length
    global png_dir
    global inter
    dl = counter
    total_length = t
    png_dir = directory
    inter = interactive

def dl_list(infos):
    global dl
    global total_length
    global should_log
    global inter
    for info in infos:
        pic_name = os.path.join(png_dir, info['external_picture_url'].split('/')[-1])
        if not os.path.isfile(pic_name):
            dl_pic(info=info, pic_name=pic_name)
            done = int(50 * dl.value / total_length)
            if inter:
                sys.stdout.flush()
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}] {dl.value}/{total_length}")
            else:
                if total_length>100 and (dl.value%50==0 or dl.value==total_length):
                    print('['+'='* done+' ' * (50 - done)+'] ' + str(dl.value)+'/'+str(total_length))
                elif total_length<=100 and (dl.value%5==0 or dl.value==total_length):
                    print('['+'='* done+' ' * (50 - done)+'] ' + str(dl.value)+'/'+str(total_length))
        else:
            pass

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@retry((Exception), total_tries=4)
def dl_pic(info, pic_name):
    try:
        response = requests.get(info["signed_url"], stream=True)
        if response.status_code == "404":
            raise ResourceNotFoundError('Picture does not exist on our server.')
        with open(pic_name, 'wb') as handler:
            for data in response.iter_content(chunk_size=1024):
                handler.write(data)
        with dl.get_lock():
            dl.value += 1
    except Exception:
        print(f"Image {pic_name} can't be downloaded")


def init_pool_annotations(p, nb, req, ds_id, h, p_size):
    global page_done
    global nb_pages
    global pxl_request
    global annotation_list
    global dataset_id
    global host
    global page_size
    page_done = p
    nb_pages = nb - 1
    pxl_request = req
    dataset_id = ds_id
    host = h
    annotation_list = []
    page_size = p_size

def dl_annotations(page_list):
    global page_done
    global nb_pages
    global pxl_request
    global annotation_list
    global dataset_id
    global host
    global page_size

    annotation_list = []
    for page in page_list:
        params = {
            'limit': page_size,
            'offset': page_size*page,
            'snapshot': False
        }
        r = pxl_request.get(host + 'annotation/{}'.format(dataset_id), params=params)
        annotation_list += r.json()["annotations"]
        with page_done.get_lock():
            page_done.value += 1
        done = int(50 * page_done.value / nb_pages)
        sys.stdout.flush()
        sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}] {int(page_done.value/nb_pages*100)}%")
    return annotation_list
    