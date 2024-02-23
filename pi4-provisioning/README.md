# Raspberry Pi 4B Provisioning

These files assume you're using Ubuntu Server 23.10 64bit. I formatted the sdcard using the RaspberryPi imager.

## Usage

This directory contains two provisioning methods:
1. bash (for installing directly on the device)
2. Containerfile

Both methods follow essentially the same strategy, which is roughly the same as https://www.raspberrypi.com/documentation/computers/camera_software.html.

## Needed tweaks

Immediately after running the `provision.sh` script on Ubuntu Server 23.10, I was able to capture images using `rpicam-still -n -o image.jpg`.

However, after installing podman, I was back to getting dmaHeap allocation errors when running `rpicam-still`.

I made these changes:
1. `sudo ln -s /dev/dma_heap/linux,cma /dev/dma_heap/vidbuf_cache`
2. Add `dtoverlay=vc4-kms-v3d,cma-256` under `[pi4]` in `/boot/firmware/config.txt`

For step 1, the `vidbuf_cache` is something that exists in Raspberry Pi OS but not in the Ubuntu Server environment. I'm not sure if this is actually needed.

Step 2 seems to be the solution. If you run `cat /proc/meminfo` *before* making this change, I saw `CmaTotal: 65536 kB`. If you run `watch -n 1 cat /proc/meminfo` you can see the CmaFree being exhausted when running `rpicam-still`.

After making the change in step 2 and rebooting, here's what I see in `meminfo`:
```
CmaTotal:         262144 kB
CmaFree:          118520 kB
```

With this change, there seems to be enough cma memory for taking pictures and everything works.

## Containerfile

I used podman to build this container. On the Pi, in this directory you can run:
```
podman build -t rpicam .
```

I was also able to crossbuild from my laptop:
```
podman build --platform=linux/arm64/v8 -t rpicam -o=dest=rpicam.tar,type=tar .
gzip -k rpicam.tar
```

You can then send to the Pi and import with podman:
```
scp rpicam.tar.gz <user>@<pi_ip>:~/rpicam.tar.gz

# on the pi (e.g., via ssh)
podman import rpicam.tar.gz 
```

Running the container is kinda funky, I wrote a script:
```
devices=""
for f in $(ls /dev/media*); do
        devices+="--device $f "
done

for f in $(ls /dev/video*); do
        devices+="--device $f "
done

echo $devices

podman run -it -v ./:/sharedvol -v /dev/dma_heap:/dev/dma_heap $devices --device /dev/v4l-subdev0 --group-add keep-groups -v /run/udev:/run/udev:ro 8fdd9499e9c5 sh
```

This will find every `video*` and `media*` device and register them with `--device`.

The `--group-add keep-groups` is to fix permissions within the container.

The `/run/udev:/run/udev:ro` was needed for cameras to be detected from within the container. Not sure why yet.
