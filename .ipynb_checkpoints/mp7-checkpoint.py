import av
from PIL import Image
import os
import numpy as np
def target_tracking_ncc_g(img1, img2):
    # Convert the images to NumPy arrays
    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)

    # Calculate the mean and standard deviation of the images
    mean1 = np.mean(arr1)
    mean2 = np.mean(arr2)
    std1 = np.std(arr1)
    std2 = np.std(arr2)

    # Normalize the images
    arr1_norm = (arr1 - mean1) / std1
    arr2_norm = (arr2 - mean2) / std2

    # Calculate the normalized cross-correlation score
    score = np.sum(np.multiply(arr1_norm, arr2_norm))

    return score

def target_tracking_cc_g(img1, img2):
    # Convert the images to NumPy arrays
    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)

    # Calculate the mean of the images
    mean1 = np.mean(arr1)
    mean2 = np.mean(arr2)

    # Subtract the mean from each image
    arr1 -= mean1
    arr2 -= mean2

    # Calculate the cross-correlation score
    score = np.sum(np.multiply(arr1, arr2))

    return score

def target_tracking_ncc(img1, img2):
    # Convert the images to NumPy arrays
    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)

    # Calculate the mean and standard deviation for each channel
    mean1 = np.mean(arr1, axis=(0, 1))
    mean2 = np.mean(arr2, axis=(0, 1))
    std1 = np.std(arr1, axis=(0, 1))
    std2 = np.std(arr2, axis=(0, 1))

    # Normalize the images
    arr1_norm = (arr1 - mean1) / std1
    arr2_norm = (arr2 - mean2) / std2

    # Calculate the normalized cross-correlation score for each channel
    scores = []
    for channel in range(3):
        score = np.sum(np.multiply(arr1_norm[:,:,channel], arr2_norm[:,:,channel]))
        scores.append(score)

    # Return the average normalized cross-correlation score
    return np.mean(scores)

def target_tracking_cc(img1, img2):
    # Convert the images to NumPy arrays
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Calculate the cross-correlation score for each channel
    scores = []
    for channel in range(3):
        score = np.sum(np.multiply(arr1[:,:,channel], arr2[:,:,channel]))
        scores.append(score)

    # Return the average cross-correlation score
    return np.mean(scores)

def target_tracking_ssd(template, image):

    # Convert the PIL images to NumPy arrays
    template_array = np.array(template)
    image_array = np.array(image)

    # Calculate the sum of squared differences between the template and the image
    ssd_array = np.sum((image_array - template_array) ** 2, axis=2)

    return np.sum(ssd_array)

def target_tracking_ssd_g(template, image):

    # Convert the PIL images to NumPy arrays
    template_array = np.array(template)
    image_array = np.array(image)

    # Calculate the sum of squared differences between the template and the image
    ssd = np.sum((image_array - template_array) ** 2)

    return ssd

