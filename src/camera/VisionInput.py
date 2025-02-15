import cv2
import os

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

def capture_photo(camera) -> tuple[bool, cv2.typing.MatLike | None]:
    camera = cv2.VideoCapture(camera)
    if camera.isOpened():
        frame = camera.read()
        camera.release()
        return frame
    
    return (False, None)

# Tell the user to rotate the camera x degrees

def rotate_camera(degrees):
    print("Rotate the camera {} degrees".format(degrees))

# crop the photo to remove edges for better stitching

def crop_photo(photo, pixels):
    height, width = photo.shape[:2]
    cropped_photo = photo[0:height, pixels:width-pixels]
    return cropped_photo

# Stitch the photos together into a panorama
def stitch_photos(photos):
    stitcher = cv2.createStitcher()
    status, panorama = stitcher.stitch(photos)
    if status != cv2.Stitcher_OK:
        print(f"Error stitching photos. Status code: {status}")
        return None
    return panorama

# Save the panorama to a file

def save_panorama(panorama, filename):
    if panorama is not None:
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Directory {directory} created.")
            except Exception as e:
                print(f"Error creating directory {directory}: {e}")
                return
        success = cv2.imwrite(filename, panorama)
        if success:
            print(f"Panorama successfully saved to {filename}")
        else:
            print(f"Error saving panorama to {filename}")
    else:
        print("Error: No panorama to save.")

# Save a photo to a file
def save_photo(photo, filename):
    if photo is not None:
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Directory {directory} created.")
            except Exception as e:
                print(f"Error creating directory {directory}: {e}")
                return
        success = cv2.imwrite(filename, photo)
        if success:
            print(f"Photo successfully saved to {filename}")
        else:
            print(f"Error saving photo to {filename}")
    else:
        print("Error: No photo to save.")

# Main function
    
def main():
    camera = select_camera()
    _const_degree_rotation = 72
    _const_pixel_crop = 332
    photos = []
    for i in range(5):
        photo = capture_photo(camera)
        if not photo[0]:
            print("Failed to take picture. ")
            return

        cropped_photo = crop_photo(photo[1], _const_pixel_crop)
        rotate_camera(_const_degree_rotation)
        photos.append(cropped_photo)
        save_photo(cropped_photo, "photo{}.jpg".format(i))

    panorama = stitch_photos(photos)
    if panorama is not None:
        save_panorama(panorama, "panorama.jpg")
        print("Panorama saved to panorama.jpg")
    else:
        print("Error: Panorama creation failed.")

if __name__ == "__main__":
    main()