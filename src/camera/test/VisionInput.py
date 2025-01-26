import cv2

# List cameras
def list_cameras():
    camera_list = []
    for i in range(0, 10):
        camera = cv2.VideoCapture(i)
        if camera.isOpened():
            camera_list.append(i)
            camera.release()
    return camera_list

# allow the user to select a camera

def select_camera():
    camera_list = list_cameras()
    print("Select a camera:")
    for i in camera_list:
        print(i)
    camera = int(input())
    return camera

# Capture a photo from the selected camera

def capture_photo(camera):
    camera = cv2.VideoCapture(camera)
    ret, frame = camera.read()
    camera.release()
    return frame

# Tell the user to rotate the camera x degrees

def rotate_camera(degrees):
    print("Rotate the camera {} degrees".format(degrees))

# crop the photo to remove edges for better stitching

def crop_photo(photo, pixels):
    height, width = photo.shape[:2]
    return photo[0:height, pixels:width-pixels]

# Stitch the photos together into a panorama
def stitch_photos(photos):
    stitcher = cv2.Stitcher()
    status, panorama = stitcher.stitch(photos)
    if status != 0:
        print("Error stitching photos")
        return None
    return panorama

# Save the panorama to a file

def save_panorama(panorama, filename):
    cv2.imwrite(filename, panorama)

# Save a photo to a file
def save_photo(photo, filename):
    cv2.imwrite(filename, photo)

# Main function
    
def main():
    camera = select_camera()
    _const_degree_rotation = 72
    _const_pixel_crop = 332
    photos = []
    for i in range(5):
        photos.append(capture_photo(camera))
        rotate_camera(_const_degree_rotation)
    

    for i in range(5):
        save_photo(photos[i], "photo{}.jpg".format(i))
    
    panorama = stitch_photos(photos)
    save_panorama(panorama, "panorama.jpg")
    print("Panorama saved to panorama.jpg")

if __name__ == "__main__":
    main()