def images_to_video(image_folder_path, video_path, fps, comp_type='ssd'):
    # Get the list of image file names in the folder
    template_path = './image_girl/0001.jpg'
    template = Image.open(template_path).convert('RGB')
    template_array=np.array(template)

    template_array = template_array[16:71,44:99]
    template = Image.fromarray(template_array)
    
    x_f, y_f = 44, 16
    x_b, y_b = x_f-18 if x_f-18 > 0 else 0, y_f-16 if y_f-16 > 0 else 0
    width_f, height_f = 55, 55
    width_b, height_b = 90, 90
    
    
    image_file_names = sorted(os.listdir(image_folder_path))

    # Load the first image to get the size of the images
    first_image_path = os.path.join(image_folder_path, image_file_names[0])
    first_image = Image.open(first_image_path)
    width, height = first_image.size

    # Create the video container object
    video_container = av.open(video_path, mode='w')

    # Add a video stream to the container
    video_stream = video_container.add_stream('libx264', rate=fps)
    video_stream.width = width
    video_stream.height = height
    video_stream.pix_fmt = 'yuv420p'

    # Iterate over all the images in the folder and add them to the video stream
    for image_file_name in image_file_names:
        # Load the image as a PIL image and convert it to RGB mode
        image_path = os.path.join(image_folder_path, image_file_name)
        pil_image = Image.open(image_path).convert('RGB')
        next_image_arr = np.array(pil_image)
        
        search_space_arr=next_image_arr[y_b:y_b+height_b,x_b:x_b+width_b]
        search_space = Image.fromarray(search_space_arr)
        

        new =[]

        
        for y in range(34):
            for x in range(34):
                cur_x=x
                cur_y=y
                # print(x,y,cur_y,cur_y+55,cur_x,cur_x+55)
                compare=search_space_arr[cur_y:cur_y+55,cur_x:cur_x+55]
                xxx,yyy,zzz = compare.shape
                if xxx==55 and yyy ==55 and zzz==3:
                    if comp_type == 'ssd':
                        new.append([x+x_b,y+y_b,target_tracking_ssd(template, Image.fromarray(compare))])
                    elif comp_type == 'ssd_gs':
                        new.append([x+x_b,y+y_b,target_tracking_ssd_g(template.convert("L"), Image.fromarray(compare).convert("L"))])
                    elif comp_type == 'cc_gs':
                        new.append([x+x_b,y+y_b,target_tracking_cc_g(template.convert("L"), Image.fromarray(compare).convert("L"))])
                    elif comp_type == 'cc':
                        new.append([x+x_b,y+y_b,target_tracking_cc(template, Image.fromarray(compare))])
                    elif comp_type == 'ncc_gs':
                        new.append([x+x_b,y+y_b,target_tracking_ncc_g(template.convert("L"), Image.fromarray(compare).convert("L"))])
                    elif comp_type == 'ncc':
                        new.append([x+x_b,y+y_b,target_tracking_ncc(template, Image.fromarray(compare))])

        xx = np.array(new)
        if comp_type=='ssd' or comp_type=='ssd_gs':
            x_f,y_f = xx[np.argmin(xx[:,2]),0:2]
        elif comp_type=='cc' or comp_type=='cc_gs' or comp_type=='ncc' or comp_type == 'ncc_gs':
            x_f,y_f = xx[np.argmax(xx[:,2]),0:2]
        
        x_f,y_f = int(x_f),int(y_f)
        if (x_f-18 > 0) and (x_f-18+90 < 128):
            x_b = x_f-18
        elif x_f-18 < 0:
            x_b=0
        elif x_f-18+90 >= 128:
            x_b=38

        if (y_f-16 > 0) and (y_f-16+90 < 128):
            y_b = y_f-16
        elif y_f-16 < 0:
            y_b=0
        elif y_f-16+90 >= 128:
            y_b=5

        
        next_image_arr[y_f:y_f+height_f, x_f:x_f+2] = [255, 0, 0]  # Top
        next_image_arr[y_f:y_f+height_f, x_f+width_f-2:x_f+width_f] = [255, 0, 0]  # Bottom
        next_image_arr[y_f:y_f+2, x_f:x_f+width_f] = [255, 0, 0]  # Left
        next_image_arr[y_f+height_f-2:y_f+height_f, x_f:x_f+width_f] = [255, 0, 0]  # Right

        next_image_arr[y_b:y_b+height_b, x_b:x_b+2] = [0, 255, 0]  # Top
        next_image_arr[y_b:y_b+height_b, x_b+width_b-2:x_b+width_b] = [0, 255, 0]  # Bottom
        next_image_arr[y_b:y_b+2, x_b:x_b+width_b] = [0, 255, 0]  # Left
        next_image_arr[y_b+height_b-2:y_b+height_b, x_b:x_b+width_b] = [0, 255, 0]  # Right
        
        pil_image = Image.fromarray(next_image_arr)
        # Convert the PIL image to a pyav video frame
        video_frame = av.VideoFrame.from_image(pil_image)
        print
        # Add the current frame to the video stream
        packet = video_stream.encode(video_frame)
        if packet:
            video_container.mux(packet)

    # Flush the video stream to finalize the video file
    packet = video_stream.encode()
    if packet:
        video_container.mux(packet)

    # Close the video container
    video_container.close()


comp_types=['ssd','ssd_gs','cc','cc_gs','ncc','ncc_gs']
image_folder_path = './image_girl/'
fps = 30
for comp_type in comp_types:
    video_path = './result_video_'+comp_type+'.mp4'
    images_to_video(image_folder_path, video_path, fps, comp_type)
