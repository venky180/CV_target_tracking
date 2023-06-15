# CV_target_tracking


Template-matching based Target Tracking
# Introduction:
Template matching is a popular technique used in computer vision for target tracking
applica>ons, where the goal is to locate a specific object or target in each scene or video. The
technique involves comparing a pre-defined template image with a larger search space, looking
for the best match based on a certain similarity measure. The objec>ve is to es>mate the loca>on
and orienta>on of the target in each frame of a video stream, allowing for its trajectory and
movement to be tracked over >me.

There are several methods for calcula>ng the similarity between the template and the search
space, including Sum of Squared Differences (SSD), Cross-Correla>on (CC), and Normalized Cross-
Correla>on (NCC). SSD measures the difference between the intensity values of each pixel in the
template and the corresponding pixel in the search space, summing them up to obtain a single
similarity score. CC calculates the correla>on between the intensity values of the template and
the search space, giving higher scores to regions with high correla>on. NCC is similar to CC, but
normalizes the intensity values to account for differences in brightness and contrast.
In addi>on to selec>ng a suitable similarity measure, the performance of template matching can
be improved by using a local search window. This technique involves sliding the template over
small regions of the search space, rather than comparing it to the en>re search space at once. By
performing the template matching on smaller sub-regions, it is possible to reduce the
computa>onal complexity of the algorithm and improve its accuracy, especially in cases where
the target is moving rapidly or undergoing significant changes in appearance.

# Python Solution:
Python script for crea>ng a video from a sequence of images, where the images have bounding
box around a target object. The video is created by itera>vely adding each image to the video
container object. The script includes func>ons for calcula>ng the normalized cross-correla>on
score (NCC), cross-correla>on score (CC), and sum of squared differences (SSD) between two
images.
The script begins by impor>ng the necessary libraries, which include av, PIL, os, and numpy.
The first func>on, target_tracking_ncc_g(img1, img2), calculates the NCC score between two
grayscale images. The func>on first converts the input images into NumPy arrays and calculates
the mean and standard devia>on of each image. The images are then normalized and the NCC
score is computed.
The second func>on, target_tracking_cc_g(img1, img2), calculates the CC score between two
grayscale images. The func>on also converts the input images into NumPy arrays, calculates the
mean of each image, subtracts the mean from each image, and computes the CC score.

The third func>on, target_tracking_ncc(img1, img2), calculates the NCC score between two color
images. The func>on first converts the input images into Nuy arrays and calculates the mean
and standard devia>on for each color channel. The images are then normalized and the NCC score
is computed for each channel. The func>on returns the average NCC score across all channels.
The fourth func>on, target_tracking_cc(img1, img2), calculates the CC score between two color
images. The func>on first converts the input images into NumPy arrays and computes the CC
score for each color channel. The func>on returns the average CC score across all channels.
The fiRh func>on, target_tracking_ssd(template, image), calculates the SSD between a template
image and an input image. The func>on converts the input images into NumPy arrays, calculates
the sum of squared differences between the template and the image, and returns the total sum
of squared differences.
The sixth func>on, target_tracking_ssd_g(template, image), calculates the SSD between two
grayscale images. The func>on converts the input images into NumPy arrays, calculates the sum
of squared differences between the template and the image, and returns the total sum of squared
differences.
The last func>on, images_to_video(image_folder_path, video_path, fps, comp_type='ssd'),
creates a video from a sequence of images. The func>on takes four input parameters: the path to
the folder containing the images, the path and name of the output video file, the frame rate of
the video, and the type of comparison to use when tracking the target object. The func>on loads
the first image from the folder to get the size of the images, creates a video container object, and
adds a video stream to the container. The func>on then iterates over all the images in the folder,
loads each image as a PIL image, converts it to RGB mode, and aligns it to the target object. The
aligned image is then added to the video stream in the container. The func>on uses one of the
four comparison methods to track the target object: normalized cross-correla>on for grayscale
images, cross-correla>on for grayscale images, normalized cross-correla>on for color images, and
cross-correla>on for color images. The comparison method is specified using the comp_type
parameter, which defaults to SSD.
# Analysis:
The >me complexity for template matching per frame with a sliding window of 30x30 can be
calculated as follows:
Let's say we have an image of size MxN and a template of size PxQ. First, we need to slide the
30x30 window over the image. This can be done in O((M-30+1) x (N-30+1)) >me complexity. For
each posi>on of the sliding window, we need to compute the sum of squared differences (SSD)
between the template and the image pixels covered by the 30x30 window. The >me complexity
for compu>ng SSD is O(PxQ), since we need to compute the difference between each pixel in the
template and the corresponding pixel in the image, and then sum up the squared differences.


Therefore, the total >me complexity for template matching with a sliding window of 30x30 is
O((M-30+1) x (N-30+1) x PxQ). Note that this is just the >me complexity for the brute-force
method of template matching.
There are more advanced algorithms like Fast Fourier Transform (FFT) based template matching,
which can reduce the >me complexity significantly.
# Results:
The results of the template-matching based target tracking solu>on indicate that there is scope
for improving the performance of the system. One poten>al area of improvement is op>mizing
the size of the local search window used during template matching. The current implementa>on
uses a fixed size local search window of 30 x 30, which may not be op>mal for all tracking
scenarios. By experimen>ng with different window sizes and shapes, it may be possible to
improve the accuracy of the tracking system.
Another interes>ng finding is that color SSD (Sum of Squared Differences) performs be^er than
grayscale SSD, indica>ng that color informa>on can be useful for tracking targets. However, when
it comes to grayscale CC (Cross Correla>on), it outperformed the color CC. This suggests that while
color informa>on can be useful in some cases, it may not always be necessary for achieving high
accuracy in tracking.
When it comes to NCC (Normalized Cross Correla>on), grayscale NCC performed be^er than color
NCC, as well as both grayscale and color SSD and CC. This is an important finding as NCC is known
to be more robust to changes in illumina>on and contrast, making it a promising approach for
target tracking in diverse environments.
Finally, there is a need for improving the overall >me complexity of the system. The current
implementa>on requires a significant amount of computa>on for each frame, which may not be
feasible for real->me applica>ons. By op>mizing the algorithms used for template matching and
other tasks, it may be possible to reduce the overall computa>onal requirements and improve
the efficiency of the tracking system.
