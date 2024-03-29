# Power consumption
  - [Official requirements](https://www.raspberrypi.org/documentation/faqs/#pi-power)
   (Raspberry Pi Zero W/WH - 1.2A)

## LED

Pi Zero has no `POWER` LED.

The `ACT` LED does not blink when Pi cannot boot, i.e. when the SD becomes corrupt, the Pi may seem dead
([diagnosing a 'dead' Pi](https://learn.adafruit.com/raspberry-pi-zero-creation/is-my-pi-zero-dead)).

## Disabling unused interfaces

  - Bluetooth ([source](https://scribles.net/disabling-bluetooth-on-raspberry-pi/))
    - uninstalled the Bluetooth stack `sudo apt-get purge bluez`
  - HDMI ([source](https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy))
    - added `tvservice -o` to `/etc/rc.local`
    - removed the command (after struggling with _Failed to start Raise network interfaces_ and being unable to use the display)
  - USB ([source](https://www.raspberrypi.org/forums/viewtopic.php?p=894674#p894674), [source 2](https://babaawesam.com/2014/01/24/power-saving-tips-for-raspberry-pi/))
    - added `echo 0 | tee /sys/devices/platform/soc/20980000.usb/buspower > /dev/null` to `/etc/rc.local`
    - removed the command

# Setup instructions for Pi-hole
  - https://scotthelme.co.uk/securing-dns-across-all-of-my-devices-with-pihole-dns-over-https-1-1-1-1/
    - However, the blog post says to modify `/etc/dnsmasq.d/01-pihole.conf` - this is not a good idea,
      since updating Pi-Hole will overwrite the changes.
    - ~Instead, you can define the DNS server (`server=127.0.0.1#54`) in `/etc/dnsmasq.d/02-pihole-custom.conf`.~
    - ~Possibly, it should be also OK to have it in `/etc/pihole/setupVars.conf` - I think
      these values (e.g. `PIHOLE_DNS_1=...`) are used during the update procedure.~
    - Configure a custom DNS server `127.0.0.1#54` at http://[pi-hole-IP]/admin/settings.php?tab=dns (appropriate entries are automatically added to all the config files mentioned above)
  - https://blog.cloudflare.com/cloudflare-argo-tunnel-with-rust-and-raspberry-pi/
  - https://oliverhough.cloud/blog/configure-pihole-with-dns-over-https/

## Encrypted DNS

- ~Utility `cloudflared`~
  - ~Segmentation fault - [older version](https://bin.equinox.io/a/4SUTAEmvqzB/cloudflared-2018.7.2-linux-arm.tar.gz) of the binary works fine ([details](https://github.com/cloudflare/cloudflared/issues/38))~
  - ~[`login` is not required for `proxy-dns`](https://developers.cloudflare.com/1.1.1.1/dns-over-https/cloudflared-proxy/)~
- DNSCrypt
  - https://itchy.nl/raspberry-pi-3-with-openvpn-pihole-dnscrypt
    - Wayback Machine copy
        > Install and setup DNSCrypt
        > 
        > Mostly sourced from https://github.com/pi-hole/pi-hole/wiki/DNSCrypt-2.0
        > 
        >     Install location shall be /opt. This is where we will place the dnscrypt-proxy files.
        >     cd /opt
        >     Download DNSCrypt.
        >     sudo wget https://github.com/jedisct1/dnscrypt-proxy/releases/download/2.0.19/dnscrypt-proxy-linux_arm-2.0.19.tar.gz
        >     Extract prebuilt binary.
        >     sudo tar -xf dnscrypt-proxy-linux_arm-2.0.19.tar.gz`
        >     Rename the extracted folder.
        >     sudo mv linux-arm dnscrypt-proxy
        >     cd into extracted directory.
        >     cd dnscrypt-proxy
        >     Create a configuration file based on the example one.
        >     sudo cp example-dnscrypt-proxy.toml dnscrypt-proxy.toml
        >     Edit the toml file.
        >     sudo nano dnscrypt-proxy.toml
        >     Edit the port, since 53 is already being used by Pi-Hole. This is the listen_addresses line.
        >     I set listen_addresses = ['127.0.0.1:54','[::1]:54'].
        >     I set require_dnssec = true.
        >     I set server_names = ['dnscrypt.nl-ns0'].
        >     Install dnscrypt-proxy service.
        >     sudo ./dnscrypt-proxy -service install
        >     Start the new service.
        >     sudo ./dnscrypt-proxy -service start
        > 
        > DNSCrypt Proxy running successfully.
        > Fig 3. DNSCrypt Proxy running.
        > Configure Pi-Hole
        > 
        > Add the dnscrypt-proxy server to Pi-Hole on the Pi-Hole admin page.
        > Pi-Hole with custom IP and port
        > Fig 4. Pi-Hole with custom IP and port.
        > Configure your clients
        > 
        > Configure your clients to use your Pi-Hole IP address as the DNS server or enter it into your router so every client on your local network will be using Pi-Hole filtering while being DNSCrypt secured.
  - https://download.dnscrypt.info/dnscrypt-resolvers/v2/public-resolvers.md

# Useful commands

    sudo /usr/sbin/logrotate --force /etc/logrotate.conf

    watch -n1 'cat /sys/class/thermal/thermal_zone0/temp; cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'

    sudo vcgencmd get_config over_voltage
    sudo vcgencmd get_config force_turbo

# Stability issues log

    # underclocked to solve the suspected problem of overheating
    #  -> temperature dropped slightly, but Pi was still unstable, so commenting out
    # arm_freq=700
    # arm_freq_min=700

    # another attempt to solve the stability issue - https://github.com/raspberrypi/linux/issues/2555
    #  -> also no change, so reverting
    # over_voltage=6

    # one more try - https://github.com/raspberrypi/linux/issues/2555#issuecomment-427649210
    force_turbo=1
    over_voltage=4

  - [Suspected hardware issue](https://github.com/raspberrypi/linux/issues/2555#issuecomment-394105250)
  
# Blocking page

 - Set `BLOCKINGMODE=IP` in `/etc/pihole/pihole-FTL.conf`
 - `sudo service pihole-FTL restart`

The blocking page is stored in `/var/www/html/pihole`; pros and cons of different blocking modes are described
in https://docs.pi-hole.net/ftldns/blockingmode/

# Misc

 - [Raspberry not showing on the DHCP Clients List (in router configuration)](https://discourse.pi-hole.net/t/pi-hole-not-visible-in-routers-dhcp-client-list/10841)
 - [No default `pi` user](https://www.raspberrypi.com/news/raspberry-pi-bullseye-update-april-2022/)
