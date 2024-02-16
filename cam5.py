import cv2
import time
import numpy as np
import subprocess

def merge_hdr(images, exposure_times):
    exposure_times = np.array(exposure_times, dtype=np.float32)
    exposure_times /= 10
    alignMTB = cv2.createAlignMTB()
    alignMTB.process(images,images)

    # Estimate camera response function (CRF)
    calibrateDebevec = cv2.createCalibrateDebevec()
    responseDebevec = calibrateDebevec.process(images, exposure_times)
    # Merge images into an HDR linear image
    mergeDebevec = cv2.createMergeDebevec()
    hdrDebevec = mergeDebevec.process(images, exposure_times, responseDebevec)

    # Tone map the HDR image to 8-bit channels
    tonemap = cv2.createTonemap(2.2)
    ldr = tonemap.process(hdrDebevec)

    # Convert to 8-bit and save
    ldr_8bit = np.clip(ldr*255, 0, 255).astype('uint8')
    cv2.imwrite('./images/hdr_image.hdr', ldr_8bit)
    merge_mertens = cv2.createMergeMertens()
    fusion = merge_mertens.process(images)
    cv2.imwrite('./images/fusion.png', fusion * 255)
    return

def main():
    cap = cv2.VideoCapture(2)
    #cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
    width = 1920
    height = 1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    exposure = 0.1
    count =0
    images=[]
    exposures=[]
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    while cap.isOpened():
        # Grab frame
        ret, frame = cap.read()
        if ret:
            #cv2.imshow('Frame', frame)
            output_path = './images/output_-'+str(exposure)+'-.png'
            cv2.imwrite(output_path, frame)
            images.append(frame)
            exposures.append(exposure)

        # Set exposure manually
        command = "v4l2-ctl -d 2 -c auto_exposure=1 -c exposure_time_absolute="+str(exposure)
        output = subprocess.call(command, shell=True)
        # Increase exposure for every frame that is displayed
        exposure += 20
        if count >=20:
            break
        else:
            count+=1

    # Close everything
    cap.release()
    cv2.destroyAllWindows()
    merge_hdr(images, exposures)

main()
