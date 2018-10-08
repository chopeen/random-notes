# Power consumption
  - [Official requirements](https://www.raspberrypi.org/documentation/faqs/#pi-power)
   (Raspberry Pi Zero W/WH - 1.2A)

## [TODO] Ideas to lower the power consumption

  - Disable HDMI - added `tvservice -o` to `/etc/rc.local` ([source](https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy))
  - Disable Bluetooth - uninstalled the Bluetooth stack `sudo apt-get purge bluez` ([source](https://scribles.net/disabling-bluetooth-on-raspberry-pi/))
  - Disable USB

# Setup instructions for Pi-hole
  - https://scotthelme.co.uk/securing-dns-across-all-of-my-devices-with-pihole-dns-over-https-1-1-1-1/
  - https://blog.cloudflare.com/cloudflare-argo-tunnel-with-rust-and-raspberry-pi/

## Utility `cloudflared`
  - Segmentation fault - [older version of the binary works fine](https://github.com/cloudflare/cloudflared/issues/38)
  - [`login` is not required for `proxy-dns`](https://developers.cloudflare.com/1.1.1.1/dns-over-https/cloudflared-proxy/)

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
