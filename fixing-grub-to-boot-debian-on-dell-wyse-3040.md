# Fixing GRUB to boot Debian 12 on Dell Wyse 3040

I followed [InstallingDebianOn/Dell/Wyse 3040](https://wiki.debian.org/InstallingDebianOn/Dell/Wyse%203040)
and the installation went smoothly, except for the fact the during the process I was **not** asked if
I wanted to enforce the option `Force GRUB Installation to the EFI removable media path`.

As a result, after restart I got error `No boot media found`.

## rEFInd Boot Manager

I found [Boot your computer with the Refind media](https://wiki.debian.org/GrubEFIReinstall#Boot_your_computer_with_the_Refind_media),
downloaded the rEFInd ISO image from [getting.html](https://www.rodsbooks.com/refind/getting.html)
and flashed it to a pendrive with Etcher.

Now I was finally able to boot my Debian installation, but I had to rely on the pendrive with rEFInd.

## EFI removable media path

Article [PSA: Dell Wyse 3040 Uses ‘Fallback’ EFI Location](https://blog.roberthallam.org/2020/05/psa-dell-wyse-3040-uses-fallback-efi-location)
contains a correct `grub-install` command, but I was confused about the `<espdir>` locations as well
as moving the files to the fallback boot path (it was not necessary in mycase).

On the other hand, [Troubleshoot boot problems by reinstalling GRUB on Linux](https://www.fosslinux.com/115031/troubleshoot-boot-problems-by-reinstalling-grub-on-linux.htm)
contains Debian-specific commands, but the crucial option `--removable` is missing.

Finally, the following two commands worked for me:

```bash
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GR --removable

update-grub
```

No mounting of partitions was required, because I executed them a running Debian instance (booted with rEFInd).
