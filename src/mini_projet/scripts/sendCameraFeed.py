#! /usr/bin/python3
# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
import numpy
import socket


ADRESSE = '192.168.1.165'
PORT = 6790
running = True
# Instantiate CvBridge
bridge = CvBridge()

print(cv2.__version__)

def image_callback(msg):
    print("Received an image!")
    cv2_img = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
    height, width, channels = cv2_img.shape
    #print(width, " ", height)
    #cv2.imshow("cv bridge img show", cv2_img)
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg',cv2_img, encode_param)
    stringData = numpy.array(imgencode).tostring()
    cv2.waitKey(1)
    #print("sending " + str(stringData))
    try:
        client.sendall(stringData)
    except:
        rospy.signal_shutdown("Connexion terminated by client")

def main():
    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/bebop2/camera_base/image_raw"
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, Image, image_callback)
    # Spin until ctrl + c
    rospy.spin()
    client.close()
        

if __name__ == '__main__':
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind((ADRESSE, PORT))
    serveur.listen(1)
    client, adresseClient = serveur.accept()
    print('Connexion de ', adresseClient)
    
    main()