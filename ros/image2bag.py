import rospy
import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import os
import cv2


def main(folder_path, bag_path,topic_name='/camera/image', rate=10):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder {folder_path} does not exist.")
    
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()  # Ensure files are in order

    if not image_files:
        raise ValueError(f"No image files found in {folder_path}.")

    bridge = CvBridge()
    bag = rosbag.Bag(bag_path, 'w')

    rospy.init_node('image_to_bag', anonymous=True)
    start_time = rospy.Time.now()


    try:
        for img_file in image_files:
            img_path = os.path.join(folder_path, img_file)
            cv_image = cv2.imread(img_path)
            if cv_image is None:
                print(f"Warning: Could not read image {img_path}. Skipping.")
                continue
            
            ros_image = bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
            ros_image.header.stamp =start_time + rospy.Duration(1.0 / rate * image_files.index(img_file))
            bag.write('/camera/image', ros_image)
            print(f"Added {img_file} to bag.")
    finally:
        bag.close()
        print(f"Bag file saved to {bag_path}")

if __name__ == "__main__":
    folder_path = 'path_to_your_image_folder'  # Replace with your image folder path
    bag_path = 'output.bag'  # Replace with your desired bag file path
    main(folder_path, bag_path)