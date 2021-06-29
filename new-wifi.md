# New WiFi

## DNS over HTTPS

https://forum.mikrotik.com/viewtopic.php?t=160243#p787643

    ./ip dns set servers=1.1.1.1,1.0.0.1
    ./system ntp client set enabled=yes server-dns-names=time.cloudflare.com
    ./tool fetch url=https://curl.haxx.se/ca/cacert.pem
    ./certificate import file-name=cacert.pem passphrase=""
    ./ip dns set use-doh-server=https://1.1.1.1/dns-query verify-doh-cert=yes
    ./ip dns set servers=""

https://mikrotikon.pl/dns-over-https-czyli-szyfrowany-dns-w-routeros/

Using only the 1.1.1.1 certificate, instead of a complete set.

## Simple ad blocking

https://forum.qnap.net.pl/threads/pi-hole-%E2%80%93-blokowanie-reklam-ale-bez-pi-hole-za-to-w-samym-mikrotiku.27017/

1. Download the file `mikrotik_adblock_updater.rsc`

       /tool fetch url="http://pool.qnapclub.pl/projects/tools/mikrotik-pihole-adlists/mikrotik_adblock_updater.rsc" mode=http;

2. Run it to create scripts and schedule them

       /import mikrotik_adblock_updater.rsc

3. Go to System > Scripts to run `DownloadAdsBlockList` and `ReplaceAdsBlockList`

4. Review the created static DNS entries

5. Disable the scripts in in scheduler, if they should not run automatically

### Copy of `mikrotik_adblock_updater.rsc`

    # Script which will download the drop list as a text file
    /system script add name="DownloadAdsBlockList" source={
    /tool fetch url="http://pool.qnapclub.pl/projects/tools/mikrotik-pihole-adlists/mikrotik_pihole_adlists.rsc" mode=http;
    :log info "Downloaded mikrotik_pihole_adlists.rsc from pool.qnapclub.pl";
    }

    # Script which will Remove old AdsBlockList list and add new one
    /system script add name="ReplaceAdsBlockList" source={
    /ip dns static remove [find where ttl=600w]
    /import file-name=mikrotik_pihole_adlists.rsc;
    :log info "Removed old AdsBlockList records and imported new list";
    }

    # Schedule the download and application of the AdsBlockList list
    /system scheduler add comment="Download AdsBlock list" interval=1d \
    name="DownloadAdsBlockListList" on-event=DownloadAdsBlockList \
    start-date=jan/01/1970 start-time=08:15:39
    /system scheduler add comment="Apply AdsBlock List" interval=1d \
    name="InstallAdsBlockListList" on-event=ReplaceAdsBlockList \
    start-date=jan/01/1970 start-time=08:20:39

## Security

- https://mikrotikon.pl/mikrotik-jako-router-domowy-konfiguracja-od-podstaw/
- https://damianmac.pl/2020/03/20/mikrotik-basic-security/

### SSL for the configuration panel

1. Generate a self-signed certificate, with router's IP as the Common Name (CN)

       openssl genrsa -out mikrotik-priv-key.pem 2048
       openssl req -new -x509 -nodes -days 5555 -subj '/C=PL/O=Acme Corporation/CN=192.168.xx.yy' -key mikrotik-priv-key.pem -out mikrotik-pub-crt.pem

2. FTP both files to the router

3. Go to System/Certificates and import both files, first the public certificate and then the private key
    - :bulb: Only one new certificate will appear on the list, with `KT` flags

4. Go to IP/Services and configure `www-ssl` to use the certificate

## Unifi

### Cannot connect though app or Web interface

Potential reason:

```
$ sudo less /var/log/unifi/mongod.log

NOTE: This is a 32 bit MongoDB binary.
       32 bit builds are limited to less than 2GB of data (or less with --journal).
       Note that journaling defaults to off for 32 bit and is currently off.
       See http://dochub.mongodb.org/core/32bit
```

If so, [mongo_prune_js.js](https://help.ui.com/hc/en-us/articles/204911424-UniFi-How-to-Remove-Prune-Older-Data-and-Adjust-Mongo-Database-Size#4) may fail with error:

```
$ mongo --port 27117 < mongo_prune_js.js

MongoDB shell version: 2.4.14
connecting to: 127.0.0.1:27117/test
Tue Jun 29 21:29:42.829 Error: couldn't connect to server 127.0.0.1:27117 at src/mon
exception: connect failed
```

[Repair the database](https://help.ui.com/hc/en-us/articles/360006634094-UniFi-Repairing-Database-Issues-on-the-UniFi-Network-Application#3):

```
sudo service unifi stop
sudo mongod --dbpath /usr/lib/unifi/data/db --smallfiles --logpath /usr/lib/unifi/logs/server.log --repair

# restore the proper ownership
sudo chown -R unifi:unifi /usr/lib/unifi/data/db/
sudo chown -R unifi:unifi /usr/lib/unifi/logs/server.log 

sudo service unifi start         
```

In the end, the Mongo database turned out so badly corrupted that I ended up reinstalling `unifi` and restoring the configuration from backup.

## Ideas

- Let's Encrypt certificate instead of a self-signed one (https://github.com/gitpel/letsencrypt-routeros)
