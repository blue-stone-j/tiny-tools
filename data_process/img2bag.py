import rospy
import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import sys

def main(folder_path, bag_path, topic_name="/camera/image_raw", rate=10):
    bag = rosbag.Bag(bag_path, 'w')
    bridge = CvBridge()
    image_files = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".jpg") or f.lower().endswith(".jpeg")
    ])

    rospy.init_node('pack_jpg_to_bag', anonymous=True)
    start_time = rospy.Time.now()

    for idx, file_name in enumerate(image_files):
        img_path = os.path.join(folder_path, file_name)
        cv_image = cv2.imread(img_path)
        if cv_image is None:
            rospy.logwarn(f"Failed to read {img_path}, skipping.")
            continue

        msg = bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
        # Simulate timestamp spacing
        msg.header.stamp = start_time + rospy.Duration(idx * 1.0 / rate)

        bag.write(topic_name, msg, t=msg.header.stamp)
        rospy.loginfo(f"Packed {file_name} at {msg.header.stamp.to_sec()} s")

    bag.close()
    rospy.loginfo(f"Bag file {bag_path} created with {len(image_files)} images.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pack_jpg_to_bag.py [image_folder] [output.bag]")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])