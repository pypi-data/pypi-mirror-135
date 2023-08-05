import pandas as pd
import urllib.request
import io
import sys
import re


def fetch(tracks, path):
    # Input - list of strings of marsis track names in the format
    # E_02086_SS3_TRK_CMP_M
    # and path to save downloaded data at

    #tracks = filter(None, tracks)  # Remove empty list items

    # Only allow ss3_trk_cmp for now, error out if anything different
    r = re.compile("e_[0-9]{5}_ss3_trk_cmp_m")
    for track in tracks:
        if r.match(track.lower()) is None:
            raise ValueError("Processor only supports SS3_TRK_CMP")

    # Get index files from pds
    print("Downloading PDS index files...")

    baseurl = "https://pds-geosciences.wustl.edu/mex/"
    indxURLs = [
                    baseurl + "mex-m-marsis-2-edr-v2/mexme_1001/index/index.tab",
                    baseurl + "mex-m-marsis-2-edr-ext1-v2/mexme_1002/index/index.tab",
                    baseurl + "mex-m-marsis-2-edr-ext2-v1/mexme_1003/index/index.tab",
                    baseurl + "mex-m-marsis-2-edr-ext3-v1/mexme_1004/index/index.tab",
                    baseurl + "mex-m-marsis-2-edr-ext4-v1/mexme_1005/index/index.tab",
                    baseurl + "mex-m-marsis-2-edr-ext5-v1/mexme_1006/index/index.tab",
                    baseurl + "mex-m-marsis-2-edr-ext6-v1/mexme_1007/index/index.tab",
                    baseurl + "mex-m-marsis-2-edr-ext7-v1/mexme_1008/index/index.tab",
                ]

    index = ""
    for url in indxURLs:
        data = urllib.request.urlopen(url)
        subIndx = str(data.read(), "utf-8")
        subPath = url.split('/')[:6]
        subPath = '/'.join(subPath) + '/'
        subIndx = subIndx.replace("DATA/", subPath + "DATA/").lower()
        index += subIndx


    # Create pandas dataframe
    print("Creating index dataframe...")

    cols = ["LBL_PATH", "ID", "TIME", "DS_ID", "RLS_ID", "REV_ID"]
    df = pd.read_csv(io.StringIO(index), sep=",", header=None, names=cols)

    # Download the data files
    print("Downloading geometry files...")

    for track in tracks:
        track = track.lower()
        lbl = df[df["ID"] == track]["LBL_PATH"]
        if(len(lbl) == 0):
            print("No file found to match %s" % track)
            sys.exit()
        lbl = lbl.iloc[0]
        geo = lbl.replace(".lbl", "_g.dat")
        print(geo)
        local_filename, headers = urllib.request.urlretrieve(geo, path + '/' + geo.split('/')[-1])
        print(local_filename)
